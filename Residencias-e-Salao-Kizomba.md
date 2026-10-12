# Residências e salão de festas - referências documentais

## Residências: BP-GE_AB_SEG_120_T3_00.pdf
AS BUILT, 05/11/2014, Casa T3-BP. Quatro vistas: piso térreo e superior, versões normal e espelhada. A legenda distingue detector óptico, termovelocimétrico, detector de fumo óptico-acústico, sirene óptico-acústica, flash, sirene de alarme, AT, MC, fonte e botão de pânico.

O desenho apresenta detectores térmicos na sala e cozinha e óptico na lavandaria. No piso superior apresenta detectores combinados nas três suites, módulos AT/MC e fonte 220 V/24 V. Indica pânico nos dois pisos e flash exterior. O relato inicial foi descartado; apenas esta planta fundamenta o modelo residencial. Não atribuir orientação normal/espelhada automaticamente às casas da planta actual.

O circuito interno é representado, com entrada/saída; não fornece endereços de cada detector nem prova da programação actual. A associação casa-central-loop permanece a transcrição das plantas 720 e 113. Não se trata de esquema de bornes para instalação. Compatibilidade, alimentação, cabos, módulos, supervisão e programação devem ser confirmados pelo técnico com o manual da referência instalada.

## Salão de festas
Zona comum de todos os moradores. SADI 2, loop 7, conforme planta geral 720. Seis desenhos únicos de 2015 disponíveis na plataforma:
- 103: SADI, extinção fixa e portátil.
- 202: CFTV.
- 501: rede hidráulica de incêndio.
- 502: sprinklers.
- 700: compartimentação e evacuação.
- 800: extinção na cozinha do primeiro pavimento.
Os pares 502 e 700 com sufixo (1) são duplicados byte a byte e foram incorporados uma vez.

Estas camadas são referências documentais. O inventário individual do salão ainda não foi transcrito e verificado; não há marcadores de equipamentos nem localização automática por ponto nesta zona até ao cadastro. É possível adicionar equipamentos individualmente na secção Equipamentos e registar a respectiva ocorrência. CFTV e protecções hidráulicas não são automaticamente pontos do loop SADI; confirmar interfaces e programação.

O nome da pasta Sistema MM8000 não confirma software instalado ou uma interface disponível. O desenho 800 é de extinção na cozinha, não de uma rede de supervisão MM8000.

## Conferência para integração real
1. Identificar referência completa das quatro centrais, firmware e interfaces disponíveis.
2. Obter exportação da configuração e inventário de endereços com assistência Siemens/integrador.
3. Conferir cada casa, orientação, piso, divisão e posição física contra o endereço lido na central.
4. Conferir a planta contra a instalação actual; guardar data e responsável.
5. Cadastrar separadamente sinais de incêndio, pânico, intrusão e avaria. Os 60 imóveis com intrusão ainda precisam ser identificados.
6. Implementar e validar adaptador autorizado para recepção de eventos; esta versão não recebe eventos reais.
7. Ensaiar correspondência ponto-local sob procedimento coordenado. Isolamento e reposição continuam fora desta demonstração.

As fichas automáticas provenientes do relato antigo são retiradas do cadastro activo e preservadas em supersededPoints no armazenamento/exportação. O histórico de ocorrências e os equipamentos adicionais permanecem; eventos antigos sem ponto no modelo actual não são remapeados automaticamente.
