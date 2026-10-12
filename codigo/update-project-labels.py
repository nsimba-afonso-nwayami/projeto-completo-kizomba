from pathlib import Path
import json,re
D=Path('work/kizomba-site/dist')
s=(D/'station-data.js').read_text();stations=json.loads(s.split('const stations=',1)[1].split(';',1)[0]);
for st in stations:
 for l in st['loops']:l['houses']=[]
(D/'station-data.js').write_text('const stations='+json.dumps(stations,ensure_ascii=False)+';\nconst stationMapping={};\n')
points=json.loads((D/'layout-data.js').read_text().split('=',1)[1].split(';',1)[0]);codes=sorted(p['code'] for p in points)
p=D/'app.js';s=p.read_text().replace("${esc(l.houses.join(', ')||'—')}","${esc(houseCodes.filter(c=>currentStationMapping[c]?.station===st.id&&currentStationMapping[c]?.loop===l.n).join(', ')||'Casas actuais: associação ao loop por confirmar')}")
s=s.replace('Estado real: desconhecido · distribuição de 2015 com numeração antiga, sem correspondência automática com as casas actuais','Casas descritas pela planta actual. Central e zonas comuns conforme documentação; associação residencial aos loops por confirmar.')
s=s.replace('<th>Residências</th>','<th>Casas · numeração actual</th>')
s=s.replace("$('stationCards').innerHTML=stations.map", "$('stationCards').innerHTML='<details><summary>Casas actuais por sector · '+houseCodes.length+' códigos</summary><p>'+['A','B','C','D','E'].map(letter=>'<strong>Sector '+letter+'</strong>: '+houseCodes.filter(c=>c.startsWith(letter)).join(', ')).join('</p><p>')+'</p><p>Central e loop: por confirmar para cada código actual.</p></details>'+stations.map")
s=s.replace('(planta de 2015 com numeração antiga; por conferir)','(referência documental da zona comum; por conferir)')
p.write_text(s)
p=D/'index.html';s=p.read_text().replace('123 residências · 60 com intrusão','Numeração actual · A01–A71 · B01–B12 · C01–C18 · D01–D14 · E01–E10').replace('Residências<strong>123</strong><small>Códigos da planta A01–E25</small>','Códigos actuais<strong>125</strong><small>A48/A49 e A62/A63 têm etiquetas conjuntas</small>').replace('4 centrais · 22 loops · 123 códigos antigos na distribuição de 2015. Distribuição transcrita do desenho AS BUILT de 31/08/2015. Não se aplica automaticamente à nova numeração. É necessário confirmar a tabela código antigo → código actual antes de associar as casas às centrais.','4 centrais · 22 loops · 125 códigos actuais na planta geral. As casas desta secção usam a numeração actual. A associação de cada código à central e ao loop está por confirmar; a planta actual não contém esses dados.').replace('Descarregar a distribuição completa','Descarregar casas actuais e estado das associações').replace('Planta dos percursos dos loops · SEG_113','Documento original dos percursos · SEG_113 (referência histórica)').replace('Desenho AS BUILT de 31/08/2015. Mostra percursos e referências à SADI de destino;','Documento original de 31/08/2015: os códigos impressos são históricos e não representam as descrições actuais das casas. Mostra percursos e referências à SADI de destino;')
p.write_text(s)
report='''# Centrais e loops - descrições actuais das casas

Numeração adoptada: Layout_atualizada_nova.pdf. 125 códigos distintos: A01-A71, B01-B12, C01-C18, D01-D14 e E01-E10. A48/A49 e A62/A63 são etiquetas conjuntas; não se extrapola a quantidade de casas independentes.

## Centrais e zonas comuns
Quatro centrais, 22 loops. Os nomes das centrais e zonas comuns provêm da documentação SADI. As casas actuais não foram atribuídas aos loops porque a planta actual não fornece a correspondência eléctrica.

| Central | Local | Loop | Casas actuais | Zonas comuns documentadas |
|---|---|---|---|---|
'''
for st in stations:
 for l in st['loops']:report+=f"| {st['id']} | {st['location']} | {l['n']} | Associação por confirmar | {', '.join(l['common']) or 'Sem zona comum indicada'} |\n"
report+='\n## Cadastro completo da numeração actual\n\n| Casa actual | Central | Loop | Estado |\n|---|---|---|---|\n'
for c in codes:report+=f'| {c} | Por confirmar | Por confirmar | Código da planta actual |\n'
report+='\nOs desenhos originais permanecem referências históricas. A sua numeração impressa não foi modificada. Os códigos residenciais históricos foram retirados das tabelas de operação e das descrições actuais. Validar a correspondência em campo e na configuração das centrais antes de completar as ligações.\n'
(D/'Centrais-e-Loops-Kizomba.md').write_text(report)
p=D/'Guia-Kizomba.md';s=p.read_text();s=re.sub(r'Total: 4 centrais, 22 loops e 123 residências distintas.*?(?=\n\n)', 'Total documental: 4 centrais e 22 loops. O cadastro actual contém 125 códigos. A relação das casas actuais e o estado das associações encontram-se em Centrais-e-Loops-Kizomba.md.',s,flags=re.S)
s=re.sub(r'A SADI 1 serve as casas A\..*?(?=\n\n)', 'As casas usam A01-A71, B01-B12, C01-C18, D01-D14 e E01-E10. A associação residencial de cada código actual à SADI e ao loop está por confirmar; não se mantêm as descrições do mapa anterior. As zonas comuns conservam as referências documentais independentes da numeração das casas.',s,flags=re.S)
s=s.replace('às 123 casas','às casas actuais').replace('123 casas','casas da planta actual').replace('Percorrer as 123 residências','Percorrer os códigos residenciais actuais');p.write_text(s)
p=D/'Residencias-e-Salao-Kizomba.md';p.write_text(p.read_text().replace('às 123 casas','às casas da planta actual'))
p=Path('work/check-platform.cjs');s=p.read_text();a=s.index("assert.equal(vm.runInContext(\"stationMapping.A01.station\"");b=s.index('\n\n',a);s=s[:a]+"assert.equal(vm.runInContext('Object.keys(stationMapping).length',context),0);assert.equal(vm.runInContext('stations.length',context),4);console.log('PASS: quatro centrais; códigos residenciais antigos retirados dos dados activos.');"+s[b:]
s+='''\nassert(node('stationCards').innerHTML.includes('A71'));assert(node('stationCards').innerHTML.includes('E10'));assert(!node('stationCards').innerHTML.includes('C32'));assert(!node('stationCards').innerHTML.includes('E25'));assert(node('stationCards').innerHTML.includes('Casas actuais: associação ao loop por confirmar'));console.log('PASS: Centrais e loops apresenta nomenclatura actual; 125 códigos; sem casas antigas nas tabelas operacionais.');\n''';p.write_text(s)
