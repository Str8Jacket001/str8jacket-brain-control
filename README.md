# Str8Jacket Brain Control

An interactive to-do "mission control" for Anthony Stover, built from real
Pocket and Fireflies notes (styled after the EmpowerMEnt Event Mission
Control reference).

- **My Tasks** — every open action item pulled from Pocket, grouped into
  life lanes (Leadership Retreat, Fun & Learn Events, Ambassadors &
  Regions, Policy & Courts, Youth Support, Org Ops & Finance, Training &
  Curriculum, Personal & Home). Checkboxes persist live for anyone viewing
  the published page.
- **Waiting on Others** — tasks other people owe you, with a "received"
  checkbox per person.
- **Follow-ups & Emails** — draft emails/messages Pocket already wrote for
  you, with a "sent" checkbox.

## How it's generated

`pocket_items.json` is a snapshot of Pocket's `search_pocket_actionitems`
output. `build.py` classifies each item into a lane, splits it into
tasks / dependencies / email drafts, and writes `fragments.json`. `build2.py`
renders `fragments.json` into the final `index.html`.

The live version of this page is published as a Claude Artifact (not
GitHub Pages) so it can use the `artifact` runtime capability: checkbox
state is saved live to the page itself (a "live doc"), so ticking a box
persists across visits without any backend.

## Refresh cycle

Claude Code refreshes this hourly (the platform's minimum scheduled
interval — true 15-minute polling isn't available) via a Routine:

1. Re-pull `search_pocket_actionitems` (and Fireflies transcripts once
   reconnected/needed) for new or changed items.
2. Fetch the *currently published* artifact HTML and read back which
   `data-task-id` rows are checked, so completed/sent/received state
   survives the refresh.
3. Re-run `build.py` / `build2.py` with the merged data.
4. Republish via the Artifact tool.

Zoom notes are not yet included — the Zoom connector's token expired and
needs to be reconnected in claude.ai connector settings.
