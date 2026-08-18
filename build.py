import json, html, re
from datetime import datetime, timezone

with open('pocket_items.json') as f:
    items = json.load(f)

TODAY = datetime(2026, 8, 18, tzinfo=timezone.utc)

LANES = {
    "Leadership Retreat": dict(color="var(--navy)"),
    "Fun & Learn Events": dict(color="var(--cyan)"),
    "Ambassadors & Regions": dict(color="var(--purple)"),
    "Policy & Courts (J4C)": dict(color="#f28b00"),
    "Youth Support": dict(color="var(--coral)"),
    "Org Ops & Finance": dict(color="var(--green)"),
    "Training & Curriculum": dict(color="#0b9fc4"),
    "Personal & Home": dict(color="#8b4bd7"),
}

def lane_for(it):
    t = (it.get("recordingTitle") or "") + " " + it.get("label","") + " " + it.get("context","")
    tl = t.lower()
    if "retreat" in tl or "orientation recap" in tl:
        return "Leadership Retreat"
    if "samson" in tl or "dog" in tl or "d&d" in tl or "shadow pickup" in tl or "childcare" in tl:
        return "Personal & Home"
    if "j4c" in tl or "committee" in tl and "governance" not in tl:
        return "Policy & Courts (J4C)"
    if "ambassador" in tl or "region 10" in tl or "region 12" in tl or "academy day" in tl:
        return "Ambassadors & Regions"
    if "appleseed" in tl or "empowerment website and training" in tl or "curriculum" in tl:
        return "Training & Curriculum"
    if "resource hub" in tl or "darnell" in tl or "housing" in tl or "na foundation" in tl:
        return "Youth Support"
    if "governance" in tl or "budget" in tl or "finance" in tl or "hilton" in tl or "ghi" in tl:
        return "Org Ops & Finance"
    if "fun and learn" in tl:
        return "Fun & Learn Events"
    return "Org Ops & Finance"

# Manual overrides: dependency person + force-self for "Attend" items, lane fixes
DEP_PERSON = {
    "3e824679-bf6b-492d-ab24-0c10864fd7f0": "Reggie & Brooklyn",
    "ba8c31e7-b5e5-468a-8540-9e1354412f0b": "LaDrina",
    "dcb159d7-91d3-476a-9b99-03dc5737a390": "Ms. Taylor",
    "87bd8307-c77c-4595-9fd0-20e445606af8": "J4C Curriculum Team",
    "30b63bdb-2b85-4d4a-a5a0-a4ad081090f5": "Amon",
    "3141ebbb-b28b-4599-babb-0a6275513439": "Amon",
    "2e0e973e-472d-4d2d-af0f-98f070222c5b": "Daren",
    "e713532e-a451-48b2-906e-f8a3530c611d": "Pilot County Partners",
    "88e30699-83f1-44c3-ba33-6af024783e58": "Data Subcommittee",
    "b601854a-05eb-4267-b64f-591fbc9d5645": None,  # actually Anthony's own calendar item
}
SELF_OVERRIDE = {"b601854a-05eb-4267-b64f-591fbc9d5645"}  # "Attend joint study committee" is Anthony's own

CONTACT_METHOD = {
    "Reggie & Brooklyn": "Text / Slack",
    "LaDrina": "Slack DM",
    "Ms. Taylor": "Email",
    "J4C Curriculum Team": "Email thread",
    "Amon": "Text",
    "Daren": "Email",
    "Pilot County Partners": "In-person (Lake Lanier)",
    "Data Subcommittee": "Email",
}

for it in items:
    it["lane"] = lane_for(it)
    aid = it["actionItemId"]
    if aid in SELF_OVERRIDE:
        it["assignee"] = "me"
    dep = DEP_PERSON.get(aid)
    if it["assignee"] not in ("me",) and dep is None and aid not in SELF_OVERRIDE:
        dep = it["assignee"] if it["assignee"] != "Other" else "Team"
    it["depPerson"] = dep if it["assignee"] != "me" else None

def parse_due(d):
    if not d:
        return None
    try:
        d2 = d.rstrip(",")
        return datetime.fromisoformat(d2.replace("Z", "+00:00"))
    except Exception:
        return None

for it in items:
    it["dueParsed"] = parse_due(it["dueDate"])
    it["overdue"] = bool(it["dueParsed"] and it["dueParsed"] < TODAY)

# Split
mine = [it for it in items if it["assignee"] == "me"]
mine.sort(key=lambda x: (x["dueParsed"] is None, x["dueParsed"] or TODAY))
others = [it for it in items if it["assignee"] != "me"]

emails = [it for it in mine if it["actionType"] == "draft_email"]
messages = [it for it in mine if it["actionType"] == "send_message"]
reminders = [it for it in mine if it["actionType"] == "create_reminder"]

TOP_N = 20
top_ids = set(it["actionItemId"] for it in (
    sorted(mine, key=lambda x: ({"high":0,"medium":1,"low":2}[x["priority"]], x["dueParsed"] is None, x["dueParsed"] or TODAY))[:TOP_N]
))

def esc(s):
    return html.escape(s or "")

def fmt_date(dt, raw):
    if not dt:
        return "No due date"
    return dt.strftime("%b %-d, %Y") if hasattr(dt, "strftime") else raw

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# ---------- Build task rows (My Top / All) ----------
def task_row(it, idx):
    lane = it["lane"]
    due_cls = "date urgent" if it["overdue"] else "date"
    due_txt = fmt_date(it["dueParsed"], it["dueDate"])
    if it["overdue"]:
        due_txt = "OVERDUE · " + due_txt
    detail = esc(it["context"])
    return f'''<tr class="task-row" data-task-id="{esc(it['actionItemId'])}" data-lane="{esc(lane)}" data-priority="{it['priority']}" data-top="{1 if it['actionItemId'] in top_ids else 0}" data-search="{esc((it['label']+' '+it['context']+' '+it['recordingTitle']).lower())}">
<td data-label="Done"><input type="checkbox" class="check" aria-label="Mark {esc(it['label'])} done"></td>
<td data-label="Task"><span class="task-number">{idx:02d}</span><span class="task-name">{esc(it['label'])}</span><div class="task-detail">{detail}</div></td>
<td data-label="Priority"><span class="priority {it['priority']}">{it['priority'].capitalize()}</span></td>
<td data-label="Owner">Anthony</td>
<td data-label="Due"><span class="{due_cls}">{due_txt}</span></td>
<td data-label="Type">{it['actionType'].replace('_',' ').title()}</td>
<td data-label="Lane"><span class="event-dot" style="background:{LANES[lane]['color']}"></span>{esc(lane)}</td>
</tr>'''

task_rows_html = "\n".join(task_row(it, i+1) for i, it in enumerate(mine))

# ---------- Build dependency rows ----------
def dep_row(it):
    lane = it["lane"]
    due_txt = fmt_date(it["dueParsed"], it["dueDate"])
    person = it["depPerson"] or "Team"
    contact = CONTACT_METHOD.get(person, "Follow up")
    return f'''<tr data-task-id="{esc(it['actionItemId'])}" data-lane="{esc(lane)}" data-search="{esc((it['label']+' '+person+' '+it['context']).lower())}">
<td data-label="Person"><span class="person-mark">{esc(person[:2].upper())}</span>{esc(person)}</td>
<td data-label="Contact">{esc(contact)}</td>
<td data-label="Deliverable">{esc(it['label'])}<div class="task-detail">{esc(it['context'])}</div></td>
<td data-label="Due"><span class="date">{due_txt}</span></td>
<td data-label="Blocks"><span class="event-dot" style="background:{LANES[lane]['color']}"></span>{esc(lane)}</td>
<td data-label="Status"><label><input type="checkbox" class="received-check" aria-label="Mark received from {esc(person)}"><span class="status"></span></label></td>
</tr>'''

dep_rows_html = "\n".join(dep_row(it) for it in others)

# ---------- Email drafts ----------
def email_card(it, i):
    subj = esc(it.get("emailSubject") or it["label"])
    body = esc(it.get("emailBody") or "")
    to = esc(it.get("emailTo") or "(add recipient)")
    kind = "Email" if it["actionType"] == "draft_email" else "Message"
    return f'''<div class="email-row" data-task-id="{esc(it['actionItemId'])}" data-search="{esc((subj+' '+body).lower())}">
<input type="checkbox" class="sent-check" aria-label="Mark {subj} as sent">
<div><strong>{subj}</strong><span>{kind} · To: {to}</span><span>{body[:160]}{"…" if len(body)>160 else ""}</span></div>
</div>'''

email_cards_html = "\n".join(email_card(it, i) for i, it in enumerate(emails+messages))

# ---------- Lane filter chips ----------
lane_counts = {}
for it in items:
    lane_counts[it["lane"]] = lane_counts.get(it["lane"], 0) + 1

def lane_chip(lane, count, first):
    color = LANES[lane]["color"]
    pressed = "true" if first else "false"
    return f'''<button class="event-filter lane-filter" style="--event:{color}" data-lane="{esc(lane)}" aria-pressed="{pressed}">
<span class="event-icon">●</span>
<span><strong>{esc(lane)}</strong><small>{count} task{"s" if count != 1 else ""}</small></span>
</button>'''

lane_chips_html = "\n".join(lane_chip(l, c, i==0) for i, (l, c) in enumerate(sorted(lane_counts.items(), key=lambda x:-x[1])))

# ---------- Side progress by lane ----------
def progress_item(lane, count):
    color = LANES[lane]["color"]
    return f'''<div class="event-progress-item" data-lane-progress="{esc(lane)}" style="--event:{color}">
<div class="progress-row"><strong>{esc(lane)}</strong><span><span class="lp-done">0</span>/{count}</span></div>
<div class="bar"><span style="--w:0%"></span></div>
</div>'''

progress_html = "\n".join(progress_item(l, c) for l, c in sorted(lane_counts.items(), key=lambda x:-x[1]))

out = dict(
    task_rows=task_rows_html,
    dep_rows=dep_rows_html,
    email_cards=email_cards_html,
    lane_chips=lane_chips_html,
    progress=progress_html,
    total_mine=len(mine),
    total_others=len(others),
    total_emails=len(emails)+len(messages),
    overdue_count=sum(1 for it in mine if it["overdue"]),
)

with open("fragments.json", "w") as f:
    json.dump(out, f)

print("mine:", len(mine), "others:", len(others), "emails:", len(emails)+len(messages), "overdue:", out["overdue_count"])
print("lanes:", lane_counts)
