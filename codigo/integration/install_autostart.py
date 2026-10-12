"""Prepare/install user launchd daemon without embedded credentials or sleep/network changes."""
import argparse,os,secrets,plistlib,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
LABEL='com.kizomba.readonly'
def prepare():
 runtime=HERE/'runtime';runtime.mkdir(exist_ok=True,mode=0o700);os.chmod(runtime,0o700)
 token=runtime/'api-token'
 if not token.exists():
  fd=os.open(token,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
  with os.fdopen(fd,'w') as f:f.write(secrets.token_urlsafe(48))
 config=runtime/'read-config.json'
 if not config.exists():config.write_bytes((HERE/'read-config.example.json').read_bytes());os.chmod(config,0o600)
 plist={'Label':LABEL,'ProgramArguments':[sys.executable,str(HERE/'service.py'),'--token-file',str(token),'--read-config',str(config)],'WorkingDirectory':str(HERE),'RunAtLoad':True,'KeepAlive':True,'ThrottleInterval':30,'StandardOutPath':str(runtime/'service.log'),'StandardErrorPath':str(runtime/'service-error.log')}
 path=runtime/(LABEL+'.plist');path.write_bytes(plistlib.dumps(plist));return path
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--install',action='store_true');a=p.parse_args();prepared=prepare();print(prepared)
 if a.install:
  dest=Path.home()/'Library/LaunchAgents'/prepared.name;dest.parent.mkdir(exist_ok=True);dest.write_bytes(prepared.read_bytes());os.chmod(dest,0o600)
  subprocess.run(['launchctl','bootstrap',f'gui/{os.getuid()}',str(dest)],check=True)
