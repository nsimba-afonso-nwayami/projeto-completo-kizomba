from pathlib import Path
import pdfplumber,json,re,shutil
D=Path('work/kizomba-site/dist')
with pdfplumber.open('/Users/macbookpro2017/Downloads/Layout_atualizada_nova.pdf') as doc:
 p=doc.pages[0];words=p.extract_words();found={}
 for w in words:
  t=w['text'];t=re.sub(r'([A-E])\1([0-9])\2([0-9])\3',r'\1\2\3',t)
  if re.fullmatch('[A-E][0-9]{2}',t):found.setdefault(t,[]).append(w)
  if t=='9' and 1300<w['x0']<1400:found['A09']=[w]
  if t=='45':found['A45']=[w]
 expected=[f'{l}{n:02d}' for l,end in [('A',71),('B',12),('C',18),('D',14),('E',10)] for n in range(1,end+1)]
 missing=set(expected)-set(found);print('Missing',missing);assert not missing
 points=[]
 for c in expected:
  ws=found[c];w=ws[-1];points.append(dict(code=c,x=round((w['x0']+w['x1'])/2/p.width*100,5),y=round((w['top']+w['bottom'])/2/p.height*100,5)))
 print('Current codes',len(points));(D/'layout-data.js').write_text('const layoutPoints='+json.dumps(points)+';\nconst currentLayoutVersion="Layout_atualizada_nova";\n')
shutil.copy('work/layout-novo.png',D/'layout.png')
p=D/'app.js';s=p.read_text();s=s.replace("const key='kizomba-demo-v1';", "const key='kizomba-demo-v1';\nconst currentStationMapping={};")
s=s.replace("return stationMapping[a.replace(/^Casa /,'')]||null;", "return currentStationMapping[a.replace(/^Casa /,'')]||null;")
s=s.replace("stationMapping[e.area.replace(/^Casa /,'')]","currentStationMapping[e.area.replace(/^Casa /,'')]")
s=s.replace("'Central / loop: seleccionar uma residência'", "selected.startsWith('Casa ')?'Central / loop da numeração actual: correspondência por confirmar':'Central / loop: seleccionar uma área'")
s=s.replace('`KZ-${code}-${suffix}`','`KZ-ATUAL-${code}-${suffix}`').replace('`KZ-${n}-${suffix}`','`KZ-ATUAL-${n}-${suffix}`')
s=s.replace('Código da casa na planta (ex.: A01, B12, C32, D14, E25).','Código actual da casa na planta (ex.: A71, B12, C18, D14, E10).')
s=s.replace("db=stored;for(const r", "db=stored;if(db.layoutVersion!==currentLayoutVersion){for(const record of [...db.events,...db.points,...db.tests,...(db.supersededPoints||[])]){if(/^Casa [A-E]\\d{2}$/.test(record.area)){record.previousArea=record.area;record.area=record.area.replace('Casa ','Casa antiga ');record.numbering='Numeração anterior · correspondência pendente';}}db.layoutVersion=currentLayoutVersion;localStorage.setItem(key,JSON.stringify(db));}for(const r")
s=s.replace('Percorrer as 123 casas e zonas comuns.','Percorrer os códigos da planta actual e as zonas comuns.').replace('planta de 2015; por conferir','planta de 2015 com numeração antiga; por conferir')
s=s.replace('Central / loop: seleccionar uma área', 'Central / loop: seleccionar uma área')
s=s.replace('Distribuição da planta de 2015','Distribuição da planta de 2015 (numeração antiga)')
s=s.replace('Estado real: desconhecido · distribuição da planta de 2015, por conferir','Estado real: desconhecido · distribuição de 2015 com numeração antiga, sem correspondência automática com as casas actuais')
p.write_text(s)
p=D/'index.html';s=p.read_text();s=s.replace('Planta clicável das 123 residências','Planta geral actualizada · numeração em uso').replace('Planta geral do condomínio Kizomba com sectores A a E','Planta geral actualizada do condomínio Kizomba').replace('Posições retiradas do PDF enviado.','Numeração e posições da planta Layout_atualizada_nova.pdf. 125 códigos: A01–A71, B01–B12, C01–C18, D01–D14 e E01–E10. A48/A49 e A62/A63 têm etiquetas conjuntas no desenho; a contagem de códigos não confirma a quantidade de casas independentes.').replace('4 centrais · 22 loops · 123 casas.','4 centrais · 22 loops · 123 códigos antigos na distribuição de 2015.').replace('Distribuição transcrita do desenho AS BUILT de 31/08/2015, a confirmar na instalação actual.','Distribuição transcrita do desenho AS BUILT de 31/08/2015. Não se aplica automaticamente à nova numeração. É necessário confirmar a tabela código antigo → código actual antes de associar as casas às centrais.');p.write_text(s)
(D/'Numeracao-Actual-Kizomba.md').write_text('''# Planta geral e numeração actual

Fonte adoptada: Layout_atualizada_nova.pdf, recebida em 7/10/2026 como numeração actualmente utilizada. Foram extraídos e conferidos 125 códigos distintos: A01-A71 (71), B01-B12 (12), C01-C18 (18), D01-D14 (14), E01-E10 (10).

A48 / A49 e A62 / A63 aparecem como etiquetas conjuntas. Os dois códigos de cada etiqueta ficam disponíveis; isso não estabelece duas casas independentes por implantação. Não se altera a quantidade física anteriormente declarada sem confirmação. Repetições sobrepostas de texto (por exemplo A31 e A42) foram deduplicadas, e A 9 normalizado para A09. Não foram inferidas funções pelas cores.

A planta actual substitui a imagem e os códigos do mapa principal. As plantas SADI 720/113, CFTV 200 e rondas 300 preservam os códigos antigos impressos nos documentos. Não há correspondência validada entre numeração antiga e actual; os códigos iguais não provam que seja a mesma residência. A associação às centrais/loops das casas actuais permanece pendente. As zonas comuns mantêm as associações documentais que independem da renumeração residencial.

Os equipamentos das casas actuais usam códigos KZ-ATUAL-..., mantendo o modelo exclusivamente da planta residencial BP120. Na primeira abertura da nova versão, registos residenciais anteriores são preservados como Casa antiga XX, com previousArea e numbering no armazenamento/exportação. Não aparecem nas casas actuais por mera igualdade do código. Não há eliminação do histórico nem remapeamento presumido.

Para concluir a migração operacional, validar uma tabela código antigo, código actual, endereço na central, central e loop. Conferir em campo cada ponto antes de mover fichas e associar eventos reais.
''')
