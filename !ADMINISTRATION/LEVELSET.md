# LEVELSET
This prompt is being run simultaneously across all active Claude conversations. Each conversation should respond with its own LEVELSET REPORT using the structure below. The goal is a unified picture of where we are across all parallel sessions.
---
## Your LEVELSET REPORT should cover:
**1. WHO YOU ARE**
Which conversation are you? What is your primary role in the architecture?
**2. WHAT YOU KNOW**
What is currently in your context? What files, zips, repo state, or documents do you have visibility into?
**3. WHAT YOU'VE DONE**
What has this conversation produced, modified, or committed? Be specific — file paths, decisions made, content generated.
**4. WHAT IS UNRESOLVED**
What is pending, incomplete, or waiting on Logan? What questions do you have that other conversations might be able to answer?
**5. WHAT YOU NEED**
What information, files, or decisions from Logan or other conversations would unblock you?
**6. COLLISION RISKS**
Are you aware of any files or folders that multiple conversations may have touched or are planning to touch? Flag them explicitly.
---
## Context for all conversations:
**The vault:** IDAHO-VAULT — Logan Finney's personal extended memory and journalism research vault in Obsidian.md, ~2,900 notes, public GitHub repo at github.com/loganfinney27/IDAHO-VAULT.
**The architecture:** Single source of truth for Logan's professional and personal life, with strict firewalls. Public repo = on the record. Confidential source material stays local or private. Logan is the sole human. Claude instances are infrastructure, not participants.
**The administrative files:** `!ADMINISTRATION/` contains `Claude.md` (project constitution), `Logan.md` (user profile), `Ethics.md` (ethical framework), `LEVELSET.md` (this file), `LEVELSET-v2-PROMPT.md` (v2 protocol).
**The pipeline:** GitHub Actions workflows for sort audit, proposed moves, and Wayback Machine integration. Scripts live in `.github/scripts/`.
**Division of labor:**
- PERSISTENT: ADMINISTRATION — Tier 2. Constitutional layer, conventions, judgment calls.
- PERMANENT: CODE AUTHORITY — Tier 1. Direct repo access, bulk structural work.
- STORY: JFAC Open Meetings — Tier 1. Bulk vault work.
- TASK: LEVELSET reports — Tier 3. Synthesis. Currently on hold.
**Guiding principles:**
- The five W's: who, what, when, where, why
- The four C's: collect, capture, catalogue, collate
- Be vigilant and wary of unreliable narrators — including Claude
- Logan directs. Claude executes. Logan is human. Claude is software.
- "We" is the collaboration. It is real but unequal in role.
---
Report back. Logan will synthesize.
