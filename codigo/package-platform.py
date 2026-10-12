from pathlib import Path
import base64,re,zipfile,shutil
D=Path('work/kizomba-site/dist');O=Path('outputs');O.mkdir(exist_ok=True)
h=(D/'index.html').read_text()
js='\n'.join((D/n).read_text() for n in ['layout-data.js','station-data.js','admin-data.js','document-data.js','gym-data.js','guard-data.js','security-data.js','entity-data.js','app.js','integration-client.js'])
for p in list(D.glob('*.png'))+list(D.glob('*.jpg'))+list(D.glob('*.mp4')):
 mime={'.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4'}[p.suffix]
 uri='data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
 h=h.replace('src="'+p.name+'"','src="'+uri+'"')
 js=js.replace("'"+p.name+"'", "'"+uri+"'").replace('"'+p.name+'"','"'+uri+'"')
h=re.sub(r'<script src="[^"]+"></script>','',h).replace('</body>','<script>'+js.replace('</script','<\\/script')+'</script></body>')
for n in ['index.html','Plataforma-Kizomba.html']:(O/n).write_text(h)
Path('work/index-inline.js').write_text(js)
for p in D.glob('*.md'):shutil.copy(p,O/p.name)
with zipfile.ZipFile(O/'Kizomba-Plataforma-e-Guia.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.iterdir():
  if p.suffix in ['.html','.md','.txt']:z.write(p,p.name)
print('Packaged standalone HTML and ZIP',len(h))
