import json, html, re
from datetime import datetime, timezone

with open('pocket_items.json') as f:
    items = json.load(f)

TODAY = datetime(2026, 8, 18, tzinfo=timezone.utc)

LANES = {
    "Leadership Retreat": dict(color="var(--navy)"),
    "Fun & Learn Events": dict(color="var(--cyan)"),
    "MARTA Day": dict(color="#f28b00"),
    "Credit Check Game Day": dict(color="#ff5f51"),
    "Grants & Funding": dict(color="#13a76b"),
    "Ambassadors & Regions": dict(color="var(--purple)"),
    "Policy & Courts (J4C)": dict(color="#c9752f"),
    "Youth Support": dict(color="#d1435a"),
    "Org Ops & Finance": dict(color="#2f8f6f"),
    "Training & Curriculum": dict(color="#0b9fc4"),
    "Personal & Home": dict(color="#8b4bd7"),
    "D&D Campaign": dict(color="#7a2e2e"),
    "Vacation & Travel": dict(color="#0e9e8a"),
    "School (KSU)": dict(color="#3355dd"),
    "Internship": dict(color="#c2185b"),
    "Navy Reserve": dict(color="#3a4a5a"),
}

def lane_for(it):
    t = (it.get("recordingTitle") or "") + " " + it.get("label","") + " " + it.get("context","")
    tl = t.lower()
    if "marta" in tl or "martyr day" in tl or "marty day" in tl:
        return "MARTA Day"
    if "credit check" in tl:
        return "Credit Check Game Day"
    if ("grant" in tl and "governance" not in tl) or "sra" in tl or "sie grant" in tl or "title iv-e" in tl or "hilton" in tl or " ghi " in (" "+tl+" "):
        return "Grants & Funding"
    if "d&d" in tl or "dungeon" in tl or "underdark" in tl or ("campaign" in tl and "avengers" not in tl and "grant" not in tl):
        return "D&D Campaign"
    if "hawaii" in tl or "excursion" in tl or "new york" in tl or "vacation" in tl:
        return "Vacation & Travel"
    if "internship support" in tl or "placement" in tl:
        return "Internship"
    if "ksu" in tl or "kennesaw" in tl or "msw" in tl:
        return "School (KSU)"
    if "navy" in tl or "drill" in tl or "pfa" in tl:
        return "Navy Reserve"
    if "retreat" in tl or "orientation recap" in tl:
        return "Leadership Retreat"
    if "samson" in tl or " dog " in (" "+tl+" ") or "shadow pickup" in tl or "childcare" in tl or "anniversary" in tl or "budget cal" in tl or "allstate" in tl or "fence debris" in tl or "fitbit" in tl or "free agents" in tl:
        return "Personal & Home"
    if "j4c" in tl or ("committee" in tl and "governance" not in tl and "housing coalition" not in tl):
        return "Policy & Courts (J4C)"
    if "ambassador" in tl or "region 10" in tl or "region 12" in tl or "academy day" in tl:
        return "Ambassadors & Regions"
    if "appleseed" in tl or "empowerment website and training" in tl or "curriculum" in tl:
        return "Training & Curriculum"
    if "resource hub" in tl or "darnell" in tl or "housing" in tl or "na foundation" in tl:
        return "Youth Support"
    if "governance" in tl or "budget" in tl or "finance" in tl or "avengers" in tl or "salesforce" in tl or "amazon requisition" in tl:
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
    "e28f9c96-2706-4843-a5a1-cd2e8715b609": "Sarabeth",
    "d42b1e31-f2c2-46fe-9096-851532e8bfd8": "Megan",
    "2979d959-8503-44c5-8e31-e70e4ddb7675": "Devin",
    "a9ce69e6-cb23-47c9-8f54-7e70e18d560f": "Leo",
    "ed39f07b-23ba-4e95-8f06-52eba20ffc9f": "DMPA Team",
    "a8df3bb2-59a6-4b0c-b905-4038cadbd2fd": "Grants Office (Sophia)",
    "2cb86f1a-cee9-4ce4-9727-a8ce741c6a83": "Devin",
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

def gcal_quickadd_url(it):
    text = it["label"]
    dt = it["dueParsed"]
    dates = ""
    if dt:
        start = dt.strftime("%Y%m%dT%H%M%S")
        end = (dt).strftime("%Y%m%dT%H%M%S")
        dates = f"&dates={start}Z/{end}Z"
    details = it["context"]
    import urllib.parse as up
    return ("https://calendar.google.com/calendar/render?action=TEMPLATE"
            f"&text={up.quote(text)}{dates}&details={up.quote(details)}")

# ---------- Build task rows (My Top / All) ----------
def task_row(it, idx):
    lane = it["lane"]
    due_cls = "date urgent" if it["overdue"] else "date"
    due_txt = fmt_date(it["dueParsed"], it["dueDate"])
    if it["overdue"]:
        due_txt = "OVERDUE · " + due_txt
    due_iso = it["dueParsed"].isoformat() if it["dueParsed"] else ""
    detail = esc(it["context"])
    at = it["actionType"]
    if at in ("draft_email", "send_message"):
        type_cell = f'<button class="type-jump" data-jump-tab="emails" data-jump-target="{esc(it["actionItemId"])}" type="button">{at.replace("_"," ").title()} ↗</button>'
    else:
        type_cell = f'<a class="type-jump" href="{esc(gcal_quickadd_url(it))}" target="_blank" rel="noopener">Create Reminder ↗</a>'
    checked = " checked" if it.get("status") == "COMPLETED" else ""
    return f'''<tr class="task-row" data-task-id="{esc(it['actionItemId'])}" data-lane="{esc(lane)}" data-priority="{it['priority']}" data-top="{1 if it['actionItemId'] in top_ids else 0}" data-due="{due_iso}" data-search="{esc((it['label']+' '+it['context']+' '+it['recordingTitle']).lower())}">
<td data-label="Done"><input type="checkbox" class="check" aria-label="Mark {esc(it['label'])} done"{checked}></td>
<td data-label="Task"><span class="task-number">{idx:02d}</span><span class="task-name">{esc(it['label'])}</span><div class="task-detail">{detail}</div></td>
<td data-label="Priority"><span class="priority {it['priority']}">{it['priority'].capitalize()}</span></td>
<td data-label="Owner">Anthony</td>
<td data-label="Due"><span class="{due_cls}">{due_txt}</span><span class="soon-badge" hidden>⏳ Coming up</span></td>
<td data-label="Type">{type_cell}</td>
<td data-label="Lane"><span class="event-dot" style="background:{LANES[lane]['color']}"></span>{esc(lane)}</td>
</tr>'''

task_rows_html = "\n".join(task_row(it, i+1) for i, it in enumerate(mine))

# ---------- Build dependency rows ----------
def dep_row(it):
    lane = it["lane"]
    due_txt = fmt_date(it["dueParsed"], it["dueDate"])
    person = it["depPerson"] or "Team"
    contact = CONTACT_METHOD.get(person, "Follow up")
    checked = " checked" if it.get("status") == "COMPLETED" else ""
    return f'''<tr data-task-id="{esc(it['actionItemId'])}" data-lane="{esc(lane)}" data-search="{esc((it['label']+' '+person+' '+it['context']).lower())}">
<td data-label="Person"><span class="person-mark">{esc(person[:2].upper())}</span>{esc(person)}</td>
<td data-label="Contact">{esc(contact)}</td>
<td data-label="Deliverable">{esc(it['label'])}<div class="task-detail">{esc(it['context'])}</div></td>
<td data-label="Due"><span class="date">{due_txt}</span></td>
<td data-label="Blocks"><span class="event-dot" style="background:{LANES[lane]['color']}"></span>{esc(lane)}</td>
<td data-label="Status"><label><input type="checkbox" class="received-check" aria-label="Mark received from {esc(person)}"{checked}><span class="status"></span></label></td>
</tr>'''

dep_rows_html = "\n".join(dep_row(it) for it in others)

# ---------- Email drafts (editable: inputs + contenteditable body) ----------
def email_card(it, i):
    subj = esc(it.get("emailSubject") or it["label"])
    body = esc(it.get("emailBody") or "")
    to = esc(it.get("emailTo") or "")
    kind = "Email" if it["actionType"] == "draft_email" else "Message"
    lane = it["lane"]
    color = LANES[lane]["color"]
    checked = " checked" if it.get("status") == "COMPLETED" else ""
    return f'''<article class="email-card" id="email-{esc(it['actionItemId'])}" data-task-id="{esc(it['actionItemId'])}" style="--event:{color}" data-search="{esc((subj+' '+body+' '+to).lower())}">
<div class="email-card-head">
  <span class="event-dot" style="background:{color}"></span>
  <strong>{esc(it['label'])}</strong>
  <span class="kind-badge">{kind}</span>
  <label class="sent-toggle"><input type="checkbox" class="sent-check" aria-label="Mark {subj} as sent"{checked}> Sent</label>
</div>
<div class="email-field"><label>To</label><input class="field email-to" value="{to}" placeholder="Add recipient email"></div>
<div class="email-field"><label>Subject</label><input class="field email-subject" value="{subj}"></div>
<div class="email-field"><label>Body</label><div class="field email-body" contenteditable="true" role="textbox" aria-multiline="true">{body}</div></div>
<div class="email-actions"><button class="action-btn secondary copy-email-btn" type="button">Copy full email</button></div>
</article>'''

email_cards_html = "\n".join(email_card(it, i) for i, it in enumerate(emails+messages))

# ---------- Draft Materials (one editable brief per lane, generated from real tasks) ----------
def material_card(lane, its):
    color = LANES[lane]["color"]
    upcoming = sorted([i for i in its if i["dueParsed"]], key=lambda x: x["dueParsed"])
    next_due = fmt_date(upcoming[0]["dueParsed"], "") if upcoming else "No date set yet"
    bullets = "\n".join(f"- {i['label']}" for i in its[:8])
    headline = lane.upper()
    subhead = f"{len(its)} open item{'s' if len(its)!=1 else ''} · next due {next_due}"
    body = bullets
    mid = slug(lane)
    return f'''<article class="material-card" id="material-{mid}" style="--material:{color}" data-search="{esc(lane.lower())}">
  <div class="material-preview">
    <span class="material-brand">Str8Jacket Brain Control</span>
    <h3 class="material-headline" contenteditable="true">{esc(headline)}</h3>
    <p class="material-subhead" contenteditable="true">{esc(subhead)}</p>
    <div class="material-body" contenteditable="true">{esc(body)}</div>
  </div>
  <div class="material-actions"><button class="action-btn secondary copy-material-btn" type="button">Copy draft</button></div>
</article>'''

materials_by_lane = {}
for it in mine:
    materials_by_lane.setdefault(it["lane"], []).append(it)

materials_html = "\n".join(material_card(l, its) for l, its in sorted(materials_by_lane.items(), key=lambda x: -len(x[1])))

# ---------- Pomodoro task list (id/title only, used by the focus timer) ----------
pomo_tasks = [{"id": it["actionItemId"], "title": it["label"], "lane": it["lane"]} for it in mine]

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
    return f'''<div class="event-progress-item" data-lane-progress="{esc(lane)}" role="button" tabindex="0" style="--event:{color}">
<div class="progress-row"><strong>{esc(lane)}</strong><span><span class="lp-done">0</span>/{count}</span></div>
<div class="bar"><span style="--w:0%"></span></div>
</div>'''

progress_html = "\n".join(progress_item(l, c) for l, c in sorted(lane_counts.items(), key=lambda x:-x[1]))

# ---------- Calendar (Google Calendar, next ~5 weeks) ----------
CALENDAR_EVENTS = [
    dict(title="KSU MSW Internship Support (Noon Placement Meeting)", when="Wed, Aug 19 · 12:00 PM ET", iso="2026-08-19T16:00:00", lane="Internship", recurring=True),
    dict(title="Navy Duties — NRC Atlanta", when="Fri, Aug 21 (all day)", iso="2026-08-21T00:00:00", lane="Navy Reserve"),
    dict(title="Drill", when="Sat, Aug 22 (all day)", iso="2026-08-22T00:00:00", lane="Navy Reserve"),
    dict(title="KSU MSW Internship Support (Noon Placement Meeting)", when="Wed, Aug 26 · 12:00 PM ET", iso="2026-08-26T16:00:00", lane="Internship", recurring=True),
    dict(title="Monthly Avengers Assembly (EmpowerMEnt)", when="Tue, Sep 1 · 9:30 AM ET", iso="2026-09-01T13:30:00", lane="Org Ops & Finance"),
    dict(title="KSU MSW Internship Support (Noon Placement Meeting)", when="Wed, Sep 2 · 12:00 PM ET", iso="2026-09-02T16:00:00", lane="Internship", recurring=True),
    dict(title="KSU MSW Internship Support (Noon Placement Meeting)", when="Wed, Sep 9 · 12:00 PM ET", iso="2026-09-09T16:00:00", lane="Internship", recurring=True),
    dict(title="New York trip", when="Sat, Sep 12 (all day)", iso="2026-09-12T00:00:00", lane="Vacation & Travel"),
    dict(title="KSU MSW Internship Support (Noon Placement Meeting)", when="Wed, Sep 16 · 12:00 PM ET", iso="2026-09-16T16:00:00", lane="Internship", recurring=True),
    dict(title="Anniversary", when="Thu, Sep 17 (all day)", iso="2026-09-17T00:00:00", lane="Personal & Home"),
    dict(title="Drill Exam / PFA Make-up", when="Sat, Sep 19 (all day)", iso="2026-09-19T00:00:00", lane="Navy Reserve"),
    dict(title="Stover monthly budget", when="Sat, Sep 19 · 8:00 AM ET", iso="2026-09-19T12:00:00", lane="Personal & Home"),
]

def cal_row(ev):
    color = LANES[ev["lane"]]["color"]
    tag = " · weekly" if ev.get("recurring") else ""
    return f'''<div class="cal-row" data-due="{ev['iso']}">
<span class="event-dot" style="background:{color}"></span>
<div><strong>{esc(ev['title'])}</strong><span>{esc(ev['when'])}{tag} · {esc(ev['lane'])}</span></div>
<span class="soon-badge" hidden>⏳ Coming up</span>
</div>'''

calendar_html = "\n".join(cal_row(e) for e in CALENDAR_EVENTS)

# ---------- Combined notes digest (Pocket + Fireflies; Zoom/Notion/Keep pending) ----------
by_recording = {}
for it in items:
    by_recording.setdefault(it["recordingTitle"], []).append(it)

FIREFLIES_ONLY_SUMMARIES = {
    "Youth Events Planning and Updates Meeting": "Welcomed intern Madison; planned Sept 26 Fun and Learns for Regions 10/12, venue talks, mandatory presenter training, grant data roles.",
    "Prep Session and Event Logistics Meeting": "Finalized Aug 5-6 training prep: mandatory attendance, virtual branding, strategic-sharing safety practices, role assignments.",
    "Leadership Retreat Planning and Guidelines": "Confirmed 12-15 person retreat roster, travel/sleeping logistics, Welcoming Committee, Wix migration off Constant Contact.",
    "Event Planning and Engagement Strategies": "Monday youth event: icebreakers, Jeopardy game, Empower University training, venue/tech/food logistics for 15-18 attendees.",
}

def note_card(title, its):
    src = "fireflies" if any(i.get("source") == "fireflies" for i in its) or title in FIREFLIES_ONLY_SUMMARIES else "pocket"
    lane = its[0]["lane"] if its else "Org Ops & Finance"
    color = LANES.get(lane, {"color": "var(--navy)"})["color"]
    items_html = "".join(f"<li>{esc(i['label'])}</li>" for i in its[:6])
    extra = FIREFLIES_ONLY_SUMMARIES.get(title, "")
    extra_html = f'<p class="note-summary">{esc(extra)}</p>' if extra else ""
    badge = "Fireflies" if src == "fireflies" else "Pocket"
    return f'''<div class="note-card" style="--event:{color}" data-search="{esc((title+" "+extra).lower())}">
<div class="note-card-head"><span class="event-dot" style="background:{color}"></span><strong>{esc(title)}</strong><span class="status">{badge}</span></div>
{extra_html}
<ul>{items_html}</ul>
</div>'''

note_cards = [note_card(title, its) for title, its in by_recording.items()]
for title, summary in FIREFLIES_ONLY_SUMMARIES.items():
    if title not in by_recording:
        note_cards.append(note_card(title, []))

notes_html = "\n".join(note_cards)

out = dict(
    task_rows=task_rows_html,
    dep_rows=dep_rows_html,
    email_cards=email_cards_html,
    materials=materials_html,
    lane_chips=lane_chips_html,
    progress=progress_html,
    calendar=calendar_html,
    notes=notes_html,
    pomo_tasks_json=json.dumps(pomo_tasks),
    total_mine=len(mine),
    total_others=len(others),
    total_emails=len(emails)+len(messages),
    total_materials=len(materials_by_lane),
    overdue_count=sum(1 for it in mine if it["overdue"]),
)

with open("fragments.json", "w") as f:
    json.dump(out, f)

print("mine:", len(mine), "others:", len(others), "emails:", len(emails)+len(messages), "overdue:", out["overdue_count"])
print("lanes:", lane_counts)
