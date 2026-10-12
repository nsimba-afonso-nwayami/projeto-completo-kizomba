import json,sqlite3,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
from service import Store,create_server

class IntegrationTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'db.sqlite';self.s=Store(self.path)
 def tearDown(self):self.s.close();self.tmp.cleanup()
 def mapping(self,status='field_validated'):
  p={'station':'SADI 2','native_id':'SIM:detector:1','code':'KZ-SIM-01','area':'Casa A48/A49','place':'Sala','discipline':'Incêndio','loop':None,'status':status,'evidence':'Fixture synthetic; not a central export','validator':'Test only','validated_at':'2026-10-09T10:00:00+01:00'}
  return {'schema_version':1,'project_version':'synthetic-test','points':[p]}
 def event(self,**extra):return dict(source='simulation',station='SADI 2',native_id='SIM:detector:1',state='fault',source_event_id='one',time='2026-10-09T10:00:00+01:00',**extra)
 def test_persistence_dedup_local_ack(self):
  self.s.import_mapping(self.mapping());e=self.s.ingest_simulation(self.event())['event'];self.assertEqual(e['location']['area'],'Casa A48/A49')
  self.assertTrue(self.s.ingest_simulation(self.event())['duplicate']);self.assertEqual(len(self.s.rows('events')),1)
  ack=self.s.acknowledge(e['id'],'Operator');self.assertFalse(ack['local_ack']['panel_command_sent']);self.assertEqual(ack['state'],'fault')
  self.s.close();self.s=Store(self.path);self.assertEqual(len(self.s.rows('events')),1);self.assertEqual(self.s.rows('outbox')[0]['status'],'blocked_provider_unconfigured')
 def test_candidate_and_unknown_never_located(self):
  self.s.import_mapping(self.mapping('candidate'));self.assertIsNone(self.s.ingest_simulation(self.event())['event']['location'])
 def test_real_ingestion_refused(self):
  e=self.event();e['source']='bacnet'
  with self.assertRaises(ValueError):self.s.ingest_simulation(e)
  self.assertEqual(self.s.rows('events'),[])
 def test_atomic_import_conflicts(self):
  m=self.mapping();m['points'].append(dict(m['points'][0]))
  with self.assertRaises(ValueError):self.s.import_mapping(m)
  self.assertEqual(self.s.rows('mappings'),[])
  self.s.import_mapping(self.mapping());m=self.mapping();m['points'][0]['area']='Casa A01'
  with self.assertRaises(ValueError):self.s.import_mapping(m)
  self.assertEqual(self.s.rows('mappings')[0]['area'],'Casa A48/A49')
 def test_timezone_and_out_of_order(self):
  old=self.event();old['time']='2026-10-09T08:00:00Z';old['source_event_id']='old'
  self.s.ingest_simulation(self.event());self.s.ingest_simulation(old);self.assertEqual(self.s.rows('current_states')[0]['time'],'2026-10-09T09:00:00+00:00')
  bad=self.event();bad['time']='2026-10-09T10:00:00'
  with self.assertRaises(ValueError):self.s.ingest_simulation(bad)
 def test_identity_collision(self):
  self.s.ingest_simulation(self.event());e=self.event();e['state']='normal'
  with self.assertRaises(ValueError):self.s.ingest_simulation(e)
 def test_audit_chain(self):
  import hashlib
  self.s.ingest_simulation(self.event());self.s.import_mapping(self.mapping())
  rows=list(reversed(self.s.rows('audit')));prev=''
  from service import canonical
  for r in rows:
   self.assertEqual(r['previous_hash'],prev)
   self.assertEqual(r['hash'],hashlib.sha256((prev+r['time']+r['actor']+r['action']+canonical(r['body'])).encode()).hexdigest());prev=r['hash']
 def test_normalization_states(self):
  from service import STATES
  for i,state in enumerate(STATES):
   e=self.event();e['state']=state;e['source_event_id']=str(i);e['time']=f'2026-10-09T09:00:{i:02d}Z';self.s.ingest_simulation(e)
  self.assertEqual(len(self.s.rows('events')),len(STATES));self.assertEqual(self.s.rows('current_states')[0]['state'],'normal')
 def test_http_auth_origin_commands_and_static(self):
  server=create_server(self.path,'a'*40,0);t=threading.Thread(target=server.serve_forever,daemon=True);t.start();url=f'http://127.0.0.1:{server.server_port}'
  def request(path,body=None,token='a'*40,origin=None):
   headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'}
   if origin:headers['Origin']=origin
   req=urllib.request.Request(url+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
   try:
    with urllib.request.urlopen(req,timeout=2) as r:return r.status,r.read()
   except urllib.error.HTTPError as e:return e.code,e.read()
  try:
   self.assertEqual(request('/api/status',token='bad')[0],401)
   self.assertEqual(request('/api/status',origin='http://evil.example')[0],403)
   self.assertFalse(json.loads(request('/api/status')[1])['real_telemetry'])
   self.assertEqual(request('/api/commands',{'command':'reset'})[0],409)
   self.assertEqual(request('/api/simulations',self.event())[0],201)
   self.assertEqual(request('/api/simulations',dict(self.event(),source='bacnet'))[0],400)
   self.assertEqual(request('/../integration/service.py')[0],404)
   self.assertEqual(request('/index.html')[0],200)
   self.assertIn(b'authentication',request('/api/status',token='bad')[1].lower())
  finally:server.shutdown();server.server_close();server.store.close();t.join()
if __name__=='__main__':unittest.main(verbosity=2)
