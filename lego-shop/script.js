// Static LEGO store listing (no build step). Edit listings.json.
// Features: categories, search, filters (price, condition, availability), sorting, responsive grid.
// Product details are on product.html (deep link ?p=<id>).

const CONFIG = {
  instagramHandle: "", // e.g. "yourhandle" (no @)
  dmText: "Hi! I'm interested in: ",
  currency: "CAD",
  siteTitle: "LEGO for Sale",
  pickupLocation: "",
  shippingNote: "",
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

function safeText(s){
  return (s ?? "").toString();
}

function norm(s){
  return safeText(s).trim().toLowerCase();
}

function toNumberOrNull(v){
  const n = Number(String(v ?? "").replace(/[^0-9.]/g, ""));
  return Number.isFinite(n) ? n : null;
}

function uniqSorted(list){
  return Array.from(new Set(list.filter(Boolean))).sort((a,b)=>a.localeCompare(b));
}

function badgeAvailability(av){
  const s = (av||"in_stock").toLowerCase();
  const cls = s === 'out_of_stock' ? 'badge--out_of_stock' : s === 'reserved' ? 'badge--reserved' : 'badge--in_stock';
  const label = s.replace(/_/g,' ');
  return `<span class="badge ${cls}">${label}</span>`;
}

function badgeCondition(cond){
  if(!cond) return "";
  return `<span class="badge">${escapeHtml(cond)}</span>`;
}

function escapeHtml(s){
  return safeText(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function primaryImage(item){
  const arr = item.images && Array.isArray(item.images) ? item.images : [];
  return arr[0] || item.image || "";
}

function applyContactLinks(){
  const ig = CONFIG.instagramHandle?.trim();
  const igUrl = ig ? `https://instagram.com/${ig}` : null;
  const igLink = $('igLink');
  const dmLink = $('dmLink');

  const titleEl = $('siteTitle');
  if(titleEl) titleEl.textContent = CONFIG.siteTitle || 'LEGO for Sale';
  const subEl = $('siteSubtitle');
  if(subEl) subEl.textContent = 'Browse listings • DM to buy';

  igLink.href = igUrl || '#';
  igLink.textContent = ig ? `@${ig}` : 'Instagram (set handle)';
  dmLink.href = igUrl || '#';
}

function dmLinkFor(item){
  const ig = CONFIG.instagramHandle?.trim();
  if(!ig) return '#';
  return `https://instagram.com/${ig}`;
}

function buildSelectOptions(selectEl, values, placeholder){
  selectEl.innerHTML = "";
  const def = document.createElement('option');
  def.value = "";
  def.textContent = placeholder;
  selectEl.appendChild(def);
  for(const v of uniqSorted(values)){
    const opt = document.createElement('option');
    opt.value = v;
    opt.textContent = v;
    selectEl.appendChild(opt);
  }
}

function parseStateFromUrl(){
  const u = new URL(location.href);
  const s = {
    q: u.searchParams.get('q') || "",
    category: u.searchParams.get('category') || "",
    condition: u.searchParams.get('condition') || "",
    availability: u.searchParams.get('availability') || "",
    priceMin: u.searchParams.get('min') || "",
    priceMax: u.searchParams.get('max') || "",
    sort: u.searchParams.get('sort') || "newest",
    p: u.searchParams.get('p') || "",
  };
  return s;
}

function writeStateToUrl(state, {replace=false}={}){
  const u = new URL(location.href);
  const setOrDel = (k,v)=>{
    if(v == null || String(v).trim()==="") u.searchParams.delete(k);
    else u.searchParams.set(k, String(v));
  };
  setOrDel('q', state.q);
  setOrDel('category', state.category);
  setOrDel('condition', state.condition);
  setOrDel('availability', state.availability);
  setOrDel('min', state.priceMin);
  setOrDel('max', state.priceMax);
  setOrDel('sort', state.sort && state.sort !== 'newest' ? state.sort : "");
  setOrDel('p', state.p);
  const next = u.toString();
  if(replace) history.replaceState(null, "", next);
  else history.pushState(null, "", next);
}

function getUiState(){
  return {
    q: $('q').value.trim(),
    category: $('category').value,
    condition: $('condition').value,
    availability: $('availability').value,
    priceMin: $('priceMin').value.trim(),
    priceMax: $('priceMax').value.trim(),
    sort: $('sort').value,
    p: "", // product id for deep links
  };
}

function setUiState(s){
  $('q').value = s.q || "";
  $('category').value = s.category || "";
  $('condition').value = s.condition || "";
  $('availability').value = s.availability || "";
  $('priceMin').value = s.priceMin || "";
  $('priceMax').value = s.priceMax || "";
  $('sort').value = s.sort || "newest";
}

function renderActiveFilters(state){
  const chips = [];
  if(state.q) chips.push({k:'q', label:`Search: ${state.q}`});
  if(state.category) chips.push({k:'category', label:`Category: ${state.category}`});
  if(state.condition) chips.push({k:'condition', label:`Condition: ${state.condition}`});
  if(state.availability) chips.push({k:'availability', label:`Availability: ${state.availability.replace(/_/g,' ')}`});
  if(state.priceMin) chips.push({k:'min', label:`Min: ${state.priceMin}`});
  if(state.priceMax) chips.push({k:'max', label:`Max: ${state.priceMax}`});

  const wrap = $('activeFilters');
  wrap.innerHTML = chips.map(c=>
    `<span class="chip">${escapeHtml(c.label)} <button type="button" data-k="${c.k}" aria-label="Remove">×</button></span>`
  ).join('');

  wrap.querySelectorAll('button[data-k]').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const k = btn.getAttribute('data-k');
      if(k==='q') $('q').value = "";
      if(k==='category') $('category').value = "";
      if(k==='condition') $('condition').value = "";
      if(k==='availability') $('availability').value = "";
      if(k==='min') $('priceMin').value = "";
      if(k==='max') $('priceMax').value = "";
      scheduleRender();
    });
  });
}

let ITEMS = [];
let RENDER_TIMER = null;

function scheduleRender(){
  window.clearTimeout(RENDER_TIMER);
  RENDER_TIMER = window.setTimeout(()=>{
    const state = getUiState();
    writeStateToUrl(state, {replace:true});
    render(ITEMS, state);
  }, 80);
}

function productUrlFor(id){
  const u = new URL(location.href);
  u.pathname = u.pathname.replace(/[^/]*$/, 'product.html');
  u.searchParams.set('p', String(id));
  return u.toString();
}

function render(items, state){
  const q = norm(state.q);
  const category = state.category;
  const condition = state.condition;
  const availability = state.availability;
  const min = toNumberOrNull(state.priceMin);
  const max = toNumberOrNull(state.priceMax);
  const sort = state.sort;

  let out = items.filter(x=>{
    if(category && x.category !== category) return false;
    if(condition && x.condition !== condition) return false;
    if(availability && (x.availability||'in_stock') !== availability) return false;

    const price = Number(x.price);
    if(min != null && Number.isFinite(price) && price < min) return false;
    if(max != null && Number.isFinite(price) && price > max) return false;
    // if no price, still show (unless min/max set)
    if((min != null || max != null) && !Number.isFinite(price)) return false;

    if(q){
      const blob = `${x.name||''} ${x.setNumber||''} ${x.category||''} ${(x.tags||[]).join(' ')} ${x.condition||''}`.toLowerCase();
      if(!blob.includes(q)) return false;
    }
    return true;
  });

  if(sort === 'price_asc') out.sort((a,b)=>(a.price??1e18)-(b.price??1e18));
  if(sort === 'price_desc') out.sort((a,b)=>(b.price??-1)-(a.price??-1));
  if(sort === 'newest') out.sort((a,b)=> new Date(b.addedAt||0) - new Date(a.addedAt||0));

  $('stats').textContent = `${out.length} product${out.length===1?'':'s'} shown`;
  renderActiveFilters(state);

  const grid = $('grid');
  if(out.length === 0){
    grid.innerHTML = '';
    $('empty').hidden = false;
    return;
  }
  $('empty').hidden = true;

  const frag = document.createDocumentFragment();
  for(const x of out){
    const card = document.createElement('article');
    card.className = 'card';
    card.setAttribute('data-id', x.id);

    const imgUrl = primaryImage(x) || 'https://images.unsplash.com/photo-1628277610521-7e2c8e85f0a3?auto=format&fit=crop&w=1200&q=60';
    const priceText = (x.price != null && x.price !== "") ? money(x.price) : 'DM';

    card.innerHTML = `
      <img class="thumb" src="${escapeHtml(imgUrl)}" alt="${escapeHtml(x.name)}" loading="lazy" />
      <div class="card__body">
        <h3 class="card__title">${escapeHtml(x.name)}</h3>
        <div class="card__meta">
          <span>${escapeHtml(x.setNumber || '')}</span>
          <span>•</span>
          <span>${escapeHtml(x.category || 'LEGO')}</span>
          <span class="price">${escapeHtml(priceText)}</span>
        </div>
        <div class="badges">
          ${badgeAvailability(x.availability)}
          ${badgeCondition(x.condition)}
        </div>
      </div>
    `;

    card.addEventListener('click', ()=>{
      location.href = productUrlFor(x.id);
    });
    frag.appendChild(card);
  }
  grid.innerHTML = '';
  grid.appendChild(frag);
}

// product details moved to product.html

async function init(){
  const res = await fetch('listings.json', {cache:'no-store'});
  const data = await res.json();

  if(data.config) Object.assign(CONFIG, data.config);
  document.title = CONFIG.siteTitle || document.title;
  applyContactLinks();

  ITEMS = (data.items || []).map(x=>({
    id: x.id ?? x.setNumber ?? x.slug,
    name: x.name ?? x.title ?? '',
    setNumber: x.setNumber ?? '',
    category: x.category ?? x.theme ?? '',
    condition: x.condition ?? '',
    availability: x.availability ?? (x.status ? ({available:'in_stock', pending:'reserved', sold:'out_of_stock'}[x.status] || 'in_stock') : 'in_stock'),
    price: (x.price === 0 ? 0 : (x.price ?? null)),
    addedAt: x.addedAt ?? x.updatedAt ?? '',
    images: x.images ?? (x.image ? [x.image] : []),
    image: x.image ?? '',
    tags: x.tags ?? [],
    description: x.description ?? '',
  })).filter(x=>x.id && x.name);

  buildSelectOptions($('category'), ITEMS.map(x=>x.category), 'All categories');
  buildSelectOptions($('condition'), ITEMS.map(x=>x.condition), 'Any');

  const urlState = parseStateFromUrl();
  setUiState(urlState);

  // event wiring
  ['q','category','condition','availability','priceMin','priceMax','sort'].forEach(id=>{
    $(id).addEventListener('input', scheduleRender);
  });

  $('clear').addEventListener('click', ()=>{
    setUiState({q:'',category:'',condition:'',availability:'',priceMin:'',priceMax:'',sort:'newest'});
    scheduleRender();
  });

  window.addEventListener('popstate', ()=>{
    const s = parseStateFromUrl();
    setUiState(s);
    render(ITEMS, getUiState());
    // if a product id is present in URL, redirect to product page
    if(s.p){
      location.replace(productUrlFor(s.p));
    }
  });

  // first paint
  render(ITEMS, getUiState());

  // deep link open
  if(urlState.p){
    location.replace(productUrlFor(urlState.p));
  }
}

init().catch(err=>{
  console.error(err);
  $('stats').textContent = 'Could not load listings.json. Use a local web server (not file://).';
});
