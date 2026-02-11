import fs from 'fs';
import path from 'path';

const STATE_PATH = 'C:\\Users\\bainz\\clawd\\data\\lego_deals_state.json';

function loadState() {
  try { return JSON.parse(fs.readFileSync(STATE_PATH,'utf8')); } catch { return { version:1, lastRunIso:null, items:{} }; }
}
function saveState(s) {
  fs.mkdirSync(path.dirname(STATE_PATH), {recursive:true});
  fs.writeFileSync(STATE_PATH, JSON.stringify(s,null,2), 'utf8');
}

function simulateRun(tag, ebayItemId, computedTotal) {
  const state = loadState();
  if (!state.items) state.items = {};
  const now = new Date().toISOString();
  const rec = state.items[ebayItemId] || {
    ebayUrl: `https://www.ebay.ca/itm/${ebayItemId}`,
    keyword: 'TESTKEY',
    legoId: 'TEST1234',
    lastSeenIso: null,
    lastComputedTotalCad: null,
    lastReportedTotalCad: null,
    lastReportedIso: null,
    bricklinkAvgCad: 999
  };

  rec.lastSeenIso = now;
  rec.lastComputedTotalCad = computedTotal;

  const shouldReport = (rec.lastReportedTotalCad == null) || (computedTotal < rec.lastReportedTotalCad);
  if (shouldReport) {
    rec.lastReportedTotalCad = computedTotal;
    rec.lastReportedIso = now;
  }

  state.items[ebayItemId] = rec;
  state.lastRunIso = now;
  saveState(state);

  return { tag, ebayItemId, computedTotal, lastReportedTotalCad: rec.lastReportedTotalCad, shouldReport };
}

const ebayItemId = '123456789012';
const r1 = simulateRun('run1', ebayItemId, 120.00);
const r2 = simulateRun('run2', ebayItemId, 130.00);
const r3 = simulateRun('run3', ebayItemId, 110.00);

console.log(JSON.stringify({r1,r2,r3}, null, 2));
