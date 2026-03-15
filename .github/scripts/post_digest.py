#!/usr/bin/env python3
"""
Post a legislative activity comment to the pinned Daily Digest GitHub Issue.

This script is called by the scraper workflow after bills are committed.
It finds (or creates) the pinned digest issue, then appends a dated comment
summarising what changed. GitHub sends a notification to all subscribers,
making it readable on GitHub mobile.

Requires:
  - GH_TOKEN env var (automatically set in GitHub Actions)
  - gh CLI (pre-installed on GitHub Actions ubuntu-latest runners)
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

DIGEST_ISSUE_TITLE = "📋 Idaho Legislature — Daily Activity Digest"
DIGEST_LABEL       = "daily-digest"
VAULT_ROOT         = Path(__file__).resolve().parents[2]
BILLS_DIR          = VAULT_ROOT / "GOVERNMENTS" / "IDAHO - LEGISLATIVE" / "BILLS"


# ─────────────────────────────────────────────────────────────────────────────
# gh CLI helpers
# ─────────────────────────────────────────────────────────────────────────────

def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a gh CLI command; return the CompletedProcess."""
    return subprocess.run(
        ["gh", *args],
        capture_output=True, text=True, check=check,
    )


def gh_json(*args: str) -> dict | list | None:
    """Run gh and parse JSON output. Returns None on failure."""
    try:
        result = gh(*args)
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def ensure_label() -> None:
    """Create the daily-digest label if it doesn't exist."""
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    existing = gh_json("label", "list", "--repo", repo, "--json", "name", "--limit", "100")
    if existing and any(l["name"] == DIGEST_LABEL for l in existing):
        return
    gh("label", "create", DIGEST_LABEL,
       "--color", "0075ca",
       "--description", "Auto-posted daily Idaho Legislature activity summary",
       "--repo", repo,
       check=False)


def find_or_create_digest_issue() -> int:
    """Return the issue number of the digest issue, creating it if needed."""
    repo = os.environ.get("GITHUB_REPOSITORY", "")

    # Search for open issue with the digest title
    issues = gh_json(
        "issue", "list",
        "--repo", repo,
        "--label", DIGEST_LABEL,
        "--state", "open",
        "--json", "number,title",
        "--limit", "5",
    )

    if issues:
        for issue in issues:
            if issue["title"] == DIGEST_ISSUE_TITLE:
                return issue["number"]

    # Not found — create it
    body = (
        "This issue receives a comment every time the Idaho Legislature scraper "
        "detects bill activity. **Subscribe** (Watch → Custom → Issues) to get "
        "a push notification on GitHub mobile each morning.\n\n"
        "- Trigger a manual scrape: **Actions → Idaho Legislature Scraper → Run workflow**\n"
        "- Each comment below is one day's legislative activity.\n"
        "- Bills are stored in `GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/`\n"
    )
    result = gh(
        "issue", "create",
        "--repo",  repo,
        "--title", DIGEST_ISSUE_TITLE,
        "--label", DIGEST_LABEL,
        "--body",  body,
    )
    # Parse issue number from URL in stdout (e.g. "https://github.com/org/repo/issues/42")
    url = result.stdout.strip()
    m = re.search(r'/issues/(\d+)$', url)
    if m:
        return int(m.group(1))

    # Fallback: re-query
    issues = gh_json(
        "issue", "list",
        "--repo", repo,
        "--label", DIGEST_LABEL,
        "--state", "open",
        "--json", "number,title",
        "--limit", "5",
    )
    if issues:
        return issues[0]["number"]

    print("ERROR: Could not find or create digest issue", file=sys.stderr)
    sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# Bill file reader
# ─────────────────────────────────────────────────────────────────────────────

def read_bill_summary(filepath: Path) -> dict:
    """
    Extract key fields from a bill markdown file for the digest.
    Returns dict: {alias, title, last_action, url}
    """
    if not filepath.exists():
        return {}
    text = filepath.read_text(encoding="utf-8")

    alias = ""
    url   = ""
    title = ""

    # Parse frontmatter
    fm_match = re.match(r'^---\n(.+?)\n---', text, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        alias_m = re.search(r'^  - (.+)$', fm, re.M)
        if alias_m:
            alias = alias_m.group(1).strip()
        url_m = re.search(r'^URL:\s*(.+)$', fm, re.M)
        if url_m:
            url = url_m.group(1).strip()

    # Pull first substantive body line as the title/description
    body = text[fm_match.end():].strip() if fm_match else text
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith(">") and not line.startswith("by "):
            title = line[:120]
            break

    # Pull last history entry as the most recent action
    last_action = ""
    for line in reversed(body.splitlines()):
        m = re.match(r'^(\d{1,2}/\d{1,2})\s+\t(.+)$', line)
        if m:
            last_action = f"{m.group(1)}: {m.group(2)}"
            break

    # Fall back to "Last action:" line
    if not last_action:
        m = re.search(r'Last action:\s*(.+)', body)
        if m:
            last_action = m.group(1).strip()

    return {
        "alias":       alias or filepath.stem,
        "title":       title,
        "last_action": last_action,
        "url":         url,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Comment builder
# ─────────────────────────────────────────────────────────────────────────────

def build_comment(
    changed_paths: list[str],
    new_paths: list[str],
    year: str,
) -> str:
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%A, %B %-d, %Y")   # e.g. "Thursday, March 12, 2026"
    time_str = now.strftime("%H:%M UTC")

    new_set     = set(new_paths)
    updated_set = set(changed_paths) - new_set

    lines = [f"## {date_str} — Idaho Legislature Activity"]
    lines.append(f"*Scraped at {time_str} · {year} Regular Session*")
    lines.append("")

    def bill_row(path_str: str) -> str:
        p = Path(path_str)
        info = read_bill_summary(BILLS_DIR / p.name if not p.is_absolute() else p)
        alias = info.get("alias", p.stem)
        title = info.get("title", "")
        action = info.get("last_action", "")
        url   = info.get("url", "")
        link  = f"[{alias}]({url})" if url else alias
        title_short = (title[:80] + "…") if len(title) > 80 else title
        return f"| {link} | {title_short} | {action} |"

    if new_set:
        lines.append(f"### 🆕 New bills introduced ({len(new_set)})")
        lines.append("")
        lines.append("| Bill | Description | Status |")
        lines.append("|------|-------------|--------|")
        for p in sorted(new_set):
            lines.append(bill_row(p))
        lines.append("")

    if updated_set:
        lines.append(f"### 🔄 Bills with activity ({len(updated_set)})")
        lines.append("")
        lines.append("| Bill | Description | Latest Action |")
        lines.append("|------|-------------|---------------|")
        for p in sorted(updated_set):
            lines.append(bill_row(p))
        lines.append("")

    total = len(new_set) + len(updated_set)
    lines.append(f"*{total} bill file(s) updated in this run.*")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Post a daily legislative digest comment to a GitHub Issue."
    )
    parser.add_argument("--changed-file", required=True,
                        help="File listing paths of changed bill files (one per line)")
    parser.add_argument("--new-file", required=True,
                        help="File listing paths of newly created bill files (one per line)")
    parser.add_argument("--year", default="2026")
    args = parser.parse_args()

    changed_paths = Path(args.changed_file).read_text().splitlines()
    new_paths     = Path(args.new_file).read_text().splitlines()
    changed_paths = [p.strip() for p in changed_paths if p.strip()]
    new_paths     = [p.strip() for p in new_paths     if p.strip()]

    if not changed_paths and not new_paths:
        print("No bill changes — skipping digest comment.")
        return 0

    ensure_label()
    issue_number = find_or_create_digest_issue()
    comment = build_comment(changed_paths, new_paths, args.year)

    repo = os.environ.get("GITHUB_REPOSITORY", "")
    result = gh(
        "issue", "comment", str(issue_number),
        "--repo", repo,
        "--body", comment,
    )
    print(f"Posted digest to issue #{issue_number}")
    print(result.stdout.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
