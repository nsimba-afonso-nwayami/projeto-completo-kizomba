# Serviço local de integração Kizomba

Estado: protótipo testável, apenas simulação. Nenhum conector real está habilitado e nenhum comando é enviado a centrais. Python 3.11+ e SQLite da biblioteca padrão; reutiliza os scripts Python existentes e serve o frontend JavaScript existente, sem instalar dependências.

## Executar localmente

No directório do projecto, usando Python 3.11+:

```sh
export KIZOMBA_API_TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
python3 work/integration/service.py
```

Abrir http://127.0.0.1:8765 e a secção «Ligação ao sistema real». Copiar o token da variável local para o campo do serviço; não o enviar por e-mail. O serviço não imprime nem guarda o token; o frontend guarda-o apenas em memória. O token não é o PIN da central. Na versão HTML file://, as fichas existentes continuam a funcionar, mas a API fica indisponível; não habilitar CORS nem acesso anónimo como atalho.

Terminar com Ctrl+C. Não foi instalado serviço de arranque, prevenção de suspensão nem alteração de rede. O serviço liga apenas em 127.0.0.1, valida Host/Origin e exige Bearer token em todas as rotas API. É um protótipo para um operador local; não tem contas individuais, RBAC, TLS ou disponibilidade redundante. Não deve ser exposto na LAN ou Internet nesta fase.

## Contrato da nossa API (não é uma API Siemens)

GET /api/status, /api/events, /api/states, /api/points, /api/audit, /api/notifications. Paginação nesta fase limitada aos últimos 100 itens por consulta (máximo 500 com ?limit=500); não é exportação integral.

POST /api/import-mapping: JSON normalizado schema_version=1, project_version e points. Cada ponto exige station (SADI 1..4), native_id, code, area, place, discipline, evidence, status; loop opcional. Pontos field_validated também exigem validator e validated_at com fuso horário. Um candidato não localiza um evento. A unicidade é (station,native_id); importação é atómica e conflitos exigem migração revista, não são sobrescritos. Uma declaração do operador não substitui o ensaio físico: a responsabilidade pela evidência permanece com quem valida. Usar mapping-template.json como estrutura vazia.

POST /api/simulations: source=simulation, station, native_id, state, source_event_id e time com fuso horário. Estados: alarm, pre_alarm, fault, isolated, test, communication_lost, normal. O esquema aceita só simulação e rejeita source=bacnet ou qualquer outro. Eventos repetidos são deduplicados por origem/estação/id; colisões diferentes são recusadas. Estado actual é separado do histórico e não recua perante eventos antigos. Estados simultâneos e qualidade do sinal real exigirão contrato Siemens; não estão resolvidos pelo exemplo de simulação.

POST /api/local-ack: event_id e actor. Reconhece no aplicativo; não altera o estado originado nem reconhece na central.

POST /api/commands: sempre 409, com panel_command_sent=false e registo de bloqueio. Não existe implementação de controlo. Conectores BACnet, NK8237, MM8000, MK8000, Cerberus DMS e Desigo CC estão descritos como bloqueados em CONNECTORS; não há endpoints Siemens inventados.

A outbox é persistida na mesma transacção do evento, com estado blocked_provider_unconfigured. Nenhuma notificação de alarme é enviada por este serviço. O envio manual de relatórios pelo Gmail no chat é um fluxo distinto. Não há worker de envio ou retentativa de fornecedor instalado.

## Persistência e auditoria

SQLite em work/integration/runtime/kizomba.sqlite3: events, mappings, current_states, outbox e audit. WAL e synchronous=FULL. Cadeia de hashes detecta alterações simples, mas não é inviolável perante alguém com acesso total ao disco. A política de retenção e backup deve ser aprovada; nenhuma limpeza automática foi instalada. Preservar as permissões da pasta e testar backup/restauro antes de operação real.

Os registos antigos localStorage kizomba-demo-v1 permanecem no navegador. Não foram copiados, apagados nem transformados em telemetria real. O serviço não assume acesso aos dados do navegador. A importação SiB-X directa está bloqueada até obter amostra sanitizada, esquema/versão e correspondência revista; este importador aceita apenas o mapa normalizado explícito.

## Verificar

```sh
python3 -m unittest discover -s work/integration -p test_service.py -v
node work/check-platform.cjs
node work/integration/test_client.cjs
```

Os testes criam bases temporárias e não enviam tráfego às centrais. Para a leitura BACnet de diagnóstico já efectuada, ver outputs/BACnet-Propriedades-SADI2-2026-10-09.json; não repetir pedidos recusados sem nova evidência e janela coordenada.


## Continuação READ_ONLY de 09/10/2026

O serviço agora possui worker de leitura condicionado e API /api/readings; comandos permanecem bloqueados. Consulte outputs/Leitura-READ_ONLY-Kizomba.md para configuração exacta, importação passiva, comparação de painel e limites. O token persistente é privado em runtime/api-token. Nenhuma leitura real validada; firmware, licença e supervisão não confirmados. LaunchAgent instalado, activação falhou e arranque automático não validado.
