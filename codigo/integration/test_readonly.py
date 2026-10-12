import unittest,json,tempfile,hashlib,struct
from pathlib import Path
from datetime import datetime,timezone,timedelta
from unittest.mock import patch
from bacnet_readonly import gates,Reader,Blocked,decode,ProtocolError
from runtime_reading import Runtime
from capture_import import analyze
from service import Store
class Tests(unittest.TestCase):
 def config(self):
  c=json.loads((Path(__file__).parent/'read-config.example.json').read_text());c.update(firmware="SYNTHETIC fixture",enabled=True,client_device_id=999,source_port=47809,client_authorized=True,license_confirmed=True,visibility_confirmed=True,document_applies_to_model_version=True,identity_method='configured_source_address',identity_method_documented=True)
  for k in ['client_authorization_evidence','client_uniqueness_evidence','visibility_evidence','license_evidence','approval_reference','integration_document','document_section']:c[k]='SYNTHETIC fixture only'
  c['point'].update(object_type=0,object_instance=1,property_id=85,native_id='SYNTHETIC:1',known_point_confirmed=True,evidence='fixture',value_semantics_reference='fixture',value_type='enumerated',state_map={'0':'normal','1':'alarm'});return c
 def test_gates_no_network(self):
  with patch('bacnet_readonly.socket.socket') as sock:
   with self.assertRaises(Blocked):Reader(json.loads((Path(__file__).parent/'read-config.example.json').read_text()),'unused').once()
   sock.assert_not_called()
  self.assertEqual(gates(self.config()),[])
 def test_response_and_denial(self):
  p=self.config()['point'];apdu=bytes([48,1,12,12])+ (1).to_bytes(4,'big')+bytes([25,85,62,145,1,63]);packet=b'\x81\x0a'+(len(apdu)+6).to_bytes(2,'big')+b'\x01\x00'+apdu
  self.assertEqual(decode(packet,p,1)['state'],'alarm')
  for raw,invoke in [(packet[:-1],1),(packet,2),(bytes.fromhex('810a000d010050010c9105911d'),1)]:
   with self.assertRaises(ProtocolError):decode(raw,p,invoke)
 def test_unknown_comparison_stale_restart(self):
  with tempfile.TemporaryDirectory() as d:
   c=self.config();s=Store(Path(d)/'db');rt=Runtime(s,Reader(c,Path(d)/'evidence'));now=datetime.now(timezone.utc);r={'id':'fixture','station':'SADI 2','native_id':'SYNTHETIC:1','observed_at':now.isoformat(),'value':1,'state':'alarm','contract_hash':hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest()}
   rt.record(r);self.assertEqual(rt.readings()[0]['effective_state'],'unknown');rt.compare('fixture',1,now.isoformat(),'tester','synthetic comparison');self.assertTrue(rt.status()['real_telemetry']);self.assertEqual(rt.readings(now+timedelta(seconds=31))[0]['effective_state'],'unknown');rt.failure('disconnected');self.assertFalse(rt.status()['real_telemetry']);rt.record(dict(r,id='fixture2'));Runtime(s,rt.reader);self.assertFalse(rt.status()['real_telemetry']);rt.failures=10;self.assertEqual(rt.delay(),300);s.close()
 def test_capture_bounds_authorization(self):
  pcap=b'\xd4\xc3\xb2\xa1'+struct.pack('<HHIIII',2,4,0,0,65535,1)
  with self.assertRaises(ValueError):analyze(pcap,False,'fixture')
  self.assertEqual(analyze(pcap,True,'fixture')['packets_total'],0)
  with self.assertRaises(ValueError):analyze(pcap+b'x',True,'fixture')
if __name__=='__main__':unittest.main()
