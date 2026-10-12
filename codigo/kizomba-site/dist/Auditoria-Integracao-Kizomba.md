# Auditoria e selecção da integração — Condomínio Kizomba

09/10/2026, Africa/Luanda. Âmbito: aplicativo existente, evidências guardadas e integração das centrais. Resultado: BACnet/IP é a primeira hipótese técnica de leitura; ainda está bloqueado. Alternativa operacional recomendada: avaliar Cerberus DMS com integrador, recuperando o projecto MM8000 se possível. Não há leitura real de alarmes nem comandos remotos habilitados.

## 1. Classificação e limites da análise

**Confirmada (C)**: código inspeccionado, evidência fotografada ou resposta guardada; confirmação documental não equivale a instalação. **Hipótese (H)**: inferência ou proposta ainda não demonstrada. **Ausente (A)**: não encontrado no material acessível. **A validar em campo (V)**: requer configuração, observação ou ensaio coordenado. Todos os dados de produto abaixo são C-documental; a sua aplicação instalada é V salvo indicação explícita. Metas e arquitectura são propostas H, não requisitos normativos.

[C] Repositório acessível. Não foram encontrados AGENTS.md no projecto/subpastas ou nos directórios ascendentes pesquisados. Não há package.json, framework de backend ou base central anterior. A árvore está sem commits de implementação acompanhados nesta auditoria; funcionalidades existentes foram verificadas pelo teste local, não por histórico Git de versões.

[C] /Users/macbookpro2017/Downloads/1111.pdf tem 340 páginas; é catálogo Cerberus PRO com rodapés ©2018, não configuração instalada. Foram extraídas e renderizadas as páginas PDF 78, 79, 89, 103, 308, 310 e 314, contando a capa como 1. As referências mal extraídas foram conferidas visualmente. Não se afirma ter validado cada produto das outras páginas. [C] O PDF Prompts_Integracao_Siemens_Kizomba.pdf tem cinco páginas e foi lido como especificação de referência; não autoriza automaticamente os outros prompts que contém.

[A] Não há exportação SiB-X, PICS aplicável ao firmware 50.21.46, backup Composer/MM8000, mapa de registos NK8237, contrato REST instalado, configuração sanitizada de clientes, matriz causa–efeito, inventário completo dos dispositivos reais ou captura passiva PCAP no material encontrado. O localStorage do navegador não foi lido por esta auditoria. Não se reproduziram segredos do painel.

## 2. Aplicativo antes e depois

| Camada | Conclusão e classificação | Ficheiro / função |
|---|---|---|
| Frontend existente | C: HTML/CSS/JavaScript sem framework, entregue como ficheiro local | work/kizomba-site/dist/index.html; app.js: render |
| Dados geográficos | C: 123 casas actuais; A48/A49 e A62/A63 unificadas; coordenadas documentais | layout-data.js: layoutPoints, houseAliases; app.js: normalArea, mergeUnifiedHouses |
| Inventário | C: referências de plantas e modelo T3, cadastro manual; não lista obtida da central | app.js: template, residencePoints, pointStatus; admin/gym/guard/security-data.js |
| Eventos existentes | C: apenas source manual ou simulation | app.js: valid, eventForm.onsubmit, eventDialog |
| Persistência anterior | C: localStorage kizomba-demo-v1; exportação/importação JSON | app.js: save, importFile.onchange, migrateImportedNumbering |
| Autenticação anterior | A: sem contas ou autenticação no aplicativo | app.js/index.html; nome do operador é texto, não identidade autenticada |
| Acções anteriores | C: reconhecimento e encerramento de ficha; pedido de isolamento não executado | app.js: events.onclick, actionForm.onsubmit |
| Transporte anterior | A: sem receptor de alarmes, WebSocket, polling Siemens ou API de produção | app.js; read_bacnet.py é diagnóstico pontual, não conector |
| Segundo plano anterior | C: watch.py executa ping limitado e caffeinate por duas horas; não lê alarmes. A: sem gestão durável de jobs | work/network-monitor/watch.py |
| Notificações anteriores | A: sem envio automático de alarmes | app.js: toast é aviso no ecrã; e-mails enviados pelo chat são relatórios distintos |
| Serviço adicionado | C: Python padrão + SQLite, sem novas bibliotecas; API própria autenticada em loopback | work/integration/service.py: Store, Handler, create_server |
| Integração adicionado | C: importação normalizada, histórico/estado separados, auditoria e outbox; só simulação | Store.import_mapping, ingest_simulation, acknowledge, audit |
| Interface adicionada | C: consulta explícita ao serviço, token em memória, eventos separados e destaque de simulação | integration-client.js: api, refresh, paint, paintMap |
| Conectores e comandos | C: todos bloqueados; A: implementação de transporte de produção | service.py: CONNECTORS; Handler.do_POST /api/commands |
| Alojamento | C: ficheiros locais; serviço opcional 127.0.0.1:8765, não instalado como daemon | service.py: main; README.md |

[C] Foi corrigida a atribuição presumida de pânico, assistência e alarmes técnicos aos loops SADI em pointRoute. Conservam-se as referências de incêndio das zonas comuns, explicitamente documentais; nenhum loop residencial actual foi deduzido dos códigos de 2015. Os testes anteriores que afirmavam a rota presumida de pânico foram ajustados para exigir interface por identificar. As fichas, plantas, numeração, exportações e registos antigos mantêm-se.

### Percurso completo

| Etapa | Situação real | Situação testável entregue |
|---|---|---|
| Origem | C: respostas BACnet de identificação/erro; A: eventos reais | Store.ingest_simulation aceita exclusivamente source=simulation |
| Transporte | C: UDP 47808 respondeu no teste anterior; leituras recusadas | API HTTP própria, local, Bearer token; sem comunicação Siemens no serviço |
| Interpretação | A: sem contrato de estados/qualidade da versão instalada | sete estados normalizados de simulação; sem interpretação de bytes Siemens inventada |
| Persistência | A: sem ingestão real | SQLite transaccional: events, current_states, mappings, audit, outbox |
| Localização/mapa | A: zero pontos nativos identificados | só mapa declarado field_validated com evidência; candidatos e desconhecidos não localizam; destaque de simulação separado |
| Notificação | A: envio operacional de alarmes | outbox durável bloqueada por fornecedor ausente; não há worker ou entrega |
| Auditoria | A: histórico de operações reais | importação, ingestão, reconhecimento local e tentativa bloqueada registados com cadeia de hashes |

## 3. Inventário de instalação

| Tipo / identificação | Local e endereço | Marca/modelo/firmware | Estação/interface | Evidência e lacunas |
|---|---|---|---|---|
| Central SADI 1 | Guarita Social 2 / Portaria de Serviço; 192.168.2.62 | C-utilizador: Siemens FC726; V: variante/firmware | Incêndio; 4 loops no desenho de 2015; interfaces efectivas V | Confirmações do utilizador e station-data.js; C: ping anterior 3/3; V: máscara, clientes, licença, visibilidade |
| Central SADI 2 | Salão de festas; 192.168.2.60/24; MAC 00:05:19:04:22:26 | C-foto: FC726-ZA, software 50.21.46 | C-foto: nome interno Central 1, hostid 1; C-rede: BACnet Device 3; 8 loops documentais | Fotos 08/10 17:01; registos BACnet; Device 3 não é SADI 3; V: cliente e direitos |
| Central SADI 3 | Guarita Social 1 / Portaria Sul; 192.168.2.61 | C-utilizador: Siemens FC726; V: variante/firmware | Incêndio; 3 loops no desenho | C: ping anterior 3/3; V: máscara, configuração, licença, visibilidade |
| Central SADI 4 | Guarita de Serviço na planta; nome actual V; 192.168.2.63/24 | C-foto: FC726; V: firmware/variante completa | Incêndio; 7 loops documentais | C: sem resposta no teste anterior; não prova desligada; nome «Serviço» conflita com uso actual na .62 |
| Unidade de operação integrada SADI 2 | Dentro da FC726, não central extra | C-foto: FCM7204-Z3; boot product A5Q000052185-3; etiqueta A5Q00037625 02 | X5 Ethernet; FCM2027 A5Q00031466-04; FCI2004 mostrado no painel | Fotografias, sem prova de terminal autónomo |
| Unidade integrada fotografada na Guarita de Serviço | Dentro da central | C: FCM7204-Z3 / FCM2027; fonte SV24V-150W V24230-Z6-A5 | Interfaces e bornes visíveis, configuração V | Levantamento-Centrais-2026-10-08.md; bornes não revelam destinos ou protocolos |
| Terminal de incêndio autónomo FT724 ou outro | A: não inventariado | A | A | FT724 no catálogo não prova unidade instalada |
| Terminais de intrusão/acessos, botões e postos | V: plantas indicam painéis/teclados e pânico; referências reais A | A | Disciplina/protocolo/servidor V | guard-data.js e desenhos 205/106; não são automaticamente dispositivos BACnet FC726 |
| Servidor MM8000 | C-utilizador: computador avariado/perdido | A: versão, licença, opções e backup | Interface antiga A | A recuperar do disco/projecto com técnico; nenhum REST/OPC instalado confirmado |
| NK8237.2 / Cerberus DMS / Desigo CC | A: não encontrados no inventário fornecido | A | A | Apenas opções documentadas, não equipamentos instalados |

[C-foto SADI 2] Configuração datada 21/04/2020 10:55:30; BDV F-FXS2004-PT_pt_2-50.21.18_03.BDV; I-Button S02. [V] S02 não foi equiparado a S2 nem determina direitos. Datas fotografadas não demonstram sincronização horária actual. [V] Número de detectores e endereços reais, disciplina por ponto, canais e visibilidade não obtidos. As oito avarias fotografadas são um retrato histórico, não eventos actuais recebidos; «A15» não se converte automaticamente numa casa actual.

[C] Mapa de candidatos entregue: Mapa-Pontos-Candidatos-Kizomba.json, 1937 referências (1845 de repetição documental T3 nas 123 casas, 26 administração, 25 ginásio, 32 guaritas e 9 rondas). Não são 1937 dispositivos instalados. native_id, station e loop ficam nulos; o ficheiro é explicitamente não importável como mapa operacional. Casas unificadas podem ter composição diferente do T3. O mapa de serviço exige identificadores reais, versão, fonte e validação. [V] Intrusão tem documentação própria; pânico pode chegar por módulos de entrada, mas isso é hipótese. Cor azul não determina função/protocolo. Avaria de loop não identifica automaticamente a residência e a integração não a repara.

## 4. Diagnóstico por camada

| Camada | Classificação / resultado | Próxima prova |
|---|---|---|
| Cabo/NIC | C: en8 activo 192.168.2.207/24 na última verificação; histórico de quedas e perda de Internet | V: confirmar simultaneamente Internet Wi-Fi e NIC Ethernet numa janela de ensaio |
| IP/rotas | C: .60 respondeu ping; .61/.62 responderam anteriormente; .63 sem resposta | V: confirmar tabela de rotas (consulta recente impedida por permissões), gateways, VLANs e firewall; mesmo switch não prova mesma VLAN |
| Porta | C: .60 UDP 47808 respondeu; TCP80/443 recusados antes | V: porta configurada exacta e regras; sem inferir ausência de supervisão pela falta de HTTP |
| Identificação | C: I-Am Device 3, vendor 7; MAC fotografado | V: correspondência com projecto e clientes autorizados; não copiar ID de cliente activo |
| Leitura | C: dez ReadProperty recusados com Services 5 / Service Request Denied 29 | V: licença, cliente BACnet, restrições de endereço, GAP e visibilidade; erro não isola causa |
| Eventos | A: destinos/NotificationClass, COV e semântica de alarmes da versão instalada | Obter configuração sanitizada e amostra de eventos autorizada |
| Tempo | A: sincronização/NTP verificada | Comparar relógios e medir desvio sem escrever data/hora |
| Aplicativo | C: simulação funcional testada; real bloqueado | Validar contrato e piloto rastreável antes de habilitar adaptador |

[C] Nesta auditoria não foram efectuadas novas sondagens à central, captura passiva ou varrimentos. Usaram-se respostas previamente guardadas e testes de software local. [H] Próxima janela: leitura limitada exclusivamente de .60, taxa máxima proposta 1 pedido/segundo e sem retentativas após recusa consistente; técnico aprova janela e serviços. Passivo primeiro: exportações e logs, depois captura autorizada apenas do tráfego necessário, com remoção de segredos. Nunca escrever propriedades, fazer força bruta/fuzzing, anunciar identidades de terceiros, testar comandos ou alterar programação nesta fase.

## 5. Comparação e escolha

As ofertas, continuidade de suporte regional e preços precisam de cotação Siemens/integrador. Não há preços, datas de fim de suporte ou compatibilidade universal confirmados. Esforço abaixo é estimativa relativa H, dependente de exportações, licenças e ensaios.

| Caminho | Requisitos e cobertura documental | Limitações/dependências | Prova mínima / decisão | Suporte, custo e esforço |
|---|---|---|---|---|
| BACnet/IP directo FC726 | Catálogo S1/S2/S3; cliente próprio autorizado, PICS/contrato exacto, mapa de pontos, destinatários de eventos | Particularidades Life Safety, direitos e qualidade; licença por estação conforme opção; não resolve pânico/intrusão de outra central | Identificação já C; aceitar só após leitura autorizada, ponto piloto e evento/normalização correspondentes ao painel. Estado actual bloqueado | Compatibilidade 50.21.46 V; licença/engenharia mediante cotação; esforço alto para adaptador completo |
| NK8237.2 / Modbus | Catálogo e A6V10316240: gateway FS720 incluindo FC726; estados e operações seleccionadas, mapa configurado | Hardware/alimentação, ferramenta e mapa real; polling de estados pode perder transições; não assumir buffer de eventos | Inventariar gateway, obter mapa/versionamento e verificar bit/registo em piloto. Não comprar antes desta prova | Documento localizado é de 2012, com referência de licença antiga L2; aplicação actual V; hardware/engenharia mediante cotação; esforço médio-alto |
| MM8000 REST | Catálogo descreve opção; recuperar disco, licença, versão, projecto, API e direitos | Servidor avariado; REST não confirmado; sem endpoints/autenticação inventados | Aceitar após restauro isolado suportado, contrato API e leitura de ponto; hoje não executável | Suporte regional V; recuperação/host/licença/cotação; esforço variável, possivelmente menor se backup íntegro |
| MM8000/MK8000 OPC DA | MK8000 é opção MM8000 ou servidor autónomo segundo ficha; exportação de tags e permissões | OPC DA não é OPC UA; ponte Windows/COM/DCOM e configuração própria; tags/qualidade/comandos V | Browse/export e actualização autorizada de tag, versão suportada e piloto | Documentação legacy, manutenção actual V; cotação; esforço alto se for necessária ponte |
| Cerberus DMS | Catálogo: gestão multidisciplina e interfaces abertas; produto actual publicado pela Siemens | Precisa versão, driver FS720, licença, projecto e contrato de interface norte para este aplicativo | Proposta do integrador + piloto de eventos; demonstrar API de saída, não apenas API para integrar subsistemas | Página actual localizada, suporte da variante/região V; cotação servidor/licenças/engenharia; esforço médio-alto |
| Desigo CC | Ajuda oficial descreve Web Service Interface com HTTPS, token e sessão | Documento da versão da plataforma não é API da central; driver/FS720/compatibilidade V | Servidor real, driver adequado, contrato/versionamento e leitura/evento piloto | Cotação e suporte da versão/região; esforço médio-alto; justifica-se se já houver plataforma ou projecto de gestão mais amplo |
| Cerberus-Remote / Cerberus Mobile | Alternativa de operação oficial; catálogo descreve funcionalidades por licença/acesso | Não é API do nosso aplicativo. Mobile depende de pacote, licença e ligação segura; compatibilidade 50.21.46 e disponibilidade actual V | Integrador demonstrar acesso e direitos numa estação piloto | Ferramenta/licença/rede por cotação; esforço operacional menor, integração própria continua separada |
| Relés / entradas supervisionadas | Alternativa H limitada se saídas reais e módulo receptor forem documentados e aprovados | Apenas sinais configurados; não inventaria divisões/dispositivos nem histórico completo; sem comandos por esta via no projecto | Identificar contacto, causa–efeito, supervisão e testar recepção de alarme/avaria em janela | Engenharia/hardware por cotação; esforço médio; excluir para localização individual completa |

[H] Escolha: preparar serviço independente do transporte e validar BACnet directo primeiro, porque já existe resposta na instalação. Não comprar gateway para contornar uma recusa de autorização. [H] Alternativa: avaliar migração/recuperação para Cerberus DMS e sua interface norte oficialmente contratada; recuperar backup MM8000 em paralelo. NK8237 entra se o integrador garantir versão/mapa/cobertura e houver vantagem real de manutenção. Decisão final fica pendente da prova piloto, não da existência do produto no catálogo.

## 6. Matriz de capacidades

D = documentado em produto, não demonstrado na instalação; B = bloqueado por contrato/versão/configuração ausente; T = testado apenas no software local/simulação; NS = não suportado por esta opção proposta. «Documentado» não habilita um comando.

Colunas BACnet: FC726 50.21.46 (PICS exacto ausente); NK: NK8237.2 conforme ficha MP4.50 de 2012 (versão instalada ausente); MM: MM8000/MK8000 versão/opções ausentes; DMS/CC: versões/interfaces norte ausentes. Assim, B nas colunas reais é uma lacuna, não declaração de incompatibilidade.

| Função | BACnet directo | NK Modbus | MM REST/OPC | DMS/CC norte | Relés limitados | Serviço local entregue |
|---|---|---|---|---|---|---|
| Alarme | B | D/B | D geral/B | D geral/B | D contacto/V | T simulação |
| Pré-alarme | B | B mapa exacto | B | B | NS sem sinal próprio | T simulação |
| Avaria | B | D/B | D geral/B | D geral/B | D contacto/V | T simulação |
| Isolamento (estado) | B | D Include/Exclude/B | B | B | NS sem sinal próprio | T simulação |
| Manutenção/teste (estado) | B | B | B | B | NS | T estado test, sem distinguir manutenção real |
| Perda de comunicação | B supervisão real | D diagnóstico/B | B | B | B supervisão eléctrica | T evento sintético; detector automático A |
| Normalização | B | B mapa/transições | B | B | V desactivação do contacto | T; não encerra manualmente o estado da central |
| Casa/divisão/dispositivo | B mapa ausente | D objectos/B mapa | B tags/projecto | B projecto | NS identificação individual completa | T somente mapa explícito validado; candidato bloqueado |
| Histórico | B recuperação real | B sequência/buffer | D geral/B | D geral/B | NS no contacto | T persistência/reabertura SQLite |
| Notificações | B destinatários | B fornecedor/histórico | D geral/B | D geral/B | B receptor/fornecedor | B entrega; T outbox não enviada |
| Reconhecimento local da ficha | NS na interface da central | NS | NS | NS | NS | T; panel_command_sent=false |
| Reconhecimento no painel | B | D/B | B operações exactas | B | NS | B |
| Reposição | B | D/B | B | B | NS | B |
| Silenciar besouro do painel | B | B operação exacta | B | B | NS | B |
| Silenciar sirenes | B | B operação exacta | B | B | NS | B |
| Activar | B | D On/Off/B por objecto | B | B | NS | B |
| Desactivar | B | D On/Off/B por objecto | B | B | NS | B |
| Isolar (comando) | B | D Include/Exclude/B | B | B | NS | B; pedido antigo apenas registo |

[C-documental] S1/S2/S3 são níveis gerais, não uma lista exacta de operações. Reconhecimento local ≠ reconhecimento no painel; reposição ≠ reparação; besouro ≠ sirenes; isolamento ≠ encerramento de ficha. Sem ensaio real nenhum comando tem estado implementado/testado. A matriz é conservadora: não marca «não suportado» para uma operação Siemens cuja documentação exacta falta.

## 7. Arquitectura, alterações e segurança prática

[H] Arquitectura de destino: interface Siemens autorizada → adaptador específico de versão → normalizador (estado, transição, qualidade, origem, relógio) → SQLite e outbox numa transacção → API autenticada → mapa validado → notificações com confirmação → auditoria. Cada evento terá origem e versão, ID único e tempos de origem/recepção. Falha de transporte deverá levar a qualidade desconhecida, nunca a «normal» presumido.

[C] Implementado autonomamente: service.py, test_service.py, integration-client.js, test_client.cjs, mapping-template.json e README.md. O serviço aceita exclusivamente simulação; dados de centrais reais são recusados. Rotas /api/* são nossas, não endpoints Siemens. API loopback, token em memória, Host/Origin validados, payload limitado, transacções, deduplicação, recusa de conflitos de mapa, estado mais recente e auditoria. As referências documentais não têm endereços fabricados. Conectores bloqueados têm motivo explícito. Não há parser SiB-X genérico, worker de notificações, contas individuais/RBAC, TLS, watchdog ou adaptador real instalado.

[V] Antes de operação multiutilizador: autenticação individual, papéis, transportes protegidos, política de backup/restauro/retensão, recuperação de filas, robustez contra interrupções e controlo de relógios. Cadeia de hashes local não oferece inviolabilidade contra administrador do disco. Aprovação do mapa declarada no importador não substitui ensaio técnico e assinatura de evidência. Não se configura arranque automático nem suspensão durante esta entrega.

[C] Testes executados: nove testes Python de importação atómica, conflitos, fonte real recusada, deduplicação, persistência/reabertura, reconhecimento local, ordem temporal/fusos, sete estados, outbox, cadeia de auditoria e HTTP (token/Origin, comando bloqueado, árvore estática). Teste do cliente JavaScript: token não persistido, origem local, rotas, etiqueta de simulação, localização e file:// bloqueado. Regressão check-platform.cjs: casas unificadas, histórico/importações, fichas, localização, camadas, inventário e distinção pânico/incêndio. Sintaxe JS verificada. Não houve ensaio de alarmes físicos, comandos, notificações entregues ou certificação. A inspecção automatizada de DOM não é ensaio visual completo num navegador real.

## 8. Metas propostas para aprovação e aceitação

| Medida proposta H | Meta inicial | Prova de aceitação V |
|---|---|---|
| Latência | P95 ≤ 3 s e máximo 10 s da recepção do evento pelo adaptador até visualização; medir painel→adaptador separadamente | 100 eventos coordenados, relógios com desvio medido ≤1 s, registar percentis; ainda não medido |
| Perda de ligação | Marcar desconhecido em ≤30 s da última confirmação válida, se interface permitir heartbeat 10 s | Desligamento controlado em manutenção e comparação de tempos; não usar silêncio de eventos como heartbeat |
| Reconexão | Reconciliar estados em ≤60 s após transporte restabelecido; backoff proposto 1–30 s, sem reenvio de comandos | Interrupção/reconexão com teste de lacunas, duplicados e estado final; interface e taxa aprovadas |
| Retenção | Proposta 365 dias de eventos/auditoria; backup diário, cópia fora do host; RPO ≤24 h e RTO ≤4 h | Aprovação do responsável, dimensionamento e restauro ensaiado; nenhuma limpeza instalada |
| Notificações | Enfileirar ≤2 s; obter aceitação do fornecedor em ≤10 s quando disponível; distinguir aceite, entregue e falhou | Fornecedor configurado e simulação de erro/repetição; nenhum envio operacional implementado |
| Localização | 100% dos pontos do âmbito piloto rastreáveis; 0 inferências por código antigo ou por falha de loop | Matriz assinada central/estação/objeto/loop/endereço/local, evento e normalização comparados ao painel |
| Comandos | 0 comandos habilitados até contrato, autorização por operação e ensaio; confirmação por estado da central, timeout sem repetição cega | Técnico coordena testes de cada operação e regista efeitos/limites/perfis; não realizado |

## 9. Pendências indispensáveis e sequência de campo

1. Recuperar projecto/backup MM8000 ou exportação SiB-X e versão do Engineering Tool. Preservar disco original; pedir configuração sanitizada de BACnet, sem PINs/passwords.
2. Obter PICS/documentação de integração que corresponda a 50.21.46, licença por estação, clientes e identificadores autorizados, IP/UDP, visibilidade/GAP, destinatários e supervisão. Não copiar ID de cliente em utilização.
3. Confirmar nomes das quatro centrais, especialmente .63; verificar firmware/interfaces/licenças de cada uma e inventariar terminais/subsistemas separados.
4. Rever os 22 loops documentais e a numeração actual em campo. Levantar identificadores reais, casas unificadas, divisões e disciplinas. Nenhum dos candidatos entra automaticamente como ponto real.
5. Aprovar janela de leitura, receber um ponto piloto, conferir cada estado e normalização. Validar a configuração central exclusivamente com responsável técnico.
6. Só então implementar o adaptador da interface escolhida, medir metas, configurar notificações e testar recuperação. Comandos continuam bloqueados até validação individual; ausência de regressões não substitui essa prova.

## 10. Fontes e correspondência de versão

- [Catálogo oficial Cerberus PRO](https://sid.siemens.com/api/khub/documents/IFS6rQE0Z_N43rKnuiSpCg/content): corresponde às referências 1111.pdf; páginas 78/79 licenças; 89 gateway; 103 Mobile; 308 DMS; 310 MM8000; 314 topologias. C-documental, instalação V.
- [Siemens A6V10316240_a, NK8237, MP4.50, 06/2012](https://sid.siemens.com/api/khub/documents/1Qt5A3GHKKui9NlXoBf2sw/content): inclui FC726, objectos/estados Modbus e algumas operações; mapa/licença/versão instalada V. A referência antiga L2 não foi substituída automaticamente por S1/S2.
- [PICS Siemens A6V10370670_k, 02/02/2022](https://bacnetinternational.net/catalog/manu/siemens/PICS_A6V10370670_k_en_--.pdf), publicado no catálogo BACnet International: válido desde MP8/IP8, firmware 80.6.48; não é contrato verificado para 50.21.46. O histórico menciona MP5, mas não prova aplicabilidade dessa edição à instalação.
- [Siemens BACnet driver, porta e identidade](https://mybuilding.siemens.com/d025938170736/help/engineeringhelp/en-US/24015022347.html): referência de configuração de gestão, não autorização na FC726.
- [Siemens Web Service Interface](https://mybuilding.siemens.com/d036861342594/help/engineeringhelp/en-US/23637026955.html): interface da plataforma de gestão documentada nessa ajuda, não REST nativo da central e não MM8000 por equivalência.
- [Siemens MK8000 datasheet](https://sid.siemens.com/api/khub/documents/0i~MLNjH2fFqdmNZdYuQjw/content): OPC DA 2.0x, tag browsing/export; plataforma/versionamento real ausentes.
- [Siemens Cerberus DMS, página de produto](https://www.siemens.com/de-de/products/cerberus/dms/): produto e migração publicados; acesso à página completa nesta pesquisa limitado, suporte/cotação regional V.
- [Siemens aplicações móveis](https://www.siemens.com/it-it/content/buildings-support-mobile-apps/): requisitos publicados; disponibilidade e compatibilidade dos pacotes antigos V.
- [Códigos BACnet, documentação PTC/Kepware](https://support.ptc.com/help/kepware/drivers/en/kepware/drivers/BACNET/error-classes-and-codes.html): classe5/código29; não identifica a causa específica Siemens.
- Evidências locais: BACnet-SADI2-2026-10-09.json, BACnet-Propriedades-SADI2-2026-10-09.json, Enderecos-Centrais-Kizomba.md, Acompanhamento-SADI2-2026-10-09.md, station-data.js e fotografias fornecidas de 08/10/2026. Identificação de ponto e comando validado: nenhum.

Não se declara certificação, suporte universal ou conclusão da integração real. A entrega é a auditoria, a selecção condicional e o serviço local verificável; lacunas de instalação permanecem explicitamente bloqueadas.
