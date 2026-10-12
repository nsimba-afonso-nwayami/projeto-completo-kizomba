"""Single-object BACnet ReadProperty. No writes, subscriptions, I-Am or replay."""
import hashlib,json,os,socket,struct,time,uuid
from datetime import datetime,timezone
from pathlib import Path
ALLOWLIST={'SADI 1':'192.168.2.62','SADI 2':'192.168.2.60','SADI 3':'192.168.2.61','SADI 4':'192.168.2.63'}
class Blocked(Exception):pass
class ProtocolError(Exception):pass

def gates(c):
 missing=[]
 if c.get('enabled') is not True:missing.append('configuration.enabled')
 if c.get('station') not in ALLOWLIST or c.get('target_ip')!=ALLOWLIST.get(c.get('station')):missing.append('authorized target/station')
 if c.get('protocol_active_confirmed') is not True:missing.append('active BACnet/IP confirmed')
 if type(c.get('target_port')) is not int or not 1<=c['target_port']<=65535:missing.append('configured UDP port')
 if type(c.get('client_device_id')) is not int or not 0<=c['client_device_id']<=4194302:missing.append('authorized unique client device ID')
 for field in ['client_authorization_evidence','client_uniqueness_evidence','visibility_evidence','license_evidence','approval_reference','model','firmware','interface','integration_document','document_section']:
  if not isinstance(c.get(field),str) or not c[field].strip():missing.append(field)
 if c.get('model') not in ('FC726','FC726-ZA'):missing.append('confirmed FC726 model')
 if c.get('document_applies_to_model_version') is not True:missing.append('integration document applicable to exact model/version')
 if c.get('license_confirmed') is not True:missing.append('license verified')
 if c.get('visibility_confirmed') is not True:missing.append('point visibility verified')
 if c.get('client_authorized') is not True:missing.append('client explicitly authorized')
 # Source binding must itself be the documented identity method. Device ID is never borrowed or advertised.
 if c.get('identity_method')!='configured_source_address' or c.get('identity_method_documented') is not True:missing.append('documented configured-source identity method (I-Am registration unsupported)')
 if c.get('source_ip')!='192.168.2.207':missing.append('authorized source IP')
 if type(c.get('source_port')) is not int or not 1024<=c['source_port']<=65535:missing.append('authorized fixed source port')
 if c.get('services')!=['ReadProperty']:missing.append('ReadProperty-only contract')
 p=c.get('point',{})
 if not isinstance(p,dict):return missing+['known point']
 for f in ['object_type','object_instance','property_id']:
  v=p.get(f);maximum={'object_type':1023,'object_instance':4194302,'property_id':255}[f]
  if type(v) is not int or not 0<=v<=maximum:missing.append('point.'+f)
 for f in ['native_id','evidence','value_semantics_reference']:
  if not isinstance(p.get(f),str) or not p[f].strip():missing.append('point.'+f)
 if p.get('known_point_confirmed') is not True:missing.append('known point confirmed')
 if p.get('value_type') not in ('enumerated','unsigned','boolean'):missing.append('documented numeric/boolean value type')
 state_map=p.get('state_map')
 if not isinstance(state_map,dict) or not state_map or any(v not in ['alarm','pre_alarm','fault','isolated','test','normal'] for v in state_map.values()):missing.append('documented point state mapping')
 for f,lo,hi in [('poll_seconds',10,3600),('stale_seconds',30,86400)]:
  if type(c.get(f)) is not int or not lo<=c[f]<=hi:missing.append(f)
 if c.get('poll_seconds',3600)>=c.get('stale_seconds',0):missing.append('stale threshold greater than poll interval')
 return missing

def request(point,invoke):
 obj=(point['object_type']<<22)|point['object_instance']
 apdu=bytes([0,5,invoke,12,12])+obj.to_bytes(4,'big')+bytes([25,point['property_id']])
 body=b'\x01\x00'+apdu
 return b'\x81\x0a'+(len(body)+4).to_bytes(2,'big')+body

def decode(packet,point,invoke):
 if len(packet)<9 or packet[:2]!=b'\x81\x0a' or int.from_bytes(packet[2:4],'big')!=len(packet) or packet[4:6]!=b'\x01\x00':raise ProtocolError('Unsupported BVLC/NPDU/length; no state inferred')
 apdu=packet[6:];kind=apdu[0]>>4
 if apdu[1]!=invoke:raise ProtocolError('Unmatched invoke ID')
 if kind==5:
  if len(apdu)==7 and apdu[2]==12 and apdu[3]==0x91 and apdu[5]==0x91:raise ProtocolError(f'BACnet Error class {apdu[4]} code {apdu[6]}')
  raise ProtocolError('BACnet Error')
 if kind in (6,7):raise ProtocolError('BACnet Reject/Abort')
 if apdu[:3]!=bytes([0x30,invoke,12]):raise ProtocolError('Segmented or unsupported ReadProperty ACK')
 expected=bytes([12])+((point['object_type']<<22)|point['object_instance']).to_bytes(4,'big')+bytes([25,point['property_id'],0x3e])
 if apdu[3:3+len(expected)]!=expected or apdu[-1]!=0x3f:raise ProtocolError('Object/property mismatch or unsupported array/value encoding')
 encoded=apdu[3+len(expected):-1]
 if not encoded:raise ProtocolError('Missing value')
 tag=encoded[0]>>4;context=(encoded[0]>>3)&1;length=encoded[0]&7
 if context:raise ProtocolError('Context value unsupported')
 if tag==1 and length in (0,1) and len(encoded)==1:value=bool(length);value_type='boolean'
 elif tag in (2,9) and 1<=length<=4 and len(encoded)==length+1:value=int.from_bytes(encoded[1:],'big');value_type='unsigned' if tag==2 else 'enumerated'
 else:raise ProtocolError('Unsupported value; no string or secret extraction')
 if value_type!=point['value_type']:raise ProtocolError('Value type differs from documented contract')
 key=str(value).lower();state=point['state_map'].get(key)
 if state is None:raise ProtocolError('Value has no documented state mapping')
 return {'value':value,'value_type':value_type,'state':state}

class Reader:
 def __init__(self,config,evidence_dir):
  self.config=config;self.evidence_dir=Path(evidence_dir);self.invoke=0
 def once(self):
  c=self.config;missing=gates(c)
  if missing:raise Blocked('; '.join(missing))
  self.invoke=self.invoke%255+1;req=request(c['point'],self.invoke)
  sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);deadline=time.monotonic()+3
  try:
   sock.bind((c['source_ip'],c['source_port']));sock.sendto(req,(c['target_ip'],c['target_port']))
   while True:
    sock.settimeout(max(.001,deadline-time.monotonic()));raw,origin=sock.recvfrom(2048)
    if origin==(c['target_ip'],c['target_port']) and len(raw)>7 and raw[7]==self.invoke:break
    if time.monotonic()>=deadline:raise TimeoutError('No matching central response')
  finally:sock.close()
  reading_id=str(uuid.uuid4());self.evidence_dir.mkdir(parents=True,exist_ok=True,mode=0o700)
  evidence={'id':reading_id,'time':datetime.now(timezone.utc).isoformat(),'station':c['station'],'target':[c['target_ip'],c['target_port']],'source':[c['source_ip'],c['source_port']],'native_id':c['point']['native_id'],'request_hex':req.hex(),'response_hex':raw.hex(),'response_sha256':hashlib.sha256(raw).hexdigest(),'integration_validated':False}
  path=self.evidence_dir/(reading_id+'.json');fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
  with os.fdopen(fd,'w') as f:json.dump(evidence,f,indent=2)
  parsed=decode(raw,c['point'],self.invoke)
  contract_hash=hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest()
  return {**parsed,'id':reading_id,'station':c['station'],'native_id':c['point']['native_id'],'observed_at':evidence['time'],'evidence_id':reading_id,'contract_hash':contract_hash,'source':'bacnet_readproperty','comparison_status':'not_confirmed'}
