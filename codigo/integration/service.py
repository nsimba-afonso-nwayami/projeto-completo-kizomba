"""Authenticated local read-only integration. No remote Siemens commands."""
import argparse, hashlib, hmac, json, os, sqlite3, threading, uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs, unquote

ROOT = Path(__file__).resolve().parents[2]
STATIONS = ('SADI 1', 'SADI 2', 'SADI 3', 'SADI 4')
STATES = ('alarm', 'pre_alarm', 'fault', 'isolated', 'test', 'communication_lost', 'normal')
CONNECTORS = {
 'bacnet': {'status':'blocked','reason':'ReadProperty refused (Services 5 / Service Request Denied 29); client, license, visibility and point contract unvalidated'},
 'nk8237_modbus': {'status':'blocked','reason':'Gateway not inventoried; register map and version absent'},
 'mm8000_rest': {'status':'blocked','reason':'Server unavailable; version, license and API contract absent'},
 'mk8000_opcda': {'status':'blocked','reason':'Server unavailable; Windows bridge, tag export and contract absent'},
 'cerberus_dms': {'status':'blocked','reason':'Not inventoried; version, license and northbound contract absent'},
 'desigo_cc': {'status':'blocked','reason':'Not inventoried; version, license and web-service contract absent'},
}

def timestamp(): return datetime.now(timezone.utc).isoformat()
def text(v, limit=500):
 if not isinstance(v,str) or not v.strip() or len(v)>limit: raise ValueError('Nonempty bounded string required')
 return v.strip()
def instant(v):
 d=datetime.fromisoformat(text(v,64).replace('Z','+00:00'))
 if d.tzinfo is None: raise ValueError('Timestamp requires timezone')
 return d.astimezone(timezone.utc).isoformat()
def canonical(v): return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))

class Store:
 def __init__(self,path):
  self.lock=threading.RLock();self.db=sqlite3.connect(path,check_same_thread=False)
  self.db.row_factory=sqlite3.Row
  self.db.executescript('''PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL;
CREATE TABLE IF NOT EXISTS mappings(station TEXT, native_id TEXT, body TEXT NOT NULL, PRIMARY KEY(station,native_id));
CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY, event_key TEXT UNIQUE, station TEXT, native_id TEXT, state TEXT, source TEXT, time TEXT, received TEXT, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS current_states(station TEXT, native_id TEXT, source TEXT, time TEXT, body TEXT NOT NULL, PRIMARY KEY(station,native_id,source));
CREATE TABLE IF NOT EXISTS audit(seq INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT, actor TEXT, action TEXT, body TEXT, previous_hash TEXT, hash TEXT);
CREATE TABLE IF NOT EXISTS outbox(event_id TEXT PRIMARY KEY, status TEXT, attempts INTEGER DEFAULT 0, body TEXT);
''');self.db.commit()
 def audit(self,action,body,actor='local-operator'):
  last=self.db.execute('SELECT hash FROM audit ORDER BY seq DESC LIMIT 1').fetchone();prev=last[0] if last else ''
  when=timestamp();content=canonical(body);digest=hashlib.sha256((prev+when+actor+action+content).encode()).hexdigest()
  self.db.execute('INSERT INTO audit(time,actor,action,body,previous_hash,hash) VALUES(?,?,?,?,?,?)',(when,actor,action,content,prev,digest))
 def import_mapping(self,payload):
  if not isinstance(payload,dict) or payload.get('schema_version')!=1:raise ValueError('schema_version must be 1')
  version=text(payload.get('project_version'),100);items=payload.get('points')
  if not isinstance(items,list) or len(items)>10000:raise ValueError('points must be a bounded list')
  prepared=[];seen=set()
  for p in items:
   if not isinstance(p,dict):raise ValueError('point must be an object')
   st=text(p.get('station'),20);native=text(p.get('native_id'),160)
   if st not in STATIONS:raise ValueError('Unknown station')
   if (st,native) in seen:raise ValueError('Duplicate station/native_id')
   seen.add((st,native));status=p.get('status')
   if status not in ('candidate','field_validated'):raise ValueError('Explicit mapping status required')
   item={'station':st,'native_id':native,'project_version':version,'status':status,'evidence':text(p.get('evidence')),'area':text(p.get('area'),100),'place':text(p.get('place'),150),'code':text(p.get('code'),120),'discipline':text(p.get('discipline'),50),'loop':p.get('loop'),'validator':None,'validated_at':None}
   if item['loop'] is not None and (type(item['loop']) is not int or not 1<=item['loop']<=64):raise ValueError('Invalid loop')
   if status=='field_validated':item.update(validator=text(p.get('validator'),100),validated_at=instant(p.get('validated_at')))
   prepared.append(item)
  with self.lock,self.db:
   for p in prepared:
    old=self.db.execute('SELECT body FROM mappings WHERE station=? AND native_id=?',(p['station'],p['native_id'])).fetchone()
    if old and json.loads(old[0])!=p:raise ValueError('Existing mapping conflict; explicit reviewed migration required')
    self.db.execute('INSERT OR IGNORE INTO mappings VALUES(?,?,?)',(p['station'],p['native_id'],canonical(p)))
   self.audit('mapping_import',{'count':len(prepared),'project_version':version})
  return {'imported':len(prepared)}
 def ingest_simulation(self,p):
  if not isinstance(p,dict):raise ValueError('Event object required')
  if p.get('source')!='simulation':raise ValueError('Only explicitly labelled simulation is accepted; real ingestion blocked')
  station=text(p.get('station'),20);native=text(p.get('native_id'),160)
  if station not in STATIONS or p.get('state') not in STATES:raise ValueError('Unknown station/state')
  when=instant(p.get('time'));eid=text(p.get('source_event_id'),160)
  event_key=canonical(['simulation',station,eid]);identity={'station':station,'native_id':native,'state':p['state'],'source':'simulation','time':when,'source_event_id':eid}
  with self.lock,self.db:
   prior=self.db.execute('SELECT body FROM events WHERE event_key=?',(event_key,)).fetchone()
   if prior:
    old=json.loads(prior[0])
    if any(old[k]!=v for k,v in identity.items()):raise ValueError('Event identity collision')
    return {'duplicate':True,'event':old}
   row=self.db.execute('SELECT body FROM mappings WHERE station=? AND native_id=?',(station,native)).fetchone();mapping=json.loads(row[0]) if row else None
   validated=mapping and mapping['status']=='field_validated'
   event={**identity,'id':str(uuid.uuid4()),'received':timestamp(),'location_status':'field_validated' if validated else 'unmapped','location':mapping if validated else None,'local_ack':None}
   self.db.execute('INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?)',(event['id'],event_key,station,native,p['state'],'simulation',when,event['received'],canonical(event)))
   current=self.db.execute('SELECT time FROM current_states WHERE station=? AND native_id=? AND source=?',(station,native,'simulation')).fetchone()
   if not current or datetime.fromisoformat(when)>datetime.fromisoformat(current[0]):
    self.db.execute('INSERT OR REPLACE INTO current_states VALUES(?,?,?,?,?)',(station,native,'simulation',when,canonical(event)))
   self.db.execute('INSERT INTO outbox(event_id,status,body) VALUES(?,?,?)',(event['id'],'blocked_provider_unconfigured',canonical({'event_id':event['id'],'source':'simulation','sent':False})))
   self.audit('simulation_ingested',{'event_id':event['id'],'state':event['state'],'location_status':event['location_status']})
  return {'duplicate':False,'event':event}
 def acknowledge(self,eid,actor):
  actor=text(actor,100)
  with self.lock,self.db:
   row=self.db.execute('SELECT body FROM events WHERE id=?',(eid,)).fetchone()
   if not row:raise ValueError('Event not found')
   event=json.loads(row[0]);event['local_ack']={'actor':actor,'time':timestamp(),'panel_command_sent':False}
   self.db.execute('UPDATE events SET body=? WHERE id=?',(canonical(event),eid))
   self.audit('local_ack',{'event_id':eid,'panel_command_sent':False},actor)
  return event
 def rows(self,table,limit=100):
  if table not in ('events','mappings','current_states','audit','outbox'):raise ValueError('Unknown table')
  order='seq DESC' if table=='audit' else 'rowid DESC'
  with self.lock:
   rows=self.db.execute(f'SELECT * FROM {table} ORDER BY {order} LIMIT ?', (max(1,min(limit,500)),)).fetchall()
  if table in ('audit','outbox'):return [{**dict(r),'body':json.loads(r['body'])} for r in rows]
  return [json.loads(r['body']) for r in rows]
 def status(self):return {'mode':'simulation_only','real_telemetry':False,'remote_commands_enabled':False,'connectors':CONNECTORS,'time':timestamp(),'notifications':'durable outbox; provider not configured','retention':'no automatic deletion; operator-approved retention pending'}
 def close(self):self.db.close()

class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass # Never log Authorization header or event data to stdout.
 def reply(self,status,body):
  data=canonical(body).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def allowed(self):
  host=self.headers.get('Host','');origin=self.headers.get('Origin');expected=f'127.0.0.1:{self.server.server_port}'
  if host!=expected or (origin and origin!=f'http://{expected}'):self.reply(403,{'error':'Host/origin refused'});return False
  if not hmac.compare_digest(self.headers.get('Authorization',''), 'Bearer '+self.server.token):self.reply(401,{'error':'Authentication required'});return False
  return True
 def do_GET(self):
  parsed=urlsplit(self.path)
  if parsed.path.startswith('/api/'):
   if not self.allowed():return
   if parsed.path=='/api/status':return self.reply(200,{**self.server.store.status(),**self.server.runtime.status()})
   if parsed.path=='/api/readings':return self.reply(200,{'items':self.server.runtime.readings()})
   tables={'/api/events':'events','/api/points':'mappings','/api/states':'current_states','/api/audit':'audit','/api/notifications':'outbox'}
   if parsed.path in tables:
    try:limit=int(parse_qs(parsed.query).get('limit',['100'])[0])
    except ValueError:return self.reply(400,{'error':'Invalid limit'})
    return self.reply(200,{'items':self.server.store.rows(tables[parsed.path],limit)})
   return self.reply(404,{'error':'Unknown API route'})
  # Serve only the existing public application tree, never database or evidence files.
  if self.headers.get('Host')!=f'127.0.0.1:{self.server.server_port}':return self.reply(403,{'error':'Host refused'})
  name=unquote(parsed.path).lstrip('/') or 'index.html';base=(ROOT/'work/kizomba-site/dist').resolve();path=(base/name).resolve()
  if not path.is_relative_to(base) or not path.is_file():return self.reply(404,{'error':'Not found'})
  import mimetypes
  data=path.read_bytes();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(path.name)[0] or 'application/octet-stream');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def do_POST(self):
  if not self.allowed():return
  try:
   length=int(self.headers.get('Content-Length','0'))
   if length<=0 or length>2_000_000:return self.reply(413,{'error':'Body size refused'})
   if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.reply(415,{'error':'JSON required'})
   body=json.loads(self.rfile.read(length));path=urlsplit(self.path).path;store=self.server.store
   if path=='/api/compare-point':return self.reply(200,self.server.runtime.compare(body.get('reading_id'),body.get('value'),body.get('panel_time'),body.get('actor'),body.get('evidence')))
   if path=='/api/import-mapping':return self.reply(200,store.import_mapping(body))
   if path=='/api/simulations':return self.reply(201,store.ingest_simulation(body))
   if path=='/api/local-ack':return self.reply(200,store.acknowledge(text(body.get('event_id'),160),body.get('actor')))
   if path=='/api/commands':
    with store.lock,store.db:store.audit('remote_command_blocked',{'reason':'No validated command contract; nothing transmitted'})
    return self.reply(409,{'error':'All remote panel commands blocked','panel_command_sent':False})
   return self.reply(404,{'error':'Unknown API route'})
  except (ValueError,TypeError,AttributeError,sqlite3.IntegrityError):self.reply(400,{'error':'Invalid or conflicting input; nothing committed'})
  except Exception:self.reply(500,{'error':'Internal error; consult local diagnostics'})

def create_server(path,token,port=8765):
 if not isinstance(token,str) or len(token)<32:raise ValueError('KIZOMBA_API_TOKEN requires at least 32 characters')
 server=ThreadingHTTPServer(('127.0.0.1',port),Handler);server.token=token;server.store=Store(path)
 from runtime_reading import Runtime
 server.runtime=Runtime(server.store);return server

def main():
 p=argparse.ArgumentParser();p.add_argument('--db',default=str(ROOT/'work/integration/runtime/kizomba.sqlite3'));p.add_argument('--port',type=int,default=8765);p.add_argument('--token-file');p.add_argument('--read-config');a=p.parse_args()
 token=os.environ.get('KIZOMBA_API_TOKEN','')
 if a.token_file:
  secret=Path(a.token_file)
  if secret.stat().st_mode & 0o077:raise SystemExit('Token file must be private (0600)')
  token=secret.read_text().strip()
 if len(token)<32:raise SystemExit('Set KIZOMBA_API_TOKEN with at least 32 characters; it is not printed or stored.')
 Path(a.db).parent.mkdir(parents=True,exist_ok=True);server=create_server(a.db,token,a.port)
 if a.read_config:
  from bacnet_readonly import Reader
  from runtime_reading import Runtime
  config=json.loads(Path(a.read_config).read_text())
  server.runtime=Runtime(server.store,Reader(config,Path(a.db).parent/'evidence'),config.get('stale_seconds',30))
 server.runtime.start()
 print(f'Local application http://127.0.0.1:{server.server_port} — gated read-only worker; remote commands disabled',flush=True)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.runtime.stop();server.server_close();server.store.close()
if __name__=='__main__':main()
