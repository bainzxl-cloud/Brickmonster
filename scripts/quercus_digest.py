import json, os, sys, time
from datetime import datetime, timezone, timedelta
import urllib.request
import urllib.parse

BASE_URL = os.environ.get('CANVAS_BASE_URL', 'https://q.utoronto.ca')
API = BASE_URL.rstrip('/') + '/api/v1'
TOKEN_PATH = os.environ.get('CANVAS_TOKEN_PATH', os.path.join(os.path.dirname(__file__), '..', 'data', 'quercus_token.txt'))
STATE_PATH = os.environ.get('CANVAS_STATE_PATH', os.path.join(os.path.dirname(__file__), '..', 'data', 'quercus_state.json'))


def load_token():
    with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
        return f.read().strip()


def api_get(path, params=None, token=None):
    if params:
        qs = urllib.parse.urlencode(params)
        url = f"{API}{path}?{qs}"
    else:
        url = f"{API}{path}"
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Accept', 'application/json')
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        return json.loads(data.decode('utf-8'))


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'last_run_iso': None,
        'seen_announcement_ids': [],
        'seen_assignment_ids': [],
        'seen_planner_ids': []
    }


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)


def iso_now():
    return datetime.now(timezone.utc).isoformat()


def to_dt(s):
    if not s:
        return None
    try:
        # Canvas timestamps are ISO 8601
        return datetime.fromisoformat(s.replace('Z', '+00:00'))
    except Exception:
        return None


def short_time(iso):
    dt = to_dt(iso)
    if not dt:
        return None
    # show in Toronto time (EST/EDT) roughly by offset -5; good enough for display
    # If you want exact DST correctness, use zoneinfo; keep deps minimal here.
    return dt.astimezone(timezone(timedelta(hours=-5))).strftime('%Y-%m-%d %H:%M')


def main():
    token = load_token()
    state = load_state()

    # Active courses
    courses = api_get('/users/self/courses', params={
        'enrollment_state': 'active',
        'include[]': ['term', 'total_students'],
        'per_page': 100
    }, token=token)

    # Planner items (global upcoming)
    planner = api_get('/planner/items', params={
        'start_date': (datetime.now(timezone.utc) - timedelta(days=1)).date().isoformat(),
        'end_date': (datetime.now(timezone.utc) + timedelta(days=14)).date().isoformat(),
        'per_page': 100
    }, token=token)

    seen_planner = set(state.get('seen_planner_ids', []))
    new_planner = []
    for it in planner:
        pid = it.get('plannable_id') or it.get('id')
        key = str(pid)
        if key and key not in seen_planner:
            new_planner.append(it)

    # Per-course announcements + assignments
    seen_ann = set(map(str, state.get('seen_announcement_ids', [])))
    seen_asg = set(map(str, state.get('seen_assignment_ids', [])))
    new_anns = []
    new_asgs = []

    for c in courses:
        cid = c.get('id')
        cname = c.get('name') or c.get('course_code') or str(cid)
        if not cid:
            continue

        # Announcements (discussions with is_announcement)
        try:
            anns = api_get(f'/courses/{cid}/announcements', params={
                'per_page': 30
            }, token=token)
            for a in anns:
                aid = str(a.get('id'))
                if aid and aid not in seen_ann:
                    new_anns.append((cname, a))
        except Exception:
            pass

        # Assignments (upcoming)
        try:
            asgs = api_get(f'/courses/{cid}/assignments', params={
                'per_page': 50,
                'order_by': 'due_at'
            }, token=token)
            for a in asgs:
                aid = str(a.get('id'))
                if aid and aid not in seen_asg:
                    # only consider if has due date or is recent
                    new_asgs.append((cname, a))
        except Exception:
            pass

    # Build digest
    lines = []
    lines.append('Quercus daily check')
    lines.append(f"Checked: {iso_now()}")

    def add_section(title, items, formatter, max_items=10):
        if not items:
            return
        lines.append('')
        lines.append(title)
        for it in items[:max_items]:
            lines.append(formatter(it))
        if len(items) > max_items:
            lines.append(f"(+{len(items)-max_items} more)")

    # Planner items (often includes quizzes/assignments)
    def fmt_planner(it):
        title = it.get('plannable', {}).get('title') or it.get('plannable', {}).get('name') or it.get('title')
        due = it.get('plannable_date') or it.get('plannable', {}).get('due_at')
        course = it.get('context_name') or it.get('course_id')
        url = it.get('html_url') or it.get('plannable', {}).get('html_url')
        st = short_time(due)
        when = f" (due {st})" if st else ''
        return f"- {course}: {title}{when} {url or ''}".rstrip()

    add_section('New / upcoming items (next 14 days):', new_planner, fmt_planner)

    # Announcements
    def fmt_ann(pair):
        cname, a = pair
        title = a.get('title') or a.get('subject') or '(announcement)'
        posted = a.get('posted_at')
        st = short_time(posted)
        url = a.get('html_url')
        when = f" ({st})" if st else ''
        return f"- {cname}: {title}{when} {url or ''}".rstrip()

    add_section('New announcements:', new_anns, fmt_ann)

    # Assignments
    def fmt_asg(pair):
        cname, a = pair
        name = a.get('name') or '(assignment)'
        due = a.get('due_at')
        st = short_time(due)
        url = a.get('html_url')
        when = f" (due {st})" if st else ''
        return f"- {cname}: {name}{when} {url or ''}".rstrip()

    # Filter assignments to those with due date in next 14 days OR newly created/updated
    horizon = datetime.now(timezone.utc) + timedelta(days=14)
    filtered = []
    for pair in new_asgs:
        _, a = pair
        due = to_dt(a.get('due_at'))
        if due is None or due <= horizon:
            filtered.append(pair)
    add_section('New assignments (relevant):', filtered, fmt_asg)

    # Update state (keep last 200)
    for it in new_planner:
        pid = it.get('plannable_id') or it.get('id')
        if pid is not None:
            seen_planner.add(str(pid))
    for _, a in new_anns:
        if a.get('id') is not None:
            seen_ann.add(str(a.get('id')))
    for _, a in new_asgs:
        if a.get('id') is not None:
            seen_asg.add(str(a.get('id')))

    state['last_run_iso'] = iso_now()
    state['seen_planner_ids'] = list(seen_planner)[-200:]
    state['seen_announcement_ids'] = list(seen_ann)[-200:]
    state['seen_assignment_ids'] = list(seen_asg)[-400:]
    save_state(state)

    print('\n'.join(lines))


if __name__ == '__main__':
    main()
