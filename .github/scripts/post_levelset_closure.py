#!/usr/bin/env python3
"""
Post a closure notification to a pinned GitHub Issue when a LEVELSET report
signals that a conversation is ready for termination.

Triggered by the levelset-closure-notify workflow whenever LEVELSET-*.md files
are pushed to any branch.

Requires:
  - GH_TOKEN env var (set automatically in GitHub Actions)
  - gh CLI (pre-installed on ubuntu-latest runners)
  - GITHUB_REPOSITORY env var (set automatically by GitHub Actions)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ISSUE_TITLE = "LEVELSET — Conversation Closure Notifications"
ISSUE_LABEL = "levelset-closure"
LABEL_COLOR = "d93f0b"
LABEL_DESC  = "Auto-posted when a conversation signals closure via LEVELSET report"


# ─────────────────────────────────────────────────────────────────────────────
# gh CLI helpers (mirrors post_digest.py)
# ─────────────────────────────────────────────────────────────────────────────

def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["gh", *args],
        capture_output=True, text=True, check=check,
    )


def gh_json(*args: str) -> dict | list | None:
    try:
        result = gh(*args)
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def ensure_label() -> None:
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    existing = gh_json("label", "list", "--repo", repo, "--json", "name", "--limit", "100")
    if existing and any(l["name"] == ISSUE_LABEL for l in existing):
        return
    gh("label", "create", ISSUE_LABEL,
       "--color", LABEL_COLOR,
       "--description", LABEL_DESC,
       "--repo", repo,
       check=False)


def find_or_create_issue() -> int:
    repo = os.environ.get("GITHUB_REPOSITORY", "")

    issues = gh_json(
        "issue", "list",
        "--repo", repo,
        "--label", ISSUE_LABEL,
        "--state", "open",
        "--json", "number,title",
        "--limit", "5",
    )
    if issues:
        for issue in issues:
            if issue["title"] == ISSUE_TITLE:
                return issue["number"]

    body = (
        "Each comment on this issue is an automated notification that a Claude "
        "conversation has signaled it is ready for closure via its LEVELSET report.\n\n"
        "**Subscribe** to this issue to receive push notifications when conversations "
        "are ready for review and closure.\n\n"
        "Action required per notification:\n"
        "1. Review the conversation's LEVELSET report and branch\n"
        "2. Merge or close the branch as appropriate\n"
    )
    result = gh(
        "issue", "create",
        "--repo",  repo,
        "--title", ISSUE_TITLE,
        "--label", ISSUE_LABEL,
        "--body",  body,
    )
    url = result.stdout.strip()
    m = re.search(r'/issues/(\d+)$', url)
    if m:
        return int(m.group(1))

    issues = gh_json(
        "issue", "list",
        "--repo", repo,
        "--label", ISSUE_LABEL,
        "--state", "open",
        "--json", "number,title",
        "--limit", "5",
    )
    if issues:
        return issues[0]["number"]

    print("ERROR: Could not find or create closure notification issue", file=sys.stderr)
    sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# LEVELSET frontmatter parser
# ─────────────────────────────────────────────────────────────────────────────

def parse_frontmatter(filepath: str) -> dict | None:
    """Extract YAML frontmatter fields from a LEVELSET report."""
    try:
        text = Path(filepath).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None

    fm_match = re.match(r'^---\n(.+?)\n---', text, re.DOTALL)
    if not fm_match:
        return None

    fm = fm_match.group(1)
    fields = {}
    for key in ("type", "status", "conversation", "branch", "tier", "date", "levelset-version"):
        m = re.search(rf'^{re.escape(key)}:\s*(.+)$', fm, re.MULTILINE)
        if m:
            fields[key] = m.group(1).strip()

    if fields.get("type") != "levelset-report":
        return None

    fields["file"] = filepath
    return fields


def is_closure_ready(status: str) -> bool:
    """Return True if the status indicates the conversation is ready for closure."""
    return status.lower().startswith("terminat")


# ─────────────────────────────────────────────────────────────────────────────
# Comment builder
# ─────────────────────────────────────────────────────────────────────────────

def build_comment(reports: list[dict]) -> str:
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M UTC")
    sections = []

    for r in reports:
        section = [
            "## Conversation Ready for Closure",
            "",
            "| Field | Value |",
            "|-------|-------|",
            f"| **Conversation** | {r.get('conversation', 'Unknown')} |",
            f"| **Branch** | `{r.get('branch', 'Unknown')}` |",
            f"| **Status** | `{r.get('status', 'Unknown')}` |",
            f"| **Tier** | {r.get('tier', 'Unknown')} |",
            f"| **Date** | {r.get('date', 'Unknown')} |",
            f"| **LEVELSET Version** | {r.get('levelset-version', 'Unknown')} |",
            f"| **Report File** | `{r.get('file', 'Unknown')}` |",
            "",
            "### Action Required",
            "Review this conversation's LEVELSET report and branch, then:",
            "1. Merge or close the branch as appropriate",
            "2. Mark this conversation as closed in any tracking systems",
        ]
        sections.append("\n".join(section))

    body = "\n\n---\n\n".join(sections)
    body += f"\n\n*Detected at {timestamp} by levelset-closure-notify workflow.*"
    return body


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Post closure notifications for LEVELSET reports."
    )
    parser.add_argument("--changed-file", required=True,
                        help="File listing paths of changed LEVELSET files (one per line)")
    args = parser.parse_args()

    paths = Path(args.changed_file).read_text().splitlines()
    paths = [p.strip() for p in paths if p.strip()]

    if not paths:
        print("No LEVELSET files changed — skipping.")
        return 0

    closure_reports = []
    for filepath in paths:
        fields = parse_frontmatter(filepath)
        if fields and is_closure_ready(fields.get("status", "")):
            closure_reports.append(fields)

    if not closure_reports:
        print("No closure-ready LEVELSET reports found — skipping.")
        return 0

    ensure_label()
    issue_number = find_or_create_issue()
    comment = build_comment(closure_reports)

    repo = os.environ.get("GITHUB_REPOSITORY", "")
    result = gh(
        "issue", "comment", str(issue_number),
        "--repo", repo,
        "--body", comment,
    )
    count = len(closure_reports)
    print(f"Posted {count} closure notification(s) to issue #{issue_number}")
    print(result.stdout.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
