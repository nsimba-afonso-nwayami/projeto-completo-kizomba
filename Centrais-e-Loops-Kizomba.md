> Distribuição documental de 2015, com numeração anterior. A planta geral actual permanece em uso; a correspondência com as casas actuais está por confirmar.

# Kizomba — distribuição das centrais e loops

Leitura da planta KICO_GE_AB_SEG_720_00.pdf, uma página, desenho AS BUILT, revisão 00, de 31/08/2015. Transcrição para conferência em campo; não confirma o estado actual da instalação.

| Central | Local da central | Loops | Residências indicadas |
|---|---|---:|---:|
| SADI 1 | Guarita Social 2 | 4 | 26 |
| SADI 2 | Salão de Festas | 8 | 38 |
| SADI 3 | Guarita Social 1 | 3 | 22 |
| SADI 4 | Guarita de Serviço | 7 | 37 |

Total: 4 centrais, 22 loops e 123 códigos residenciais distintos. Cada residência foi encontrada uma única vez nesta transcrição. As casas não seguem sempre intervalos consecutivos; por exemplo B08 está no loop 3 da SADI 2, enquanto B09 está no loop 1.

## SADI 1 — Guarita Social 2

| Loop | Residências | Outros locais/pontos indicados |
|---|---|---|
| 1 | A19, A20, A21, A22, A23, A24, A25, A26 | — |
| 2 | A13, A14, A15, A16, A17, A18 | Guarita Social 2 |
| 3 | A07, A08, A09, A10, A11, A12 | Banheiro social, PT1 |
| 4 | A01, A02, A03, A04, A05, A06 | Módulo Serviço 2 |

## SADI 2 — Salão de Festas

| Loop | Residências | Outros locais/pontos indicados |
|---|---|---|
| 1 | B01, B02, B03, B04, B05, B06, B07, B09 | — |
| 2 | B11, B13, B15, B17, B19, B20 | — |
| 3 | B08, B10, B12, B14, B16, B18 | — |
| 4 | B21, B22, B23, B24, B25, B26 | PT2 |
| 5 | D01, D02, D03, D04, D05, D06, D07 | — |
| 6 | E03, E02, E01, E24, E25 | — |
| 7 | — | Salão de Festas |
| 8 | — | Academia, Área técnica (SADI 2), Churrascaria |

## SADI 3 — Guarita Social 1

| Loop | Residências | Outros locais/pontos indicados |
|---|---|---|
| 1 | C01, C03, C05, C07, C09, C10, C11, C12 | — |
| 2 | C23, C25, C27, C29, C31, C32 | Guarita Social 1, PT4 |
| 3 | C24, C26, C28, C30, C02, C04, C06, C08 | — |

## SADI 4 — Guarita de Serviço

| Loop | Residências | Outros locais/pontos indicados |
|---|---|---|
| 1 | E15, E16, E17, E18, E19, E20 | — |
| 2 | E04, E05, E07, E09, E11, E13 | — |
| 3 | E06, E08, E10, E12, E14, E21, E22, E23 | — |
| 4 | D08, D09, D10, D11, D12, D13, D14 | PT3 |
| 5 | C13, C14, C15, C16, C17, C18, C19, C20 | — |
| 6 | C21, C22 | Módulo Serviço 1, Edifício administrativo |
| 7 | — | Área técnica (SADI 4), Depósito, Guarita de Serviço |

## Consequência para o software

A hierarquia de supervisão deve ser: condomínio → central → loop → residência/área → ponto → evento. Exemplo: Casa A01 → SADI 1 → Loop 4 → detector da sala (endereço individual ainda por levantar).

A integração deve cobrir as quatro centrais. O diagrama apresenta os loops associados a cada central, mas não estabelece uma rede entre as centrais, um gateway para computador, protocolos de supervisão ou comandos remotos. É preciso verificar as interfaces e a configuração existentes.

Não confundir o código da casa, o número do loop e o endereço individual do dispositivo. A planta não fornece os endereços dos seis detectores de cada residência nem confirma a integração de intrusão/pânico.

As designações PT1–PT4 foram preservadas sem expandir o seu significado. As áreas técnicas da SADI 2 e da SADI 4 não foram equiparadas automaticamente à área técnica da piscina. Identificar esses locais em campo.

As 60 casas com intrusão continuam por identificar. Não deduzir intrusão das cores da planta geral.

O desenho identifica uma especificação de cabo na legenda; isso não basta para dimensionar ou alterar a cablagem. Conferir a revisão do projecto, o estado real, os manuais da variante e o cálculo das linhas antes de intervir.

## Verificações no local

1. Conferir as quatro localizações e referências técnicas das centrais.
2. Exportar a configuração de cada central e comparar os loops com esta tabela.
3. Mapear os endereços individuais e textos de localização, confirmando cada ponto por ensaio.
4. Identificar a rede, interfaces ou gateways existentes e os protocolos/licenças suportados.
5. Confirmar que eventos de incêndio, intrusão, pânico e inundação são distintos.
6. Validar perda de comunicação por central: não declarar normalidade quando uma central estiver sem dados.
7. Validar comandos por central e ponto, com permissões e confirmação de execução.


## Planta dos percursos — KICO_GE_AB_SEG_113_00

Recebida a planta de implantação do sistema automático de detecção de incêndios, infraestrutura geral, AS BUILT, revisão 00, de 31/08/2015, escala indicada 1:750.

O desenho apresenta os percursos dos circuitos pelo condomínio, passagens junto das residências e zonas comuns, identificação do loop e referências à SADI de destino. Indica SADI 1 com 4 loops, SADI 2 com 8, SADI 3 com 3 e SADI 4 com 7, em concordância com os totais do diagrama SEG_720.

Na legenda constam central de incêndio (SADI), central de intrusão/controlo de acessos (CI), bastidor da rede de segurança e módulo de amplificação do loop (AL). A presença de símbolos na legenda não determina, por si só, a quantidade instalada ou a interligação funcional actual. Não confundir módulo de amplificação com isolador de curto-circuito.

A legenda identifica cabo em vala das instalações de comunicações, circuito de detecção em cabo resistente ao fogo FE180 2x1,5 e indicação de fecho do loop com a SADI de destino. Estas são especificações documentais do desenho; não comprovam a cablagem actual nem substituem os cálculos e manuais necessários para qualquer alteração.

Para a supervisão, usar sempre a chave central + loop + endereço/canal. Por exemplo, SADI 1 / Loop 1 e SADI 2 / Loop 1 são circuitos diferentes. Um alarme individual exige ainda o endereço do ponto; uma falha de linha pode afectar vários locais do mesmo circuito e não deve ser atribuída a uma única residência sem diagnóstico.

A planta não fornece os bornes, a lista de endereços individuais, a programação causa–efeito ou o protocolo de comunicação para o software. Os percursos de loop também não comprovam uma rede de comunicação entre as quatro centrais. A identificação das 60 casas com intrusão continua por confirmar.

Conferir no terreno saídas e retornos de cada circuito, caixas de passagem, alterações desde 2015, módulos e pontos de acesso. Não abrir ou desligar circuitos activos para confirmar o percurso sem intervenção coordenada do técnico e medidas de protecção durante o trabalho.
