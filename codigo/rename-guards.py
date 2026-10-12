from pathlib import Path
import json,shutil,re
D=Path('work/kizomba-site/dist')
names={'social1':'Guarita Social 1','social2':'Guarita Social 2','service':'Guarita de Serviço'}
for k in names:shutil.copy(f'work/guarita-sul/106-{k}.png',D/f'guarita-{k}-106.png')
rows=[]
def add(k,c,kind,room,x,y,system='Incêndio',note=''):
 rows.append(dict(id='',code='KZ-'+{'social1':'GS1','social2':'GS2','service':'GSV'}[k]+'-'+c,area=names[k],kind=kind,place='Piso 0 · '+room,layer='106',x=x,y=y,system=system,source='KICO_GE_AB_SEG_106_00.pdf',documentLocation=note or 'Símbolo da planta AS BUILT de 13/08/2015, por conferir em campo',address='',physical='',model='',verified='Por verificar',expected=True))
# Coordinates are percentages of the inspected per-guardhouse crops.
for k,positions in {'social1':[( 'GUAR','Guarita / posto',35,61),( 'ESP','Sala de espera',46,23),( 'ENT','Sala de bens / entregas',32,25)],'social2':[( 'GUAR','Guarita / posto',53,36),( 'ESP','Sala de espera',43,73),( 'ENT','Sala de bens / entregas',57,73)],'service':[( 'GUAR','Guarita / posto',77,32),( 'ESP','Sala de espera',36,43),( 'ENT','Sala de entregas',27,34),( 'REV','Sala de revista',55,34)]}.items():
 for c,r,x,y in positions:add(k,'DF-'+c,'Detector óptico de fumo',r,x,y)
for k,pts in {'social1':[(33,51),(38,51),(38,57),(51,71),(43,52),(43,37),(28,49)],'social2':[(43,48),(49,47),(49,42),(66,31),(59,47),(49,63),(41,42)],'service':[(55,26),(60,30),(71,23),(73,48),(77,48),(46,27),(60,22)]}.items():
 kinds=[('BI','Botão de incêndio','Guarita / junto ao acesso','Incêndio'),('BP','Botão de pânico','Guarita / posto','Pânico'),('AT','Módulo de entrada AT','Guarita / interface de pânico','Alarme técnico'),('SADI','Central de detecção e alarme de incêndio','Guarita / posto','Incêndio'),('RACK','Bastidor rede de segurança','Guarita / posto','Rede de segurança'),('SIR','Painel óptico e acústico','Circulação / junto ao posto','Incêndio'),('EXT','Extintor portátil ABC 4 kg','Guarita / junto ao acesso','Protecção portátil')]
 for (c,kind,r,sys),(x,y) in zip(kinds,pts):add(k,c,kind,r,x,y,sys)
add('service','CI','Painéis de intrusão / controlo de acessos','Guarita / posto',67,38,'Intrusão','O desenho indica x2 junto ao conjunto; confirmar referências e unidades instaladas')
layers=[dict(id='106',title='Incêndio, pânico e equipamentos',image='',date='13/08/2015'),dict(id='205',title='Intrusão, CFTV e postos',image='guarita-sul-205.png',date='14/08/2015'),dict(id='703',title='Sinalização e implantação',image='guarita-sul-703.png',date='14/08/2015')]
config={names[k]:dict(image=f'guarita-{k}-106.png',station=st,loop=lp) for k,st,lp in [('social1','SADI 3',2),('social2','SADI 1',2),('service','SADI 4',7)]}
(D/'guard-data.js').write_text('const guardEquipment='+json.dumps(rows,ensure_ascii=False)+';\nconst guardConfig='+json.dumps(config,ensure_ascii=False)+';\nconst guardLayers='+json.dumps(layers,ensure_ascii=False)+';\nlet guardLayer="106";\n')
p=D/'app.js';s=p.read_text();s=s.replace("'Guarita Social Sul'","'Guarita Social 1','Guarita Social 2','Guarita de Serviço'",3) if False else s
s=s.replace("['Administração','Salão de festas','Ginásio','Guarita Social Sul']","['Administração','Salão de festas','Ginásio','Guarita Social 1','Guarita Social 2','Guarita de Serviço']")
s=s.replace("['guarita social sul','guarita sul'].includes(text.toLowerCase())?'Guarita Social Sul':", "Object.keys(guardConfig).find(n=>n.toLowerCase()===text.toLowerCase())||") # ternary precedence fix below
s=s.replace("return Object.keys(guardConfig).find(n=>n.toLowerCase()===text.toLowerCase())||['ginásio'", "const guardName=Object.keys(guardConfig).find(n=>n.toLowerCase()===text.toLowerCase());if(guardName)return guardName;return ['ginásio'")
s=s.replace("a==='Ginásio'?gymEquipment:","guardConfig[a]?guardEquipment.filter(p=>p.area===a):a==='Ginásio'?gymEquipment:")
s=s.replace("if(a==='Guarita Social Sul')return {station:'Correspondência Social 1 / Social 2 por confirmar',loop:null};", "if(guardConfig[a])return !p||['Incêndio','Pânico','Alarme técnico'].includes(p.system)?{station:guardConfig[a].station,loop:guardConfig[a].loop}:{station:'Central / interface por identificar',loop:null};")
s=s.replace("selected==='Guarita Social Sul'?'As folhas incluem Social 1, Social 2 e Serviço. Correspondência entre Sul e o nome da planta pendente; não foi atribuída uma central nem um loop à zona Sul.':", "guardConfig[selected]?'Equipamentos da guarita identificada na planta 106. Camadas 205 e 703 apresentam as três guaritas. Endereços e posições físicas por verificar.':")
s=s.replace("if(selected==='Guarita Social Sul')renderGuardSouthPlans(points,opened);else if(['Administração','Ginásio'].includes(selected))", "if(guardConfig[selected]||['Administração','Ginásio'].includes(selected))")
s=s.replace("const layers=selected==='Ginásio'?gymLayers:adminLayers;const layer=layers.find(l=>l.id===(selected==='Ginásio'?gymLayer:adminLayer))||layers[0];", "const layers=guardConfig[selected]?guardLayers:selected==='Ginásio'?gymLayers:adminLayers;let layer=layers.find(l=>l.id===(guardConfig[selected]?guardLayer:selected==='Ginásio'?gymLayer:adminLayer))||layers[0];if(guardConfig[selected]&&layer.id==='106')layer={...layer,image:guardConfig[selected].image};")
s=s.replace("if(selected==='Ginásio')gymLayer=layer.dataset.adminLayer;", "if(guardConfig[selected])guardLayer=layer.dataset.adminLayer;else if(selected==='Ginásio')gymLayer=layer.dataset.adminLayer;")
s=s.replace("const guardDoc=e.target.closest('[data-guard-layer]');if(guardDoc){guardSouthLayer=guardDoc.dataset.guardLayer;render();return;}","")
s=s.replace("if(a==='Ginásio'&&p&&p.layer)gymLayer=p.layer;", "if(a==='Ginásio'&&p&&p.layer)gymLayer=p.layer;if(guardConfig[a]&&p&&p.layer)guardLayer=p.layer;")
s=s.replace("if(selected==='Ginásio'&&point&&point.layer)gymLayer=point.layer;", "if(selected==='Ginásio'&&point&&point.layer)gymLayer=point.layer;if(guardConfig[selected]&&point&&point.layer)guardLayer=point.layer;")
s=s[:s.index('\nfunction renderGuardSouthPlans')]
# Preserve ambiguous historic records as unassigned, without renaming them to a specific guardhouse.
s=s.replace("db=stored;if(db.residenceBasis", "db=stored;for(const r of [...db.events,...db.points,...db.tests])if(r.area==='Guarita Social Sul')r.area='Guarita · identificação pendente';if(db.residenceBasis")
p.write_text(s)
p=D/'index.html';s=p.read_text().replace('<button data-area="Guarita Social Sul">Guarita Social Sul</button>',''.join(f'<button data-area="{n}">{n}</button>' for n in names.values())).replace('<button data-area="Guaritas">Guaritas</button>',''.join(f'<button data-area="{n}">{n}</button>' for n in names.values()));p.write_text(s)
(D/'Guarita-Social-Sul-Kizomba.md').unlink(missing_ok=True)
(D/'Guaritas-Kizomba.md').write_text('''# Guaritas - nomes e referências das plantas

Adoptados exclusivamente Guarita Social 1, Guarita Social 2 e Guarita de Serviço. Fontes: SEG_106 (13/08/2015), SEG_205 e SEG_703 (14/08/2015), AS BUILT.

## Equipamentos
A planta 106 representa em cada Social três detectores ópticos (posto, sala de espera, sala de bens/entregas), um botão manual de incêndio, um pânico, um AT, uma central SADI, um bastidor, um painel óptico/acústico e um extintor ABC 4 kg. A guarita de Serviço tem também detector na sala de revista e conjunto de painéis de intrusão/acessos com indicação x2. Códigos de cadastro e marcadores não são endereços electrónicos. A quantidade/compatibilidade instalada deve ser conferida.

A planta 205 representa intrusão/CFTV e postos de vigilância nas três guaritas; está disponível como folha completa, sem inventar sensores/câmaras a partir do título ou legendas. A planta 703 apresenta implantação de equipamentos, sinais e evacuação. Os números da legenda não são endereços. As duas folhas completas mantêm os nomes originais para referência cruzada.

## Centrais e loops
Segundo SEG_720: Social 1 -> SADI 3 / loop 2; Social 2 -> SADI 1 / loop 2; Serviço -> SADI 4 / loop 7. A ligação refere-se ao sistema SADI; bastidores, painéis de intrusão/acessos e extintores não recebem automaticamente esse loop.

Abra a guarita pelo nome, seleccione a camada 106 e um marcador para registar ocorrência. Ver localização regressa à camada do equipamento. Os eventos continuam manuais/simulados, sem comunicação real com as centrais. As referências são por verificar em campo.

Registos antigos com a designação descartada são conservados como Guarita - identificação pendente; não se atribuem a uma guarita por suposição.
''')
for root in [Path('outputs')]:
 (root/'Guarita-Social-Sul-Kizomba.md').unlink(missing_ok=True)
# Replace previous pending-identification test with tests of the three documented identities.
p=Path('work/check-platform.cjs');s=p.read_text();s=re.sub(r'\nvm.runInContext\("selected=\'Guarita Social Sul\'.*?\n','\n',s)
s+='''\nfor(const [name,st,loop,count] of [['Guarita Social 1','SADI 3',2,10],['Guarita Social 2','SADI 1',2,10],['Guarita de Serviço','SADI 4',7,12]]){vm.runInContext(`selected=${JSON.stringify(name)};guardLayer='106';render();`,fresh);assert.equal(node('residenceDetail').hidden,false);assert.equal(vm.runInContext(`residencePoints(${JSON.stringify(name)}).length`,fresh),count);assert.equal((node('equipmentFloors').innerHTML.match(/class="adminMarker/g)||[]).length,count);const route=vm.runInContext(`pointRoute(${JSON.stringify(name)},null)`,fresh);assert.equal(route.station,st);assert.equal(route.loop,loop);}assert.equal(vm.runInContext("pointRoute('Guarita de Serviço',guardEquipment.find(p=>p.system==='Intrusão')).loop",fresh),null);vm.runInContext("selected='Guarita Social 1';eventDialog(true,'KZ-GS1-BP');",fresh);node('eventForm').onsubmit({preventDefault(){},target:{entries:[['area','Guarita Social 1'],['point','KZ-GS1-BP'],['place','Errado'],['type','Pânico'],['notes','Teste']]}});assert.equal(vm.runInContext('db.events.at(-1).station',fresh),'SADI 3');assert.equal(vm.runInContext('db.events.at(-1).loop',fresh),2);vm.runInContext("guardLayer='703';render();",fresh);assert.equal((node('equipmentFloors').innerHTML.match(/class="adminMarker/g)||[]).length,0);console.log('PASS: três guaritas conforme planta; 32 referências distintas; centrais/loops; ocorrência no ponto; intrusão sem loop SADI presumido.');\n''';p.write_text(s)
