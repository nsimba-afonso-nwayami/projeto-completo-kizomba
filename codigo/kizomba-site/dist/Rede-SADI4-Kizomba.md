# Rede da SADI 4 — Guarita de Serviço

Levantamento de 08/10/2026, fotografia do painel e localização confirmada pelo utilizador.

- IP Ethernet da central: 192.168.2.63.
- Máscara Ethernet: 255.255.255.0 (/24).
- Gateway: não visível; por confirmar.
- O valor anterior 192.168.200.155 foi observado no elemento Impressora Ethernet; não foi adoptado como IP da central.

## Verificação a partir do computador

Três pedidos ICMP, origem 192.168.160.123. Nenhuma resposta da central. O router 192.168.1.1 devolveu Destination Host Unreachable. Rota por defeito do computador: 192.168.160.1, interface en8.

O resultado indica que o destino não foi alcançado por este caminho; não confirma central desligada, cablagem defeituosa ou protocolo indisponível. Não foram alterados IPs, rotas, configuração ou comandos das centrais.

Próximo passo: conferir ligação física e configuração do switch, eventual VLAN da rede 192.168.2.0/24 e encaminhamento autorizado a partir da rede de trabalho. Para acesso nessa rede, obter do responsável de rede um endereço livre e a configuração correcta do posto, evitando IP duplicado. Confirmar também gateway e interface/protocolo de supervisão na configuração Siemens. O IP isoladamente não garante leitura de alarmes.
