from pathlib import Path
import re,json
D=Path('work/kizomba-site/dist');p=D/'app.js';s=p.read_text()
rows=[('P0-DT-SALA','Detector termovelocimétrico','Piso 0 · Sala de estar / jantar'),('P0-DT-COZ','Detector termovelocimétrico','Piso 0 · Cozinha'),('P0-DF-LAV','Detector óptico de fumo','Piso 0 · Lavandaria'),('P1-DA-S1','Detector de fumo óptico-acústico','Piso 1 · Suite 01'),('P1-DA-S2','Detector de fumo óptico-acústico','Piso 1 · Suite 02'),('P1-DA-MASTER','Detector de fumo óptico-acústico','Piso 1 · Suite master'),('P0-BP-VEST','Botão de pânico','Piso 0 · Vestíbulo'),('P1-BP-MASTER','Botão de pânico','Piso 1 · Suite master'),('P0-SOA-ENT','Sirene óptico-acústica','Piso 0 · Entrada / acesso ao lavabo'),('P1-SIR-HALL','Sirene de alarme','Piso 1 · Hall / circulação'),('P1-FLASH-EXT','Flash estroboscópico','Piso 1 · Varanda da suite master'),('P0-AT','Módulo de entrada AT','Piso 0 · Despensa / junto ao vestíbulo'),('P1-AT','Módulo de entrada AT','Piso 1 · Hall / circulação'),('P1-MC','Módulo de comando MC','Piso 1 · Hall / circulação'),('P1-FONTE','Fonte de alimentação','Piso 1 · Hall / circulação')]
# BP namespace keeps documentary references distinct from prior narrative records.
rows=[('BP-'+a,b,c) for a,b,c in rows]
s=re.sub(r'const template=\[.*?\];','const template='+json.dumps(rows,ensure_ascii=False)+';',s)
s=s.replace("verified:'Por verificar',expected:true}","verified:'Por verificar',expected:true,source:'BP-GE_AB_SEG_120_T3_00.pdf',system:kind==='Botão de pânico'?'Pânico':'Incêndio',documentLocation:'Símbolo na planta T3 AS BUILT de 05/11/2014; orientação normal/espelhada por confirmar'}")
s=s.replace("const rooms=[['Piso 0',['Sala','Corredor da casa de banho','Cozinha','Entrada']],['Piso 1',['Quarto 1','Quarto 2','Quarto 3','Hall','Exterior do quarto principal']]];", "const rooms=[['Piso 0',['Sala de estar / jantar','Cozinha','Lavandaria','Vestíbulo','Entrada / acesso ao lavabo','Despensa / junto ao vestíbulo']],['Piso 1',['Suite 01','Suite 02','Suite master','Hall / circulação','Varanda da suite master']]];")
s=s.replace('dez equipamentos previstos pelo relato','15 referências da planta SADI T3 de 05/11/2014').replace('Não representa posições exactas no tecto ou nas paredes.','Orientação normal/espelhada e posições físicas por confirmar.')
s=s.replace('O relato actual e esta planta divergem: conferir em campo antes de alterar o cadastro.','Esta planta é a única referência adoptada para o modelo residencial; confirmar a instalação em campo.')
s=s.replace("else if(p.kind==='Detector de fumo'||p.kind==='Botão de incêndio')", "else if(p.kind.startsWith('Detector ')||p.kind==='Botão de incêndio')")
s=s.replace("try{const s=JSON.parse(localStorage.getItem(key));if(valid(s))db=s;}catch{}", """try{const stored=JSON.parse(localStorage.getItem(key));if(valid(stored)){db=stored;if(db.residenceBasis!=='BP120-2014'){const legacy=/^KZ-[A-E]\\d{2}-(P0-DF-(SALA|CORR|COZ)|P1-DF-Q[123]|P0-BP-SALA|P0-SIR-ENT|P1-SIR-(HALL|EXT))$/;const retired=db.points.filter(p=>legacy.test(p.code));db.supersededPoints=[...(db.supersededPoints||[]),...retired];db.points=db.points.filter(p=>!legacy.test(p.code));db.residenceBasis='BP120-2014';localStorage.setItem(key,JSON.stringify(db));}}}catch{}""")
p.write_text(s)
p=D/'index.html';s=p.read_text();s=s.replace('738 detectores · 123 botões de pânico · 369 sirenes esperados pelo relato.','Modelo residencial baseado exclusivamente na planta SADI T3: 15 referências por casa, incluindo detectores, pânico, avisadores, módulos e fonte; instalação por verificar.');s=s.replace('Os dez equipamentos descritos aparecem como previstos até serem conferidos em campo.','As referências da planta SADI T3 aparecem por verificar até à conferência em campo.');p.write_text(s)
p=D/'Guia-Kizomba.md';s=p.read_text();a=s.index('Por residência, segundo a descrição:');b=s.index('Nas zonas comuns,',a);s=s[:a]+'''Por residência, exclusivamente segundo BP-GE_AB_SEG_120_T3_00.pdf (05/11/2014):

| Piso | Referência | Local | Quantidade |
|---|---|---|---:|
| 0 | Detector termovelocimétrico | Sala e cozinha | 2 |
| 0 | Detector óptico de fumo | Lavandaria | 1 |
| 1 | Detector de fumo óptico-acústico | Suite 01, Suite 02, Suite master | 3 |
| 0 / 1 | Botão de pânico | Vestíbulo / Suite master | 2 |
| 0 | Sirene óptico-acústica | Entrada / acesso ao lavabo | 1 |
| 1 | Sirene de alarme | Hall / circulação | 1 |
| 1 | Flash estroboscópico | Varanda da suite master | 1 |
| 0 / 1 | Módulo AT | Despensa / hall | 2 |
| 1 | Módulo MC e fonte de alimentação | Hall / circulação | 2 |

São 15 referências documentais por modelo. Não são 15 endereços electrónicos: módulos, fonte e avisadores podem ter ligações distintas, a confirmar. A planta apresenta versões normal e espelhada. Não há associação automática da orientação a cada casa. Os 123 códigos da planta geral mantêm-se; não se extrapolam quantidades instaladas a partir do modelo. O relato inicial foi retirado da base residencial por instrução do utilizador.

'''+s[b:];s=s.replace('Conferir os seis detectores e o botão de pânico no cadastro.','Conferir todas as referências do desenho T3 no cadastro.').replace('os locais dos dez equipamentos descritos: seis detectores de fumo, um botão de pânico e três sirenes.','os locais das 15 referências documentais do modelo T3.').replace('previstos segundo o relato','baseados exclusivamente na planta SADI T3');p.write_text(s)
p=D/'Residencias-e-Salao-Kizomba.md';s=p.read_text();s=re.sub(r'Esta distribuição diverge.*?Não atribuir orientação', 'O relato inicial foi descartado; apenas esta planta fundamenta o modelo residencial. Não atribuir orientação',s);s=s.replace('Resolver as diferenças entre relato, planta e instalação actual','Conferir a planta contra a instalação actual');s+='\nAs fichas automáticas provenientes do relato antigo são retiradas do cadastro activo e preservadas em supersededPoints no armazenamento/exportação. O histórico de ocorrências e os equipamentos adicionais permanecem; eventos antigos sem ponto no modelo actual não são remapeados automaticamente.\n';p.write_text(s)
p=D/'Centrais-e-Loops-Kizomba.md';s=p.read_text().replace('dos seis detectores de cada residência','dos dispositivos de cada residência');p.write_text(s)
