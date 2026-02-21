// Product details page (no build step). Loads listings.json and renders one item by ?p=<id>

const CONFIG = {
  instagramHandle: "",
  dmText: "Hi! I'm interested in: ",
  currency: "CAD",
  siteTitle: "LEGO for Sale",
  pickupLocation: "",
  shippingNote: "",
};

let PAYMENT_LINKS = {};

const $ = (id) => document.getElementById(id);

function safeText(s){
  return (s ?? "").toString();
}

function escapeHtml(s){
  return safeText(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function money(n){
  if (n == null || n === "") return "";
  try{
    return new Intl.NumberFormat(undefined,{style:'currency',currency:CONFIG.currency,maximumFractionDigits:0}).format(Number(n));
  }catch{
    return `$${n}`;
  }
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

function primaryImage(item){
  const arr = item.images && Array.isArray(item.images) ? item.images : [];
  return arr[0] || item.image || "";
}

function normalizeCategory(cat){
  const raw = safeText(cat).trim();
  const s = raw.toLowerCase().replace(/[-_\s]/g, "");
  if(!s) return "";
  if(s === 'minifig' || s === 'minifigure' || s === 'minifigures' || s === 'minifigure(s)') return 'Minifigure';
  return raw;
}

function applyContactLinks(){
  const ig = CONFIG.instagramHandle?.trim();
  const igUrl = ig ? `https://instagram.com/${ig}` : null;
  $('igLink').href = igUrl || '#';
  $('igLink').textContent = ig ? `@${ig}` : 'Instagram (set handle)';
  $('dmLink').href = igUrl || '#';
  $('siteTitle').textContent = CONFIG.siteTitle || 'LEGO for Sale';
  const sub = $('siteSubtitle');
  if(sub) sub.textContent = 'Details • DM to buy';
}

function dmLinkFor(){
  const ig = CONFIG.instagramHandle?.trim();
  if(!ig) return '#';
  return `https://instagram.com/${ig}`;
}

function setGallery(item, initialIndex=0){
  const imgs = (item.images && Array.isArray(item.images) && item.images.length)
    ? item.images
    : (item.image ? [item.image] : []);

  const main = $('pImg');
  const thumbs = $('pThumbs');
  const prev = $('gPrev');
  const next = $('gNext');
  const count = $('gCount');

  let idx = Math.max(0, Math.min(initialIndex, Math.max(0, imgs.length-1)));

  const show = (i)=>{
    if(!imgs.length){
      main.removeAttribute('src');
      main.alt = safeText(item.name);
      if(count) count.textContent = '';
      return;
    }
    idx = (i + imgs.length) % imgs.length;
    const url = imgs[idx] || primaryImage(item) || '';
    main.src = url;
    main.alt = safeText(item.name);
    thumbs.querySelectorAll('button').forEach((b, j)=> b.setAttribute('aria-current', j===idx ? 'true' : 'false'));
    if(count) count.textContent = `${idx+1}/${imgs.length}`;
  };

  thumbs.innerHTML = '';

  const hasMany = imgs.length > 1;
  if(prev) prev.style.display = hasMany ? '' : 'none';
  if(next) next.style.display = hasMany ? '' : 'none';
  if(count) count.style.display = imgs.length ? '' : 'none';

  if(prev) prev.onclick = ()=> show(idx - 1);
  if(next) next.onclick = ()=> show(idx + 1);

  // swipe (touch) + click-to-advance
  let startX = null;
  main.addEventListener('click', ()=>{ if(hasMany) show(idx + 1); });
  main.addEventListener('touchstart', (e)=>{
    if(!hasMany) return;
    const t = e.touches && e.touches[0];
    startX = t ? t.clientX : null;
  }, {passive:true});
  main.addEventListener('touchend', (e)=>{
    if(!hasMany) return;
    if(startX == null) return;
    const t = e.changedTouches && e.changedTouches[0];
    const endX = t ? t.clientX : null;
    if(endX == null) return;
    const dx = endX - startX;
    startX = null;
    if(Math.abs(dx) < 40) return;
    if(dx < 0) show(idx + 1);
    else show(idx - 1);
  }, {passive:true});

  // keyboard
  window.addEventListener('keydown', (e)=>{
    if(!hasMany) return;
    if(e.key === 'ArrowLeft') show(idx - 1);
    if(e.key === 'ArrowRight') show(idx + 1);
  });

  if(!hasMany){
    show(0);
    return;
  }

  imgs.forEach((url, i)=>{
    const b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('aria-label', `Image ${i+1}`);
    b.innerHTML = `<img src="${escapeHtml(url)}" alt="" loading="lazy" />`;
    b.addEventListener('click', ()=> show(i));
    thumbs.appendChild(b);
  });

  show(idx);
}

function buildBackLink(){
  const u = new URL(location.href);
  const back = new URL(location.href);
  back.searchParams.delete('p');
  // if user came from index.html with filters, keep them
  back.pathname = back.pathname.replace(/[^/]*$/, 'index.html');
  $('backLink').href = back.toString();

  // keep header links consistent
  // (also lets us keep query params as-is in case you want them)
}

function parseId(){
  const u = new URL(location.href);
  return u.searchParams.get('p') || '';
}

function setMetaTitle(name){
  document.title = name ? `${name} • ${CONFIG.siteTitle || 'LEGO Listings'}` : (CONFIG.siteTitle || document.title);
}

async function init(){
  buildBackLink();

  // Load payment links
  try {
    const plRes = await fetch('payment_links.json', {cache:'no-store'});
    const plData = await plRes.json();
    PAYMENT_LINKS = {};
    plData.forEach(p => { PAYMENT_LINKS[p.id] = p.link; });
  } catch(e) { console.log('No payment links'); }

  const res = await fetch('listings.json', {cache:'no-store'});
  const data = await res.json();
  if(data.config) Object.assign(CONFIG, data.config);

  applyContactLinks();

  const id = parseId();
  if(!id){
    $('notFound').hidden = false;
    return;
  }

  const items = (data.items || []).map(x=>({
    id: x.id ?? x.setNumber ?? x.slug,
    name: x.name ?? x.title ?? '',
    setNumber: x.setNumber ?? '',
    category: normalizeCategory(x.category ?? x.theme ?? ''),
    condition: x.condition ?? '',
    availability: x.availability ?? (x.status ? ({available:'in_stock', pending:'reserved', sold:'out_of_stock'}[x.status] || 'in_stock') : 'in_stock'),
    price: (x.price === 0 ? 0 : (x.price ?? null)),
    addedAt: x.addedAt ?? x.updatedAt ?? '',
    images: x.images ?? (x.image ? [x.image] : []),
    image: x.image ?? '',
    tags: x.tags ?? [],
    description: x.description ?? '',
    remaining: (x.remaining ?? null),
  })).filter(x=>x.id && x.name);

  const item = items.find(x=>String(x.id)===String(id));
  if(!item){
    $('notFound').hidden = false;
    return;
  }

  $('product').hidden = false;

  $('pTitle').textContent = safeText(item.name);
  $('pDesc').textContent = safeText(item.description || '');
  $('pSet').textContent = safeText(item.setNumber || '—');
  $('pCat').textContent = safeText(item.category || '—');
  $('pCond').textContent = safeText(item.condition || '—');
  $('pPrice').textContent = (item.price != null && item.price !== "") ? money(item.price) : 'DM';
  $('pBadges').innerHTML = `${badgeAvailability(item.availability)}${badgeCondition(item.condition)}`;

  // remaining box
  const rb = $('remainingBox');
  const rv = $('pRemaining');
  if(item.remaining != null && item.remaining !== ''){
    if(rv) rv.textContent = String(item.remaining);
    if(rb) rb.hidden = false;
  } else {
    if(rb) rb.hidden = true;
  }

  setGallery(item, 0);

  const dm = dmLinkFor(item);
  $('pDm').href = dm;
  $('pIg').href = dm;

  // Add Buy Now button if payment link exists
  const buyBtn = document.getElementById('pBuy');
  if(buyBtn && PAYMENT_LINKS[item.id]) {
    buyBtn.href = PAYMENT_LINKS[item.id];
    buyBtn.style.display = 'inline-block';
  } else if(buyBtn) {
    buyBtn.style.display = 'none';
  }

  setMetaTitle(item.name);

  // pickup + shipping hint
  const parts = [];
  if(CONFIG.pickupLocation) parts.push(`Pickup: ${CONFIG.pickupLocation}`);
  if(CONFIG.shippingNote) parts.push(CONFIG.shippingNote);
  const pickupHint = $('pickupHint');
  if(pickupHint) pickupHint.textContent = parts.join(' • ');

  $('copyLink').onclick = async ()=>{
    try{
      await navigator.clipboard.writeText(location.href);
      $('copyLink').textContent = 'Copied!';
      setTimeout(()=> $('copyLink').textContent = 'Copy link', 1200);
    }catch{
      prompt('Copy link:', location.href);
    }
  };
}

init().catch(err=>{
  console.error(err);
  $('notFound').hidden = false;
});
