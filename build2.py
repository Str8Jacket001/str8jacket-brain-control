import json

with open("fragments.json") as f:
    frag = json.load(f)

HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#061b4d">
<title>Str8Jacket Brain Control</title>
<style>
:root {{
  --navy: #061b4d; --navy-2: #0b2f76; --cyan: #08bfe6; --yellow: #ffcc19;
  --coral: #ff5f51; --green: #13a76b; --purple: #8b4bd7; --ink: #101b36;
  --muted: #64708b; --line: #dfe5ef; --soft: #f5f8fc; --white: #ffffff;
  --shadow: 0 16px 42px rgba(6,27,77,.13); --radius: 14px;
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0; color: var(--ink); background: #eaf0f8;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 15px;
}}
button, input, select {{ font: inherit; }}
button {{ cursor: pointer; }}
button:focus-visible, input:focus-visible, select:focus-visible {{ outline: 3px solid rgba(8,191,230,.35); outline-offset: 2px; }}
.app-shell {{ width: min(1440px, 100%); min-height: 100vh; margin: 0 auto; background: var(--white); box-shadow: 0 0 70px rgba(6,27,77,.16); }}
.hero {{ position: relative; overflow: hidden; padding: 26px clamp(20px,3vw,48px) 30px; color: white;
  background: radial-gradient(circle at 73% 20%, rgba(8,191,230,.19) 0 4px, transparent 5px), linear-gradient(120deg, var(--navy) 0%, #07163d 68%, #102c67 100%); }}
.hero-grid {{ position: relative; z-index: 1; display: grid; grid-template-columns: minmax(340px,1.2fr) minmax(420px,.9fr); align-items: center; gap: 34px; }}
.brand {{ color: var(--cyan); font-size: 17px; font-weight: 900; letter-spacing: .04em; text-transform: uppercase; }}
h1 {{ max-width: 760px; margin: 5px 0 8px; font-family: Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif; font-size: clamp(38px,5vw,66px); line-height: .96; letter-spacing: .015em; text-transform: uppercase; }}
.hero-copy {{ display: flex; flex-wrap: wrap; gap: 14px; align-items: center; margin: 0; color: var(--yellow); font-weight: 850; font-size: 17px; }}
.hero-copy .owner {{ padding-left: 14px; color: var(--cyan); border-left: 2px solid var(--yellow); text-transform: uppercase; }}
.hero-stats {{ display: grid; grid-template-columns: 138px 1fr; align-items: center; gap: 22px; }}
.overall-ring {{ --pct: 0; display: grid; place-items: center; width: 130px; aspect-ratio: 1; border-radius: 50%;
  background: conic-gradient(var(--yellow) 0 calc(var(--pct) * 1%), var(--cyan) calc(var(--pct) * 1%) calc(var(--pct) * 1% + 4%), rgba(255,255,255,.14) 0);
  box-shadow: inset 0 0 0 11px rgba(0,0,0,.16), 0 10px 30px rgba(0,0,0,.25); }}
.overall-ring::before {{ content: ""; grid-area: 1/1; width: 88px; aspect-ratio: 1; border-radius: 50%; background: var(--navy); }}
.overall-ring strong {{ z-index: 1; grid-area: 1/1; font-family: Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif; font-size: 34px; }}
.stat-title {{ margin: 0 0 12px; font-size: 19px; }}
.stat-grid {{ display: grid; grid-template-columns: repeat(3,1fr); }}
.stat {{ padding: 0 14px; border-left: 1px solid rgba(255,255,255,.24); text-align: center; }}
.stat:first-child {{ padding-left: 0; border-left: 0; }}
.stat strong {{ display: block; color: var(--cyan); font-family: Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif; font-size: 30px; line-height: 1; }}
.stat:nth-child(2) strong {{ color: var(--yellow); }}
.stat:nth-child(3) strong {{ color: var(--coral); }}
.stat span {{ display: block; margin-top: 5px; color: #dce8ff; font-size: 11px; }}
.view-nav {{ display: grid; grid-template-columns: repeat(5, minmax(0,1fr)); background: white; border-bottom: 1px solid var(--line); }}
.view-tab {{ position: relative; display: flex; align-items: center; justify-content: center; gap: 9px; min-height: 62px; padding: 14px; color: var(--navy); background: white; border: 0; font-weight: 900; font-size: 15px; text-transform: uppercase; }}
.view-tab::after {{ content: ""; position: absolute; right: 15%; bottom: -1px; left: 15%; height: 5px; border-radius: 4px 4px 0 0; background: transparent; }}
.view-tab[aria-selected="true"] {{ background: #f9fbfe; }}
.view-tab[aria-selected="true"]::after {{ background: var(--cyan); }}
.nav-count {{ display: inline-grid; place-items: center; min-width: 22px; height: 22px; padding: 0 6px; color: white; background: var(--coral); border-radius: 999px; font-size: 11px; }}
.main {{ padding: 24px clamp(16px,2.7vw,42px) 34px; }}
.view[hidden] {{ display: none !important; }}
.section-head {{ display: flex; align-items: flex-end; justify-content: space-between; gap: 20px; margin-bottom: 18px; flex-wrap: wrap; }}
.section-title {{ margin: 0; padding-left: 13px; border-left: 4px solid var(--cyan); color: var(--navy); font-family: Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif; font-size: clamp(24px,3vw,36px); letter-spacing: .025em; line-height: 1; text-transform: uppercase; }}
.section-subtitle {{ margin: 8px 0 0 17px; color: var(--muted); }}
.as-of {{ color: var(--muted); font-size: 12px; white-space: nowrap; }}
.lane-rail-wrap {{ position: relative; margin-bottom: 18px; }}
.lane-rail {{ position: relative; display: flex; gap: 8px; overflow-x: auto; padding: 0 0 8px; scrollbar-width: thin; }}
.event-filter {{ --event: var(--navy); flex: 0 0 auto; position: relative; display: grid; grid-template-columns: 34px 1fr; gap: 9px; align-items: center; min-width: 168px; min-height: 62px; padding: 10px 12px; color: var(--navy); background: white; border: 1px solid var(--line); border-radius: 10px; text-align: left; transition: transform .15s ease, box-shadow .15s ease; }}
.event-filter:hover {{ transform: translateY(-2px); box-shadow: 0 8px 18px rgba(6,27,77,.1); }}
.event-filter[aria-pressed="true"] {{ color: white; background: var(--event); border-color: var(--event); box-shadow: 0 10px 20px rgba(6,27,77,.18); }}
.event-icon {{ display: grid; place-items: center; width: 32px; height: 32px; color: white; background: var(--event); border-radius: 50%; font-size: 10px; }}
.event-filter[aria-pressed="true"] .event-icon {{ background: rgba(255,255,255,.22); }}
.event-filter strong {{ display: block; line-height: 1.15; font-size: 13px; }}
.event-filter small {{ display: block; margin-top: 3px; color: var(--muted); font-size: 10px; }}
.event-filter[aria-pressed="true"] small {{ color: #dce8ff; }}
.toolbar {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 16px; }}
.phase-group {{ display: inline-flex; padding: 3px; background: var(--soft); border: 1px solid var(--line); border-radius: 8px; }}
.phase-btn {{ padding: 7px 13px; color: var(--navy); background: transparent; border: 0; border-radius: 5px; font-weight: 800; font-size: 13px; }}
.phase-btn[aria-pressed="true"] {{ color: white; background: var(--navy); }}
.field {{ min-height: 38px; padding: 7px 11px; color: var(--ink); background: white; border: 1px solid #cfd7e5; border-radius: 7px; font-size: 13px; }}
.search-wrap {{ position: relative; min-width: 200px; flex: 1 1 220px; }}
.search-wrap input {{ width: 100%; }}
.toolbar-spacer {{ flex: 1 1 20px; }}
.action-btn {{ display: inline-flex; align-items: center; justify-content: center; gap: 7px; min-height: 38px; padding: 8px 14px; color: white; background: var(--navy); border: 1px solid var(--navy); border-radius: 7px 7px 2px 7px; font-weight: 850; font-size: 13px; box-shadow: 0 5px 12px rgba(6,27,77,.12); }}
.action-btn:hover {{ background: var(--navy-2); }}
.action-btn.secondary {{ color: var(--navy); background: white; border-color: var(--cyan); box-shadow: none; }}
.task-layout {{ display: grid; grid-template-columns: minmax(0,1fr) 270px; gap: 22px; align-items: start; }}
.table-wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; background: white; }}
table {{ width: 100%; border-collapse: collapse; }}
th {{ padding: 11px 10px; color: var(--navy); background: #f7f9fc; border-bottom: 1px solid var(--line); font-size: 10px; letter-spacing: .04em; text-align: left; text-transform: uppercase; white-space: nowrap; }}
td {{ padding: 10px; border-bottom: 1px solid #e8edf4; vertical-align: top; font-size: 13px; }}
tr:last-child td {{ border-bottom: 0; }}
.task-row {{ transition: background .15s ease, opacity .15s ease; }}
.task-row:hover {{ background: #fbfdff; }}
.task-row:has(.check:checked) {{ opacity: .5; }}
.task-row:has(.check:checked) .task-name {{ text-decoration: line-through; }}
.task-row[data-local-hidden="true"] {{ display: none; }}
.check {{ width: 19px; height: 19px; margin: 0; accent-color: var(--green); cursor: pointer; }}
.task-number {{ display: inline-block; min-width: 22px; color: var(--muted); font-variant-numeric: tabular-nums; font-size: 12px; }}
.task-name {{ color: var(--ink); font-weight: 700; line-height: 1.25; }}
.task-detail {{ margin-top: 4px; color: var(--muted); font-size: 11px; line-height: 1.3; }}
.event-dot {{ display: inline-block; width: 8px; height: 8px; margin-right: 6px; border-radius: 50%; }}
.priority {{ display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; font-size: 12px; }}
.priority::before {{ content: ""; width: 0; height: 0; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-left: 8px solid var(--flag); }}
.priority.high {{ --flag: #ee3d42; }}
.priority.medium {{ --flag: #f28b00; }}
.priority.low {{ --flag: var(--green); }}
.date {{ white-space: nowrap; font-variant-numeric: tabular-nums; font-size: 12px; }}
.date.urgent {{ color: #d73f3f; font-weight: 800; }}
.empty-state {{ padding: 44px 20px; color: var(--muted); text-align: center; }}
.side-panel {{ padding: 15px; border: 1px solid var(--line); border-radius: 10px; background: #fbfcfe; }}
.side-panel + .side-panel {{ margin-top: 14px; }}
.side-panel h3 {{ margin: 0 0 13px; color: var(--navy); font-size: 12px; letter-spacing: .04em; text-transform: uppercase; }}
.event-progress-item {{ padding: 9px 0; border-top: 1px solid var(--line); }}
.event-progress-item:first-of-type {{ border-top: 0; padding-top: 0; }}
.progress-row {{ display: flex; justify-content: space-between; gap: 10px; align-items: baseline; }}
.progress-row strong {{ font-size: 11.5px; }}
.progress-row span {{ color: var(--muted); font-size: 11px; }}
.bar {{ height: 6px; margin-top: 7px; overflow: hidden; background: #e4e9f1; border-radius: 999px; }}
.bar > span {{ display: block; height: 100%; width: var(--w); background: var(--event); border-radius: inherit; transition: width .35s ease; }}
.legend-row {{ display: flex; align-items: center; gap: 8px; margin: 8px 0; color: var(--muted); font-size: 12px; }}
.legend-row .priority {{ color: var(--ink); font-weight: 800; min-width: 66px; }}
.dependency-layout {{ display: grid; grid-template-columns: minmax(0,1fr); gap: 22px; }}
.dep-person {{ font-weight: 800; font-size: 13px; }}
.person-mark {{ display: inline-grid; place-items: center; width: 26px; height: 26px; margin-right: 7px; color: white; background: var(--cyan); border-radius: 50%; font-size: 11px; font-weight: 900; }}
.status {{ display: inline-block; padding: 4px 8px; color: #0a75a0; background: #e1f6fc; border: 1px solid #9ee2f2; border-radius: 4px; font-size: 10px; font-weight: 900; letter-spacing: .04em; text-transform: uppercase; white-space: nowrap; }}
.status.received {{ color: #087245; background: #e4f8ef; border-color: #9edcc2; }}
tr:has(.received-check:checked) .status {{ color: #087245; background: #e4f8ef; border-color: #9edcc2; }}
tr:has(.received-check:checked) .status::before {{ content: "Received"; }}
tr:has(.received-check:not(:checked)) .status::before {{ content: "Waiting"; }}
.status-text {{ display: none; }}
.received-check {{ width: 18px; height: 18px; margin-right: 8px; vertical-align: middle; accent-color: var(--green); cursor: pointer; }}
.email-panel-list {{ display: grid; gap: 9px; }}
.email-row {{ display: grid; grid-template-columns: auto 1fr; gap: 10px; align-items: start; padding: 12px; background: white; border: 1px solid var(--line); border-radius: 8px; }}
.email-row[data-local-hidden="true"] {{ display: none; }}
.email-row strong {{ display: block; color: var(--navy); font-size: 13px; }}
.email-row span {{ display: block; margin-top: 3px; color: var(--muted); font-size: 12px; line-height: 1.3; }}
.email-row:has(.sent-check:checked) {{ opacity: .5; }}
.email-row:has(.sent-check:checked) strong {{ text-decoration: line-through; }}
.sent-check {{ width: 19px; height: 19px; margin-top: 2px; accent-color: var(--green); cursor: pointer; }}
.cal-list {{ display: grid; gap: 8px; }}
.cal-row {{ display: grid; grid-template-columns: auto 1fr; gap: 10px; align-items: start; padding: 11px 12px; background: white; border: 1px solid var(--line); border-radius: 8px; }}
.cal-row .event-dot {{ margin-top: 5px; }}
.cal-row strong {{ display: block; color: var(--navy); font-size: 13px; }}
.cal-row span {{ display: block; margin-top: 3px; color: var(--muted); font-size: 12px; }}
.notes-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr)); gap: 14px; }}
.note-card {{ --event: var(--navy); padding: 13px 14px; background: white; border: 1px solid var(--line); border-left: 4px solid var(--event); border-radius: 8px; }}
.note-card[data-local-hidden="true"] {{ display: none; }}
.note-card-head {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }}
.note-card-head strong {{ flex: 1; color: var(--navy); font-size: 13px; line-height: 1.25; }}
.note-summary {{ margin: 0 0 8px; color: var(--muted); font-size: 12px; line-height: 1.4; }}
.note-card ul {{ margin: 0; padding-left: 18px; color: var(--ink); font-size: 12px; line-height: 1.5; }}
.notes-legend {{ display: flex; gap: 14px; margin-bottom: 14px; color: var(--muted); font-size: 12px; flex-wrap: wrap; }}
.event-progress-item[role="button"] {{ cursor: pointer; border-radius: 7px; padding-left: 6px; padding-right: 6px; margin: 0 -6px; transition: background .12s ease; }}
.event-progress-item[role="button"]:hover {{ background: #eef4fb; }}
.event-progress-item[aria-pressed="true"] {{ background: #e8f0fb; box-shadow: inset 3px 0 var(--event); }}
.type-jump {{ display: inline-flex; align-items: center; gap: 4px; padding: 5px 9px; color: var(--navy); background: #eefbfe; border: 1px solid #b8eaf3; border-radius: 5px; font-size: 11px; font-weight: 800; white-space: nowrap; text-decoration: none; }}
.type-jump:hover {{ background: #dcf3fb; }}
.soon-badge {{ display: inline-block; margin-top: 4px; padding: 2px 7px; color: #8a5b00; background: #fff2cf; border: 1px solid #f0cf82; border-radius: 999px; font-size: 10px; font-weight: 800; white-space: nowrap; }}
.task-row.is-soon {{ box-shadow: inset 3px 0 var(--yellow); }}
.cal-row.is-soon {{ box-shadow: inset 3px 0 var(--yellow); }}
.email-panel-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px,1fr)); gap: 14px; align-items: start; }}
.email-card {{ --event: var(--navy); padding: 14px; background: white; border: 1px solid var(--line); border-left: 4px solid var(--event); border-radius: 10px; }}
.email-card[data-local-hidden="true"] {{ display: none; }}
.email-card-head {{ display: flex; align-items: center; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; }}
.email-card-head strong {{ flex: 1; color: var(--navy); font-size: 13px; line-height: 1.25; min-width: 120px; }}
.kind-badge {{ padding: 2px 7px; color: var(--navy); background: var(--soft); border: 1px solid var(--line); border-radius: 999px; font-size: 10px; font-weight: 800; text-transform: uppercase; }}
.sent-toggle {{ display: flex; align-items: center; gap: 5px; color: var(--muted); font-size: 11px; font-weight: 800; text-transform: uppercase; cursor: pointer; }}
.sent-toggle input {{ width: 16px; height: 16px; accent-color: var(--green); cursor: pointer; }}
.email-card:has(.sent-check:checked) {{ opacity: .55; }}
.email-field {{ margin-bottom: 9px; }}
.email-field label {{ display: block; margin-bottom: 3px; color: var(--navy); font-size: 10px; font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }}
.email-field .field {{ width: 100%; }}
.email-body {{ min-height: 90px; line-height: 1.4; font-size: 12px; white-space: pre-wrap; }}
.email-body:empty::before {{ content: attr(data-placeholder); color: var(--muted); }}
.email-actions {{ margin-top: 6px; }}
.materials-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px,1fr)); gap: 16px; }}
.material-card {{ --material: var(--navy); overflow: hidden; border: 1px solid var(--line); border-radius: 10px 10px 3px 10px; background: white; box-shadow: 0 8px 20px rgba(6,27,77,.06); }}
.material-card[data-local-hidden="true"] {{ display: none; }}
.material-preview {{ position: relative; overflow: hidden; padding: 20px; color: white; background: linear-gradient(150deg, var(--navy) 0 60%, color-mix(in srgb, var(--material) 82%, #000) 60% 100%); }}
.material-brand {{ display: block; color: var(--cyan); font-size: 11px; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; }}
.material-headline {{ margin: 10px 0 6px; font-family: Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif; font-size: 26px; line-height: 1; letter-spacing: .01em; outline: none; }}
.material-subhead {{ margin: 0 0 12px; color: var(--yellow); font-size: 12px; font-weight: 800; outline: none; }}
.material-body {{ margin: 0; color: #e6eeff; font-size: 12px; line-height: 1.6; white-space: pre-wrap; outline: none; min-height: 60px; }}
.material-actions {{ padding: 10px 14px; }}
.focus-launch {{ position: fixed; z-index: 88; right: 20px; bottom: 20px; display: flex; align-items: center; gap: 10px; padding: 10px 15px 10px 10px; color: white; background: var(--navy); border: 2px solid var(--cyan); border-radius: 999px; box-shadow: 0 14px 32px rgba(6,27,77,.28); font-weight: 900; }}
.focus-launch:hover {{ background: var(--navy-2); }}
.focus-launch-icon {{ display: grid; place-items: center; width: 30px; height: 30px; color: var(--navy); background: var(--yellow); border-radius: 50%; font-size: 15px; }}
.focus-backdrop {{ position: fixed; z-index: 109; inset: 0; background: rgba(6,20,52,.5); opacity: 0; pointer-events: none; transition: opacity .2s ease; }}
.focus-backdrop.open {{ opacity: 1; pointer-events: auto; }}
.focus-panel {{ position: fixed; z-index: 110; top: 0; right: 0; bottom: 0; width: min(400px,100vw); overflow-y: auto; color: var(--ink); background: white; box-shadow: -18px 0 50px rgba(6,27,77,.24); transform: translateX(105%); transition: transform .25s ease; }}
.focus-panel.open {{ transform: translateX(0); }}
.focus-head {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 18px 20px; color: white; background: var(--navy); }}
.focus-head h2 {{ margin: 0; font-family: Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif; font-size: 24px; letter-spacing: .02em; text-transform: uppercase; }}
.focus-head p {{ margin: 3px 0 0; color: var(--cyan); font-size: 11px; font-weight: 800; }}
.focus-close {{ width: 32px; height: 32px; color: white; background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.3); border-radius: 50%; font-size: 20px; line-height: 1; }}
.focus-content {{ padding: 18px 20px 26px; }}
.pomo-modes {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 6px; }}
.pomo-mode {{ min-height: 38px; padding: 7px; color: var(--navy); background: var(--soft); border: 1px solid var(--line); border-radius: 7px; font-size: 11px; font-weight: 900; }}
.pomo-mode[aria-pressed="true"] {{ color: white; background: var(--navy); border-color: var(--navy); }}
.timer-ring {{ --timer-pct: 0; display: grid; place-items: center; width: 200px; aspect-ratio: 1; margin: 22px auto 16px; border-radius: 50%; background: conic-gradient(var(--cyan) calc(var(--timer-pct)*1%), #e8edf5 0); }}
.timer-ring::before {{ content: ""; grid-area: 1/1; width: 172px; aspect-ratio: 1; background: white; border-radius: 50%; }}
.timer-display {{ z-index: 1; grid-area: 1/1; text-align: center; }}
.timer-display strong {{ display: block; color: var(--navy); font-family: Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif; font-size: 48px; line-height: 1; font-variant-numeric: tabular-nums; }}
.timer-display span {{ display: block; margin-top: 6px; color: var(--muted); font-size: 10px; font-weight: 900; letter-spacing: .07em; text-transform: uppercase; }}
.focus-task-box {{ margin: 14px 0; padding: 12px; background: #f7fafd; border: 1px solid var(--line); border-left: 4px solid var(--yellow); border-radius: 8px; }}
.focus-task-box label {{ display: block; margin-bottom: 6px; color: var(--navy); font-size: 10px; font-weight: 900; letter-spacing: .05em; text-transform: uppercase; }}
.focus-task-box select {{ width: 100%; }}
.focus-controls {{ display: grid; grid-template-columns: 1.3fr 1fr 1fr; gap: 8px; }}
.pomo-stats {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 7px; margin: 16px 0; }}
.pomo-stat {{ padding: 10px 6px; background: var(--navy); border-radius: 7px 7px 2px 7px; color: white; text-align: center; }}
.pomo-stat strong {{ display: block; color: var(--yellow); font-family: Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif; font-size: 22px; }}
.pomo-stat span {{ display: block; margin-top: 2px; color: #dce8ff; font-size: 9px; text-transform: uppercase; }}
.focus-empty {{ padding: 14px; color: var(--muted); background: var(--soft); border-radius: 7px; text-align: center; font-size: 11px; }}
.footer {{ display: flex; justify-content: space-between; gap: 20px; padding: 15px clamp(20px,3vw,48px); color: #dce8ff; background: var(--navy); font-size: 11px; flex-wrap: wrap; }}
.footer strong {{ color: var(--yellow); }}
.banner {{ display: flex; align-items: center; justify-content: space-between; gap: 14px; margin: 0 0 18px; padding: 11px 15px; background: #eefbfe; border: 1px solid #b8eaf3; border-radius: 8px; color: var(--navy); font-size: 12px; flex-wrap: wrap; }}
.banner strong {{ color: var(--navy); }}
[artifact-sync-state="off"] {{ outline: 2px dashed var(--coral); }}
@media (max-width: 1080px) {{
  .hero-grid {{ grid-template-columns: 1fr; }}
  .task-layout {{ grid-template-columns: 1fr; }}
  .task-side {{ display: grid; grid-template-columns: repeat(2,1fr); gap: 14px; }}
  .side-panel + .side-panel {{ margin-top: 0; }}
}}
@media (max-width: 720px) {{
  .hero-stats {{ grid-template-columns: 92px 1fr; }}
  .overall-ring {{ width: 92px; }}
  .overall-ring::before {{ width: 62px; }}
  .view-tab {{ font-size: 11px; padding: 10px 6px; }}
  .task-side {{ grid-template-columns: 1fr; }}
  .table-wrap {{ border: 0; overflow: visible; }}
  table thead {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }}
  table, tbody, tr, td {{ display: block; width: 100%; }}
  tr {{ position: relative; margin: 0 0 10px; padding: 10px 10px 10px 42px; border: 1px solid var(--line); border-left: 5px solid var(--event-color, var(--cyan)); border-radius: 8px; }}
  td {{ padding: 3px 0; border: 0; }}
  td:first-child {{ position: absolute; top: 12px; left: 10px; }}
  td::before {{ content: attr(data-label); display: inline-block; min-width: 70px; margin-right: 6px; color: var(--muted); font-size: 9px; font-weight: 800; text-transform: uppercase; }}
  td:nth-child(2)::before {{ display: none; }}
}}
</style>
</head>
<body>
<div class="app-shell">
  <header class="hero">
    <div class="hero-grid">
      <div>
        <div class="brand">Str8Jacket Brain Control</div>
        <h1>Mission Control</h1>
        <p class="hero-copy"><span>Synced from Pocket &amp; Fireflies notes.</span><span class="owner">Anthony Stover</span></p>
      </div>
      <div class="hero-stats" aria-label="Overall task progress">
        <div class="overall-ring" id="overallRing"><strong id="overallPct">0%</strong></div>
        <div>
          <h2 class="stat-title">Overall Progress</h2>
          <div class="stat-grid">
            <div class="stat"><strong id="totalTasks">{frag['total_mine']}</strong><span>Total Tasks</span></div>
            <div class="stat"><strong id="doneTasks">0</strong><span>Completed</span></div>
            <div class="stat"><strong id="overdueTasks">{frag['overdue_count']}</strong><span>Overdue</span></div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <nav class="view-nav" role="tablist" aria-label="Mission control views">
    <button class="view-tab" id="tab-my" data-view="my" role="tab" aria-selected="true">My Tasks <span class="nav-count">{frag['total_mine']}</span></button>
    <button class="view-tab" id="tab-others" data-view="others" role="tab" aria-selected="false">Waiting on Others <span class="nav-count">{frag['total_others']}</span></button>
    <button class="view-tab" id="tab-emails" data-view="emails" role="tab" aria-selected="false">Follow-ups &amp; Emails <span class="nav-count">{frag['total_emails']}</span></button>
    <button class="view-tab" id="tab-materials" data-view="materials" role="tab" aria-selected="false">Draft Materials <span class="nav-count">{frag['total_materials']}</span></button>
    <button class="view-tab" id="tab-calendar" data-view="calendar" role="tab" aria-selected="false">Calendar</button>
    <button class="view-tab" id="tab-notes" data-view="notes" role="tab" aria-selected="false">All Notes</button>
  </nav>

  <main class="main">
    <div class="banner">
      <span>⏱ Auto-refreshes hourly from Pocket + Fireflies (platform minimum interval). <span id="lastSynced">Last synced: just now</span>.</span>
      <button class="action-btn secondary" id="refreshBtn">↻ Refresh now</button>
    </div>

    <section class="view" id="view-my" role="tabpanel">
      <div class="section-head">
        <div>
          <h2 class="section-title">What Needs To Happen</h2>
          <p class="section-subtitle">Check it off as you go. Everything here came straight from a real note.</p>
        </div>
        <span class="as-of">Built from Pocket action items • Fireflies pending • Zoom needs reconnect</span>
      </div>

      <div class="lane-rail-wrap"><div class="lane-rail" id="laneRail">
{frag['lane_chips']}
      </div></div>

      <div class="toolbar">
        <div class="phase-group" aria-label="Priority filter">
          <button class="phase-btn priority-btn" data-priority="all" aria-pressed="true">All</button>
          <button class="phase-btn priority-btn" data-priority="high" aria-pressed="false">High</button>
          <button class="phase-btn priority-btn" data-priority="medium" aria-pressed="false">Medium</button>
          <button class="phase-btn priority-btn" data-priority="low" aria-pressed="false">Low</button>
        </div>
        <div class="phase-group" aria-label="Top vs all">
          <button class="phase-btn top-btn" data-top="top" aria-pressed="true">Top 20</button>
          <button class="phase-btn top-btn" data-top="all" aria-pressed="false">All {frag['total_mine']}</button>
        </div>
        <label class="search-wrap">
          <input class="field" id="taskSearch" type="search" placeholder="Search tasks…">
        </label>
        <div class="toolbar-spacer"></div>
        <button class="action-btn secondary" id="showDoneBtn" aria-pressed="false">Hide completed</button>
      </div>

      <div class="task-layout">
        <div class="table-wrap">
          <table>
            <thead><tr><th></th><th>Task</th><th>Priority</th><th>Owner</th><th>Due</th><th>Type</th><th>Lane</th></tr></thead>
            <tbody id="taskBody" artifact-sync>
{frag['task_rows']}
            </tbody>
          </table>
          <div class="empty-state" id="taskEmpty" hidden>No tasks match those filters.</div>
        </div>
        <aside class="task-side">
          <div class="side-panel">
            <h3>Progress by Lane</h3>
            <div id="eventProgress">
{frag['progress']}
            </div>
          </div>
          <div class="side-panel">
            <h3>Priority Key</h3>
            <div class="legend-row"><span class="priority high">High</span><span>Deadline or critical path</span></div>
            <div class="legend-row"><span class="priority medium">Medium</span><span>Needs movement this cycle</span></div>
            <div class="legend-row"><span class="priority low">Low</span><span>Planned after blockers clear</span></div>
          </div>
        </aside>
      </div>
    </section>

    <section class="view" id="view-others" role="tabpanel" hidden>
      <div class="section-head">
        <div>
          <h2 class="section-title">What Is Blocking You</h2>
          <p class="section-subtitle">These deliverables belong to other people, but affect your work. Check "Received" once they deliver.</p>
        </div>
      </div>
      <div class="dependency-layout">
        <div class="table-wrap">
          <table>
            <thead><tr><th>Person</th><th>Contact</th><th>Deliverable</th><th>Due</th><th>Blocks</th><th>Status</th></tr></thead>
            <tbody id="dependencyBody" artifact-sync>
{frag['dep_rows']}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="view" id="view-emails" role="tabpanel" hidden>
      <div class="section-head">
        <div>
          <h2 class="section-title">Follow-ups &amp; Email Drafts</h2>
          <p class="section-subtitle">Edit To / Subject / Body right here — it saves as you type. Check "Sent" once it's out the door.</p>
        </div>
        <label class="search-wrap"><input class="field" id="emailSearch" type="search" placeholder="Search drafts…"></label>
      </div>
      <div class="email-panel-list" id="emailList" artifact-sync>
{frag['email_cards']}
      </div>
    </section>

    <section class="view" id="view-materials" role="tabpanel" hidden>
      <div class="section-head">
        <div>
          <h2 class="section-title">Draft Materials</h2>
          <p class="section-subtitle">One editable brief per lane, built from the real open tasks in it. Edit headline/subhead/body inline.</p>
        </div>
        <label class="search-wrap"><input class="field" id="materialSearch" type="search" placeholder="Search materials…"></label>
      </div>
      <div class="materials-grid" id="materialsGrid" artifact-sync>
{frag['materials']}
      </div>
    </section>

    <section class="view" id="view-calendar" role="tabpanel" hidden>
      <div class="section-head">
        <div>
          <h2 class="section-title">Upcoming Appointments</h2>
          <p class="section-subtitle">Pulled from Google Calendar (primary calendar, next ~5 weeks). Read-only — edit in Google Calendar directly.</p>
        </div>
      </div>
      <div class="cal-list">
{frag['calendar']}
      </div>
    </section>

    <section class="view" id="view-notes" role="tabpanel" hidden>
      <div class="section-head">
        <div>
          <h2 class="section-title">All Notes, Combined</h2>
          <p class="section-subtitle">Every source meeting/note, matched by title where they overlap.</p>
        </div>
        <label class="search-wrap"><input class="field" id="notesSearch" type="search" placeholder="Search notes…"></label>
      </div>
      <div class="notes-legend">
        <span>✅ Pocket &amp; Fireflies — live</span>
        <span>⏳ Zoom — token expired, needs reconnect</span>
        <span>⏳ Notion — connected, nothing relevant found yet</span>
        <span>✕ Google Keep — not connected</span>
      </div>
      <div class="notes-grid" id="notesGrid">
{frag['notes']}
      </div>
    </section>
  </main>

  <footer class="footer">
    <span>Sources: <strong>Pocket</strong> (49 action items) · <strong>Fireflies</strong> (22 transcripts scanned) · <strong>Zoom</strong> needs reconnect in claude.ai connector settings</span>
    <span>Str8Jacket Brain Control</span>
  </footer>
</div>

<button class="focus-launch" id="focusLaunch" aria-controls="focusPanel" aria-expanded="false">
  <span class="focus-launch-icon" aria-hidden="true">⏱</span>
  <span><span id="focusMiniTime">25:00</span></span>
</button>
<div class="focus-backdrop" id="focusBackdrop"></div>
<aside class="focus-panel" id="focusPanel" role="dialog" aria-modal="true" aria-hidden="true">
  <div class="focus-head">
    <div><h2>Focus Station</h2><p>One task. One timer.</p></div>
    <button class="focus-close" id="focusClose" aria-label="Close focus timer">×</button>
  </div>
  <div class="focus-content">
    <div class="pomo-modes">
      <button class="pomo-mode" data-pomo-mode="focus" aria-pressed="true">Focus • 25</button>
      <button class="pomo-mode" data-pomo-mode="short" aria-pressed="false">Short • 5</button>
      <button class="pomo-mode" data-pomo-mode="long" aria-pressed="false">Long • 15</button>
    </div>
    <div class="timer-ring" id="timerRing"><div class="timer-display"><strong id="timerText">25:00</strong><span id="timerModeLabel">Focus Session</span></div></div>
    <div class="focus-task-box">
      <label for="focusTaskSelect">Task for this session</label>
      <select class="field" id="focusTaskSelect"></select>
    </div>
    <div class="focus-controls">
      <button class="action-btn" id="timerStart">Start Focus</button>
      <button class="action-btn secondary" id="timerReset">Reset</button>
      <button class="action-btn secondary" id="timerSkip">Skip</button>
    </div>
    <button class="action-btn secondary" style="width:100%;margin-top:10px" id="completeFocusTask">Check off this task</button>
    <div class="pomo-stats">
      <div class="pomo-stat"><strong id="pomoSessionCount">0</strong><span>Sessions</span></div>
      <div class="pomo-stat"><strong id="pomoMinuteCount">0</strong><span>Minutes</span></div>
      <div class="pomo-stat"><strong id="pomoCycleCount">0/4</strong><span>Cycle</span></div>
    </div>
  </div>
</aside>

<script>window.__POMO_TASKS__ = {frag['pomo_tasks_json']};</script>
<script>
(function () {{
  var taskBody = document.getElementById('taskBody');
  var rows = function() {{ return Array.prototype.slice.call(taskBody.querySelectorAll('.task-row')); }};

  function recompute() {{
    var all = rows();
    var total = all.length;
    var done = all.filter(function(r) {{ return r.querySelector('.check').checked; }}).length;
    var overdue = all.filter(function(r) {{
      return !r.querySelector('.check').checked && r.querySelector('.date.urgent');
    }}).length;
    document.getElementById('totalTasks').textContent = total;
    document.getElementById('doneTasks').textContent = done;
    document.getElementById('overdueTasks').textContent = overdue;
    var pct = total ? Math.round(done / total * 100) : 0;
    document.getElementById('overallPct').textContent = pct + '%';
    document.getElementById('overallRing').style.setProperty('--pct', pct);

    var laneCounts = {{}}, laneDone = {{}};
    all.forEach(function(r) {{
      var lane = r.dataset.lane;
      laneCounts[lane] = (laneCounts[lane]||0) + 1;
      if (r.querySelector('.check').checked) laneDone[lane] = (laneDone[lane]||0) + 1;
    }});
    document.querySelectorAll('[data-lane-progress]').forEach(function(el) {{
      var lane = el.dataset.laneProgress;
      var c = laneCounts[lane] || 0, d = laneDone[lane] || 0;
      var pctL = c ? Math.round(d/c*100) : 0;
      el.querySelector('.lp-done').textContent = d;
      el.querySelector('.bar > span').style.setProperty('--w', pctL + '%');
    }});
  }}

  function applyFilters() {{
    var lane = document.querySelector('.lane-filter[aria-pressed="true"]');
    var laneVal = lane ? lane.dataset.lane : null;
    var priority = document.querySelector('.priority-btn[aria-pressed="true"]').dataset.priority;
    var topOnly = document.querySelector('.top-btn[aria-pressed="true"]').dataset.top === 'top';
    var q = document.getElementById('taskSearch').value.trim().toLowerCase();
    var hideDone = document.getElementById('showDoneBtn').getAttribute('aria-pressed') === 'true';
    var any = false;
    rows().forEach(function(r) {{
      var ok = true;
      if (laneVal && r.dataset.lane !== laneVal) ok = false;
      if (priority !== 'all' && r.dataset.priority !== priority) ok = false;
      if (topOnly && r.dataset.top !== '1') ok = false;
      if (q && r.dataset.search.indexOf(q) === -1) ok = false;
      if (hideDone && r.querySelector('.check').checked) ok = false;
      r.dataset.localHidden = ok ? 'false' : 'true';
      if (ok) any = true;
    }});
    document.getElementById('taskEmpty').hidden = any;
  }}

  taskBody.addEventListener('change', function(e) {{
    if (e.target.classList.contains('check')) recompute();
  }});
  taskBody.addEventListener('claude:edit', recompute);

  document.getElementById('laneRail').addEventListener('click', function(e) {{
    var btn = e.target.closest('.lane-filter');
    if (!btn) return;
    var wasOn = btn.getAttribute('aria-pressed') === 'true';
    document.querySelectorAll('.lane-filter').forEach(function(b) {{ b.setAttribute('aria-pressed', 'false'); }});
    if (!wasOn) btn.setAttribute('aria-pressed', 'true');
    applyFilters();
  }});
  document.querySelectorAll('.priority-btn').forEach(function(b) {{
    b.addEventListener('click', function() {{
      document.querySelectorAll('.priority-btn').forEach(function(x) {{ x.setAttribute('aria-pressed', 'false'); }});
      b.setAttribute('aria-pressed', 'true');
      applyFilters();
    }});
  }});
  document.querySelectorAll('.top-btn').forEach(function(b) {{
    b.addEventListener('click', function() {{
      document.querySelectorAll('.top-btn').forEach(function(x) {{ x.setAttribute('aria-pressed', 'false'); }});
      b.setAttribute('aria-pressed', 'true');
      applyFilters();
    }});
  }});
  document.getElementById('taskSearch').addEventListener('input', applyFilters);
  document.getElementById('showDoneBtn').addEventListener('click', function() {{
    var on = this.getAttribute('aria-pressed') === 'true';
    this.setAttribute('aria-pressed', on ? 'false' : 'true');
    this.textContent = on ? 'Hide completed' : 'Show completed';
    applyFilters();
  }});

  function wireSearch(inputId, cardSelector) {{
    var input = document.getElementById(inputId);
    if (!input) return;
    input.addEventListener('input', function() {{
      var q = input.value.trim().toLowerCase();
      document.querySelectorAll(cardSelector).forEach(function(card) {{
        card.dataset.localHidden = (!q || card.dataset.search.indexOf(q) !== -1) ? 'false' : 'true';
      }});
    }});
  }}
  wireSearch('notesSearch', '.note-card');
  wireSearch('emailSearch', '.email-card');
  wireSearch('materialSearch', '.material-card');

  document.getElementById('refreshBtn').addEventListener('click', function() {{
    alert('This button flags the refresh for Claude to pick up. Automatic hourly refreshes already keep this page current — ask Claude in your session for an instant one if you need it sooner.');
  }});

  // ---- Clickable "Progress by Lane" side panel: syncs with the lane rail filter ----
  document.getElementById('eventProgress').addEventListener('click', function(e) {{
    var item = e.target.closest('[data-lane-progress]');
    if (!item) return;
    activateLane(item.dataset.laneProgress);
  }});
  document.getElementById('eventProgress').addEventListener('keydown', function(e) {{
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var item = e.target.closest('[data-lane-progress]');
    if (!item) return;
    e.preventDefault();
    activateLane(item.dataset.laneProgress);
  }});
  function activateLane(lane) {{
    var chip = document.querySelector('.lane-filter[data-lane="' + CSS.escape(lane) + '"]');
    var wasOn = chip && chip.getAttribute('aria-pressed') === 'true';
    document.querySelectorAll('.lane-filter').forEach(function(b) {{ b.setAttribute('aria-pressed', 'false'); }});
    if (chip && !wasOn) chip.setAttribute('aria-pressed', 'true');
    document.querySelectorAll('[data-lane-progress]').forEach(function(el) {{
      el.setAttribute('aria-pressed', String(el.dataset.laneProgress === lane && !wasOn));
    }});
    applyFilters();
    setView('my');
  }}

  // ---- Tab switching + jump-to helper ----
  function setView(view) {{
    document.querySelectorAll('.view-tab').forEach(function(t) {{ t.setAttribute('aria-selected', String(t.dataset.view === view)); }});
    document.querySelectorAll('.view').forEach(function(v) {{ v.hidden = (v.id !== 'view-' + view); }});
  }}
  document.querySelectorAll('.view-tab').forEach(function(tab) {{
    tab.addEventListener('click', function() {{ setView(tab.dataset.view); }});
  }});

  // ---- "Type" jump: click a Draft Email / Send Message badge to jump straight to that draft ----
  document.getElementById('taskBody').addEventListener('click', function(e) {{
    var btn = e.target.closest('.type-jump[data-jump-tab]');
    if (!btn) return;
    setView(btn.dataset.jumpTab);
    var target = document.getElementById('email-' + btn.dataset.jumpTarget);
    if (target) {{
      target.dataset.localHidden = 'false';
      var search = document.getElementById('emailSearch'); if (search) search.value = '';
      document.querySelectorAll('.email-card').forEach(function(c) {{ c.dataset.localHidden = 'false'; }});
      target.scrollIntoView({{behavior: 'smooth', block: 'center'}});
      target.animate([{{boxShadow: '0 0 0 4px rgba(8,191,230,.55)'}}, {{boxShadow: '0 0 0 0 rgba(8,191,230,0)'}}], {{duration: 1200}});
    }}
  }});

  // ---- Coming-up highlight: computed fresh on every load, never synced ----
  var SOON_DAYS = 14;
  function markSoon(el) {{
    var iso = el.dataset.due;
    if (!iso) return;
    var due = new Date(iso);
    var now = new Date();
    var diffDays = (due - now) / 86400000;
    var badge = el.querySelector('.soon-badge');
    if (diffDays >= 0 && diffDays <= SOON_DAYS) {{
      el.classList.add('is-soon');
      if (badge) {{ badge.hidden = false; badge.textContent = '⏳ ' + Math.ceil(diffDays) + 'd out'; }}
    }}
  }}
  document.querySelectorAll('.task-row[data-due]').forEach(markSoon);
  document.querySelectorAll('.cal-row[data-due]').forEach(markSoon);

  // ---- Copy buttons (email + material) ----
  function copyText(text, btn) {{
    var done = function() {{ var old = btn.textContent; btn.textContent = 'Copied ✓'; setTimeout(function() {{ btn.textContent = old; }}, 1500); }};
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done); else done();
  }}
  document.getElementById('emailList').addEventListener('click', function(e) {{
    var btn = e.target.closest('.copy-email-btn');
    if (!btn) return;
    var card = btn.closest('.email-card');
    var to = card.querySelector('.email-to').value;
    var subj = card.querySelector('.email-subject').value;
    var body = card.querySelector('.email-body').innerText;
    copyText('To: ' + to + '\\nSubject: ' + subj + '\\n\\n' + body, btn);
  }});
  document.getElementById('materialsGrid').addEventListener('click', function(e) {{
    var btn = e.target.closest('.copy-material-btn');
    if (!btn) return;
    var card = btn.closest('.material-card');
    var text = card.querySelector('.material-headline').innerText + '\\n' + card.querySelector('.material-subhead').innerText + '\\n\\n' + card.querySelector('.material-body').innerText;
    copyText(text, btn);
  }});

  // ---- Pomodoro focus timer (per-browser via localStorage; not part of the shared doc) ----
  (function () {{
    var DURATIONS = {{focus: 25*60, short: 5*60, long: 15*60}};
    var KEY = 'sjbc-pomo-v1';
    var state = Object.assign({{mode: 'focus', remaining: DURATIONS.focus, running: false, endAt: null, sessions: 0, selectedTask: null}}, JSON.parse(localStorage.getItem(KEY) || '{{}}'));
    var tasks = window.__POMO_TASKS__ || [];
    var sel = document.getElementById('focusTaskSelect');
    sel.innerHTML = tasks.map(function(t) {{ return '<option value="' + t.id + '">' + (t.title.length > 46 ? t.title.slice(0,46) + '…' : t.title) + '</option>'; }}).join('');
    if (state.selectedTask && tasks.some(function(t) {{ return t.id === state.selectedTask; }})) sel.value = state.selectedTask;
    else if (tasks.length) state.selectedTask = tasks[0].id;

    function save() {{ localStorage.setItem(KEY, JSON.stringify(state)); }}
    function fmt(sec) {{ sec = Math.max(0, Math.ceil(sec)); return String(Math.floor(sec/60)).padStart(2,'0') + ':' + String(sec%60).padStart(2,'0'); }}
    function label(mode) {{ return mode === 'focus' ? 'Focus Session' : mode === 'short' ? 'Short Break' : 'Long Break'; }}
    function render() {{
      if (state.running && state.endAt) state.remaining = Math.max(0, Math.ceil((state.endAt - Date.now())/1000));
      var total = DURATIONS[state.mode];
      var pct = total ? Math.min(100, Math.max(0, (1 - state.remaining/total) * 100)) : 0;
      var t = fmt(state.remaining);
      document.getElementById('timerRing').style.setProperty('--timer-pct', pct);
      document.getElementById('timerText').textContent = t;
      document.getElementById('timerModeLabel').textContent = label(state.mode);
      document.getElementById('focusMiniTime').textContent = t;
      document.getElementById('timerStart').textContent = state.running ? 'Pause' : (state.mode === 'focus' ? 'Start Focus' : 'Start Break');
      document.getElementById('pomoSessionCount').textContent = state.sessions;
      document.getElementById('pomoMinuteCount').textContent = state.sessions * 25;
      document.getElementById('pomoCycleCount').textContent = (state.sessions % 4) + '/4';
      document.querySelectorAll('.pomo-mode').forEach(function(b) {{ b.setAttribute('aria-pressed', String(b.dataset.pomoMode === state.mode)); }});
    }}
    function setMode(mode) {{ state.mode = mode; state.running = false; state.endAt = null; state.remaining = DURATIONS[mode]; save(); render(); }}
    function toggle() {{
      if (state.running) {{ state.remaining = Math.max(0, Math.ceil((state.endAt - Date.now())/1000)); state.running = false; state.endAt = null; }}
      else {{ if (state.remaining <= 0) state.remaining = DURATIONS[state.mode]; state.running = true; state.endAt = Date.now() + state.remaining*1000; }}
      save(); render();
    }}
    function complete() {{
      if (state.mode === 'focus') state.sessions += 1;
      var next = state.mode === 'focus' ? (state.sessions % 4 === 0 ? 'long' : 'short') : 'focus';
      state.mode = next; state.remaining = DURATIONS[next]; state.running = false; state.endAt = null;
      save(); render();
    }}
    document.getElementById('focusLaunch').addEventListener('click', function() {{
      document.getElementById('focusPanel').classList.add('open');
      document.getElementById('focusBackdrop').classList.add('open');
      document.getElementById('focusPanel').setAttribute('aria-hidden', 'false');
    }});
    function closeFocus() {{
      document.getElementById('focusPanel').classList.remove('open');
      document.getElementById('focusBackdrop').classList.remove('open');
      document.getElementById('focusPanel').setAttribute('aria-hidden', 'true');
    }}
    document.getElementById('focusClose').addEventListener('click', closeFocus);
    document.getElementById('focusBackdrop').addEventListener('click', closeFocus);
    document.querySelectorAll('.pomo-mode').forEach(function(b) {{ b.addEventListener('click', function() {{ setMode(b.dataset.pomoMode); }}); }});
    document.getElementById('timerStart').addEventListener('click', toggle);
    document.getElementById('timerReset').addEventListener('click', function() {{ state.running = false; state.endAt = null; state.remaining = DURATIONS[state.mode]; save(); render(); }});
    document.getElementById('timerSkip').addEventListener('click', complete);
    sel.addEventListener('change', function() {{ state.selectedTask = sel.value; save(); }});
    document.getElementById('completeFocusTask').addEventListener('click', function() {{
      var row = document.querySelector('.task-row[data-task-id="' + sel.value + '"]');
      if (row) {{ var cb = row.querySelector('.check'); if (cb && !cb.checked) {{ cb.checked = true; cb.dispatchEvent(new Event('change', {{bubbles: true}})); }} }}
    }});
    setInterval(function() {{
      if (!state.running) return;
      var remaining = Math.max(0, Math.ceil((state.endAt - Date.now())/1000));
      if (remaining !== state.remaining) {{ state.remaining = remaining; render(); }}
      if (remaining <= 0) complete();
    }}, 250);
    render();
  }})();

  recompute();
  applyFilters();

  document.addEventListener('claude:sync-off', function(e) {{
    console.warn('Sync turned off for a region', e.target);
  }});
}})();
</script>
</body>
</html>
'''

with open("index.html", "w") as f:
    f.write(HTML)

print("wrote", len(HTML), "bytes")
