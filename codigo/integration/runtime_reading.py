"""Durable observations with fail-closed freshness and supervised read-only loop."""
import json,threading,time
from datetime import datetime,timezone
from bacnet_readonly import gates,Blocked,ProtocolError

class Runtime:
 def __init__(self,store,reader=None,stale_seconds=30):
  self.store=store;self.reader=reader;self.stale_seconds=stale_seconds;self.stop_event=threading.Event();self.thread=None;self.failures=0;self.protocol_block=None
  with store.lock,store.db:
   store.db.executescript('''CREATE TABLE IF NOT EXISTS observations(id TEXT PRIMARY KEY,station TEXT,native_id TEXT,observed_at TEXT,body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS comparisons(contract_hash TEXT PRIMARY KEY,reading_id TEXT,body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS transport(station TEXT PRIMARY KEY,status TEXT,time TEXT);''')
   previous=store.db.execute("SELECT status FROM transport WHERE status='blocked_protocol_review_required' LIMIT 1").fetchone()
   if previous:self.protocol_block='Previous protocol failure requires integrator review before retry'
   store.db.execute("UPDATE transport SET status='unknown_after_restart' WHERE status!='blocked_protocol_review_required'")
 def record(self,reading):
  with self.store.lock,self.store.db:
   self.store.db.execute('INSERT INTO observations VALUES(?,?,?,?,?)',(reading['id'],reading['station'],reading['native_id'],reading['observed_at'],json.dumps(reading)))
   self.store.db.execute('INSERT OR REPLACE INTO transport VALUES(?,?,?)',(reading['station'],'response_received',datetime.now(timezone.utc).isoformat()))
   self.store.audit('real_property_response',{'reading_id':reading['id'],'comparison_status':'not_confirmed'})
 def failure(self,status):
  station=self.reader.config.get('station','SADI 2') if self.reader else 'SADI 2'
  with self.store.lock,self.store.db:self.store.db.execute('INSERT OR REPLACE INTO transport VALUES(?,?,?)',(station,status,datetime.now(timezone.utc).isoformat()))
 def compare(self,reading_id,value,panel_time,actor,evidence):
  from service import text,instant
  actor=text(actor,100);evidence=text(evidence);panel_time=instant(panel_time)
  with self.store.lock,self.store.db:
   row=self.store.db.execute('SELECT body FROM observations WHERE id=?',(reading_id,)).fetchone()
   if not row:raise ValueError('No real observation for this reading ID')
   r=json.loads(row[0])
   if type(value)!=type(r['value']) or value!=r['value']:raise ValueError('Panel and read property disagree')
   delta=abs((datetime.fromisoformat(panel_time)-datetime.fromisoformat(r['observed_at'])).total_seconds())
   if delta>60:raise ValueError('Panel comparison not within 60 seconds of original reading')
   proof={'reading_id':reading_id,'actor':actor,'evidence':evidence,'panel_time':panel_time,'compared_at':datetime.now(timezone.utc).isoformat(),'scope':'single configured point/property; not entire installation'}
   self.store.db.execute('INSERT OR REPLACE INTO comparisons VALUES(?,?,?)',(r['contract_hash'],reading_id,json.dumps(proof)))
   self.store.audit('panel_comparison_confirmed',{'reading_id':reading_id,'scope':proof['scope']},actor)
  return proof
 def readings(self,at=None):
  at=at or datetime.now(timezone.utc)
  with self.store.lock:
   rows=self.store.db.execute('SELECT body FROM observations ORDER BY rowid DESC LIMIT 100').fetchall()
   transport={r['station']:r['status'] for r in self.store.db.execute('SELECT * FROM transport')}
   proofs={r[0] for r in self.store.db.execute('SELECT contract_hash FROM comparisons')}
   mappings={(r[0],r[1]):json.loads(r[2]) for r in self.store.db.execute('SELECT * FROM mappings')}
  output=[];seen=set()
  for row in rows:
   r=json.loads(row[0]);age=max(0,(at-datetime.fromisoformat(r['observed_at'])).total_seconds())
   same_contract=self.reader is not None and not gates(self.reader.config) and r['contract_hash']==__import__('hashlib').sha256(json.dumps(self.reader.config,sort_keys=True).encode()).hexdigest()
   current=(r['station'],r['native_id']) not in seen;seen.add((r['station'],r['native_id']))
   not_future=datetime.fromisoformat(r['observed_at'])<=at
   quality='fresh' if current and not_future and age<=self.stale_seconds and transport.get(r['station'])=='response_received' and same_contract else 'unknown_stale_or_disconnected'
   confirmed=r['contract_hash'] in proofs
   mapping=mappings.get((r['station'],r['native_id']))
   output.append({**r,'quality':quality,'age_seconds':round(age,1),'comparison_status':'compared_with_panel' if confirmed else 'not_confirmed','integration_validated':confirmed and quality=='fresh','effective_state':r['state'] if confirmed and quality=='fresh' else 'unknown','location_status':'field_validated' if mapping and mapping['status']=='field_validated' else 'unmapped','location':mapping if mapping and mapping['status']=='field_validated' else None})
  return output
 def status(self):
  missing=gates(self.reader.config) if self.reader else ['Read-only configuration absent']
  if self.protocol_block:missing.append(self.protocol_block)
  readings=self.readings();return {'mode':'read_only_gated','real_telemetry':any(r['integration_validated'] for r in readings),'real_response_obtained':bool(readings),'integration_validated_scope':'single point/property only' if any(r['integration_validated'] for r in readings) else None,'remote_commands_enabled':False,'bacnet_blockers':missing,'last_failure_count':self.failures,'stale_seconds':self.stale_seconds,'continuous_worker':bool(self.thread and self.thread.is_alive())}
 def delay(self):return min(300,10*(2**min(self.failures,5)))
 def loop(self):
  while not self.stop_event.is_set():
   try:
    if self.protocol_block or not self.reader or gates(self.reader.config):self.failure('blocked_configuration');self.stop_event.wait(10);continue
    result=self.reader.once();self.record(result);self.failures=0;delay=self.reader.config['poll_seconds']
   except Blocked:self.failure('blocked_configuration');delay=30
   except ProtocolError as exc:self.protocol_block=str(exc);self.failure('blocked_protocol_review_required');delay=30
   except Exception:self.failures+=1;self.failure('communication_or_protocol_failure');delay=self.delay()
   self.stop_event.wait(delay)
 def start(self):self.thread=threading.Thread(target=self.loop,name='read-only-worker',daemon=True);self.thread.start()
 def stop(self):self.stop_event.set();self.thread.join(timeout=5) if self.thread else None
