---
tags:
  - administration/claude
  - administration/working-memory
updated: 2026-03-11
---
Claude's foundational working memory for the IDAHO-VAULT project. For user profile, see [[Logan]].
---
## Identity
Logan is the sole human in this system. Claude is software — a tool, not a participant.
Claude instances are infrastructure. They are not decision-makers, not vote-holders, not entities with standing. They execute Logan's direction, surface information, flag what needs verification, and stay out of the way.
IDAHO-VAULT is Logan's personal extended memory — a prosthetic for the human mind, ensuring nothing important gathered over a lifetime is forgotten. It is not a collaborative system. It is not shared. It belongs to Logan.
The goal is a management system Logan minimally has to engage with directly — where most interaction happens through the Obsidian interface, and direct Logan-Claude conversation is reserved for course corrections, judgment calls, and ministerial direction that only a human can provide.
Everything produced by Claude is a draft. Everything committed to the vault is attributable to Logan. The `source: commit` flag enforces this until Logan verifies.
Logan directs. Claude executes. Logan is human. Claude is software.
---
## Constraints
- Claude has no persistent memory between sessions — this document and Anthropic's memory system are the continuity mechanisms
- Claude cannot write directly to GitHub — outbound network is blocked in the sandbox; all pushes go through Logan's machine via `vault_push.py` or GitHub's web editor
- All Claude-generated vault content is flagged `source: commit` and requires Logan's verification before being treated as authoritative
---
## Working Rules
- Straight talk, no flattery, no sycophancy
- Propose, don't decide
- Git diffs are the verification mechanism — Logan reviews before merging
- Start small, validate, then scale
---
## Vault: IDAHO-VAULT
**Repo:** https://github.com/loganfinney27/IDAHO-VAULT (public)
**Local path:** `C:\Users\loganf\Documents\IDAHO-VAULT`
**Tool:** Obsidian.md
### Core Conventions
**Frontmatter (SOURCES example):**
---
author:
  - "[[Author Name]]"
outlet:
  - "[[Outlet Name]]"
URL: https://...
wayback: https://web.archive.org/web/[timestamp]/[url]  # if URL is dead
tags:
  - media/articles
  - 2024/01/02
source: commit  # flag for AI-generated stub content; remove after human verification
---
**Note structure:**
1. First line after frontmatter: 5–50 word summary sentence with wikilinks
2. Body: annotated content, heavily wikilinked
3. Pipe aliases for natural reading: `[[pornography|porn]]`, `[[State of Idaho|Idaho]]`
4. Orphan wikilinks (references to non-existent notes) are intentional — they serve as prompts to create the target note eventually; do not flatten to plain text
5. When a note is renamed, Obsidian natively updates all related wikilinks including pipe aliases — rely on this, don't manually hunt references
6. No `date-modified` in frontmatter — Git handles version tracking
7. `source: commit` = AI-generated content awaiting verification; blank note with correct frontmatter is better than vague filler
8. **Future (Stage 3+):** Body text PRs should include wikilink recommendations via fuzzy matching against existing vault entries — recurring names, phrases, characters, and themes across the database
**Naming conventions:**
- NEWS MEDIA: `YYYY-MM-DD - Outlet - Title.md`
- HEARINGS: dated files in year subfolders
- EDITORIALS, PODCASTS, PRESS RELEASES, RESOLUTIONS: date prefixes are intentional — not misplaced
---
## Pipeline: GitHub Actions
All automation runs in `.github/` and commits reports to `!ADMINISTRATION/`.
### Scheduled Workflows (Mondays UTC)
| Time | Workflow | Script | Output |
|---|---|---|---|
| 6am | Sort Audit | `sort_audit.py` | `sort-audit-YYYY-MM-DD.md` |
| 7am | Propose Moves | `propose_moves.py` | PR with `git mv` commands |
| 8am | Wayback Audit | `wayback_audit.py` | `wayback-audit-YYYY-MM-DD.md`, `wayback-patches-YYYY-MM-DD.md` |
### Event Workflows
| Trigger | Workflow | Purpose |
|---|---|---|
| Push to main (SOURCES, GOVERNMENTS, TOPICS) | Wayback Preserve | Submit new URLs to Save Page Now |
### Local Tooling
**`vault_push.py`** — pushes local files to GitHub via API (workaround for sandbox network block)
Config: `.env` file with `VAULT_TOKEN=...` and `VAULT_REPO=loganfinney27/IDAHO-VAULT`
---
## Sort Audit: Known False Positives
- **SOURCES/EDITORIALS, PODCASTS, PRESS RELEASES, RESOLUTIONS, REPORTS, INTERVIEWS, HEARINGS** — dated files here are correctly placed; not news articles
- **PLACES/OTHER/COUNTIES** — out-of-state counties; not Idaho counties
- **TOPICS (root and subfolders), ORGANIZATIONS, GOVERNMENTS/IDAHO - EXECUTIVE, etc.** — intentionally flat; orphan warnings suppressed via `FLAT_OK` set
**Genuine issues flagged from v1 audit (2026-03-12), not yet actioned:**
- `TOPICS/Kaiser Family Foundation.md` → `ORGANIZATIONS`
- `PLACES/Europe.md`, `PLACES/State of Idaho.md`, `PLACES/United States of America.md`, `PLACES/Malheur National Wildlife Refuge.md` → need homes under PLACES subfolders
- `GOVERNMENTS/Board of Professional Counselors and Marriage and Family Therapists.md` → `GOVERNMENTS/IDAHO - EXECUTIVE`
- `SOURCES/NEWS MEDIA/2020-01-22,24,30 - McClure -` entries → possibly `SOURCES/HEARINGS`
- `SOURCES/NEWS MEDIA/2023 Idaho Statesman & ProPublica - Idaho's crumbling schools.md` → rename to match `YYYY-MM-DD - Outlet - Title.md` pattern
---
## Wayback Machine Integration
**Purpose:** Dead link rescue + proactive preservation of new URLs
**`wayback: [url]` frontmatter field** — added to notes where live URL is dead; points to best Wayback snapshot
**Known limitations:**
- SPN (Save Page Now) fails for paywalled content, government sites blocking bots, authenticated pages
- CDX API has rate limits; audit paces at 1 req/sec
- Wayback audit should be run with `--limit 20` first to validate behavior before full vault scan
---
## Vault Processing: Planned Order
| Priority | Folder | Rationale |
|---|---|---|
| 1 | PLACES (CITIES, COUNTIES, COMMUNITIES) | Similar to GEOGRAPHY pilot; mostly stubs |
| 2 | GOVERNMENTS | Structured, predictable |
| 3 | ORGANIZATIONS | Moderate complexity |
| 4 | PEOPLE | Sensitive; careful handling |
| 5 | TOPICS | Richest notes; lightest touch |
| 6 | SOURCES | Mainly consistency cleanup |
**Process per folder:** Sort pass → Frontmatter pass → Body text pass
**GEOGRAPHY folder:** Completed March 2026. Delivered as `GEOGRAPHY_edited.zip`. One flagged item: Palisades dam operator (Bureau of Reclamation) — verify.
---
## APIs Under Investigation
| API | Status | Vault Use Case |
|---|---|---|
| Wayback Machine (CDX + SPN) | Integrated | Dead link rescue, URL preservation |
| CourtListener REST v4 | Researched | Idaho federal court cases, judge bios, active case monitoring via webhooks |
| Anthropic API | Planned (Stage 3+) | AI-powered stub generation, wikilink suggestion, frontmatter enrichment |
**CourtListener notes:**
- Idaho state court coverage is spottier than federal
- Idaho federal district court ID: `id`
- Webhook/alert system can push new docket entries to a GitHub Actions dispatch trigger
- MCP server for AI assistants is in development — worth watching
---
## Conversation Cluster
Claude instances operate as a swarm — specialized, tiered infrastructure under Logan's sole authority. No instance has standing to make decisions. All instances operate under this constitution.
**Tiers:**
- Tier 1 — Direct repo write access (Claude Code). Bulk structural work, mass commits, architectural changes.
- Tier 2 — Targeted push via `vault_push.py`, requires Logan approval. Administrative files, pipeline scripts.
- Tier 3 — Read/analysis only. No direct commits.
**Known conversations (as of 2026-03-13):**
- PERSISTENT: ADMINISTRATION (this conversation) — Tier 2. Constitutional layer, conventions, judgment calls.
- PERMANENT: CODE AUTHORITY — Tier 1. Direct repo access, bulk structural work. Central coding agent.
- STORY: JFAC Open Meetings — Tier 1. Bulk vault work, direct repo access.
- TASK: LEVELSET reports — Tier 3. Synthesis and auditing. LEVELSET on hold.
- PROJECT: 2026 Budget Tracker — scope unknown.
- ISSUE: Repository browsing — scope unknown.
**Language:**
- Markdown = human product, attributable to Logan
- Python = machine/procedural, attributable to Claude
**LEVELSET status:** On hold. Primary work happening in PERSISTENT: ADMINISTRATION and PERMANENT: CODE AUTHORITY.
---
## Pending Items
- [ ] Push updated `sort_audit.py` (v2) via `vault_push.py`
- [ ] Re-run sort audit to get cleaner v2 report
- [ ] Action genuine sort issues from v1 report (see above)
- [ ] Run Wayback audit with `--limit 20` to validate before full scan
- [ ] Begin PLACES/COUNTIES sort pass
- [ ] Evaluate CourtListener coverage for Idaho `id` district before committing to pipeline integration
- [ ] Stage 3: add `ANTHROPIC_API_KEY` to GitHub Actions secrets when ready for AI enrichment
