# AI Usage Manager Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a local budget tracking system that monitors AI account limits across Claude Pro, Copilot Pro, and Gemini API, plans tasks against available resources, and logs session costs automatically.

**Architecture:** A standalone local git repo at `~/.ai-budget/` stores current budget state (JSON) and session logs (markdown). Three Python scripts handle data fetching and processing. Two Claude Code skills (`budget-check`, `budget-log`) wrap the scripts into a workflow run at session start and end. Claude's own utilisation is auto-fetched via OAuth API; Copilot and Gemini are manual inputs.

**Tech Stack:** Python 3.12 stdlib only (no pip installs), Anthropic OAuth API, Claude Code local JSONL files, Claude Code custom skills (markdown)

---

### Task 1: Initialise ~/.ai-budget/ repo

**Files:**
- Create: `~/.ai-budget/budget.json`
- Create: `~/.ai-budget/tasks/backlog.md`
- Create: `~/.ai-budget/tasks/completed.md`
- Create: `~/.ai-budget/sessions/.gitkeep`
- Create: `~/.ai-budget/scripts/` directory

**Step 1: Create directory structure**

```bash
mkdir -p ~/.ai-budget/tasks ~/.ai-budget/sessions ~/.ai-budget/scripts
cd ~/.ai-budget && git init
```

Expected: `Initialized empty Git repository in /home/stewards_path/.ai-budget/.git/`

**Step 2: Create budget.json**

Write to `~/.ai-budget/budget.json`:

```json
{
  "claude": {
    "plan": "pro",
    "five_hour_util": null,
    "seven_day_util": null,
    "five_hour_resets_at": null,
    "seven_day_resets_at": null,
    "last_fetched": null
  },
  "copilot": {
    "plan": "pro",
    "premium_requests_used": null,
    "premium_requests_limit": 300,
    "resets_at": null,
    "last_updated": null
  },
  "gemini": {
    "plan": "api",
    "status": "billing_pending",
    "last_updated": null
  },
  "calibration": {
    "flashcard":       {"unit": "per card",      "samples": 0, "avg_output_tokens": null, "avg_5h_pct": null},
    "circuit_diagram": {"unit": "per diagram",   "samples": 0, "avg_output_tokens": null, "avg_5h_pct": null},
    "migration":       {"unit": "per migration", "samples": 0, "avg_output_tokens": null, "avg_5h_pct": null},
    "feature":         {"unit": "per feature",   "samples": 0, "avg_output_tokens": null, "avg_5h_pct": null},
    "css_component":   {"unit": "per component", "samples": 0, "avg_output_tokens": null, "avg_5h_pct": null},
    "refactor":        {"unit": "per file",      "samples": 0, "avg_output_tokens": null, "avg_5h_pct": null}
  }
}
```

**Step 3: Create tasks/backlog.md**

Populate from current study platform priorities:

```markdown
# Backlog

## Study Platform

[L] span.topic-code CSS styling in base stylesheet
[H] Flashcard content — 30 mathematics topics SMA101/102 (plan: 15 per session)
[H] Flashcard content — SMA209/SMA212 mathematics topics
[H] Circuit Analysis Fundamentals diagrams (~8, passive components)
[M] Feature decision: SM-2 algorithm / feedback loop / progress dashboard

## AI Budget Manager

[L] Verify fetch_claude_usage.py token key against credentials.json
[L] First real budget-check + budget-log run to seed calibration
```

**Step 4: Create remaining empty files**

```bash
touch ~/.ai-budget/sessions/.gitkeep
echo "# Completed Tasks" > ~/.ai-budget/tasks/completed.md
```

**Step 5: Initial commit**

```bash
cd ~/.ai-budget
git add -A
git commit -m "init: ai-budget repo with budget.json and backlog"
```

Expected: clean commit on main branch

---

### Task 2: fetch_claude_usage.py

**Files:**
- Create: `~/.ai-budget/scripts/fetch_claude_usage.py`

**Step 1: Check the credentials.json key names first**

```bash
python3 -c "import json; d=json.load(open('$HOME/.claude/.credentials.json')); print(list(d.keys()))"
```

Note the key name that holds the OAuth token (do not print the value). Common names: `accessToken`, `access_token`, `claudeAiOauthToken`.

**Step 2: Write the script**

Write to `~/.ai-budget/scripts/fetch_claude_usage.py`:

```python
#!/usr/bin/env python3
"""Fetch Claude Pro utilisation from the Anthropic OAuth API and update budget.json."""

import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

CREDENTIALS_PATH = Path.home() / ".claude" / ".credentials.json"
BUDGET_PATH = Path.home() / ".ai-budget" / "budget.json"
API_URL = "https://api.anthropic.com/api/oauth/usage"


def get_token():
    creds = json.loads(CREDENTIALS_PATH.read_text())
    for key in ("accessToken", "access_token", "claudeAiOauthToken"):
        if key in creds:
            return creds[key]
    # Nested structure fallback
    for val in creds.values():
        if isinstance(val, dict):
            for key in ("accessToken", "access_token"):
                if key in val:
                    return val[key]
    return None


def fetch_usage(token):
    req = urllib.request.Request(
        API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "anthropic-beta": "oauth-2025-04-20",
            "Accept": "application/json",
            "User-Agent": "claude-code/2.0.32",
        }
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def main():
    token = get_token()
    if not token:
        print("ERROR: Could not find access token in ~/.claude/.credentials.json")
        print("Keys found:", list(json.loads(CREDENTIALS_PATH.read_text()).keys()))
        return 1

    try:
        data = fetch_usage(token)
    except urllib.error.HTTPError as e:
        print(f"ERROR: API call failed: {e.code} {e.reason}")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    budget = json.loads(BUDGET_PATH.read_text())
    now = datetime.now(timezone.utc).isoformat()

    budget["claude"]["five_hour_util"] = data["five_hour"]["utilization"]
    budget["claude"]["seven_day_util"] = data["seven_day"]["utilization"]
    budget["claude"]["five_hour_resets_at"] = data["five_hour"]["resets_at"]
    budget["claude"]["seven_day_resets_at"] = data["seven_day"]["resets_at"]
    budget["claude"]["last_fetched"] = now

    BUDGET_PATH.write_text(json.dumps(budget, indent=2))

    five = data["five_hour"]
    seven = data["seven_day"]
    print(f"Claude 5h:  {five['utilization']:.1f}%  (resets {five['resets_at']})")
    print(f"Claude 7d:  {seven['utilization']:.1f}%  (resets {seven['resets_at']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 3: Make executable and test**

```bash
chmod +x ~/.ai-budget/scripts/fetch_claude_usage.py
python3 ~/.ai-budget/scripts/fetch_claude_usage.py
```

Expected output (values will vary):
```
Claude 5h:  12.0%  (resets 2026-02-27T14:00:00+00:00)
Claude 7d:  35.0%  (resets 2026-03-05T00:00:00+00:00)
```

If token key error: check output for "Keys found:" and update `get_token()` to match.

**Step 4: Verify budget.json updated**

```bash
python3 -c "
import json
d = json.load(open('$HOME/.ai-budget/budget.json'))
c = d['claude']
print(f\"5h: {c['five_hour_util']}%  7d: {c['seven_day_util']}%  fetched: {c['last_fetched']}\")
"
```

Expected: real numbers, not null.

**Step 5: Commit**

```bash
cd ~/.ai-budget
git add scripts/fetch_claude_usage.py budget.json
git commit -m "feat: fetch Claude OAuth usage and update budget.json"
```

---

### Task 3: parse_session_tokens.py

**Files:**
- Create: `~/.ai-budget/scripts/parse_session_tokens.py`

Finds the most recent Claude Code session JSONL, sums all token fields, outputs JSON.

**Step 1: Write the script**

Write to `~/.ai-budget/scripts/parse_session_tokens.py`:

```python
#!/usr/bin/env python3
"""Parse the most recent Claude Code session JSONL and output token totals as JSON."""

import json
import sys
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"


def find_latest_session():
    """Find the most recently modified top-level session JSONL (not subagents)."""
    jsonl_files = []
    if not PROJECTS_DIR.exists():
        return None
    for project_dir in PROJECTS_DIR.iterdir():
        if project_dir.is_dir():
            for f in project_dir.glob("*.jsonl"):
                jsonl_files.append(f)
    if not jsonl_files:
        return None
    return max(jsonl_files, key=lambda f: f.stat().st_mtime)


def parse_session(path):
    totals = {
        "exchanges": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
        "web_search_requests": 0,
        "web_fetch_requests": 0,
    }
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                usage = obj.get("message", {}).get("usage")
                if not usage:
                    continue
                totals["exchanges"] += 1
                totals["input_tokens"] += usage.get("input_tokens", 0)
                totals["output_tokens"] += usage.get("output_tokens", 0)
                totals["cache_read_input_tokens"] += usage.get("cache_read_input_tokens", 0)
                totals["cache_creation_input_tokens"] += usage.get("cache_creation_input_tokens", 0)
                st = usage.get("server_tool_use", {})
                totals["web_search_requests"] += st.get("web_search_requests", 0)
                totals["web_fetch_requests"] += st.get("web_fetch_requests", 0)
            except json.JSONDecodeError:
                continue
    return totals


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else find_latest_session()

    if not path or not path.exists():
        print(json.dumps({"error": "No session JSONL found"}))
        return 1

    totals = parse_session(path)
    totals["session_file"] = str(path)
    print(json.dumps(totals, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 2: Make executable and test**

```bash
chmod +x ~/.ai-budget/scripts/parse_session_tokens.py
python3 ~/.ai-budget/scripts/parse_session_tokens.py
```

Expected output:
```json
{
  "exchanges": 322,
  "input_tokens": 452,
  "output_tokens": 9843,
  "cache_read_input_tokens": 28906638,
  "cache_creation_input_tokens": 348691,
  "web_search_requests": 0,
  "web_fetch_requests": 0,
  "session_file": "/home/stewards_path/.claude/projects/..."
}
```

Verify: `output_tokens` and `exchanges` are non-zero. `session_file` points to a real path.

**Step 3: Commit**

```bash
cd ~/.ai-budget
git add scripts/parse_session_tokens.py
git commit -m "feat: parse Claude Code session JSONL for token totals"
```

---

### Task 4: update_calibration.py

**Files:**
- Create: `~/.ai-budget/scripts/update_calibration.py`

Takes task type, units completed, 5h % delta, and output tokens. Updates the running weighted average in budget.json.

**Step 1: Write the script**

Write to `~/.ai-budget/scripts/update_calibration.py`:

```python
#!/usr/bin/env python3
"""Update calibration running averages in budget.json after a session."""

import json
import sys
from pathlib import Path

BUDGET_PATH = Path.home() / ".ai-budget" / "budget.json"


def weighted_avg(old_avg, old_samples, new_value):
    if old_avg is None:
        return new_value
    return ((old_avg * old_samples) + new_value) / (old_samples + 1)


def main():
    if len(sys.argv) < 4:
        print("Usage: update_calibration.py <task_type> <units> <five_hour_pct_delta> [output_tokens]")
        print("  task_type:           flashcard|circuit_diagram|migration|feature|css_component|refactor")
        print("  units:               count completed this session (e.g. 15)")
        print("  five_hour_pct_delta: % of 5h window used this session (e.g. 38.5)")
        print("  output_tokens:       total output tokens from session (optional)")
        return 1

    task_type = sys.argv[1]
    units = int(sys.argv[2])
    delta_pct = float(sys.argv[3])
    output_tokens = int(sys.argv[4]) if len(sys.argv) > 4 else None

    if units <= 0:
        print("ERROR: units must be > 0")
        return 1

    budget = json.loads(BUDGET_PATH.read_text())
    cal = budget.get("calibration", {})

    if task_type not in cal:
        print(f"ERROR: unknown task type '{task_type}'")
        print(f"Known types: {list(cal.keys())}")
        return 1

    entry = cal[task_type]
    old_samples = entry["samples"]
    pct_per_unit = delta_pct / units

    entry["avg_5h_pct"] = round(weighted_avg(entry["avg_5h_pct"], old_samples, pct_per_unit), 2)

    if output_tokens is not None:
        tokens_per_unit = output_tokens / units
        entry["avg_output_tokens"] = round(
            weighted_avg(entry["avg_output_tokens"], old_samples, tokens_per_unit)
        )

    entry["samples"] += 1
    BUDGET_PATH.write_text(json.dumps(budget, indent=2))

    print(f"Updated '{task_type}': {entry['samples']} sample(s)")
    print(f"  avg_5h_pct:      {entry['avg_5h_pct']}% per {entry['unit']}")
    if entry["avg_output_tokens"]:
        print(f"  avg_output_tokens: {entry['avg_output_tokens']:,} per {entry['unit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 2: Make executable**

```bash
chmod +x ~/.ai-budget/scripts/update_calibration.py
```

**Step 3: Test with mock data — first sample**

```bash
python3 ~/.ai-budget/scripts/update_calibration.py flashcard 15 38.5 9843
```

Expected:
```
Updated 'flashcard': 1 sample(s)
  avg_5h_pct:      2.57% per card
  avg_output_tokens: 656 per card
```

**Step 4: Test averaging — second sample**

```bash
python3 ~/.ai-budget/scripts/update_calibration.py flashcard 20 51.0 12000
```

Expected:
```
Updated 'flashcard': 2 sample(s)
  avg_5h_pct:      2.93% per card
  avg_output_tokens: 728 per card
```

Verify: `(2.57 * 1 + 2.55) / 2 ≈ 2.93` — averaging is working.

**Step 5: Reset calibration to null for real use**

The mock data seeded flashcard calibration. Reset it:

```bash
python3 -c "
import json
from pathlib import Path
p = Path.home() / '.ai-budget' / 'budget.json'
d = json.loads(p.read_text())
d['calibration']['flashcard'] = {'unit': 'per card', 'samples': 0, 'avg_output_tokens': None, 'avg_5h_pct': None}
p.write_text(json.dumps(d, indent=2))
print('Reset done')
"
```

**Step 6: Commit**

```bash
cd ~/.ai-budget
git add scripts/update_calibration.py budget.json
git commit -m "feat: update calibration running averages in budget.json"
```

---

### Task 5: budget-check skill

**Files:**
- Create: `~/.claude/skills/budget-check.md`

**Step 1: Check/create skills directory**

```bash
ls ~/.claude/skills/ 2>/dev/null || mkdir -p ~/.claude/skills
```

**Step 2: Write the skill**

Write to `~/.claude/skills/budget-check.md`:

````markdown
---
name: budget-check
description: Session start budget check. Fetches Claude usage, reads budget.json, reads backlog, outputs session brief with task recommendations.
---

# Budget Check — Session Start

Run these steps in order and present the session brief.

## Step 1: Fetch Claude utilisation

Run:
```bash
python3 ~/.ai-budget/scripts/fetch_claude_usage.py
```

If it errors, note "Claude API unavailable — using last known values from budget.json" and continue.

## Step 2: Read current budget state

Read `~/.ai-budget/budget.json`. Extract:
- Claude: five_hour_util %, five_hour_resets_at, seven_day_util %
- Copilot: premium_requests_used, premium_requests_limit, resets_at, last_updated
- Gemini: status
- Calibration: avg_5h_pct and samples for each task type

Compute time until 5h reset from five_hour_resets_at vs current UTC time.

## Step 3: Read backlog

Read `~/.ai-budget/tasks/backlog.md`.

## Step 4: Estimate task costs

For each [H] and [M] task, estimate 5h window cost:
- If calibration samples > 0 for the task type: use avg_5h_pct × estimated units
- If samples == 0: use tag estimates: [L]=5%, [M]=15%, [H]=35%, [X]=70%

## Step 5: Output session brief

```
=== Budget Check: [DATE TIME] ===

Claude:  5h at X% (resets in Xh Xm) | 7-day at X%
Copilot: X of 300 requests used — X remaining (resets DATE, last updated DATE)
Gemini:  [status]

Backlog — estimated session cost:
[tag] Task description  →  ~X% 5h window  ([calibrated: X samples] or [estimated])
...

Recommendation:
→ [First task and why]
→ [Any mid-task limit warnings with specific checkpoint advice]
→ [What to defer]
```

## Step 6: Prompt for stale Copilot data

If copilot.last_updated is more than 2 days ago, ask:
"Copilot data is [N] days old — do you know your current premium request count? Enter number used, or press enter to skip."

If they provide a number, update budget.json:
```bash
python3 -c "
import json
from pathlib import Path
from datetime import date
p = Path.home() / '.ai-budget' / 'budget.json'
d = json.loads(p.read_text())
d['copilot']['premium_requests_used'] = USER_NUMBER
d['copilot']['last_updated'] = str(date.today())
p.write_text(json.dumps(d, indent=2))
"
```
````

**Step 3: Verify skill loads**

In Claude Code, run:
```
/budget-check
```

Expected: skill executes, session brief is printed.

**Step 4: Commit**

```bash
cd ~/.ai-budget
git commit -m "docs: budget-check skill at ~/.claude/skills/budget-check.md" --allow-empty
```

---

### Task 6: budget-log skill

**Files:**
- Create: `~/.claude/skills/budget-log.md`

**Step 1: Write the skill**

Write to `~/.claude/skills/budget-log.md`:

````markdown
---
name: budget-log
description: Session end logging. Gathers work summary, fetches updated Claude usage, parses JSONL tokens, updates calibration, writes session log, commits to ~/.ai-budget.
---

# Budget Log — Session End

Run these steps in order.

## Step 1: Capture pre-log Claude state

Read `~/.ai-budget/budget.json` — note current five_hour_util as `util_before`.

## Step 2: Fetch updated Claude utilisation

Run:
```bash
python3 ~/.ai-budget/scripts/fetch_claude_usage.py
```

Read the new five_hour_util from budget.json as `util_after`.
Calculate `delta_pct = util_after - util_before`.

## Step 3: Parse session token totals

Run:
```bash
python3 ~/.ai-budget/scripts/parse_session_tokens.py
```

Record: output_tokens, cache_creation_input_tokens, web_search_requests, web_fetch_requests.

## Step 4: Ask what was completed

Ask:
"What did you complete this session? For each task type give: type, units, description.
Known types: flashcard, circuit_diagram, migration, feature, css_component, refactor
Example: 'flashcard 15 — SMA101 voltage divider topics'
Or just describe it and I'll map to a type."

Wait for response. Map free-text descriptions to known task types if needed.

## Step 5: Update calibration

For each completed task type, run:
```bash
python3 ~/.ai-budget/scripts/update_calibration.py <task_type> <units> <delta_pct> <output_tokens>
```

If multiple task types, split output_tokens proportionally by estimated heaviness.

## Step 6: Write session log

Determine today's date (YYYY-MM-DD). Write to `~/.ai-budget/sessions/YYYY-MM-DD.md`:

```markdown
## Session: YYYY-MM-DD

**Claude:** 5h window X%→X% (Δ+X%) | 7-day X%→X%
**Tokens — output:** X,XXX | cache built: XXXk | web fetches: X | searches: X
**Copilot:** [used X requests / not used]
**Gemini:** [used / billing pending]

**Work done:**
- [task_type] N units — description

**Cost breakdown:**
- [task]: ~X% 5h window, Xk output tokens (~X tokens/unit, ~X%/unit)

**Calibration:** [task_type] N→N+1 samples, avg now X%/unit

**Lessons:**
- [Observations about cost, context bloat, unexpected token spikes]

**Next session:**
- [Top 2-3 backlog items]
```

## Step 7: Move completed tasks in backlog if requested

Ask: "Should I move any tasks from backlog.md to completed.md?"
If yes, edit `~/.ai-budget/tasks/backlog.md` and `~/.ai-budget/tasks/completed.md`.

## Step 8: Commit everything

```bash
cd ~/.ai-budget && git add -A && git commit -m "session: YYYY-MM-DD"
```

Expected: clean commit. Verify with `git log --oneline -3`.
````

**Step 2: Test by running budget-log**

In Claude Code, run `/budget-log`. Walk through a real session end. Verify:
- Session log written to `~/.ai-budget/sessions/`
- budget.json updated with fresh Claude utilisation
- Calibration entry updated for at least one task type
- Git commit created

**Step 3: Commit**

```bash
cd ~/.ai-budget
git commit -m "docs: budget-log skill at ~/.claude/skills/budget-log.md" --allow-empty
```

---

### Task 7: Update MEMORY.md

**Files:**
- Modify: `~/.claude/projects/-home-stewards-path/memory/MEMORY.md`

**Step 1: Add budget manager section to MEMORY.md**

Add after the "Agent Permissions" section:

```markdown
## AI Budget Manager
- Repo: `~/.ai-budget/` — local git only, never push to GitHub
- Skills: `budget-check` (session start), `budget-log` (session end)
- Scripts: `~/.ai-budget/scripts/` — fetch_claude_usage, parse_session_tokens, update_calibration
- Claude usage API: `GET https://api.anthropic.com/api/oauth/usage`
  - Token: `~/.claude/.credentials.json`
  - Returns: five_hour utilisation %, seven_day utilisation %
- Copilot/Gemini: manual input only — update budget.json when checking dashboards
- Session JSONL location: `~/.claude/projects/-home-stewards-path/<session-id>.jsonl`
```

**Step 2: Verify MEMORY.md is under 200 lines**

```bash
wc -l ~/.claude/projects/-home-stewards-path/memory/MEMORY.md
```

If over 200, condense older sections.

---

## Quick Reference: Workflow After Setup

**Start of every session:**
```
/budget-check
```

**End of every session:**
```
/budget-log
```

**Manually update Copilot balance** (after checking github.com/settings/billing):
```bash
python3 -c "
import json; from pathlib import Path; from datetime import date
p = Path.home() / '.ai-budget' / 'budget.json'
d = json.loads(p.read_text())
d['copilot']['premium_requests_used'] = 285  # update this number
d['copilot']['last_updated'] = str(date.today())
p.write_text(json.dumps(d, indent=2))
print('Copilot updated')
"
```
