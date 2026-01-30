import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const BASE_URL = process.env.CANVAS_BASE_URL || 'https://q.utoronto.ca';
const API = `${BASE_URL.replace(/\/$/, '')}/api/v1`;

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TOKEN_PATH = process.env.CANVAS_TOKEN_PATH || path.resolve(__dirname, '..', 'data', 'quercus_token.txt');
const STATE_PATH = process.env.CANVAS_STATE_PATH || path.resolve(__dirname, '..', 'data', 'quercus_state.json');

function readToken() {
  return fs.readFileSync(TOKEN_PATH, 'utf8').trim();
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
  } catch {
    return {
      last_run_iso: null,
      seen_announcement_ids: [],
      seen_assignment_ids: [],
      seen_planner_ids: [],
    };
  }
}

function saveState(state) {
  fs.mkdirSync(path.dirname(STATE_PATH), { recursive: true });
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2), 'utf8');
}

function isoNow() {
  return new Date().toISOString();
}

function toLocalToronto(iso) {
  if (!iso) return null;
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return null;
  // Use America/Toronto if available (it is in Node Intl)
  try {
    return new Intl.DateTimeFormat('en-CA', {
      timeZone: 'America/Toronto',
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit',
      hour12: false,
    }).format(d).replace(',', '');
  } catch {
    return d.toISOString().slice(0, 16).replace('T', ' ');
  }
}

async function apiGet(pathname, params, token) {
  const url = new URL(API + pathname);
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      if (Array.isArray(v)) {
        for (const vv of v) url.searchParams.append(k, vv);
      } else if (v !== undefined && v !== null) {
        url.searchParams.set(k, String(v));
      }
    }
  }

  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: 'application/json',
    },
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`GET ${url} -> ${res.status} ${text.slice(0, 200)}`);
  }
  return await res.json();
}

function clampSeen(arr, max) {
  const s = Array.from(new Set(arr.map(String)));
  return s.slice(Math.max(0, s.length - max));
}

function section(lines, title, items, fmt, maxItems = 10) {
  if (!items.length) return;
  lines.push('');
  lines.push(title);
  for (const it of items.slice(0, maxItems)) lines.push(fmt(it));
  if (items.length > maxItems) lines.push(`(+${items.length - maxItems} more)`);
}

async function main() {
  const token = readToken();
  const state = loadState();

  const courses = await apiGet('/users/self/courses', {
    enrollment_state: 'active',
    'include[]': ['term'],
    per_page: 100,
  }, token);

  const start = new Date(Date.now() - 24 * 3600 * 1000).toISOString().slice(0, 10);
  const end = new Date(Date.now() + 14 * 24 * 3600 * 1000).toISOString().slice(0, 10);
  const planner = await apiGet('/planner/items', {
    start_date: start,
    end_date: end,
    per_page: 100,
  }, token);

  const firstRun = !state.last_run_iso;

  const seenPlanner = new Set((state.seen_planner_ids || []).map(String));
  const newPlanner = [];
  for (const it of planner) {
    const pid = it?.plannable_id ?? it?.id;
    if (pid == null) continue;
    const key = String(pid);
    const due = it?.plannable_date || it?.plannable?.due_at;
    const dueMs = due ? new Date(due).getTime() : null;
    const isFutureish = dueMs == null ? true : dueMs >= (Date.now() - 6 * 3600 * 1000);

    if (firstRun) {
      // First run: don't flood — only show relevant upcoming items.
      if (isFutureish) newPlanner.push(it);
    } else {
      if (isFutureish && !seenPlanner.has(key)) newPlanner.push(it);
    }
  }

  const seenAnn = new Set((state.seen_announcement_ids || []).map(String));
  const seenAsg = new Set((state.seen_assignment_ids || []).map(String));
  const newAnns = [];
  const newAsgs = [];

  for (const c of courses) {
    const cid = c?.id;
    const cname = c?.name || c?.course_code || String(cid);
    if (!cid) continue;

    // Announcements
    try {
      const anns = await apiGet(`/courses/${cid}/announcements`, { per_page: 30 }, token);
      for (const a of anns) {
        const aid = a?.id;
        if (aid == null) continue;
        const key = String(aid);
        if (firstRun) {
          // first run: only include announcements posted in last 7 days
          const postedMs = a?.posted_at ? new Date(a.posted_at).getTime() : null;
          if (postedMs == null || postedMs >= (Date.now() - 7 * 24 * 3600 * 1000)) newAnns.push([cname, a]);
        } else {
          if (!seenAnn.has(key)) newAnns.push([cname, a]);
        }
      }
    } catch {}

    // Assignments
    try {
      const asgs = await apiGet(`/courses/${cid}/assignments`, { per_page: 50, order_by: 'due_at' }, token);
      for (const a of asgs) {
        const aid = a?.id;
        if (aid == null) continue;
        const key = String(aid);
        const dueMs = a?.due_at ? new Date(a.due_at).getTime() : null;
        const isFutureish = dueMs == null ? true : dueMs >= (Date.now() - 6 * 3600 * 1000);

        if (firstRun) {
          // first run: don't list old/past-due assignments
          if (isFutureish) newAsgs.push([cname, a]);
        } else {
          if (!seenAsg.has(key)) newAsgs.push([cname, a]);
        }
      }
    } catch {}
  }

  const lines = [];
  lines.push('Quercus daily check');
  lines.push(`Checked: ${isoNow()}`);

  section(lines, 'New / upcoming items (next 14 days):', newPlanner, (it) => {
    const title = it?.plannable?.title || it?.plannable?.name || it?.title || '(item)';
    const due = it?.plannable_date || it?.plannable?.due_at;
    const course = it?.context_name || it?.course_id || '(course)';
    const url = it?.html_url || it?.plannable?.html_url || '';
    const when = toLocalToronto(due);
    return `- ${course}: ${title}${when ? ` (due ${when})` : ''}${url ? ` ${url}` : ''}`;
  });

  section(lines, 'New announcements:', newAnns, ([cname, a]) => {
    const title = a?.title || a?.subject || '(announcement)';
    const posted = toLocalToronto(a?.posted_at);
    const url = a?.html_url || '';
    return `- ${cname}: ${title}${posted ? ` (${posted})` : ''}${url ? ` ${url}` : ''}`;
  });

  const horizon = Date.now() + 14 * 24 * 3600 * 1000;
  const filteredAsg = newAsgs.filter(([, a]) => {
    const due = a?.due_at ? new Date(a.due_at).getTime() : null;
    if (due == null) return true;
    return due >= (Date.now() - 6 * 3600 * 1000) && due <= horizon;
  });

  section(lines, 'New assignments (relevant):', filteredAsg, ([cname, a]) => {
    const name = a?.name || '(assignment)';
    const due = toLocalToronto(a?.due_at);
    const url = a?.html_url || '';
    return `- ${cname}: ${name}${due ? ` (due ${due})` : ''}${url ? ` ${url}` : ''}`;
  });

  // Update state
  for (const it of newPlanner) {
    const pid = it?.plannable_id ?? it?.id;
    if (pid != null) seenPlanner.add(String(pid));
  }
  for (const [, a] of newAnns) {
    if (a?.id != null) seenAnn.add(String(a.id));
  }
  for (const [, a] of newAsgs) {
    if (a?.id != null) seenAsg.add(String(a.id));
  }

  state.last_run_iso = isoNow();
  state.seen_planner_ids = clampSeen(Array.from(seenPlanner), 200);
  state.seen_announcement_ids = clampSeen(Array.from(seenAnn), 200);
  state.seen_assignment_ids = clampSeen(Array.from(seenAsg), 400);
  saveState(state);

  console.log(lines.join('\n'));
}

main().catch((e) => {
  console.error('ERROR:', e?.message || e);
  process.exit(1);
});
