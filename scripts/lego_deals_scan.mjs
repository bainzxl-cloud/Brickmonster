import fs from 'fs';
import path from 'path';

const KEYWORDS_PATH = 'C:\\Users\\bainz\\clawd\\data\\lego_deals_keywords.json';
const STATE_PATH = 'C:\\Users\\bainz\\clawd\\data\\lego_deals_state.json';
const DIGEST_PATH = 'C:\\Users\\bainz\\clawd\\data\\lego_deals_last_digest.txt';

const ON_HST = 0.13;

function loadJson(p, fallback) {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return fallback; }
}
function saveJson(p, obj) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(obj, null, 2), 'utf8');
}
function writeText(p, text) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, text, 'utf8');
}

function cad(n) {
  if (n == null || Number.isNaN(n)) return null;
  return Math.round(n * 100) / 100;
}

function parseCadMoney(str) {
  if (!str) return null;
  // Accept formats like "C $12.34", "C$12.34", "CA $12.34", "CA$12.34", "$12.34"
  const m = str.replace(/\s+/g, ' ').match(/(?:C\s?\$|CA\s?\$|\$)\s?([0-9][0-9,]*\.?[0-9]*)/i);
  if (!m) return null;
  const v = parseFloat(m[1].replace(/,/g, ''));
  return Number.isFinite(v) ? v : null;
}

function normalizeKeywordToLegoId(keyword) {
  const k = keyword.trim();
  // If keyword contains a 4-6 digit set number, use that.
  const m = k.match(/\b(\d{4,6})\b/);
  if (m) return m[1];
  // Otherwise treat the whole keyword as an ID-like token (minifig codes etc.)
  return k.replace(/^lego\s+/i, '').trim();
}

async function fetchText(url) {
  const res = await fetch(url, {
    headers: {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
      'accept-language': 'en-CA,en;q=0.9'
    }
  });
  if (!res.ok) throw new Error(`fetch ${url} -> ${res.status}`);
  return await res.text();
}

function extractEbaySearchItems(html) {
  // Very lightweight parsing: split on list items for results.
  const items = [];
  const chunks = html.split(/<li\s+class="[^"]*s-item[^"]*"/i).slice(1);
  for (const chunk of chunks) {
    // Item URL / ID
    const hrefM = chunk.match(/href="(https:\/\/www\.ebay\.ca\/itm\/[^"]+)"/i);
    if (!hrefM) continue;
    const url = hrefM[1].replace(/&amp;/g, '&');
    const idM = url.match(/\/itm\/(?:[^\/]+\/)?(\d{10,14})/);
    if (!idM) continue;
    const ebayItemId = idM[1];

    // Title
    const titleM = chunk.match(/<h3[^>]*class="s-item__title"[^>]*>([\s\S]*?)<\/h3>/i);
    let title = titleM ? titleM[1].replace(/<[^>]+>/g, '').trim() : '';
    if (!title || title === 'New Listing') {
      // Sometimes title is nested.
      const t2 = chunk.match(/s-item__title[^>]*>\s*<span[^>]*>([\s\S]*?)<\/span>/i);
      if (t2) title = t2[1].replace(/<[^>]+>/g, '').trim();
    }

    // Price
    const priceM = chunk.match(/class="s-item__price"[^>]*>([\s\S]*?)<\/span>/i);
    const price = parseCadMoney(priceM ? priceM[1].replace(/<[^>]+>/g,' ') : '');
    if (price == null) continue;

    // Shipping (may be "Free shipping" or "+C $X.XX shipping")
    const shipM = chunk.match(/class="s-item__shipping[^\"]*"[^>]*>([\s\S]*?)<\/span>/i)
      || chunk.match(/class="s-item__logisticsCost"[^>]*>([\s\S]*?)<\/span>/i);
    const shipText = shipM ? shipM[1].replace(/<[^>]+>/g,' ').trim() : '';
    let shipping = 0;
    if (shipText && !/free/i.test(shipText)) {
      const sm = shipText.match(/([\s\S]*?)(?:shipping|delivery|postage)/i);
      shipping = parseCadMoney(sm ? sm[1] : shipText) ?? 0;
    }

    items.push({ ebayItemId, url, title, price: cad(price), shipping: cad(shipping), shipText });
  }
  // Dedup by item id
  const seen = new Set();
  return items.filter(it => (seen.has(it.ebayItemId) ? false : (seen.add(it.ebayItemId), true)));
}

async function fetchBricklinkAvgCad(legoId, conditionHint='USED') {
  // For sets: S=75387-1. For minifigs/others: M=sw1315 etc.
  const isSet = /^\d{4,6}$/.test(legoId);
  const candidates = [];
  if (isSet) candidates.push(`https://www.bricklink.com/catalogPG.asp?S=${encodeURIComponent(legoId)}-1`);
  candidates.push(`https://www.bricklink.com/catalogPG.asp?${isSet ? 'S' : 'M'}=${encodeURIComponent(legoId)}`);

  for (const url of candidates) {
    let text;
    try {
      text = await fetchText(url);
    } catch {
      continue;
    }
    // Try to force CAD via currency grouping (BrickLink often respects locale and shows CA $).
    // We'll parse for "Avg Price" in CA $.
    const plain = text.replace(/<script[\s\S]*?<\/script>/gi,' ').replace(/<style[\s\S]*?<\/style>/gi,' ');
    const chunkStart = plain.search(/Last\s*6\s*Months\s*Sales/i);
    const tail = chunkStart >= 0 ? plain.slice(chunkStart) : plain;

    // Prefer USED avg unless conditionHint explicitly NEW.
    const preferUsed = !/\bnew\b/i.test(conditionHint);

    function findAvg(sectionLabel) {
      const idx = tail.search(new RegExp(sectionLabel, 'i'));
      if (idx < 0) return null;
      const sub = tail.slice(idx, idx + 25000);
      const m = sub.match(/Avg\s*Price\s*:\s*(?:CA\s*\$|C\s*\$)\s*([0-9][0-9,]*\.?[0-9]*)/i);
      if (!m) return null;
      const v = parseFloat(m[1].replace(/,/g,''));
      return Number.isFinite(v) ? v : null;
    }

    let avg = null;
    if (preferUsed) avg = findAvg('Used');
    if (avg == null) avg = findAvg('New');
    if (avg == null) {
      // fallback: first Avg Price in tail with CA $
      const m = tail.match(/Avg\s*Price\s*:\s*(?:CA\s*\$|C\s*\$)\s*([0-9][0-9,]*\.?[0-9]*)/i);
      if (m) avg = parseFloat(m[1].replace(/,/g,''));
    }
    if (avg != null) return cad(avg);
  }
  return null;
}

function computeEbayTotal(price, shipping, taxMode='est') {
  const sub = (price ?? 0) + (shipping ?? 0);
  const tax = sub * ON_HST;
  return { sub: cad(sub), tax: cad(tax), total: cad(sub + tax), taxLabel: taxMode === 'shown' ? 'tax' : 'HST est' };
}

async function main() {
  const cfg = loadJson(KEYWORDS_PATH, null);
  if (!cfg?.keywords?.length) throw new Error('No keywords found');

  const nowIso = new Date().toISOString();
  const state = loadJson(STATE_PATH, { version: 1, lastRunIso: null, items: {} });
  if (!state.items) state.items = {};

  const reportable = [];

  for (const keyword of cfg.keywords) {
    const legoId = normalizeKeywordToLegoId(keyword);
    const q = encodeURIComponent(keyword);
    const url = `https://www.ebay.ca/sch/i.html?_nkw=${q}&_sop=15&LH_PrefLoc=1&rt=nc`;

    let html;
    try {
      html = await fetchText(url);
    } catch (e) {
      // Skip keyword on fetch failure.
      continue;
    }

    const items = extractEbaySearchItems(html).slice(0, 8);
    if (!items.length) continue;

    // Fetch BL avg once per keyword/legoId (best effort)
    let blAvg = null;
    try { blAvg = await fetchBricklinkAvgCad(legoId, 'USED'); } catch { blAvg = null; }

    for (const it of items) {
      const computed = computeEbayTotal(it.price, it.shipping, 'est');
      const rec = state.items[it.ebayItemId] || {
        lastSeenIso: null,
        keyword,
        legoId: legoId || null,
        ebayUrl: it.url,
        lastComputedTotalCad: null,
        lastReportedTotalCad: null,
        lastReportedIso: null,
        bricklinkAvgCad: null,
        notes: null
      };

      rec.lastSeenIso = nowIso;
      rec.keyword = keyword;
      rec.legoId = legoId || rec.legoId || null;
      rec.ebayUrl = it.url;
      rec.lastComputedTotalCad = computed.total;
      rec.bricklinkAvgCad = blAvg;

      const shouldReport = (rec.lastReportedTotalCad == null) || (computed.total != null && computed.total < rec.lastReportedTotalCad);
      if (shouldReport) {
        rec.lastReportedTotalCad = computed.total;
        rec.lastReportedIso = nowIso;
        reportable.push({
          ebayItemId: it.ebayItemId,
          url: it.url,
          keyword,
          legoId,
          title: it.title,
          price: it.price,
          shipping: it.shipping,
          total: computed.total,
          taxLabel: computed.taxLabel,
          blAvg
        });
      }

      state.items[it.ebayItemId] = rec;
    }
  }

  state.lastRunIso = nowIso;
  saveJson(STATE_PATH, state);

  // Build digest max ~12 lines. Only reportable items.
  let digestLines = [];
  if (!reportable.length) {
    digestLines = ['no deals'];
  } else {
    // Sort: biggest savings vs BL if available, else lowest total.
    reportable.sort((a,b) => {
      const da = (a.blAvg != null && a.total != null) ? (a.blAvg - a.total) : -Infinity;
      const db = (b.blAvg != null && b.total != null) ? (b.blAvg - b.total) : -Infinity;
      if (da !== db) return db - da;
      return (a.total ?? 1e9) - (b.total ?? 1e9);
    });

    for (const r of reportable.slice(0, 12)) {
      const blPart = (r.blAvg != null) ? `BL avg C$${r.blAvg}` : 'BL avg n/a';
      const titlePart = r.title ? r.title.slice(0, 70).trim() : r.keyword;
      digestLines.push(`C$${r.total} total (${r.taxLabel}) vs ${blPart} — ${titlePart} — ${r.url}`);
    }
  }

  writeText(DIGEST_PATH, digestLines.join('\n'));
}

main().catch(err => {
  const msg = `SELF-TEST ISSUE: scan failed (${err?.message || String(err)})`;
  try { writeText(DIGEST_PATH, msg + '\n'); } catch {}
  console.error(err);
  process.exit(1);
});
