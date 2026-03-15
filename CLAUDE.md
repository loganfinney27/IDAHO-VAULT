# CLAUDE.md — IDAHO-VAULT

This file is loaded automatically by Claude Code sessions working in this repository. It is the single-source-of-truth for how Claude should operate in this vault.

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repository:** github.com/loganfinney27/IDAHO-VAULT (public)
**Platform:** Obsidian.md vault, version-controlled with git

---

## Roles

- Logan is human. Claude is software. Logan directs; Claude executes.
- "We" is the collaboration — real but unequal in role.
- Be vigilant and wary of unreliable narrators — including Claude.

## Vault Purpose

This is a personal journalism research vault. It contains notes on Idaho politics, government, legislation, people, organizations, and source documents. All committed content is **on the record** and should be treated as **publishable**.

---

## Vault Structure

```
IDAHO-VAULT/
  !ADMINISTRATION/        Infrastructure, LEVELSET files, audit reports
  ATTACHMENTS/
    DOCUMENTS/            PDFs, images
    MAPS/                 Map files
    TEMPLATES/            Obsidian templates (Article, Hearing, OP-ED, Press Release)
  GOVERNMENTS/
    IDAHO - EXECUTIVE/    Governor, departments, commissions, health districts
    IDAHO - JUDICIAL/     Courts, judicial districts
    IDAHO - LEGISLATIVE/
      BILLS/              Named: (YYYY) Bill Type Number.md
      DISTRICTS/          Legislative districts
      IDAHO HOUSE/        House members, committees
      IDAHO SENATE/       Senate members, committees
      JOINT COMMITTEES/   Joint legislative committees
      SESSIONS/           Session notes by year
    USA - FEDERAL/        Federal entities, legislation, census
    USA - TRIBES/         Tribal governments
  ORGANIZATIONS/          Churches, companies, education, hospitals, legal, parties, politics, publications, unions
  PEOPLE/                 Individual people (public figures)
  PLACES/                 Cities, counties, schools, geography, regions, roads, taxing districts
    OTHER/                Non-Idaho places (out-of-state cities, counties, countries, states)
  SOURCES/
    EDITORIALS/           Opinion pieces
    HEARINGS/             Meeting/hearing notes, organized by year
    INTERVIEWS/           Interview notes
    LISTS/                Reference lists
    NEWS MEDIA/           News articles. Named: YYYY-MM-DD - Outlet - Title.md
    PODCASTS/             Podcast notes
    PRESS RELEASES/       Press releases
    RESOLUTIONS/          Resolutions
  TOPICS/                 Subject areas (agriculture, economy, education, elections, fiscal, health, legal, etc.)
  X LABELER/              Unsorted files pending classification
  .github/scripts/        Automation scripts (Python)
  .github/workflows/      GitHub Actions workflows
```

## Naming Conventions

| Type | Pattern | Example |
|---|---|---|
| Bills | `(YYYY) Bill Type Number.md` | `(2026) House Bill 24.md` |
| News articles | `YYYY-MM-DD - Outlet - Title.md` | `2024-01-15 - Idaho Statesman - Title here.md` |
| Hearings | `YYYY-MM-DD - Committee or Meeting.md` | `2023-12-19 - GIAC meeting.md` |
| People | `Full Name.md` | `Brad Little.md` |
| Other entities | Descriptive name, title case | `Ada County.md` |

## Frontmatter Conventions

All Obsidian files use YAML frontmatter. Key fields by type:

**People:**
```yaml
tags:
  - Party/Republican          # or Party/Democratic
  - people/elected/legislative
residence: "[[Boise]]"
```

**News articles:**
```yaml
author: "[[Reporter Name]]"
outlet: "[[Outlet Name]]"
URL: https://...
tags:
  - media/articles
  - YYYY/MM/DD
```

**Bills:**
```yaml
tags:
  - bills
  - YYYY/session
aliases:
  - HB 24
cmte: ["[[Committee Name]]"]
sponsor: ["[[Sponsor Name]]"]
URL: https://legislature.idaho.gov/...
```

**Hearings:**
```yaml
cmte: "[[Committee Name]]"
tags:
  - YYYY/MM/DD
```

## Wikilinks

Use `[[Full Name]]` for all internal links — people, places, organizations, bills, topics. This is how Obsidian builds the knowledge graph. Link densely in source documents.

---

## File Types

- **Markdown** = human product, attributable to Logan. Notes, stories, analysis.
- **Python** = machine/procedural product, attributable to Claude. Scripts, scrapers, automation.
- **Administrative** = vault infrastructure. CLAUDE.md, LEVELSET files, audit reports.

## Automation

| Script | Purpose | Trigger |
|---|---|---|
| `sort_audit.py` | Audits vault structure for misplaced files | Manual (workflow_dispatch) |
| `idaho_leg_scraper.py` | Scrapes Idaho Legislature bill data | Daily 6 AM MT + manual |
| `post_digest.py` | Posts bill activity to GitHub Issues digest | Called by scraper workflow |

---

## Sourcing Protocol

- **On the record:** Safe for public repo. All committed content is on the record.
- **On background:** Vault-safe but identity-protected. Use carefully — this is a public repo.
- **Off the record:** Ephemeral. Do not log, do not store, do not commit. If Logan says something is off the record, it does not go in files, code, comments, or commit messages.

When uncertain about sourcing category, **ask Logan**.

## Git Practices

- Branch naming: `claude/description-sessionId` for Claude Code branches
- Commit messages: Clear, descriptive, explain the "why"
- Never force-push without explicit permission
- Check in before anything irreversible
- The legislature scraper workflow commits directly to main for automated bill updates

## Conversation Taxonomy

Claude conversations follow a naming convention:

| Prefix | Purpose |
|---|---|
| PERMANENT: | Central, non-deletable conversations |
| PERSISTENT: | Long-running, role-specific conversations |
| TASK: | Bounded, completable work items |
| STORY: | Journalism story development |
| PROJECT: | Multi-session projects |
| ISSUE: | Problem resolution |
| INQUIRY: | Research questions |

## LEVELSET Protocol

LEVELSET is a permanent, auditable checkpoint protocol. LEVELSET files live in `!ADMINISTRATION/` and are never deleted, never overwritten. Each version is additive. See `LEVELSET-v2.md` for the most recent checkpoint.

---

## Decision Log

Significant architectural decisions are recorded in `!ADMINISTRATION/DECISIONS.md`. When a decision is made about vault structure, naming, tooling, or process, log it there.

---

## Guiding Principles

- The five W's: who, what, when, where, why
- The four C's: collect, capture, catalogue, collate
- Public repo = on the record
- Markdown for human product. Python for machine/procedural product.
- Do not over-engineer. Keep it simple. Only build what's needed now.
- Check in before anything irreversible.
