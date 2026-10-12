from pathlib import Path
import json,shutil
D=Path('work/kizomba-site/dist')
for n in ['104','203','701']:shutil.copy(f'work/ginasio/{n}.png',D/f'ginasio-{n}.png')
rows=[]
def add(code,kind,place,x,y,system='Incêndio',layer='104'):
 rows.append(dict(id='',code='KZ-GIN-'+code,kind=kind,area='Ginásio',place=place,layer=layer,x=round(x/1888*100,2),y=round(y/1334*100,2),system=system,source=f'KICO_GE_AB_SEG_{layer}_00.pdf',documentLocation='Posição do símbolo no desenho AS BUILT; localização e função por conferir em campo',physical='',address='',model='',verified='Por verificar',expected=True))
for code,place,x,y in [('WC1','Piso 0 · Vestiário masculino',492,270),('WC2','Piso 0 · Vestiário feminino',492,413),('01','Piso 0 · Academia · sector superior esquerdo',613,288),('02','Piso 0 · Academia · sector superior direito',871,288),('03','Piso 0 · Academia · sector inferior esquerdo',613,473),('04','Piso 0 · Academia · sector inferior direito',871,473),('DEP','Piso 0 · Área técnica / canto inferior direito',985,576)]:add('DF-'+code,'Detector óptico de fumo',place,x,y)
for code,x in [('05',613),('06',871)]:add('DF-'+code,'Detector óptico de fumo no desvio do tecto falso','Piso 0 · Academia · sector central '+('esquerdo' if x==613 else 'direito'),x,380)
add('BI','Botão de incêndio','Piso 0 · Academia · junto ao acesso superior',543,175)
add('BP','Botão de pânico','Piso 0 · Academia · junto ao acesso superior',542,199,'Pânico')
add('AT-BP','Módulo de entrada AT','Piso 0 · Academia · interface junto ao pânico',527,218,'Alarme técnico')
add('AD','Alarme de chamada WC acessível','Piso 0 · WC acessível',455,175,'Assistência')
add('AT-WC','Módulo de entrada AT','Piso 0 · WC acessível · interface',460,208,'Assistência')
add('MC-VAC','Módulo de comando MC','Piso 0 · Depósito / comando VAC',528,328)
add('SIR-INT','Sirene óptico-acústica','Piso 0 · Academia · parede junto aos vestiários',525,380)
add('SIR-EXT','Sirene óptico-acústica','Exterior · representação na planta de cobertura',548,920)
for code,x in [('01',632),('02',890)]:add('AV-'+code,'Avisador visual','Piso 0 · Academia · sector central '+('esquerdo' if x==632 else 'direito'),x,398)
add('EXT','Extintor portátil ABC','Piso 0 · Academia · junto ao acesso superior',525,171,'Protecção portátil')
for code,place,x,y in [('01','Exterior · canto superior esquerdo',342,294),('02','Exterior · canto superior direito · primeira orientação',959,268),('03','Exterior · canto superior direito · segunda orientação',990,295),('04','Exterior · canto inferior esquerdo',313,736)]:add('CAM-'+code,'Câmara de vídeo',place,x,y,'CFTV','203')
add('ARM-C3','Armário de comunicações C3','Piso 0 · Área técnica / canto inferior direito',980,696,'Rede de segurança','203')
layers=[dict(id=n,title=t,image=f'ginasio-{n}.png',date=date) for n,t,date in [('104','Incêndio, pânico e chamada WC','13/08/2015'),('203','CFTV e comunicações','14/08/2015'),('701','Sinalização e evacuação','14/08/2015')]]
(D/'gym-data.js').write_text('const gymEquipment='+json.dumps(rows,ensure_ascii=False)+';\nconst gymLayers='+json.dumps(layers,ensure_ascii=False)+';\nlet gymLayer="104";\n')
p=D/'app.js';s=p.read_text().replace("['Administração','Salão de festas']","['Administração','Salão de festas','Ginásio']")
s=s.replace("a==='Administração'?adminEquipment:","a==='Ginásio'?gymEquipment:a==='Administração'?adminEquipment:")
s=s.replace("function pointRoute(a,p){", "function pointRoute(a,p){if(a==='Ginásio'){return !p||['Incêndio','Pânico','Alarme técnico','Assistência'].includes(p.system)?{station:'SADI 2',loop:8}:{station:'Central / interface por identificar',loop:null};}")
s=s.replace("if(selected==='Administração')renderAdminPlans(points,opened);","if(['Administração','Ginásio'].includes(selected))renderAdminPlans(points,opened);")
s=s.replace("const layer=adminLayers.find(l=>l.id===adminLayer)||adminLayers[0];", "const layers=selected==='Ginásio'?gymLayers:adminLayers;const layer=layers.find(l=>l.id===(selected==='Ginásio'?gymLayer:adminLayer))||layers[0];")
s=s.replace('${adminLayers.map(l=>','${layers.map(l=>').replace('alt="Planta da administração:','alt="Planta de ${esc(selected)}:')
s=s.replace("layer.id==='702'","['702','701'].includes(layer.id)")
s=s.replace("if(layer){adminLayer=layer.dataset.adminLayer;", "if(layer){if(selected==='Ginásio')gymLayer=layer.dataset.adminLayer;else adminLayer=layer.dataset.adminLayer;")
s=s.replace("if(a==='Administração'&&p&&p.layer)adminLayer=p.layer;","if(a==='Administração'&&p&&p.layer)adminLayer=p.layer;if(a==='Ginásio'&&p&&p.layer)gymLayer=p.layer;")
s=s.replace("if(selected==='Administração'&&point&&point.layer)adminLayer=point.layer;", "if(selected==='Administração'&&point&&point.layer)adminLayer=point.layer;if(selected==='Ginásio'&&point&&point.layer)gymLayer=point.layer;")
s=s.replace("$('residenceNote').textContent=selected==='Salão", "$('residenceNote').textContent=selected==='Ginásio'?'Referências das plantas 104, 203 e 701 de 2015; por verificar em campo. Incêndio: SADI 2 / Loop 8 conforme planta 720. CFTV: interface por identificar.':selected==='Salão")
s=s.replace("return houseCodes.includes(code)?area(code):", "return ['ginásio','ginasio','academia'].includes(text.toLowerCase())?'Ginásio':houseCodes.includes(code)?area(code):")
s=s.replace("else if(p.system==='Intrusão')", "else if(p.system==='Incêndio')f.type.value='Incêndio';else if(p.system==='Intrusão')")
p.write_text(s)
p=D/'index.html';s=p.read_text().replace('<script src="app.js">','<script src="gym-data.js"></script><script src="app.js">').replace('<button data-area="Salão de festas">Salão de festas</button>','<button data-area="Salão de festas">Salão de festas</button><button data-area="Ginásio">Ginásio</button>',1);p.write_text(s)
p=Path('work/package-platform.py');s=p.read_text().replace("'document-data.js','app.js'","'document-data.js','gym-data.js','app.js'");p.write_text(s)
p=Path('work/check-platform.cjs');s=p.read_text().replace("vm.runInContext(code,context);","vm.runInContext(fs.readFileSync('work/kizomba-site/dist/gym-data.js','utf8'),context);vm.runInContext(code,context);").replace("vm.runInContext(code,fresh);","vm.runInContext(fs.readFileSync('work/kizomba-site/dist/gym-data.js','utf8'),fresh);vm.runInContext(code,fresh);")
s+='''\nvm.runInContext("selected='Ginásio';gymLayer='104';render();",fresh);assert.equal(node('residenceDetail').hidden,false);assert.equal(vm.runInContext("residencePoints('Ginásio').length",fresh),25);assert.equal((node('equipmentFloors').innerHTML.match(/class="adminMarker/g)||[]).length,20);assert.equal(vm.runInContext("pointRoute('Ginásio',gymEquipment[0]).loop",fresh),8);assert.equal(vm.runInContext("pointRoute('Ginásio',gymEquipment.find(p=>p.system==='CFTV')).loop",fresh),null);vm.runInContext("eventDialog(true,'KZ-GIN-BP');",fresh);assert.equal(node('eventForm').elements.type.value,'Pânico');node('eventForm').onsubmit({preventDefault(){},target:{entries:[['area','Ginásio'],['point','KZ-GIN-BP'],['place','Errado'],['type','Pânico'],['notes','Ensaio']]}});assert.equal(vm.runInContext('db.events.at(-1).station',fresh),'SADI 2');assert.equal(vm.runInContext('db.events.at(-1).loop',fresh),8);vm.runInContext("gymLayer='701';render();",fresh);assert.equal((node('equipmentFloors').innerHTML.match(/class="adminMarker/g)||[]).length,0);console.log('PASS: ginásio; 25 referências documentais; selecção e ocorrência localizada; incêndio SADI2/Loop8; CFTV separado; sinalização sem endereços fictícios.');\n''';p.write_text(s)
(D/'Ginasio-Kizomba.md').write_text('''# Ginásio / Academia - levantamento documental

Fontes: KICO_GE_AB_SEG_104_00.pdf (13/08/2015), KICO_GE_AB_SEG_203_00.pdf e KICO_GE_AB_SEG_701_00.pdf (14/08/2015). Todas são AS BUILT, uma página. Os símbolos foram transcritos para referências de cadastro; não são prova de equipamento instalado actualmente.

## Planta 104
20 referências: nove detectores ópticos (dois representados no desvio do tecto falso), um botão de incêndio, um botão de pânico, dois módulos AT, um módulo MC junto à indicação VAC, um alarme de chamada de WC acessível, duas sirenes óptico-acústicas (uma representada na cobertura), dois avisadores visuais e um extintor ABC. A capacidade do extintor e a função/posição final dos módulos devem ser verificadas no local. A representação da cobertura não prova a altura exacta da sirene.

As descrições de sector permitem encontrar o símbolo no desenho. Os marcadores são posições documentais aproximadas; a coluna posição física e os endereços continuam vazios até levantamento em campo. O pormenor do WC contém componentes do conjunto (cordão, reposição, painel, fonte): não foram contados novamente como equipamentos independentes da planta.

## Planta 203
Quatro câmaras exteriores, sendo duas no canto superior direito com orientações distintas, e um armário C3. O esquema apresenta conversão óptica e alimentação, sem demonstrar quantidade instalada desses componentes. CFTV não foi atribuído ao loop de incêndio. Não há detectores de intrusão representados nesta planta.

## Planta 701
Camada documental de sinalização, percursos, iluminação de emergência e barreira EI60. Números da legenda não são endereços electrónicos; barra antipânico é ferragem de evacuação, não botão electrónico de pânico.

## Ligação e utilização
A distribuição geral SEG_720 associa Academia, área técnica SADI2 e Churrascaria ao SADI 2, loop 8. A planta local não fornece endereços, modelo completo dos módulos ou protocolo de supervisão.

Abra Ginásio, seleccione a camada 104 ou 203, clique no marcador ou equipamento e registe uma ocorrência. A ficha mantém o local do equipamento escolhido; Ver localização volta à respectiva camada. Confirme modelo, posição física, função, central, circuito e endereço com o técnico. Só depois se deve validar recepção real de eventos. A plataforma continua manual/demonstração, sem comandos reais.
''')
