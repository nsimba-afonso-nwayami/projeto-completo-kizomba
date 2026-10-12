# Continuação READ_ONLY — 09/10/2026

## Resultado real e limite

Diagnóstico executado às 10:43 UTC (11:43 Luanda): Ethernet en8 activa em 192.168.2.207/24, rota directa 192.168.2/24 por en8; rota Internet por Wi-Fi en0, gateway 192.168.1.1. Um ping por endereço autorizado: .60 respondeu em 5,100 ms; .61 em 1,406 ms; .62 em 1,595 ms; .63 sem resposta. Falta de ICMP não prova central desligada. Firewall de aplicações desligado; PF não consultável (`Permission denied`), regras intermédias desconhecidas. Evidência: `Diagnostico-Leitura-2026-10-09.json`.

Não houve nova tentativa ReadProperty, varrimento, PIN, escrita ou comando na central. Diagnóstico de serviço bloqueado por contrato e configuração não confirmados. Evidências anteriores: I-Am de .60 em UDP 47808, Device 3, fornecedor 7; ReadProperty recusado com classe Services 5 / código ServiceRequestDenied 29. Device 3 não significa SADI 3. Não foi obtido valor real de detector/alarme nem comparação com painel. A causa da recusa não está isolada.

## Inventário e origem das referências

Confirmado pelas etiquetas e pelo responsável: Siemens FC726, unidade FCM7204-Z3, placa PMI/mainboard FCM2027, artigo A5Q00031466-04. SADI 2 / salão de festas, endereço 192.168.2.60/24, MAC 00:05:19:04:22:26. Fotografia do interior mostra Ethernet RJ45 X5 ligado; isso não confirma a configuração de supervisão. FCI2004 aparece no levantamento da periferia, não é identificador de API.

`50.21.46` foi transcrito do campo **Software** da fotografia `WhatsApp Image 2026-10-08 at 17.01.26 (1).jpeg` e também aparece no ecrã de arranque. Mantém-se como referência fotografada; firmware aplicável ao contrato, licença e configuração de supervisão permanecem **não confirmados**, conforme instrução do responsável. Nenhum driver foi seleccionado por esse número. A variante FC726-ZA fotografada permanece evidência complementar, sem alargar automaticamente compatibilidade às outras centrais.

Documentação consultada:

- [Documento disponibilizado pela Siemens A6V10327161, p.17](https://cache.industry.siemens.com/dl/files/089/109819089/att_1138185/v2/A6V10327161.pdf): enumera FC726, FCM7204-Z3, FCI2004-A1 e FCM2027. Corrobora a família de hardware, não autoriza integração de rede.
- [Declaração Siemens FC726 A6V10324755](https://sid.siemens.com/v/u/A6V10324755): referência oficial de hardware; não é contrato BACnet da instalação.
- [PICS Siemens FS20/FS720 A6V10370670_k](https://bacnetinternational.net/catalog/manu/siemens/PICS_A6V10370670_k_en_--.pdf): inclui FC726, mas descreve MP8/IP8 e firmware 80.6.48. Aplicabilidade à instalação **não confirmada**. Solicitar ao integrador a edição correspondente à versão instalada e os detalhes de integração, licença, cliente e objectos.

Endereços autorizados: SADI 1/Guarita Social 2/Portaria de Serviço .62; SADI 2/Salão .60; SADI 3/Guarita Social 1/Portaria Sul .61; SADI 4/Guarita de Serviço documental .63 (nome actual a confirmar). Não se transferem firmware, Device ID ou licença entre centrais por igualdade do modelo.

## Bloqueios exactos e código

| Camada | Ficheiro / função | Implementado | Bloqueio restante |
|---|---|---|---|
| Contrato BACnet | `work/integration/bacnet_readonly.py:gates` | Validação prévia de todos os parâmetros; nenhum socket com configuração incompleta | Configuração e documentação de campo ausentes |
| Transporte | `bacnet_readonly.py:Reader.once`, `request`, `decode` | Uma propriedade de um ponto, origem fixa, prazo 3 s, identidade de resposta/invoke/objecto/propriedade, valores boolean/unsigned/enumerated, resposta original privada | Não validado numa leitura operacional; serviços segmentados, arrays, strings, routed NPDU e inscrição I-Am não implementados |
| Execução | `runtime_reading.py:Runtime.loop`, `delay` | Worker, reconexão 10–300 s para falhas de comunicação; erro de protocolo/recusa suspende pedidos, inclusive após reinício | Revisão de protocolo pelo integrador; não repetir recusas |
| Persistência e qualidade | `Runtime.record`, `readings`, `compare` | SQLite WAL/FULL, histórico, estado desconhecido após reinício/falha/expiração; prova de comparação de um ponto | Leitura real e comparação presencial ausentes |
| Localização | `service.py:Store.import_mapping`, `Runtime.readings` | Associação apenas por estação/native_id e evidência field_validated | Identificadores reais e levantamento ponto a ponto ausentes |
| Captura passiva | `capture_import.py:analyze` | Importação offline PCAP Ethernet/IPv4/UDP, enquadramento BACnet, erros simples; não replay | Nenhuma captura operacional fornecida; PCAPNG exige conversão local; TCP, fragmentos, NPDU complexo e semântica completa não implementados |
| API e aplicação | `service.py:Handler`, `integration-client.js:refresh` | API local autenticada, leituras separadas de simulações, qualidade e localização explícitas | Sem feed real validado nem notificações de alarmes reais |
| Comandos | `Handler.do_POST` `/api/commands` | Sempre recusados; nada transmitido | Permanecem desactivados nesta etapa |
| Outros conectores | `service.py:CONNECTORS` | Bloqueios explícitos | NK8237/Modbus, MM8000 REST, MK8000 OPC, DMS e Desigo: equipamentos/contratos/licenças ausentes e drivers não implementados |

O estado `READ_ONLY` é o modo do serviço local, não uma propriedade escrita na central. O adaptador não implementa I-Am de cliente nem subscrição de eventos. Se a documentação exigir inscrição/autenticação diferente da associação ao endereço de origem, permanece bloqueado e será necessário implementar essa identidade documentada. Não copiar Device ID de cliente activo.

## Parâmetros exactos para a primeira leitura

Todos os nomes abaixo existem no template `work/integration/read-config.example.json` e são verificados por `gates`. Não preencher confirmações como verdadeiras sem evidência.

| Parâmetro | Situação / responsável |
|---|---|
| `station`, `target_ip` | SADI 2, 192.168.2.60; existentes, lista autorizada fixa |
| `model`, `operating_unit`, `mainboard`, `mainboard_article` | FC726, FCM7204-Z3, FCM2027, A5Q00031466-04; inventário confirmado |
| `firmware` | Em branco; integrador confirma versão efectiva e documento correspondente. Referência observada guardada separadamente |
| `protocol_active_confirmed`, `target_port` | BACnet/IP e 47808 observados em I-Am anterior; integrador confirma interface operacional e porta configurada |
| `source_ip`, `source_port` | IP local .207 existente; porta UDP fixa exclusiva, livre e autorizada depende do integrador (não assumir 47808) |
| `client_device_id`, `client_authorized`, `client_authorization_evidence`, `client_uniqueness_evidence` | ID próprio e prova de autorização/unicidade ausentes; integrador fornece |
| `identity_method`, `identity_method_documented` | Código suporta somente `configured_source_address` quando oficialmente documentado. Método efectivo por confirmar; outro método exige código adicional |
| `license_confirmed`, `license_evidence` | Não confirmados; integrador valida licença e âmbito da leitura |
| `visibility_confirmed`, `visibility_evidence` | Não confirmados; integrador valida que o cliente vê o ponto seleccionado |
| `integration_document`, `document_section`, `document_applies_to_model_version` | Edição/seção aplicáveis ausentes; integrador fornece e confirma |
| `approval_reference` | Janela de leitura e responsável técnico; ainda ausente |
| `services` | Código restringe a `['ReadProperty']`; suporte desta instalação por confirmar |
| `point.object_type`, `object_instance`, `property_id` | Identificadores verificados ausentes; integrador exporta um ponto conhecido. Driver actual: tipo 0–1023, instância 0–4194302, propriedade 0–255, sem índice de array |
| `point.native_id`, `evidence`, `known_point_confirmed` | ID real e prova da correspondência no painel ausentes |
| `point.value_type`, `state_map`, `value_semantics_reference` | Tipo e interpretação oficiais ausentes; código aceita boolean/unsigned/enumerated, sem inferir que zero significa normal |
| `poll_seconds`, `stale_seconds` | Template 10 e 30 s; limites no código, validar taxa com integrador. Estado desconhecido quando desactualizado |
| `enabled` | False até completar/rever todos os requisitos; modelo identificado não altera este campo |

Após resposta válida: original em `work/integration/runtime/evidence` (0600); registo durável sem validação. `/api/compare-point` recebe `reading_id`, `value`, `panel_time` com fuso, `actor`, `evidence`; exige mesmo valor e comparação até 60 s da leitura. Trata-se de declaração do operador com prova, não acesso automático ao painel. Valida somente aquele contrato/ponto/propriedade, não todos os alarmes da instalação. Dados antigos e pontos sem prova continuam desconhecidos.

## Ferramentas e operação

```sh
python3 work/integration/diagnose.py --output outputs/novo-diagnostico.json
python3 work/integration/capture_import.py captura.pcap --authorized-operational-supervision --reference 'Autorização e ligação operacional identificada' --output outputs/resumo-captura.json
python3 work/integration/service.py --token-file work/integration/runtime/api-token --read-config work/integration/runtime/read-config.json
```

Captura: nenhum tráfego recolhido activamente por estas ferramentas. Não exporta payload, MAC ou Device ID do cliente; IPs externos à lista ficam pseudonimizados. Pseudónimos não são anonimização. O original continua sob controlo local do responsável e não deve ser enviado por e-mail. Não importar captura de uma ligação não autorizada. O resumo não é telemetria.

Serviço iniciado manualmente em `http://127.0.0.1:8765`, worker bloqueado por configuração, comandos desactivados. Token é local privado e não é o PIN da central. Não é incorporado na página nem nos pacotes.

Autostart: `install_autostart.py` criou e instalou `~/Library/LaunchAgents/com.kizomba.readonly.plist` com RunAtLoad/KeepAlive/ThrottleInterval. **Activação launchctl falhou (código 5); não está validado o arranque automático.** `launchctl print` não encontrou o serviço. Não foi usado root nem alterada suspensão/rede. É necessário activar no contexto da sessão macOS e verificar o processo após novo login; a ferramenta local de instalação está entregue. O processo manual não substitui essa validação.

1937 pontos documentais em `Mapa-Pontos-Candidatos-Kizomba.json` preservados; nenhum associado automaticamente nem elevado a leitura confirmada. Importação operacional requer mapa normalizado com IDs verificados, local e evidência.

Validação de software: 13 testes Python (9 existentes + 4 de leitura/captura/qualidade), cliente JavaScript e regressões da plataforma aprovados. As respostas de testes são exclusivamente sintéticas. Nenhum teste substitui validação de campo. Retenção sem apagamento automático; dimensão do histórico e política de retenção por aprovar. Ainda não há feed de eventos/COV, cobertura completa de alarmes ou provedor de notificações reais.

## Pendências de campo

1. Confirmar firmware, edição do contrato Siemens e método de identidade do cliente para estes módulos.
2. Confirmar porta, ID próprio, endereço/porta de origem, unicidade, permissões, visibilidade, licença e janela de leitura.
3. Fornecer um ponto conhecido com IDs BACnet, propriedade, tipo e tabela de valores oficiais; identificar residência/divisão no painel.
4. Obter primeira resposta e prova comparativa temporal no painel; nenhum valor real está actualmente disponível.
5. Fornecer captura passiva autorizada de supervisão funcional ou exportação de configuração sanitizada, se disponível.
6. Confirmar regras PF/firewall de percurso, situação de .63 e nomes actuais; não ampliar descoberta.
7. Validar arranque automático no macOS, reinício, reconexão e dimensão/retensão da base em operação.
8. Expandir serviços/eventos apenas após contrato e testes de campo; comandos continuam desactivados.
