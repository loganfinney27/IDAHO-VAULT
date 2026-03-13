# Decision Log — IDAHO-VAULT

Significant architectural decisions, recorded when made. Each entry is permanent.

---

## 2026-03-13 — LEVELSET protocol established

**Decision:** Adopt LEVELSET as the permanent checkpoint protocol for the vault ecosystem. LEVELSET files are stored in `!ADMINISTRATION/`, are never deleted, never overwritten. Each version is additive.
**Context:** Multiple Claude conversations operating concurrently needed a synchronization mechanism.
**Decided by:** Logan Finney

## 2026-03-13 — CLAUDE.md created

**Decision:** Create a `CLAUDE.md` at repo root to give all Claude Code sessions consistent context about vault structure, naming conventions, sourcing protocols, and operating principles.
**Context:** Claude Code sessions were starting with no context about the vault's architecture, leading to repeated discovery work.
**Decided by:** Logan Finney, drafted by PERSISTENT: CODE AUTHORITY

## 2026-03-13 — Conversation taxonomy adopted

**Decision:** Claude conversations follow a naming prefix convention: PERSISTENT, TASK, STORY, PROJECT, ISSUE, INQUIRY.
**Context:** Multiple concurrent conversations needed clear role differentiation.
**Decided by:** Logan Finney

## 2026-03-13 — File type attribution

**Decision:** Markdown files are human product (Logan). Python files are machine/procedural product (Claude). Administrative files are vault infrastructure.
**Context:** Public repo needs clear attribution of authorship.
**Decided by:** Logan Finney

## 2026-03-13 — Sort audit and legislature scraper deployed

**Decision:** Automated vault maintenance via GitHub Actions — `sort_audit.py` for structure auditing, `idaho_leg_scraper.py` for daily bill data, `post_digest.py` for activity digests.
**Context:** Manual bill tracking is unsustainable during legislative session.
**Decided by:** Logan Finney

## 2026-03-13 — Option A sequencing for LEVELSET synthesis

**Decision:** CODE AUTHORITY session owns LEVELSET synthesis. TASK: LEVELSET provides content routing. Logan routes cache blocks between conversations.
**Context:** Three options evaluated (A: CODE AUTHORITY synthesizes, B: TASK conversation synthesizes, C: new dedicated session). Option A chosen for directness — the session with repo write access produces the synthesis.
**Decided by:** Logan Finney
**Source session:** PERSISTENT: CODE AUTHORITY

## 2026-03-13 — LEVELSET-CURRENT as rolling synthesis document

**Decision:** LEVELSET-CURRENT.md is a living document updated each LEVELSET round, distinct from numbered LEVELSET files (v1, v2, v3...) which are permanent snapshots. LEVELSET-CURRENT reflects present state; numbered files are the audit trail.
**Context:** Needed a way to maintain current ecosystem state without proliferating snapshot files for every minor update.
**Decided by:** Logan Finney
**Source session:** PERSISTENT: CODE AUTHORITY

## 2026-03-13 — LEVELSET promoted to persistent state layer

**Decision:** LEVELSET is canonical shared memory for all Claude instances. All sessions read on open, write on close.
**Context:** Claude conversations lack persistent memory across sessions. LEVELSET files in `!ADMINISTRATION/` serve as the durable synchronization layer.
**Decided by:** Logan Finney
**Source session:** STORY: JFAC Open Meetings, 2026-03-12

## 2026-03-13 — Session-open and session-close protocols defined

**Decision:** Session-open: fetch LEVELSET-CURRENT, read fully, confirm to Logan. Session-close: produce labeled cache block, hand to Logan for routing. Defined, implementation pending full adoption across all session types.
**Context:** Without consistent open/close behavior, sessions would drift from shared state and produce redundant or conflicting work.
**Decided by:** Logan Finney
**Source session:** STORY: JFAC Open Meetings, 2026-03-12

## 2026-03-13 — Task assignment lives in !ADMINISTRATION, not conversation memory

**Decision:** Persistent task tracking belongs in committed files in `!ADMINISTRATION/`, not in ephemeral conversation context.
**Context:** Tasks assigned in conversation would be lost when context windows expired or sessions ended. Committed files survive across all sessions.
**Decided by:** Logan Finney
**Source session:** STORY: JFAC Open Meetings, 2026-03-12

## 2026-03-13 — Handoff/handshake built into LEVELSET workflow

**Decision:** Session handoff is not a separate procedure — it IS the session-open protocol. Reading LEVELSET-CURRENT on open constitutes the handshake.
**Context:** Attempted to define handoff as a distinct step; recognized it was redundant with the session-open protocol already defined.
**Decided by:** Logan Finney
**Source session:** STORY: JFAC Open Meetings, 2026-03-12

## 2026-03-13 — Session type taxonomy needs formal definition

**Decision:** The current informal session type prefixes (PERSISTENT, TASK, STORY, PROJECT, ISSUE, INQUIRY) require formal definitions including scope, lifecycle, and privileges for each type. This is a decision to formalize, not a formalization itself.
**Context:** Session types are in active use but not defined. Ambiguity about what each type means leads to role overlap (e.g., PERSISTENT: ADMINISTRATION vs PERSISTENT: CODE AUTHORITY).
**Decided by:** Logan Finney
**Source session:** STORY: JFAC Open Meetings, 2026-03-12
**Status:** Open task — taxonomy definition work pending
