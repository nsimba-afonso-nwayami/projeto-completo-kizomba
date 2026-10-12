> Actualização: mapa principal e cadastro residencial usam Layout_atualizada_nova.pdf. Distribuições de 2015 usam numeração antiga; associação às casas actuais pendente. Consultar Numeracao-Actual-Kizomba.md.

# Condomínio Kizomba — guia de levantamento, configuração e operação

Versão preliminar · 7 de Outubro de 2026

Este guia organiza a descrição fornecida, as seis fotografias e os PDFs «Layout completo _ Casas antigas» e «KICO_GE_AB_SEG_720_00». Não é o projecto eléctrico nem certifica a instalação. A planta geral actual é Layout_atualizada_nova.pdf: 125 códigos originais correspondem a 123 casas: A48/A49 é uma única casa, assim como A62/A63, conforme confirmação do utilizador em 08/10/2026. As plantas anteriores permanecem referências históricas. O segundo desenho indica as quatro centrais e os respectivos loops, mas não os endereços individuais dos dispositivos ou as interfaces de comunicação. As quantidades das zonas comuns e os modelos dos equipamentos precisam de confirmação.

## 1. O que existe e o que falta confirmar

Por residência, exclusivamente segundo BP-GE_AB_SEG_120_T3_00.pdf (05/11/2014):

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

São 15 referências documentais por modelo. Não são 15 endereços electrónicos: módulos, fonte e avisadores podem ter ligações distintas, a confirmar. A planta apresenta versões normal e espelhada. Não há associação automática da orientação a cada casa. Os códigos da planta geral foram substituídos pela numeração actual; não se extrapolam quantidades instaladas a partir do modelo. O relato inicial foi retirado da base residencial por instrução do utilizador.

Nas zonas comuns, registar separadamente salão de festas, administração, cada guarita e área técnica da piscina. Nas guaritas foram descritos um botão de pânico e um de incêndio. A função dos dois botões de cada outra área deve ser confirmada. Na piscina foram descritos dois botões e sirenes de incêndio e inundação; falta confirmar que sensores ou contactos originam a inundação.

O levantamento de 08/10/2026 confirma Siemens FC726 na placa técnica da Guarita de Serviço (SADI 4). O utilizador confirma a mesma marca e modelo nas quatro centrais. FS726 é uma etiqueta frontal. Os módulos internos observados estão documentados em Levantamento-Centrais-2026-10-08.md e não são extrapolados para as outras centrais. Os indicadores AVARIA e ISOLADOS parecem acesos na fotografia; verificar o estado actual e registar os respectivos pontos. As fotos dos botões e detectores não mostram referências técnicas suficientes para estabelecer compatibilidade ou bornes. A cor azul, por si só, não confirma a função programada do botão.

## 2. Infraestrutura de referência

```text
Detectores / botões de incêndio → circuitos ou módulos compatíveis → central de incêndio
Sensores de intrusão → central de intrusão / interface existente ──┐
Botões de pânico → entradas identificadas e supervisionadas ──────┤
Sensor de inundação → entrada técnica identificada ───────────────┤
                                                              ↓
                                           supervisão centralizada autorizada
                                                              ↓
                              posto de segurança: local, evento e atendimento
```

É um esquema funcional proposto, não uma indicação de ligações físicas. No sistema existente, o técnico deverá identificar por onde cada sinal chega à central. Não assumir que todos os dispositivos estão directamente no mesmo circuito ou usam o mesmo protocolo.

Para software em tempo real: central/interface suportada → serviço de integração na rede local → base de dados e registo de auditoria → aplicação do posto de segurança. A central deverá continuar a detectar e a comandar os alarmes quando o computador ou a aplicação falhar. A perda de comunicação deve aparecer como estado desconhecido/sem comunicação, nunca como normal.

O equipamento local precisa de alimentação de reserva dimensionada, rede protegida, cópias de segurança e contas individuais. O caminho exacto depende da interface Siemens e do sistema de intrusão existentes. Um contacto geral de alarme não permite, por si só, identificar residência e detector: é necessário receber identificadores individuais ou sinais separados suficientes.

## 3. Primeiro passo: levantamento sem alterar o sistema

1. Nomear o responsável do condomínio e o técnico de incêndio/intrusão.
2. Registar referência completa da central, versão de firmware, placas, módulos e interfaces. Não abrir a central sem o procedimento eléctrico apropriado e pessoal qualificado.
3. Obter a planta final da instalação, o ficheiro de configuração, o manual da variante e o histórico de manutenção.
4. Ler e registar as avarias e pontos isolados actuais. Não limpar eventos para esconder falhas.
5. Visitar cada residência e zona comum. Dar um código físico a cada ponto e registar a sua localização.
6. Comparar o inventário com a lista de dispositivos que a central conhece. Um dispositivo montado pode estar sem ligação ou mal identificado.
7. Confirmar todos os dispositivos de intrusão e a forma de armar/desarmar cada casa.
8. Confirmar a origem e o alcance de cada sirene: incêndio, intrusão, pânico ou inundação. Não atribuir funções apenas pela aparência.

Ficha por ponto: código; casa/área; piso; divisão; função; fabricante; referência; central; circuito/loop; endereço/canal; módulo; estado; data do teste; resultado; observações. O endereço real tem de ser lido ou validado pelo técnico; o código administrativo não é um endereço electrónico.

## 4. Nomes padronizados

Exemplo administrativo para a Casa A01 da planta. Estes códigos são nomes de cadastro; o endereço electrónico real precisa de ser verificado.

| Código | Nome apresentado ao operador |
|---|---|
| KZ-A01-P0-DF-SALA | Casa A01 · Piso 0 · Sala · Detector de fumo |
| KZ-A01-P0-DF-CORR | Casa A01 · Piso 0 · Corredor · Detector de fumo |
| KZ-A01-P0-DF-COZ | Casa A01 · Piso 0 · Cozinha · Detector de fumo |
| KZ-A01-P1-DF-Q1 | Casa A01 · Piso 1 · Quarto 1 · Detector de fumo |
| KZ-A01-P1-DF-Q2 | Casa A01 · Piso 1 · Quarto 2 · Detector de fumo |
| KZ-A01-P1-DF-Q3 | Casa A01 · Piso 1 · Quarto 3 · Detector de fumo |
| KZ-A01-P0-BP-SALA | Casa A01 · Piso 0 · Sala · Pânico |
| KZ-A01-P0-SIR-ENT | Casa A01 · Piso 0 · Entrada · Sirene |
| KZ-A01-P1-SIR-HALL | Casa A01 · Piso 1 · Hall · Sirene |
| KZ-A01-P1-SIR-EXT | Casa A01 · Piso 1 · Exterior do quarto principal · Sirene |

Usar igualmente códigos para cada guarita e zona comum. Se a central limitar o comprimento do texto, usar uma abreviatura e manter a correspondência completa no cadastro.

## 5. Preparar as regras antes de programar

A matriz causa–efeito define o que acontece quando cada ponto actua. O projectista/técnico e a administração devem validar o alcance da evacuação e as acções de cada sistema.

| Entrada | Evento distinto | Atendimento | Saídas a confirmar no projecto |
|---|---|---|---|
| Detector ou botão de incêndio | Incêndio | Procedimento de emergência e evacuação | Sirenes e comandos definidos para a área e eventual alarme geral |
| Botão de pânico | Pânico | Apoio da segurança | Aviso discreto ou audível conforme o plano de segurança |
| Sensor de intrusão | Intrusão | Segurança; considerar estado armado | Sirenes/avisos de intrusão previstos |
| Sensor de inundação | Alarme técnico de inundação | Manutenção e protecção da área | Sirene/aviso técnico previsto |
| Cabo, dispositivo ou fonte com falha | Avaria | Manutenção e avaliação da protecção afectada | Aviso de avaria |
| Perda de comunicação com software | Sem comunicação | Verificação no posto e na central | Aviso técnico; não declarar normalidade |

Incêndio deve permanecer operacional independentemente do estado armado da intrusão. Pânico deve ter a disponibilidade definida no projecto, tipicamente permanente. Não programar atrasos de incêndio, alcance de sirenes, corte de energia ou accionamento de bombas a partir de regras genéricas deste guia. A adequação do detector na cozinha precisa de avaliação do modelo e do ambiente; vapores e fumos de cozinha podem causar actuações indevidas.

## 6. Como ligar e configurar — sequência para o técnico

Estas tarefas exigem formação no equipamento. A equipa sem formação pode acompanhar, identificar locais e preencher as fichas.

1. **Guardar a situação actual.** Obter cópia da configuração, versão do software e relatório dos pontos. Preparar o procedimento de recuperação.
2. **Planear a intervenção.** Avisar moradores, segurança e destinatários de transmissão de alarmes. Definir zona de trabalho, duração e medidas de protecção durante a indisponibilidade.
3. **Validar a compatibilidade.** Conferir central, detectores, bases, botões, sirenes, módulos e protocolos nas listas do fabricante. A presença de marcas diferentes exige verificar como se integram.
4. **Conferir o circuito.** Validar tipo de linha, trajecto, continuidade, polaridade, supervisão, isolamento, protecção exterior e capacidade. Dimensionar alimentação, baterias e sirenes. Não aplicar tensão de rede a entradas de sinal nem ligar sirenes directamente a um loop sem compatibilidade documentada.
5. **Executar a cablagem pelo manual exacto.** Ligar cada dispositivo ao circuito ou módulo apropriado, identificando os cabos. Resistências de fim de linha, tensões e bornes variam por modelo: não existem valores universais seguros para esta instalação.
6. **Identificar os pontos.** Ler/importar os dispositivos com a ferramenta apropriada. Associar cada endereço/canal ao código e local verificados. Não usar uma autoconfiguração que substitua o projecto existente sem cópia e plano de recuperação.
7. **Organizar as zonas.** Agrupar por residência, piso e áreas comuns conforme o projecto; manter distinguíveis as funções de incêndio e os alarmes de segurança/técnicos.
8. **Aplicar a matriz causa–efeito validada.** Mapear entradas e saídas, incluindo o comportamento das três sirenes de cada casa.
9. **Carregar a configuração compatível.** Usar o software e versão autorizados para a central, com o procedimento do fabricante. Não actualizar firmware apenas para tentar resolver uma avaria.
10. **Testar uma residência piloto.** Conferir cada ponto e cada saída antes de repetir a configuração nas restantes casas. Repetir nomes e estrutura; os endereços e a cablagem precisam de validação individual.
11. **Testar integralmente.** Percorrer todos os pontos e áreas, comparar resultados com a matriz e corrigir divergências.
12. **Entregar.** Guardar configuração final, planta actualizada, resultados dos testes e instruções para operadores.

Sem as referências técnicas e a planta, não é possível fornecer uma sequência fiel de menus, bornes, resistências ou endereçamento para a central fotografada.

## 7. Teste por residência

1. Confirmar que todos sabem que é um teste e que existe protecção durante a intervenção.
2. Conferir todas as referências do desenho T3 no cadastro.
3. O técnico activa cada detector com equipamento de ensaio aprovado, conforme o seu manual. Não usar chama, cigarro ou aquecimento improvisado.
4. No posto, conferir casa, piso, divisão, tipo de evento e hora. Se o sistema só indicar a casa, documentar essa limitação; o software não pode inventar a divisão.
5. Verificar as sirenes esperadas segundo a matriz, incluindo audibilidade nos locais necessários. Ter três sirenes não comprova cobertura acústica adequada.
6. Ensaiar o pânico com coordenação da segurança.
7. Ensaiar a intrusão com o estado armado apropriado e confirmar que não actua como incêndio.
8. O técnico testa avaria/supervisão conforme o fabricante e confirma o retorno ao estado correcto. Não deixar cabos desligados após os ensaios.
9. Retirar modos de teste e isolamentos temporários; conferir central e software.
10. Registar resultado, falhas, responsável e data. Se uma falha permanecer, documentar a protecção afectada e as medidas temporárias; não marcar o teste como aprovado.

Para piscina e áreas comuns, usar a mesma sequência e confirmar separadamente incêndio, pânico e inundação. Não provocar inundação real para testar; usar o método de ensaio previsto para o sensor.

## 8. Operação para o posto de segurança

**Ao receber incêndio:** ler o local, seguir imediatamente o plano de emergência, alertar os responsáveis e serviços de socorro previstos, orientar a evacuação e não atrasar essas acções à espera de confirmação pelo software.

**Ao receber pânico:** identificar o local e activar o procedimento de apoio da segurança, evitando uma divulgação que possa agravar a situação.

**Ao receber intrusão:** identificar casa, ponto e estado armado; encaminhar a segurança conforme o procedimento.

**Ao receber inundação:** encaminhar manutenção, avaliar riscos eléctricos e manter pessoas afastadas da área afectada.

**Ao receber avaria:** registar ponto, mensagem e protecção afectada; abrir atendimento técnico. Uma avaria não significa que a protecção desse ponto esteja disponível.

Comandos têm significados diferentes:

| Comando | Significado |
|---|---|
| Reconhecer | O operador recebeu o evento; não corrige a causa |
| Silenciar besouro | Cala o aviso interno da central, se autorizado; não implica calar sirenes |
| Silenciar sirenes | Altera a sinalização aos ocupantes; requer o procedimento de emergência e autorização aplicáveis |
| Repor/reset | Solicita retorno após causa resolvida e local seguro; o evento pode voltar |
| Isolar ponto | Retira temporariamente a sua função de protecção; exige responsável, motivo, medidas temporárias e prazo |
| Corrigir avaria | Reparar a causa e testar o ponto; não é apagar a mensagem |

Não pressionar Reposição repetidamente nem isolar um detector apenas para parar uma ocorrência não investigada. O botão Presença depende da programação existente; a legenda não é suficiente para determinar os seus efeitos.

## 9. Software de supervisão e controlo

A plataforma entregue é uma primeira versão demonstrativa com cadastro, ocorrências manuais/simuladas, acompanhamento e pedido de isolamento. Não recebe eventos reais nem transmite comandos à central. Os dados ficam no navegador deste dispositivo; exportar uma cópia JSON. Não há sincronização entre computadores nem contas operacionais nesta versão.

Para converter em sistema operacional, é necessário:

1. Identificar as centrais e interfaces existentes, respectivas licenças e protocolos documentados.
2. Confirmar que a integração disponibiliza alarmes e avarias por ponto, bem como os comandos realmente suportados.
3. Instalar um serviço de integração no local. Não expor a central directamente à Internet.
4. Mapear central + circuito + endereço/canal para casa, piso e local, sem duplicados.
5. Implementar base de dados central, contas individuais, perfis de operador/supervisor/técnico e auditoria das acções. A identidade do utilizador no navegador demonstrativo não constitui autenticação.
6. Receber e tratar eventos de alarme, reconhecimento, retorno, avaria, isolamento e perda/restabelecimento de comunicação. Manter a hora da central e a de recepção, além do estado de sincronização.
7. Validar primeiro a leitura em paralelo com a central. O estado deve ser desconhecido enquanto não houver sincronização completa.
8. Activar comandos apenas após ensaio e autorização: seleccionar ponto exacto, pedir motivo, validar permissões, enviar e esperar confirmação da central. Um envio não confirmado deve ficar pendente/indeterminado, não executado. Evitar repetição cega.
9. Para isolamento, aplicar prazo, avisos de expiração, medidas compensatórias e confirmação da reintegração. O fim do prazo gera aviso; não pressupõe reintegração automática.
10. Ensaiar falta de rede, energia, dados duplicados e retorno da comunicação. A falha do software não pode impedir a função autónoma da central.
11. Fazer testes de aceitação com todos os pontos e comandos autorizados antes de utilizar o software como meio operacional.

Uma via a avaliar é Siemens Cerberus DMS, que suporta supervisão integrada de incêndio e segurança. Isso não confirma a compatibilidade da instalação fotografada nem dispensa drivers, licenças ou interfaces específicos. Um software personalizado também depende dessas condições.

## 10. Fontes e vídeos

- [Documentação técnica Cerberus PRO — índice de manuais Siemens](https://sid.siemens.com/api/khub/documents/yCTgN8SxgRcIHKa_687o5A/content): se confirmada a família FS720, procurar A6V10210390 (montagem/instalação), A6V10210416 (comissionamento/manutenção) e A6V10210424 (configuração), na revisão aplicável. Confirmar também o manual de operação da variante.
- [Cerberus DMS — Siemens](https://www.siemens.com/en-gb/products/cerberus/dms/): referência para avaliar a supervisão integrada.
- [Descrição técnica Cerberus DMS](https://sid.siemens.com/r/A6V11852712/16300527371_16300696971__en-US_16308761611): integração de incêndio e intrusão, com interfaces dependentes do sistema.
- [Vídeo Siemens — operação do FC922](https://resources.sw.siemens.com/en-US/video-cerberus-fire-panel/): introdução de cerca de sete minutos, em inglês; é outro modelo. Não aplicar os seus menus directamente à central do Kizomba.
- [Série Siemens — Cerberus PRO Modular UL](https://resources.sw.siemens.com/en-US/video-cerberus-pro-modular/): formação sobre outra variante; útil como contexto, não como instrução específica desta instalação.
- [Formação Siemens Cerberus PRO](https://www.sitrain-learning.siemens.com/BE/nl/rw20410/Cerberus-PRO): formação técnica de comissionamento; disponibilidade, idioma e condições dependem da oferta.

## 11. Informação necessária para a versão específica da instalação

Referência completa da central e interfaces; modelos dos detectores, botões e sirenes; central de intrusão; software já instalado e tipo de ligação; planta dos circuitos; ficheiro de configuração; total de residências; quantidades e funções nas zonas comuns; matriz de sirenes/evacuação aprovada. Não enviar palavras-passe ou códigos de acesso.


## 12. Distribuição das centrais confirmada no desenho recebido

A planta KICO_GE_AB_SEG_720_00 tem uma página e está identificada como AS BUILT, revisão 00, de 31/08/2015. É referência documental histórica, a conferir na instalação actual.

| Central | Localização | Loops | Casas indicadas |
|---|---|---:|---:|
| SADI 1 | Guarita Social 2 | 4 | 26 |
| SADI 2 | Salão de Festas | 8 | 38 |
| SADI 3 | Guarita Social 1 | 3 | 22 |
| SADI 4 | Guarita de Serviço | 7 | 37 |

Total documental: 4 centrais e 22 loops. O cadastro actual contém 123 casas (125 códigos originais; A48/A49 e A62/A63 unificadas). A relação das casas actuais e o estado das associações encontram-se em Centrais-e-Loops-Kizomba.md.

As casas usam A01-A71, B01-B12, C01-C18, D01-D14 e E01-E10. A associação residencial de cada código actual à SADI e ao loop está por confirmar; não se mantêm as descrições do mapa anterior. As zonas comuns conservam as referências documentais independentes da numeração das casas.

Exemplo: Casa A01 → SADI 1 → Loop 4 → detector da sala, cujo endereço individual ainda deve ser levantado. Não confundir esses níveis. Alguns loops misturam sectores; não atribuir uma central automaticamente pela letra da casa.

O diagrama não estabelece uma rede entre as quatro centrais nem identifica a interface para o software. A integração em tempo real deverá receber eventos de todas elas, com supervisão de comunicação individual. Perder comunicação com uma central não pode apresentar as suas casas como normais.

Este desenho é de incêndio; não identifica quais são as 60 casas com intrusão nem demonstra a integração dos pontos de pânico ou inundação. As designações PT1–PT4 e as áreas técnicas devem ser confirmadas em campo, preservando as designações do projecto.


## Planta dos percursos — KICO_GE_AB_SEG_113_00

Recebida a planta de implantação do sistema automático de detecção de incêndios, infraestrutura geral, AS BUILT, revisão 00, de 31/08/2015, escala indicada 1:750.

O desenho apresenta os percursos dos circuitos pelo condomínio, passagens junto das residências e zonas comuns, identificação do loop e referências à SADI de destino. Indica SADI 1 com 4 loops, SADI 2 com 8, SADI 3 com 3 e SADI 4 com 7, em concordância com os totais do diagrama SEG_720.

Na legenda constam central de incêndio (SADI), central de intrusão/controlo de acessos (CI), bastidor da rede de segurança e módulo de amplificação do loop (AL). A presença de símbolos na legenda não determina, por si só, a quantidade instalada ou a interligação funcional actual. Não confundir módulo de amplificação com isolador de curto-circuito.

A legenda identifica cabo em vala das instalações de comunicações, circuito de detecção em cabo resistente ao fogo FE180 2x1,5 e indicação de fecho do loop com a SADI de destino. Estas são especificações documentais do desenho; não comprovam a cablagem actual nem substituem os cálculos e manuais necessários para qualquer alteração.

Para a supervisão, usar sempre a chave central + loop + endereço/canal. Por exemplo, SADI 1 / Loop 1 e SADI 2 / Loop 1 são circuitos diferentes. Um alarme individual exige ainda o endereço do ponto; uma falha de linha pode afectar vários locais do mesmo circuito e não deve ser atribuída a uma única residência sem diagnóstico.

A planta não fornece os bornes, a lista de endereços individuais, a programação causa–efeito ou o protocolo de comunicação para o software. Os percursos de loop também não comprovam uma rede de comunicação entre as quatro centrais. A identificação das 60 casas com intrusão continua por confirmar.

Conferir no terreno saídas e retornos de cada circuito, caixas de passagem, alterações desde 2015, módulos e pontos de acesso. Não abrir ou desligar circuitos activos para confirmar o percurso sem intervenção coordenada do técnico e medidas de protecção durante o trabalho.


## Visualização dos equipamentos por residência — actualização

Clique numa residência na lista ou na planta geral. A secção «Localização dos equipamentos» apresenta dois pisos e os locais das 15 referências documentais do modelo T3.

É um esquema por divisão, sem escala. Até à verificação no terreno, os pontos são baseados exclusivamente na planta SADI T3 e não constituem um cadastro confirmado. Seleccione cada equipamento e use «Conferir / editar localização» para registar a posição física exacta, o modelo e o endereço electrónico. Para marcar «Verificado em campo», a ficha exige posição física e endereço preenchidos; a veracidade deve ser validada pelo técnico mediante ensaio.

Os quartos 1, 2 e 3 devem receber uma correspondência explícita com os quartos reais, incluindo a suíte principal. Não assumir essa correspondência apenas pela numeração. A orientação das versões espelhadas também precisa de confirmação na casa concreta.

Use «Registar ocorrência neste ponto» ou «Simular neste ponto». A casa e a divisão são preenchidas a partir do equipamento seleccionado. O registo conserva uma cópia da identificação, posição e endereço no momento da criação. Não permite escolher um equipamento pertencente a outra residência. Uma ocorrência aberta destaca o respectivo equipamento; «Ver equipamento na residência» abre a vista do ponto.

Eventos sem ponto individual, como uma falha de circuito ainda não diagnosticada, aparecem como ocorrências sem correspondência individual. Não se atribui uma falha geral a um detector sem confirmação. Sensores de intrusão ou outros dispositivos efectivamente levantados podem ser adicionados ao cadastro e aparecem na vista da residência.

Esta versão continua a trabalhar com introdução manual e simulações. A localização automática de eventos da central depende da integração real e do mapeamento verificado central + loop + endereço/canal.


## Administração — actualização com as plantas 105, 204 e 702

A administração foi incorporada como área específica, com localização documental de detectores, sirenes, botões de incêndio/pânico, alarmes técnicos e equipamentos de intrusão/CFTV/rondas. A camada de evacuação é apresentada como referência. Consulte Administracao-Kizomba.md para a transcrição, quantidades e limitações. Na plataforma, seleccione Administração e clique nos marcadores para abrir a ficha de cada equipamento. A associação documental do incêndio é SADI 4 / Loop 6; as interfaces de intrusão e vídeo continuam por identificar.
