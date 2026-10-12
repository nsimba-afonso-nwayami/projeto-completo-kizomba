"""Bounded local diagnostics: four authorized hosts, no service probes without contract."""
import subprocess,json,platform,argparse
from datetime import datetime,timezone
from pathlib import Path
HOSTS=['192.168.2.60','192.168.2.61','192.168.2.62','192.168.2.63']
def command(args):
 try:
  r=subprocess.run(args,capture_output=True,text=True,timeout=12)
  return {'exit_code':r.returncode,'output':(r.stdout+r.stderr)[:18000]}
 except Exception as e:return {'unavailable':type(e).__name__}
def run():
 return {'time':datetime.now(timezone.utc).isoformat(),'scope':HOSTS,'interfaces':command(['/sbin/ifconfig','en8']),'wifi':command(['/sbin/ifconfig','en0']),'routes':command(['/usr/sbin/netstat','-rn','-f','inet']),'application_firewall':command(['/usr/libexec/ApplicationFirewall/socketfilterfw','--getglobalstate']),'packet_filter':command(['/sbin/pfctl','-s','info']),'ping':{ip:command(['/sbin/ping','-c','1','-W','1000',ip]) for ip in HOSTS},'service_diagnostic':'Blocked: exact integration contract, client authorization and configured service not confirmed. Ping does not validate telemetry.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();Path(a.output).write_text(json.dumps(run(),indent=2))
