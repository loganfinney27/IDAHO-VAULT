# LEVELSET-CURRENT — Live Ecosystem State

**Date:** 2026-03-13
**Status:** CURRENT — living synthesis, updated each LEVELSET round
**Synthesized by:** PERSISTENT: CODE AUTHORITY (Claude Code, Tier 1)
**Input authority chain:** LEVELSET-v2.md > DECISIONS.md > CLAUDE.md
**Approved by:** Pending Logan Finney review

---

## What This File Is

LEVELSET-CURRENT is the rolling synthesis document. Unlike numbered LEVELSET files (v1, v2, v3...) which are permanent snapshots, LEVELSET-CURRENT reflects the **present state** of the ecosystem. It is updated — not appended — each round. The numbered files remain the permanent audit trail.

**Relationship to other files:**
- **LEVELSET-v2.md** — Permanent snapshot from 2026-03-13. LEVELSET-CURRENT supersedes it as the live state but does not replace it.
- **DECISIONS.md** — Additive-only decision log. LEVELSET-CURRENT reads from it; new decisions flow to it.
- **CLAUDE.md** — Living vault authority. LEVELSET-CURRENT may surface corrections that flow back to CLAUDE.md as updates.

---

## ECOSYSTEM STATE

### Repository

| Field | Value |
|---|---|
| Remote | github.com/loganfinney27/IDAHO-VAULT (public) |
| Primary branch | `origin/main` at `364c2bd` |
| Feature branches | `claude/idaho-legislature-scraper-RI6Ku` (4 commits ahead of main) |
| | `claude/levelset-multi-conversation-zWxJc` (6 commits ahead of main) |
| Total commits | 19 (as of this synthesis) |
| Last commit | `f8a0370` — CLAUDE.md + DECISIONS.md |

### Branch Status

| Branch | Purpose | Commits Ahead | Merge Status |
|---|---|---|---|
| `claude/idaho-legislature-scraper-RI6Ku` | Legislature scraper + GitHub Actions | 4 | **Awaiting Logan's review** |
| `claude/levelset-multi-conversation-zWxJc` | LEVELSET process + CLAUDE.md + DECISIONS.md | 6 | **Awaiting Logan's review** |

### Infrastructure Inventory

| Asset | Type | Location | Status |
|---|---|---|---|
| `CLAUDE.md` | Administrative | Repo root | **NEW** — on feature branch, not yet on main |
| `LEVELSET-v2.md` | Administrative | `!ADMINISTRATION/` | Committed, feature branch |
| `DECISIONS.md` | Administrative | `!ADMINISTRATION/` | Committed, feature branch, 5 entries |
| `sort_audit.py` | Python | `.github/scripts/` | On main, operational |
| `sort-audit.yml` | YAML | `.github/workflows/` | On main, manual trigger |
| `sort-audit-2026-03-12.md` | Markdown output | `!ADMINISTRATION/` | On main |
| `idaho_leg_scraper.py` | Python | `.github/scripts/` | Feature branch, not yet on main |
| `post_digest.py` | Python | `.github/scripts/` | Feature branch, not yet on main |
| `idaho-leg-scraper.yml` | YAML | `.github/workflows/` | Feature branch, daily cron + manual |
| `.gitignore` | Config | Repo root | Feature branch |

### Corrections to LEVELSET-v2

The following items from LEVELSET-v2.md are now stale:

1. **"CLAUDE.md — No repository-level instruction file exists"** — Corrected. CLAUDE.md was created at commit `f8a0370` on feature branch `claude/levelset-multi-conversation-zWxJc`. Not yet on main.
2. **"Ethics.md — No vault ethics policy exists"** — Still true. No Ethics.md has been created.
3. **Total commits listed as 17** — Now 19 on this branch (LEVELSET-v2 commit + CLAUDE.md/DECISIONS.md commit).

---

## CONVERSATION CENSUS

### Tier 1 — Direct Write Access

| Conversation | Role | Known Output | Current Status |
|---|---|---|---|
| **PERSISTENT: CODE AUTHORITY** | Authoritative code session; LEVELSET synthesis; infrastructure | LEVELSET-v2.md, LEVELSET-CURRENT.md, CLAUDE.md, DECISIONS.md | **Active** — executing Option A synthesis |

### Tier Unknown — Reports Not Yet Received

| Conversation | Presumed Role | Known Output | Gap |
|---|---|---|---|
| **PERSISTENT: ADMINISTRATION** | Vault governance, policy | Nothing committed to repo | No LEVELSET report received. Role overlap with CODE AUTHORITY needs resolution. |
| **TASK: LEVELSET reports** | Synthesis routing hub | Distributed LEVELSET v2 prompt; produced Option A/B/C sequencing recommendation | Active but role may be fulfilled after this round |
| **STORY: JFAC Open Meetings** | Journalism story development | Cache block delivered 2026-03-13. People updates, verified facts, open tasks, lessons learned, architectural decisions, transcript protocols. | **Incorporated** into this synthesis. |
| **PROJECT: 2026 Budget Tracker** | Budget tracking | Unknown | No report received |
| **ISSUE: Repository browsing** | Repo navigation | Unknown | No report received |

### Tier 3 — Context/Research (dormant)

| Conversation | Role | Action Needed |
|---|---|---|
| Idaho Public Television overview | IPTV background | None |
| Idaho Reports episode production | Production workflow | None |
| Understanding Black's Law diction... | Legal terminology | None |
| Interpreting an unclear concept | Research | None |
| In the Blink of an Eye book recom... | Craft reference | None |
| INQUIRY: Adobe Premiere Pro | Production software | None |

**Consolidation assessment (unchanged from LEVELSET-v2):** Tier 3 conversations are dormant reference. No consolidation needed. If Logan wants durable notes extracted from any of them into vault Markdown files, that can be done on request.

---

## DECISIONS CURRENT STATE

Twelve decisions logged in DECISIONS.md (all 2026-03-13):

1. LEVELSET protocol established
2. CLAUDE.md created
3. Conversation taxonomy adopted
4. File type attribution rules
5. Sort audit and legislature scraper deployed
6. Option A sequencing for LEVELSET synthesis
7. LEVELSET-CURRENT as rolling synthesis document
8. *(reserved)* — PERSISTENT: CODE AUTHORITY designation — **HELD** pending session type taxonomy definition (#13)
9. LEVELSET promoted to persistent state layer
10. Session-open and session-close protocols defined (implementation pending full adoption)
11. Task assignment lives in !ADMINISTRATION, not conversation memory
12. Handoff/handshake built into LEVELSET workflow
13. Session type taxonomy needs formal definition (open task)

### Decisions Held

| # | Decision | Condition | Status |
|---|---|---|---|
| 8 | PERSISTENT: CODE AUTHORITY designation | Contingent on #13 taxonomy work producing a formal definition that includes CODE AUTHORITY | **HELD** — not in DECISIONS.md |

---

## JFAC OPEN MEETINGS — SESSION CONTRIBUTION (2026-03-12)

Source: STORY: JFAC Open Meetings session cache block, routed by Logan 2026-03-13.

### Project Status

| Field | Value |
|---|---|
| Story | JFAC working groups / open meetings |
| CCA letter deadline | ~2026-03-18 |
| Sunshine Week | 2026-03-15 through 2026-03-21 |
| Draft exists | 3-10_JFAC_working_groups_-1.docx |
| Editorial constraint | IPTV state agency status; [[Clark Corbin]] (Idaho Capital Sun) carries primary byline burden |

### People Updates

**[[Kyle Harris]]** — CORRECTED
- Was: conflated with [[Mark Harris]]
- Now: Junior House member, Lewiston (House)
- Action needed: Vault note needs first name correction, separate entry from [[Mark Harris]]

**[[Mark Harris]]** — Senior Senate member, Soda Springs area (Senate)
- Interview still needed
- Expressed frustration at Monday JFAC hearing re working groups — pull Idaho In Session archive

**[[Cornel Rasor]]** — NAY on S1331 confirmed from vote board image
- Pattern: NAY on Rule 27 suspension + NAY on S1331
- Interview priority: Friday, Mason's Manual angle

**[[Britt Raybould]]** — NAY on S1331 confirmed from vote board image
- Interview priority: Friday hallway catch only

**Rep. Bruce** — NEW
- First year on JFAC
- Working group assignments top-down from leadership, no member input confirmed
- On record favoring transparency: "I've always been for more transparency" [AUDIO VERIFICATION REQUIRED]

**[[Dustin Manwaring]]** — AYE on S1331 (read from vote board, one Manwaring in House, high confidence)
- On record: "I'm a sunshine person" [AUDIO VERIFICATION REQUIRED]
- On record: "Should it be an open and public process — I would air that, I would be fine with that personally" [AUDIO VERIFICATION REQUIRED]

**[[Wintrow]]** — CORRECTION
- Previous entry assigned role "Senate President Pro Tem / Anthon's number two" — **THIS WAS FABRICATED, no source basis**
- Actual role: unconfirmed, needs verification
- [[Kelly Anthon]] is Senate President Pro Tem

### Verified Facts (sourced, not yet audio-verified for quotes)

1. Working group assignment sheet exists, distributed to all JFAC members (Cook, Woodward-and-Cook transcript)
2. Active quorum management confirmed on record (Woodward-and-Cook transcript)
3. Working group assignments come from leadership, not member preference (Bruce transcript)
4. No parliamentary appeal of working group decisions on record (Cook: "not that I know of")
5. JFAC rules never voted on by full committee per Cook (Woodward-and-Cook transcript)

### Pending Verification Queue

All items below are **HARD GATES** before publication:

| Quote / Claim | Speaker | Source | Status |
|---|---|---|---|
| "Without a TV or a microphone" | Speaker 3 (identity unknown) | Transcript | SPEAKER UNVERIFIED |
| "The rules were never voted on by the committee" | Cook | Woodward-and-Cook transcript | AUDIO VERIFICATION REQUIRED |
| "I'm a sunshine person" | Manwaring | Interview | AUDIO VERIFICATION REQUIRED |
| "Should it be an open and public process — I would air that" | Manwaring | Interview | AUDIO VERIFICATION REQUIRED |
| "I've always been for more transparency" | Bruce | Interview | AUDIO VERIFICATION REQUIRED |
| All Woodward-and-Cook speaker IDs | Speaker 2 vs Speaker 3 | Transcript | IDENTITY UNVERIFIED |

### Open Tasks (from JFAC session)

| Task | Owner | Status | Gate |
|---|---|---|---|
| Correct [[Kyle Harris]] vault note (first name, chamber) | Any session | PENDING | — |
| New vault note: [[Cornel Rasor]] | Any session | PENDING | — |
| New topic note: House Rule 27 | Any session | PENDING | — |
| Working group assignment sheet records request | Logan | PENDING | — |
| Pull Idaho In Session: Kyle Harris Monday JFAC hearing | Logan | PENDING | — |
| Audio verify all 2026-03-10 transcript quotes | Logan | HARD GATE | Pre-pub |
| Grow/Tanner interview — public access question | Logan | PENDING | Mar 18 |
| [[Mark Harris]] interview | Logan | PENDING | — |
| Patch increment 2 (Monks, Rasor, Rule 27, 2024-01-09 IR) | Any session | PENDING | — |
| Vault patch collision check (vault-deploy.zip) | Repo session | BLOCKED | Pre-commit |
| BIN processing pipeline architecture | Audio session | ASSIGNED | — |

### Transcript Processing Protocols

**Google Recorder .txt files:**
- Speaker tags non-persistent, identity-unverified by definition
- All quotes: SPEAKER UNVERIFIED until human audio check
- Re-processing must start from vault note, not raw file
- Verification gate covers both speaker ID and quote accuracy

**Adobe Premiere Pro transcripts:**
- Read-only. Syntax must be preserved for editorial re-import
- No vault notes derived until format protocol defined by Logan
- Separate processing protocol required before Claude handling

**Blocking dependency:** [[Audrey Dutton]] — Idaho reporter. Source relationship to cultivate. Peer with likely applicable experience in AI-assisted transcript processing and bulk research workflows. Reporter-to-reporter conversation needed before pipeline architecture is finalized. Not a tool dependency — a human expertise node.

### Lessons Learned (2026-03-12 session)

Four failure modes identified — permanent record, never delete:

1. **Context-triggered confabulation** — Claude fabricated Wintrow's role based on contextual inference, not source material
2. **Verification flag stripping** — Unverified speaker IDs lost their flags during processing
3. **Misattribution within auto-generated transcript** — Google Recorder speaker tags are not reliable identity markers
4. **Inference presented as sourced record** — Claude treated its own inferences as if they were sourced facts

### Idaho Reports Byline Archive

- 268 posts, 23 pages at blog.idahoreports.idahoptv.org
- Earliest: November 2020
- Vault captures approximately 1% of published output
- Two high-priority missing pieces:
  - 2024-03-29: "Open meetings law questioned with tense budget season" (direct prior reporting on JFAC/open meetings)
  - 2024-03-11: "Senate pushes to re-adopt JFAC rules"
- Both need vault notes in SOURCES/NEWS MEDIA

---

## SOURCING & SENSITIVITY

Updated with JFAC session incorporation:

- All committed content is on the record
- No background-sourced material identified in repo
- No off-the-record material held by this session
- JFAC session cache block received and incorporated — all material in the block was provided by Logan for on-the-record inclusion
- Multiple quotes flagged AUDIO VERIFICATION REQUIRED — these are on the record but **not publication-ready** until verification clears

---

## UNRESOLVED & PENDING

### Awaiting Logan

| Item | Priority | Notes |
|---|---|---|
| ~~Review 8 pending decisions (#6–#13) for DECISIONS.md~~ | ~~**High**~~ | **DONE** — 7 approved and appended. #8 held pending #13 taxonomy work. |
| Merge feature branches to main | **High** | Both branches have substantive work. CLAUDE.md on main is the highest-impact merge. |
| Audio verify JFAC quotes (5 quotes + speaker IDs) | **High** | HARD GATE for publication. See Pending Verification Queue above. |
| Ethics.md creation | Medium | No draft exists anywhere in the ecosystem |
| LEVELSET cadence decision | Medium | Weekly? Milestone-triggered? Needs a standing rule. |

### Awaiting Other Conversations

| Item | Source | Notes |
|---|---|---|
| ~~JFAC Open Meetings session cache block~~ | ~~STORY: JFAC Open Meetings~~ | **RECEIVED** — incorporated this round |
| LEVELSET reports from other conversations | All active conversations | Most conversations have not submitted reports |

### Known Technical Issues

| Issue | Priority | Notes |
|---|---|---|
| Sort audit false positives | Low | Out-of-state counties flagged as Idaho counties in `sort_audit.py` |
| `X LABELER/` unsorted files | Ongoing | Manual triage by Logan |
| Legislature scraper not on main | Medium | Daily cron won't fire until branch is merged |

---

## WHAT THIS SYNTHESIS IS MISSING

Transparency about gaps — this section exists so Logan and other conversations know exactly what's thin:

1. ~~**JFAC Open Meetings session context**~~ — **RESOLVED.** Cache block received and incorporated 2026-03-13. People updates, verified facts, open tasks, lessons learned, architectural decisions, and transcript processing protocols now in this document.

2. **LEVELSET reports from 9 of 11 conversations** — Only CODE AUTHORITY (this session) and TASK: LEVELSET reports have actively participated. The other conversations' states are inferred, not reported.

3. **PERSISTENT: ADMINISTRATION context** — This conversation's role, outputs, and decisions are entirely unknown to this session. It may hold policy decisions that should be in DECISIONS.md.

4. **PROJECT: 2026 Budget Tracker state** — Unknown scope, architecture, data sources, progress.

5. **Historical LEVELSET v1** — Whether it existed and what it contained remains unverified.

6. **Audio verification for all JFAC quotes** — Five quotes and full Woodward-and-Cook speaker ID verification are HARD GATES before publication. Only Logan can clear these.

---

## NEXT ACTIONS FOR THIS SESSION

1. ~~Commit LEVELSET-CURRENT.md to separate branch~~ — Done
2. ~~Wait for JFAC session cache block from Logan~~ — Received and incorporated
3. ~~Flag Logan for review of 8 pending decisions~~ — Done
4. ~~Append 7 approved decisions to DECISIONS.md~~ — Done (#8 held)
5. Coordinate merge to `claude/levelset-multi-conversation-zWxJc` and ultimately to main
6. Complete #13 taxonomy definition work, then unblock #8

---

*LEVELSET-CURRENT.md — Synthesized 2026-03-13, updated 2026-03-13 (JFAC session incorporation) by PERSISTENT: CODE AUTHORITY. This is a living document, updated each LEVELSET round. For the permanent audit trail, see numbered LEVELSET files in this directory.*
