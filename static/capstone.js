'use strict';
const $ = s => document.querySelector(s);
let traces = [], selectedContent = null, fetching = false;
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function openTab(id) {
  document.querySelectorAll('.page').forEach(el => el.hidden = el.id !== id);
  document.querySelectorAll('.nav').forEach(el => el.classList.toggle('active', el.dataset.tab === id));
  $('#page-name').textContent = ({overview:'Overview',studio:'Writing studio',activity:'Request explorer',method:'Method & limits'})[id];
}
document.querySelectorAll('[data-tab],[data-open]').forEach(el => el.addEventListener('click', () => openTab(el.dataset.tab || el.dataset.open)));
function table(rows) {
  if (!rows.length) return '<div class="empty">No matching requests yet.<br>Analyze a sample in the writing studio to create a trace.</div>';
  return '<div class="table-wrap"><table><thead><tr><th>REQUEST</th><th>ROUTE</th><th>STATUS</th><th>WALL TIME</th><th>TIME</th></tr></thead><tbody>' + rows.map(r => `<tr><td><button class="request-link" data-request="${esc(r.request_id)}">${esc(r.request_id.slice(0,8))} ↗</button></td><td class="route">${esc(r.method)} ${esc(r.route)}</td><td><span class="status ${r.status>=400?'error':''}">${esc(r.status)} ${r.status>=400?'Rejected':'OK'}</span></td><td>${Number(r.wall_ms).toFixed(1)} ms</td><td>${esc(new Date(r.timestamp).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit',second:'2-digit'}))}</td></tr>`).join('') + '</tbody></table></div>';
}
function renderActivity() {
  const search = $('#search').value.toLowerCase(), filter = $('#status-filter').value;
  const rows = traces.slice().reverse().filter(r => `${r.route} ${r.request_id} ${r.input.creator_id||''}`.toLowerCase().includes(search) && (filter==='all'||(filter==='error'?r.status>=400:r.status<400)));
  $('#all-requests').innerHTML = table(rows);
}
async function refresh() {
  if (fetching) return;
  fetching = true;
  try {
    const response = await fetch('/ops/traces', {cache:'no-store'});
    if (!response.ok) throw new Error('Could not load request traces.');
    traces = (await response.json()).entries;
    $('#total').textContent = traces.length;
    $('#success').textContent = traces.length ? `${(100*traces.filter(r=>r.status<400).length/traces.length).toFixed(0)}%` : '—';
    const sorted = traces.map(r=>r.wall_ms).sort((a,b)=>a-b), n=sorted.length;
    const median = n ? (sorted[Math.floor((n-1)/2)]+sorted[Math.floor(n/2)])/2 : 0;
    $('#latency').textContent = n ? `${median.toFixed(1)} ms` : '—';
    $('#cpu').textContent = n ? `${(traces.reduce((s,r)=>s+r.cpu_ms,0)/n/1000).toFixed(4)} s` : '—';
    $('#updated').textContent = `Updated ${new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}`;
    const last = traces.slice(-24), max = Math.max(...last.map(r=>r.wall_ms),1);
    $('#latency-chart').innerHTML = last.length ? last.map(r=>`<div class="bar ${r.status>=400?'error':''}" style="height:${Math.max(3,100*r.wall_ms/max)}%" title="${esc(r.route)} · ${Number(r.wall_ms).toFixed(2)} ms · HTTP ${r.status}"></div>`).join('') : '<p class="empty">Make a request to begin collecting evidence.</p>';
    $('#recent').innerHTML = table(traces.slice(-5).reverse());
    renderActivity();
    $('#connection-status').textContent = '';
  } catch (error) { $('#connection-status').textContent = `${error.message} Is the local service running?`; }
  finally { fetching = false; }
}
document.addEventListener('click', e => {
  const btn = e.target.closest('[data-request]');
  if (!btn) return;
  const row = traces.find(r=>r.request_id===btn.dataset.request);
  if (!row) return;
  openTab('activity'); $('#trace-detail').hidden=false;
  $('#detail-json').textContent=JSON.stringify(row,null,2);
  $('#trace-detail').scrollIntoView({behavior:'smooth',block:'nearest'});
});
$('#close-detail').onclick=()=>$('#trace-detail').hidden=true;
$('#refresh').onclick=refresh;
$('#search').oninput=renderActivity;
$('#status-filter').onchange=renderActivity;
$('#writing').oninput=()=>$('#char-count').textContent=`${$('#writing').value.length.toLocaleString()} / 20,000`;
const sample = 'The implementation of an effective framework requires careful consideration of several key factors. First, organizations should establish clear objectives and define measurable outcomes. Furthermore, consistent communication helps stakeholders understand their responsibilities and work toward shared goals. By adopting a structured approach, teams can improve efficiency and achieve sustainable results.';
$('#sample').onclick=()=>{$('#writing').value=sample;$('#writing').oninput();};
async function postJSON(route,payload) {
  const response=await fetch(route,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  let body;
  try { body=await response.json(); } catch { throw new Error(`The server returned HTTP ${response.status} without a JSON response.`); }
  if(!response.ok) throw new Error(body.message||body.error||`HTTP ${response.status}`);
  return {body,id:response.headers.get('X-Request-ID')};
}
$('#submit-form').onsubmit=async e=>{
  e.preventDefault(); $('#analyze').disabled=true;
  $('#submit-status').className=''; $('#submit-status').textContent='Analyzing locally… First use may load the model; please keep this page open.';
  selectedContent=null; $('#appeal-form').hidden=true;
  try {
    const {body:b,id}=await postJSON('/submit',{text:$('#writing').value,creator_id:$('#creator').value});
    selectedContent=b.content_id;
    const title=({unsure:'Creation method uncertain',ai:'AI-like signals observed',human:'Human-like signals observed'})[b.guess]||'Assessment returned';
    $('#result').innerHTML=`<h2 class="result-title">${esc(title)}</h2><p class="result-label">${esc(b.label)}</p><div class="result-score"><span>Combined heuristic index</span><b>${Number(b.confidence).toFixed(4)}</b></div><div class="meter"><span style="width:${Math.max(0,Math.min(100,b.confidence*100))}%"></span></div><div class="signal-row"><div><b>Model signal</b><small>Weight · 70%</small></div><strong>${Number(b.model_score).toFixed(4)}</strong></div><div class="signal-row"><div><b>Style signal</b><small>Weight · 30%</small></div><strong>${Number(b.style_score).toFixed(4)}</strong></div><p class="form-note">This index is not a calibrated probability of AI authorship.</p><p class="result-id">Content: ${esc(b.content_id)}<br>Request: ${esc(id)}</p>`;
    $('#appeal-form').hidden=false; $('#appeal-status').textContent='';
    $('#submit-status').className='success-message'; $('#submit-status').textContent='Assessment recorded. Your request trace is available in the explorer.';
  } catch(error) { $('#submit-status').className='error-message';$('#submit-status').textContent=error.message; }
  finally {$('#analyze').disabled=false;refresh();}
};
$('#appeal-form').onsubmit=async e=>{
  e.preventDefault(); const btn=e.target.querySelector('button');btn.disabled=true;
  try { const {body}=await postJSON('/appeal',{content_id:selectedContent,reasoning:$('#reason').value});$('#appeal-status').textContent=body.message;$('#appeal-status').className='success-message'; }
  catch(error) {$('#appeal-status').textContent=error.message;$('#appeal-status').className='error-message';}
  finally {btn.disabled=false;refresh();}
};
refresh();
