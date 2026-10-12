/* Local service API only. No Siemens endpoints or remote command implementation. */
(()=>{
 const panel=document.getElementById('servicePanel');if(!panel)return;
 let token='',snapshot=[],serviceStates=[];
 const el=id=>document.getElementById(id);
 async function api(path,body){
  if(location.hostname!=='127.0.0.1'||location.protocol!=='http:')throw Error('Abra a plataforma pelo serviço local em http://127.0.0.1:8765.');
  const response=await fetch('/api/'+path,{method:body?'POST':'GET',headers:{Authorization:'Bearer '+token,...(body?{'Content-Type':'application/json'}:{})},body:body?JSON.stringify(body):undefined,cache:'no-store'});
  if(!response.ok)throw Error('Pedido recusado pelo serviço ('+response.status+').');return response.json();
 }
 function paint(){
  el('serviceEvents').innerHTML=snapshot.length?snapshot.map(e=>`<article class="event"><span class="badge">SIMULAÇÃO DO SERVIÇO · NÃO É ALARME REAL</span><h3>${esc(e.state)} · ${esc(e.station)}</h3><p>Identificador: ${esc(e.native_id)}</p><p>${e.location?esc(e.location.area+' · '+e.location.place):'Localização não validada — sem destaque de equipamento'}</p><small>${fmt(e.time)}</small><div class="toolbar">${e.location?`<button data-service-locate="${esc(e.id)}">Ver área validada</button>`:''}<button data-service-ack="${esc(e.id)}">Reconhecer apenas no aplicativo</button></div></article>`).join(''):'<p>Nenhum evento no serviço. Isto não confirma estado normal das centrais.</p>';
  // The existing map keeps its manual events. Service simulations get a separate label.
  document.querySelectorAll('[data-house]').forEach(b=>{
   const events=serviceStates.filter(e=>e.state!=='normal'&&e.location&&e.location.area==='Casa '+b.dataset.house);
   if(events.length){b.dataset.serviceSimulation='true';b.title='SIMULAÇÃO DO SERVIÇO · '+events.length+' estado(s) activo(s)';}
   else if(b.dataset.serviceSimulation){delete b.dataset.serviceSimulation;b.removeAttribute('title');}
  });
 }
 async function refresh(){
  const [status,events,states,readings]=await Promise.all([api('status'),api('events'),api('states'),api('readings')]);
  const view=el('serviceReadings');
  if(view)view.innerHTML=readings.items.length?readings.items.map(r=>`<article class="event"><span class="badge">${r.integration_validated?'LEITURA COMPARADA COM O PAINEL':'LEITURA NÃO VALIDADA'}</span><h3>${esc(r.station)} · ${esc(r.native_id)}</h3><p>Estado efectivo: ${esc(r.effective_state)} · Qualidade: ${esc(r.quality)}</p><p>${r.location?esc(r.location.area+' · '+r.location.place):'Não mapeado'}</p><small>${fmt(r.observed_at)} · Evidência ${esc(r.evidence_id)}</small></article>`).join(''):'<p>Nenhuma leitura real obtida. Estado das centrais desconhecido.</p>';
  snapshot=events.items;serviceStates=states.items;
  el('serviceStatus').textContent=status.mode==='read_only_gated'?'Serviço local ligado · leitura condicionada · comandos desactivados. '+(status.real_telemetry?'Um ponto validado; restantes desconhecidos.':'Alarmes reais ainda indisponíveis.'):'Serviço local ligado · apenas simulação · leitura Siemens bloqueada.';
  el('serviceConnectors').textContent=Object.entries(status.connectors).map(([name,c])=>name+': '+c.status+' — '+c.reason).join('\n')+'\n'+(status.bacnet_blockers||[]).join('\n');paint();
 }
 el('serviceConnect').onclick=async()=>{token=el('serviceToken').value;el('serviceToken').value='';try{await refresh();}catch(e){el('serviceStatus').textContent=e.message;}};
 el('serviceRefresh').onclick=async()=>{try{await refresh();}catch(e){el('serviceStatus').textContent=e.message;}};
 el('serviceMapping').onchange=async e=>{const f=e.target.files[0];if(!f)return;try{if(f.size>2000000)throw Error('Ficheiro demasiado grande.');const body=JSON.parse(await f.text());await api('import-mapping',body);await refresh();toast('Mapa importado no serviço; apenas pontos validados poderão ser localizados.');}catch(err){el('serviceStatus').textContent=err.message;}finally{e.target.value='';}};
 el('serviceEvents').onclick=async e=>{
  const locate=e.target.closest('[data-service-locate]');if(locate){const ev=snapshot.find(x=>x.id===locate.dataset.serviceLocate);if(ev?.location){selected=ev.location.area;selectedEquipment=ev.location.code;render();paint();el('residenceDetail').scrollIntoView({behavior:'smooth',block:'start'});}return;}
  const ack=e.target.closest('[data-service-ack]');if(ack){const actor=prompt('Nome do operador — reconhecimento apenas no aplicativo:');if(!actor)return;try{await api('local-ack',{event_id:ack.dataset.serviceAck,actor});await refresh();}catch(err){el('serviceStatus').textContent=err.message;}}
 };
 const observer=new MutationObserver(()=>paintMap());
 function paintMap(){document.querySelectorAll('[data-house]').forEach(b=>{if(serviceStates.some(e=>e.state!=='normal'&&e.location?.area==='Casa '+b.dataset.house)){b.dataset.serviceSimulation='true';b.title='SIMULAÇÃO DO SERVIÇO · não é telemetria real';}});}
 observer.observe(el('mapPoints'),{childList:true});observer.observe(el('houses'),{childList:true});
})();
