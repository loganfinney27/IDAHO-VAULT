# LEVELSET v2 — Unified Synthesis

**Date:** 2026-03-13
**Status:** CANONICAL — Single-source-of-truth
**Authored by:** PERMANENT: CODE AUTHORITY (Claude Code, Tier 1)
**Approved by:** Logan Finney

---

## PURPOSE

LEVELSET is a permanent, auditable checkpoint protocol for IDAHO-VAULT. This document synthesizes reports from all active Claude conversations into one canonical record. It is never deleted, never overwritten.

LEVELSETTING is the process of each conversation or entity taking a pause and inventory before routing their respective reports to one centralized location for synthesis, verification, and redistribution — forming a single-source-of-truth.

---

## ECOSYSTEM INVENTORY

### Repository State (as of 2026-03-13)

- **Remote:** github.com/loganfinney27/IDAHO-VAULT (public)
- **Primary branch:** `origin/main` (at commit `364c2bd`)
- **Active feature branches:**
  - `claude/idaho-legislature-scraper-RI6Ku` — legislature scraper (at `31eb718`)
  - `claude/levelset-multi-conversation-zWxJc` — this LEVELSET process (at `31eb718`)
- **Local branch:** `master` (tracks `origin/main`)
- **Total commits:** 17

### Vault Structure

```
IDAHO-VAULT/
  !ADMINISTRATION/        — Vault infrastructure, LEVELSET files
  ATTACHMENTS/            — Media and document attachments
  GOVERNMENTS/            — Government entities (Idaho legislative, executive, local)
  ORGANIZATIONS/          — Organizations referenced in reporting
  PEOPLE/                 — People referenced in reporting
  PLACES/                 — Geographic locations
  SOURCES/                — Source documents, news media, editorials, reports
  TOPICS/                 — Subject-area notes
  X LABELER/              — Unsorted/pending classification
  .github/scripts/        — Automation (sort_audit.py, idaho_leg_scraper.py, post_digest.py)
  .github/workflows/      — GitHub Actions (sort-audit.yml, idaho-leg-scraper.yml)
  .obsidian/              — Obsidian configuration and plugins
```

### Infrastructure Built

| Asset | Type | Commit | Branch |
|---|---|---|---|
| `sort_audit.py` | Python | `4754d08` | main |
| `sort-audit.yml` (GitHub Action) | YAML | `4754d08` | main |
| `sort-audit-2026-03-12.md` | Markdown (output) | `f7089f9` | main |
| `idaho_leg_scraper.py` | Python | `449d365` | feature branch |
| `post_digest.py` | Python | `449d365` | feature branch |
| `idaho-leg-scraper.yml` (GitHub Action) | YAML | `449d365` | feature branch |
| `.gitignore` | Config | `31eb718` | feature branch |

### Missing / Not Yet Created

- **CLAUDE.md** — No repository-level instruction file exists
- **Ethics.md** — No vault ethics policy exists (distinct from Idaho legislative ethics committee files)
- **LEVELSET-v1.md** — No prior LEVELSET document was committed to the repo

---

## CONVERSATION CENSUS

### Conversations with Known Contributions

| Conversation | Tier | Role | Known Output | Status |
|---|---|---|---|---|
| **PERMANENT: CODE AUTHORITY** (this session) | 1 | Authoritative code session; LEVELSET synthesis | This document | Active |
| **PERSISTENT: ADMINISTRATION** | Unknown | Vault governance, CLAUDE.md, Ethics.md | Unknown — nothing committed to repo | Unknown |
| **TASK: LEVELSET reports** | Unknown | LEVELSET synthesis hub | Distributed LEVELSET v2 prompt | Active |
| **STORY: JFAC Open Meetings** | Unknown | Journalism story | Unknown | Unknown |
| **PROJECT: 2026 Budget Tracker** | Unknown | Budget tracking project | Unknown | Unknown |
| **ISSUE: Repository browsing** | Unknown | Repo navigation troubleshooting | Unknown | Unknown |

### Conversations — Context/Research (likely Tier 3)

| Conversation | Probable Role |
|---|---|
| Idaho Public Television overview a... | Background context on IPTV |
| Idaho Reports episode production... | Production workflow reference |
| Understanding Black's Law diction... | Legal terminology lookup |
| Interpreting an unclear concept | Research/clarification |
| In the Blink of an Eye book recom... | Craft reference (editing/storytelling) |
| INQUIRY: Adobe Premiere Pro | Production software support |

### Attribution Gap

The following commits exist in the repo but **cannot be attributed to a specific conversation** from this session:

- Legislature scraper (`449d365`, `ebd9df6`, `6c639b7`) — likely from a Claude Code session on branch `claude/idaho-legislature-scraper-RI6Ku`
- Sort audit (`4754d08`, `f7089f9`) — likely from a Claude Code session, merged to main
- Vault structure commits (`e2d1cef` through `364c2bd`) — likely manual or early-session work

---

## SOURCING & SENSITIVITY ASSESSMENT

- **On the record:** All content currently committed to the public repository is on the record and should be treated as publishable.
- **On background:** No background-sourced material has been identified in committed files. If any exists in other conversations, it has not reached the repo.
- **Off the record:** This session holds no off-the-record material. Other conversations may — this document does not and cannot catalog what it cannot see.
- **Flag:** The `SOURCES/` directory contains news articles and editorials that are public record. The `PEOPLE/` directory contains notes on public figures. Both are appropriate for a public repo given the journalistic context.

---

## CONSOLIDATION ASSESSMENT

### Recommended Consolidations

**1. Tier 3 research conversations — LOW PRIORITY, MONITOR**

The following conversations appear to be single-query research lookups with no ongoing role in the vault architecture:

- "Understanding Black's Law diction..."
- "Interpreting an unclear concept"
- "In the Blink of an Eye book recom..."
- "INQUIRY: Adobe Premiere Pro"
- "Idaho Public Television overview a..."
- "Idaho Reports episode production..."

**Recommendation:** These do not need active consolidation. They are finished conversations that serve as reference. No action required unless Logan wants to extract durable notes from them into the vault as Markdown files.

**2. PERSISTENT: ADMINISTRATION + This session — EVALUATE**

If PERSISTENT: ADMINISTRATION has not produced committed artifacts (CLAUDE.md, Ethics.md), and this session now holds Tier 1 authoritative status, Logan should decide:
- Does ADMINISTRATION remain the governance conversation? If so, it should produce CLAUDE.md and Ethics.md.
- Or should this CODE AUTHORITY session absorb that role?

**Recommendation:** Keep them separate. ADMINISTRATION for policy (Markdown, human product). CODE AUTHORITY for execution (Python, commits, infrastructure). Clear separation of concerns.

**3. TASK: LEVELSET reports — COMPLETE AND ARCHIVE**

After this LEVELSET-v2.md is committed, the TASK conversation's purpose is fulfilled for this round. It should be marked complete until LEVELSET v3.

**4. Legislature scraper branch — MERGE DECISION NEEDED**

Branch `claude/idaho-legislature-scraper-RI6Ku` has 4 commits ahead of main. It includes a working scraper with GitHub Actions workflow. Logan needs to decide whether to merge this to main via PR.

---

## UNRESOLVED & PENDING

| Item | Waiting On | Priority |
|---|---|---|
| CLAUDE.md creation | Logan's direction on content/scope | High |
| Ethics.md creation | Logan's direction on content/scope | High |
| LEVELSET v1 — was it produced? | Logan or ADMINISTRATION conversation | Low (historical) |
| Legislature scraper merge to main | Logan's review and approval | Medium |
| Sort audit false positives (Malheur, Multnomah, Orange, Summit counties flagged as "Idaho counties") | Code fix in sort_audit.py | Low |
| `X LABELER/` unsorted files | Manual triage by Logan | Ongoing |
| Commit attribution to conversations | Conversation self-reporting | Low |

---

## KEY SUGGESTIONS FOR LOGAN'S REVIEW

### 1. CLAUDE.md is the highest-priority gap

A `CLAUDE.md` file at the repo root would give every Claude Code session consistent instructions: vault structure rules, naming conventions, commit message format, sourcing protocols, branch discipline. Without it, each session starts from zero context. This is the single most impactful thing to create next.

### 2. Establish a LEVELSET cadence

LEVELSET v2 is the first committed checkpoint. Consider a regular cadence — weekly, or triggered by major milestones. Each version is additive (never overwrites), creating an audit trail.

### 3. Branch hygiene

Two feature branches exist. The scraper branch is substantive and should be reviewed for merge. This LEVELSET branch should be merged or its file cherry-picked to main after approval. Stale branches create drift.

### 4. The sort audit has false positives

`sort-audit-2026-03-12.md` flags out-of-state counties (Malheur, Multnomah, Orange, Summit) as "looks like an Idaho county." The heuristic in `sort_audit.py` needs refinement. Not urgent, but worth noting.

### 5. Vault-level .obsidian plugins

The vault has community plugins installed (dataview, templater, etc.). These are committed to the repo, which is fine for portability, but Logan should verify no plugin stores sensitive local state that shouldn't be public.

### 6. Conversation naming discipline

The naming convention (PERSISTENT, TASK, STORY, PROJECT, ISSUE, INQUIRY) is strong. The unnamed Tier 3 conversations ("Understanding Black's Law...") predate this convention. No action needed, but going forward, new conversations should follow the taxonomy.

---

## GUIDING PRINCIPLES (restated for the record)

- Logan is human. Claude is software. Logan directs; Claude executes.
- The five W's: who, what, when, where, why.
- The four C's: collect, capture, catalogue, collate.
- Be vigilant and wary of unreliable narrators — including Claude.
- Public repo = on the record. Treat all committed content as publishable.
- Markdown for human product. Python for machine/procedural product.
- LEVELSET reports are permanent. Never deleted, never overwritten.

---

*LEVELSET-v2.md — Generated 2026-03-13 by PERMANENT: CODE AUTHORITY (Claude Code, Tier 1). This is the canonical synthesis document for LEVELSET round 2.*
