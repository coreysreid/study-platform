# AI Usage Manager — Design

**Date:** 2026-02-27
**Status:** Approved, pending implementation plan

## Problem

Running out of tokens mid-task causes lost sessions and wasted work. Three paid AI accounts (Claude Pro, GitHub Copilot Pro, Gemini API) are underutilised because there's no visibility into what's available before starting work.

## Goal

A lightweight system that:
1. Shows current budget across all accounts at session start
2. Plans tasks against available resources before starting
3. Logs session cost automatically at session end
4. Builds a calibration table over time (cost per work unit by task type)
5. Maximises use of all paid accounts

---

## Data Layer

### Storage Location

Local git repo at `~/.ai-budget/` — never pushed to GitHub, full local history.

```
~/.ai-budget/
  budget.json          ← tiny current state, always-loaded
  tasks/
    backlog.md         ← master task list with weight tags
    completed.md
  sessions/
    YYYY-MM-DD.md      ← narrative log per session, read on demand only
```

### budget.json Schema

```json
{
  "claude": {
    "plan": "pro",
    "five_hour_util": 12,
    "seven_day_util": 35,
    "five_hour_resets_at": "2026-02-27T14:00:00Z",
    "seven_day_resets_at": "2026-03-05T00:00:00Z",
    "last_fetched": "2026-02-27T09:00:00Z"
  },
  "copilot": {
    "plan": "pro",
    "premium_requests_used": 285,
    "premium_requests_limit": 300,
    "resets_at": "2026-03-01",
    "last_updated": "2026-02-27"
  },
  "gemini": {
    "plan": "api",
    "status": "billing_pending",
    "last_updated": "2026-02-27"
  },
  "calibration": {
    "flashcard": {
      "unit": "per card",
      "samples": 0,
      "avg_output_tokens": null,
      "avg_5h_pct": null
    },
    "circuit_diagram": {
      "unit": "per diagram",
      "samples": 0,
      "avg_output_tokens": null,
      "avg_5h_pct": null
    },
    "migration": {
      "unit": "per migration",
      "samples": 0,
      "avg_output_tokens": null,
      "avg_5h_pct": null
    },
    "feature": {
      "unit": "per feature",
      "samples": 0,
      "avg_output_tokens": null,
      "avg_5h_pct": null
    },
    "css_component": {
      "unit": "per component",
      "samples": 0,
      "avg_output_tokens": null,
      "avg_5h_pct": null
    }
  }
}
```

### Task Weight Tags

Tasks in `backlog.md` are tagged:

| Tag | Meaning | Approx 5h window |
|-----|---------|-----------------|
| `[L]` | Light — single file, small edit | <10% |
| `[M]` | Medium — feature, 10-20 cards | 10-25% |
| `[H]` | Heavy — batch work, 30+ cards, diagrams | 25-50% |
| `[X]` | Multi-session — too large for one sitting | >50% |

---

## Token Data Source

Claude Code writes full per-exchange token data to local JSONL files:

```
~/.claude/projects/-home-stewards-path/<session-id>.jsonl
```

Each exchange contains:
```json
{
  "input_tokens": 452,
  "output_tokens": 9843,
  "cache_read_input_tokens": 28906638,
  "cache_creation_input_tokens": 348691,
  "server_tool_use": {
    "web_search_requests": 3,
    "web_fetch_requests": 5
  }
}
```

A Python script sums these at session end to produce the token summary without any manual counting.

Claude's 5h/7-day utilisation % is fetched from:
```
GET https://api.anthropic.com/api/oauth/usage
Authorization: Bearer <token from ~/.claude/.credentials.json>
anthropic-beta: oauth-2025-04-20
```

---

## Programmatic Access by Account

| Account | Auto-fetchable | Method |
|---------|---------------|--------|
| Claude Pro | Yes | `/api/oauth/usage` → 5h + 7-day utilisation % |
| Copilot Pro | No | Manual input — paste from github.com/settings/billing |
| Gemini API | No | Manual input — paste from AI Studio dashboard |

---

## Session Workflow

### Session Start — `budget-check` skill

1. Auto-fetches Claude utilisation from API, updates `budget.json`
2. Reads Copilot/Gemini balances from `budget.json` (manual, last known)
3. Reads `tasks/backlog.md`
4. Applies calibration table to estimate task costs
5. Outputs session brief:

```
=== Budget Check: 2026-02-27 09:15 ===

Claude:  5h at 12% (resets in 4h20m) | 7-day at 35%
Copilot: 15 premium requests remaining (last updated yesterday)
Gemini:  billing pending

Backlog:
[M] topic-code CSS styling      → ~8% 5h window (1 Copilot req alt.)
[H] 30 SMA101 flashcards        → ~93% 5h window (calibration: 3.1%/card)
[M] SM-2 feature decision       → ~15% 5h window

Recommendation:
→ CSS styling first (light, quick win)
→ Begin flashcards — but checkpoint at 15 cards (~50% window used)
→ SM-2 decision: defer to next session

Warning: Starting all 30 cards risks hitting the 5h limit mid-task.
Plan: 15 today, 15 next session.
```

### Session End — `budget-log` skill

1. Prompts: "What did you complete? How many units?"
2. Fetches updated Claude utilisation from API
3. Parses current session JSONL for token totals
4. Updates calibration averages for completed task types
5. Writes session log to `sessions/YYYY-MM-DD.md`
6. Updates `budget.json` with new utilisation values
7. Runs `git add -A && git commit -m "session: YYYY-MM-DD"` in `~/.ai-budget/`

### Session Log Format

```markdown
## Session: 2026-02-27

**Claude:** 5h window 12%→58% | 7-day 35%→41%
**Tokens — output:** 9,843 | cache built: 348k | web fetches: 5 | searches: 3
**Copilot:** not used
**Gemini:** not used

**Work done:** CSS topic-code styling (1 component) + 15 SMA101 flashcards

**Cost breakdown:**
- CSS component: ~8% 5h window, 1.8k output tokens
- 15 flashcards: ~38% 5h window, 8k output tokens (~530 tokens/card, ~2.5%/card)

**Calibration update:** flashcard samples 0→1, avg 2.5%/card (was null)

**Lesson:** Cards run lighter early session before context builds. Expect 3-4%/card later.
**Next session:** Remaining 15 SMA101 cards, then SMA102 batch
```

---

## Calibration System

Starts empty. Fills in as sessions accumulate. After 3-4 sessions of the same task type, averages stabilise.

The script computes running weighted average after each session:

```
new_avg = ((old_avg * old_samples) + session_value) / (old_samples + 1)
```

The session brief uses calibration data to forecast. When `samples == 0`, it shows `[uncalibrated]` and uses weight tag estimates instead.

Natural work units by task type:

| Task type | Unit |
|-----------|------|
| Flashcards | per card |
| Circuit diagrams | per diagram |
| Django features/views | per feature |
| Migrations | per migration |
| CSS/styling | per component |
| Refactors | per file touched |

---

## Implementation Scope

- `~/.ai-budget/` local git repo with initial `budget.json` and empty `tasks/backlog.md`
- Python script: `fetch_claude_usage.py` — calls the OAuth API, updates budget.json
- Python script: `parse_session_tokens.py` — reads JSONL, outputs token summary
- Python script: `update_calibration.py` — updates calibration averages in budget.json
- Claude Code skill: `budget-check` — session start brief
- Claude Code skill: `budget-log` — session end logging
- Initial backlog populated from `project_shortterm.md`

Out of scope (v1): Gemini API token tracking via response headers, Copilot API (no personal endpoint exists).
