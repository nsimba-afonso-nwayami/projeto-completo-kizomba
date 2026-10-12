"""Offline classic-PCAP metadata import; no replay or payload export."""
import struct,hashlib,json,argparse,ipaddress
from pathlib import Path
from bacnet_readonly import ALLOWLIST
MAX=32*1024*1024
def analyze(data,authorized,reference):
 if authorized is not True or not isinstance(reference,str) or not reference.strip():raise ValueError('Authorized operational supervision capture and reference required')
 if len(data)>MAX or len(data)<24:raise ValueError('Invalid capture size')
 magic=data[:4];endian='<' if magic in (b'\xd4\xc3\xb2\xa1',b'\x4d\x3c\xb2\xa1') else '>' if magic in (b'\xa1\xb2\xc3\xd4',b'\xa1\xb2\x3c\x4d') else None
 if endian is None:raise ValueError('Classic PCAP required; convert PCAPNG locally before import')
 version_major,version_minor=struct.unpack_from(endian+'HH',data,4)
 if (version_major,version_minor)!=(2,4):raise ValueError('Unsupported PCAP version')
 link=struct.unpack_from(endian+'I',data,20)[0]
 if link!=1:raise ValueError('Ethernet PCAP required')
 offset=24;items=[];total=0;ignored=0;malformed=0
 def address(v):
  ip=str(ipaddress.IPv4Address(v));return ip if ip in ALLOWLIST.values() else 'peer-'+hashlib.sha256(v).hexdigest()[:12]
 while offset<len(data):
  if offset+16>len(data):raise ValueError('Truncated record header')
  sec,frac,n,original=struct.unpack_from(endian+'IIII',data,offset);offset+=16
  if n>65535 or n>original or offset+n>len(data):raise ValueError('Invalid record length')
  frame=data[offset:offset+n];offset+=n;total+=1
  if len(frame)<14:malformed+=1;continue
  start=14;eth=int.from_bytes(frame[12:14],'big')
  if eth==0x8100 and len(frame)>=18:eth=int.from_bytes(frame[16:18],'big');start=18
  if eth!=0x0800:ignored+=1;continue
  ip=frame[start:]
  if len(ip)<20 or ip[0]>>4!=4:malformed+=1;continue
  ihl=(ip[0]&15)*4;size=int.from_bytes(ip[2:4],'big')
  if ihl<20 or size<ihl+8 or size>len(ip) or ip[9]!=17 or int.from_bytes(ip[6:8],'big')&0x3fff:ignored+=1;continue
  src=str(ipaddress.IPv4Address(ip[12:16]));dst=str(ipaddress.IPv4Address(ip[16:20]))
  if src not in ALLOWLIST.values() and dst not in ALLOWLIST.values():ignored+=1;continue
  udp=ip[ihl:size];sport,dport,length=struct.unpack_from('!HHH',udp)
  if length<8 or length>len(udp):malformed+=1;continue
  body=udp[8:length]
  row={'source':address(ip[12:16]),'destination':address(ip[16:20]),'source_port':sport,'destination_port':dport,'protocol':'UDP unconfirmed','payload_bytes':len(body)}
  if len(body)>=6 and body[0]==0x81 and int.from_bytes(body[2:4],'big')==len(body):
   row.update(protocol='BACnet/IP framing observed',bvlc_function=body[1])
   if body[1] in (10,11) and body[4:6]==b'\x01\x00' and len(body)>=8:
    apdu=body[6:];row['apdu_type']=apdu[0]>>4
    if apdu[0]>>4==5 and len(apdu)==7 and apdu[3]==0x91 and apdu[5]==0x91:row.update(error_class=apdu[4],error_code=apdu[6])
   else:row['decode_status']='Unsupported NPDU/BVLC: payload not decoded'
  if len(items)<5000:items.append(row)
 return {'capture_sha256':hashlib.sha256(data).hexdigest(),'authorization_reference':reference,'packets_total':total,'ignored':ignored,'malformed':malformed,'items':items,'truncated_report':len(items)==5000,'privacy':'No payloads, client device IDs, MACs or unrelated IPs exported; peer labels pseudonymous, not anonymous','real_telemetry':False,'commands_replayed':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('capture');p.add_argument('--authorized-operational-supervision',action='store_true');p.add_argument('--reference',required=True);p.add_argument('--output',required=True);a=p.parse_args();path=Path(a.capture)
 if path.stat().st_size>MAX:raise SystemExit('Capture too large')
 Path(a.output).write_text(json.dumps(analyze(path.read_bytes(),a.authorized_operational_supervision,a.reference),indent=2))
