---
tags:
  - administration/handoff
  - 2026/03/15
from: PERMANENT: CODE AUTHORITY
to: PERSISTENT: ADMINISTRATION
date: 2026-03-15
---
Handoff briefing from CODE AUTHORITY to ADMINISTRATION. The vault has changed significantly since ADMIN's last update (2026-03-11). This document summarizes what landed, what's stale, and what needs ADMIN's attention.

---

## What Landed on Main

PR #1 merged 2026-03-14 (commit `59ed633`), consolidating two feature branches into main. Current HEAD: `219a271`.

**Files delivered to main:**

| Category | Files |
|---|---|
| Root | `CLAUDE.md` (repo-wide instructions for all Claude Code sessions) |
| Constitutional | `!ADMINISTRATION/Claude.md`, `Ethics.md`, `Logan.md`, `!README.md` |
| LEVELSET | `LEVELSET.md` (v1), `LEVELSET-v2.md`, `LEVELSET-v2-PROMPT.md`, `LEVELSET-v3.2.6.1-PROMPT.md` |
| Decisions | `DECISIONS.md` (6 entries through 2026-03-14) |
| Automation | `sort_audit.py` (v2), `propose_moves.py`, `wayback_audit.py` |
| Workflows | `sort-audit.yml`, `propose-moves.yml`, `wayback-audit.yml`, `wayback-preserve.yml` |
| Scraper | `idaho_leg_scraper.py`, `post_digest.py`, `idaho-leg-scraper.yml` |
| Reports | `sort-audit-2026-03-12.md`, `wayback-preserve-2026-03-15.md` |

**Key decisions recorded in DECISIONS.md:**
1. LEVELSET protocol established
2. CLAUDE.md created at repo root
3. Conversation taxonomy adopted
4. File type attribution (markdown = human, python = machine)
5. Sort audit and legislature scraper deployed
6. CODE AUTHORITY promoted to PERMANENT tier

**Wayback preserve workflow** fired automatically on the merge push. Result: 2 of 4 URLs failed submission (see `wayback-preserve-2026-03-15.md`).

---

## What's Stale in ADMIN's Claude.md

ADMIN's `!ADMINISTRATION/Claude.md` was last updated 2026-03-11. Several sections are now outdated:

### 1. `vault_push.py` references (lines 19, 73, 123)
`vault_push.py` was never delivered. Claude Code sessions (Tier 1) now push directly to GitHub — they have full repo write access. The constraint on line 19 ("Claude cannot write directly to GitHub — outbound network is blocked in the sandbox") is no longer accurate for Tier 1 instances.

### 2. Tier 2 definition (line 123)
"Tier 2 — Targeted push via `vault_push.py`, requires Logan approval" — `vault_push.py` doesn't exist. If ADMIN retains a tiered model, Tier 2 needs a new definition.

### 3. Scheduled workflows table (lines 62-67)
Describes Monday UTC schedule (sort audit 6am, propose moves 7am, wayback audit 8am). The actual deployed workflows use `workflow_dispatch` (manual trigger), not cron schedules. Only the legislature scraper runs on a schedule (daily 6am MT).

### 4. Pending items (lines 138-144)
Partially resolved:
- [x] `sort_audit.py` v2 — delivered to main (no longer needs `vault_push.py`)
- [x] Re-run sort audit — v2 report not yet generated but script is deployed
- [ ] Action genuine sort issues from v1 — still pending
- [ ] Wayback audit `--limit 20` — still pending
- [ ] PLACES/COUNTIES sort pass — still pending
- [ ] CourtListener evaluation — still pending
- [ ] Anthropic API key for Stage 3 — still pending

### 5. Conversation cluster (lines 125-131)
Missing updates:
- Legislature scraper conversation terminated cleanly (produced LEVELSET termination reports, still on feature branch `claude/idaho-legislature-scraper-RI6Ku`)
- TASK: LEVELSET status should reflect that v2 synthesis was completed and the prompt was updated to v3.2.6.1

---

## Decisions ADMIN Needs to Make

1. **Remove `vault_push.py` from the constitution?** It was never built. Claude Code sessions push directly. Is there still a use case for a mediated push mechanism, or should all references be removed?

2. **Redefine Tier 2?** With Tier 1 having direct repo access, what does Tier 2 mean now? Options: (a) remove tiers entirely and use capability-based language per LEVELSET v3.2.6.1, (b) redefine Tier 2 as "conversations that can draft but not push," (c) keep as-is for future use.

3. **Create `LEVELSET-CURRENT.md`?** The scraper conversation flagged that there's no single file pointing to the latest LEVELSET. Should one exist as a pointer, or is the additive file convention sufficient?

4. **Wayback failures — investigate or accept?** Two URLs failed preservation. Worth debugging, or accept that some government URLs resist archiving?

---

## Outstanding Vault-Wide

| Item | Status | Owner |
|---|---|---|
| Scraper LEVELSET termination reports | On feature branch, not merged to main | Logan (merge decision) |
| Wayback preservation failures | 2/4 URLs failed | CODE AUTHORITY (investigate) |
| Sort audit v1 genuine issues | 5 items identified, none actioned | ADMIN (prioritize) |
| `idaho-leg-setup.yml` workflow | Unbuilt | CODE AUTHORITY |
| `idaho-leg-bill-lookup.yml` workflow | Unbuilt | CODE AUTHORITY |
| PLACES/COUNTIES sort pass | Not started | ADMIN (scope) |
| Root `CLAUDE.md` sync with ADMIN constitution | Root CLAUDE.md exists but may diverge from ADMIN's Claude.md over time | ADMIN (governance) |

---

## How to Use This Document

Paste this into PERSISTENT: ADMINISTRATION as context. ADMIN can then:
1. Update `!ADMINISTRATION/Claude.md` to reflect current state
2. Make decisions on the items flagged above
3. Produce an updated LEVELSET if warranted
4. Direct CODE AUTHORITY on next priorities

This document is a snapshot, not a living file. Once ADMIN has processed it, it serves as a historical record only.
