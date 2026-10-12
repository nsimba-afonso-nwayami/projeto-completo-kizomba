"""Legacy probe disabled: use gated integration/bacnet_readonly.py after field contract validation."""
if __name__ == "__main__":
 raise SystemExit("Legacy property probe disabled; complete READ_ONLY contract and use service.py")
"""Directed read-only diagnostic. Explicit --run-reviewed-window required; no import side effects."""
import argparse, socket, json, time
from datetime import datetime, timezone
from pathlib import Path

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--run-reviewed-window',action='store_true');args=parser.parse_args()
 if not args.run_reviewed_window:raise SystemExit('Blocked: coordinate a read-only window and review client/configuration before repeating a refused request.')
 records=[];sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);sock.bind(('192.168.2.207',0));sock.settimeout(2)
 try:
  for invoke,prop in enumerate([77,70,121,44,76],1):
   apdu=bytes([0,5,invoke,12,12])+((8<<22)|3).to_bytes(4,'big')+bytes([25,prop])
   if prop==76:apdu+=bytes([41,0])
   body=b'\x01\x00'+apdu;packet=b'\x81\x0a'+(len(body)+4).to_bytes(2,'big')+body
   record={'property':prop,'request_hex':packet.hex()};sock.sendto(packet,('192.168.2.60',47808));deadline=time.monotonic()+2
   try:
    while True:
     sock.settimeout(max(.001,deadline-time.monotonic()));response,origin=sock.recvfrom(4096)
     if origin==('192.168.2.60',47808) and len(response)>8 and response[7]==invoke:
      record['response_hex']=response.hex();record['apdu_type']=response[6]>>4;break
     if time.monotonic()>=deadline:raise TimeoutError('No matching response')
   except (TimeoutError,socket.timeout):record['result']='timeout'
   records.append(record)
   if record.get('apdu_type') in (5,6,7) or record.get('result')=='timeout':break
   time.sleep(1)
 finally:sock.close()
 result={'time':datetime.now(timezone.utc).isoformat(),'target':'192.168.2.60','operation':'ReadProperty only','records':records,'real_alarm_reading':False}
 path=Path('outputs/BACnet-Diagnostico-Revisado-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.json');path.write_text(json.dumps(result,indent=2));print(str(path))
if __name__=='__main__':main()
