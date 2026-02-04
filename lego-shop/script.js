// Simple LEGO listings page (no build step). Edit listings.json.

const CONFIG = {
  instagramHandle: "", // e.g. "yourhandle" (no @)
  dmText: "Hi! I'm interested in: ",
  currency: "CAD",
};

const $ = (id) => document.getElementById(id);

function money(n){
  if (n == null || n === "") return "";
  try{
    return new Intl.NumberFormat(undefined,{style:'currency',currency:CONFIG.currency,maximumFractionDigits:0}).format(Number(n));
  }catch{
    return `$${n}`;
  }
}

function badge(status){
  const s = (status||"available").toLowerCase();
  const cls = s === 'sold' ? 'badge--sold' : s === 'pending' ? 'badge--pending' : 'badge--available';
  const label = s.charAt(0).toUpperCase() + s.slice(1);
  return `<span class="badge ${cls}">${label}</span>`;
}

function safeText(s){
  return (s ?? "").toString();
}

function buildThemeOptions(items){
  const themes = Array.from(new Set(items.map(x=>x.theme).filter(Boolean))).sort((a,b)=>a.localeCompare(b));
  const sel = $('theme');
  for(const t of themes){
    const opt = document.createElement('option');
    opt.value = t;
    opt.textContent = t;
    sel.appendChild(opt);
  }
}

function applyContactLinks(){
  const ig = CONFIG.instagramHandle?.trim();
  const igUrl = ig ? `https://instagram.com/${ig}` : null;
  $('igLink').href = igUrl || '#';
  $('igLink').textContent = ig ? `@${ig}` : 'Instagram (set handle)';
  $('dmLink').href = igUrl ? `${igUrl}` : '#';
}

function dmLinkFor(item){
  const ig = CONFIG.instagramHandle?.trim();
  if(!ig) return '#';
  const msg = CONFIG.dmText + `${item.title}${item.setNumber ? ` (Set ${item.setNumber})` : ''}`;
  // Instagram doesn't have a universal deep link that works everywhere on desktop.
  // So we open profile; user can DM from there. We still show the exact text to copy.
  return `https://instagram.com/${ig}`;
}

function render(items){
  const q = $('q').value.trim().toLowerCase();
  const theme = $('theme').value;
  const status = $('status').value;
  const sort = $('sort').value;

  let out = items.filter(x=>{
    if(theme && x.theme !== theme) return false;
    if(status && (x.status||'available') !== status) return false;
    if(q){
      const blob = `${x.title||''} ${x.setNumber||''} ${x.theme||''} ${x.condition||''}`.toLowerCase();
      if(!blob.includes(q)) return false;
    }
    return true;
  });

  if(sort === 'price_asc') out.sort((a,b)=>(a.price??1e18)-(b.price??1e18));
  if(sort === 'price_desc') out.sort((a,b)=>(b.price??-1)-(a.price??-1));
  if(sort === 'updated_desc') out.sort((a,b)=> new Date(b.updatedAt||0) - new Date(a.updatedAt||0));

  $('stats').textContent = `${out.length} listing${out.length===1?'':'s'} shown`;

  const grid = $('grid');
  grid.innerHTML = out.map(x=>{
    const img = x.image || 'https://images.unsplash.com/photo-1628277610521-7e2c8e85f0a3?auto=format&fit=crop&w=1200&q=60';
    const price = x.status === 'sold' ? 'Sold' : (x.price != null ? money(x.price) : 'DM');
    return `
      <article class="card" data-id="${x.id}">
        <img class="thumb" src="${img}" alt="${safeText(x.title)}" loading="lazy" />
        <div class="card__body">
          <h3 class="card__title">${safeText(x.title)}</h3>
          <div class="card__meta">
            <span>${safeText(x.setNumber || '')}</span>
            <span>•</span>
            <span>${safeText(x.theme || 'LEGO')}</span>
            <span class="price">${price}</span>
          </div>
          <div class="badges">
            ${badge(x.status)}
            ${x.condition ? `<span class="badge">${safeText(x.condition)}</span>` : ''}
          </div>
        </div>
      </article>
    `;
  }).join('');

  $('empty').hidden = out.length !== 0;

  grid.querySelectorAll('.card').forEach(card=>{
    card.addEventListener('click', ()=>{
      const id = card.getAttribute('data-id');
      const item = items.find(x=>String(x.id)===String(id));
      if(item) openModal(item);
    });
  });
}

function openModal(item){
  const img = item.image || 'https://images.unsplash.com/photo-1628277610521-7e2c8e85f0a3?auto=format&fit=crop&w=1200&q=60';
  $('mImg').src = img;
  $('mImg').alt = safeText(item.title);
  $('mTitle').textContent = safeText(item.title);
  $('mDesc').textContent = safeText(item.description || '');
  $('mSet').textContent = safeText(item.setNumber || '—');
  $('mTheme').textContent = safeText(item.theme || '—');
  $('mCond').textContent = safeText(item.condition || '—');
  $('mPrice').textContent = item.status === 'sold' ? 'Sold' : (item.price != null ? money(item.price) : 'DM');

  $('mBadges').innerHTML = `${badge(item.status)}${item.condition?`<span class="badge">${safeText(item.condition)}</span>`:''}`;

  const dm = dmLinkFor(item);
  $('mDm').href = dm;
  $('mIg').href = dm;

  // Show copyable DM text in console for convenience
  const msg = CONFIG.dmText + `${item.title}${item.setNumber ? ` (Set ${item.setNumber})` : ''}`;
  console.log('DM text:', msg);

  $('modal').showModal();
}

async function init(){
  applyContactLinks();

  const res = await fetch('listings.json', {cache:'no-store'});
  const data = await res.json();
  const items = data.items || [];

  buildThemeOptions(items);

  const rerender = ()=>render(items);
  ['q','theme','status','sort'].forEach(id=> $(id).addEventListener('input', rerender));
  rerender();

  // Optional: override config from listings.json
  if(data.config){
    Object.assign(CONFIG, data.config);
    applyContactLinks();
    rerender();
  }
}

init().catch(err=>{
  console.error(err);
  $('stats').textContent = 'Could not load listings.json. Open this page with a local web server (not file://) or use Chrome with disabled file restrictions.';
});
