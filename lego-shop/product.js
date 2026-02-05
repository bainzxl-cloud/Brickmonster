// Product details page (no build step). Loads listings.json and renders one item by ?p=<id>

const CONFIG = {
  instagramHandle: "",
  dmText: "Hi! I'm interested in: ",
  currency: "CAD",
  siteTitle: "LEGO for Sale",
  pickupLocation: "",
  shippingNote: "",
};

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

  const show = (i)=>{
    const url = imgs[i] || primaryImage(item) || '';
    main.src = url;
    main.alt = safeText(item.name);
    thumbs.querySelectorAll('button').forEach((b,idx)=> b.setAttribute('aria-current', idx===i ? 'true' : 'false'));
  };

  thumbs.innerHTML = '';
  if(imgs.length <= 1){
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

  show(Math.max(0, Math.min(initialIndex, imgs.length-1)));
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

  setGallery(item, 0);

  const dm = dmLinkFor(item);
  $('pDm').href = dm;
  $('pIg').href = dm;

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
