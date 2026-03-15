#!/usr/bin/env python3
"""
IDAHO-VAULT Wayback Machine Audit
Scans all vault notes for URL fields, checks live status, and for dead links
queries the Wayback Machine for the best available snapshot.

Outputs:
  !ADMINISTRATION/wayback-audit-YYYY-MM-DD.md  — human-readable report
  !ADMINISTRATION/wayback-patches-YYYY-MM-DD.md — proposed frontmatter patches

Usage:
  python3 wayback_audit.py           # dry run, report only
  python3 wayback_audit.py --save    # also submit dead URLs to Save Page Now
  python3 wayback_audit.py --limit N # only check first N URLs (for testing)
"""

import os
import re
import sys
import time
import json
import argparse
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

VAULT_ROOT = Path(".")
ADMIN_DIR = VAULT_ROOT / "!ADMINISTRATION"

SKIP_FOLDERS = {"X LABELER", "ATTACHMENTS"}

RATE_LIVE = 0.5
RATE_CDX = 1.0
RATE_SAVE = 5.0
TIMEOUT = 10
UA = "IDAHO-VAULT/1.0 (Idaho Reports journalism archive; github.com/loganfinney27/IDAHO-VAULT)"
DEAD_STATUSES = {400, 403, 404, 410, 451, 500, 502, 503, 504}


def head_request(url: str) -> int | None:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


def cdx_lookup(url: str) -> dict | None:
    cdx_url = (
        "http://web.archive.org/cdx/search/cdx"
        f"?url={urllib.parse.quote(url, safe='')}"
        "&output=json&limit=1&fl=timestamp,statuscode,original&filter=statuscode:200"
        "&fastLatest=true"
    )
    try:
        req = urllib.request.Request(cdx_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read())
            if len(data) < 2:
                return None
            ts, sc, orig = data[1]
            return {
                "snapshot_url": f"https://web.archive.org/web/{ts}/{orig}",
                "timestamp": ts,
                "status_code": sc,
            }
    except Exception:
        return None


def save_page_now(url: str) -> str | None:
    save_url = f"https://web.archive.org/save/{url}"
    try:
        req = urllib.request.Request(
            save_url,
            method="GET",
            headers={"User-Agent": UA, "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            loc = resp.headers.get("Content-Location", "")
            if loc:
                return f"https://web.archive.org{loc}"
            return save_url
    except Exception:
        return None


def find_vault_notes() -> list[Path]:
    notes = []
    for path in sorted(VAULT_ROOT.rglob("*.md")):
        parts = path.parts
        if any(p in SKIP_FOLDERS for p in parts):
            continue
        if ".github" in parts:
            continue
        notes.append(path)
    return notes


def extract_url(content: str) -> str | None:
    m = re.search(r"^URL:\s*(.+)$", content, re.MULTILINE)
    if not m:
        return None
    url = m.group(1).strip()
    if not url or url.lower() == "null" or url.lower() == "n/a":
        return None
    if "web.archive.org" in url:
        return None
    return url


def extract_wayback_field(content: str) -> str | None:
    m = re.search(r"^wayback:\s*(.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else None


def main():
    parser = argparse.ArgumentParser(description="Wayback Machine audit for IDAHO-VAULT")
    parser.add_argument("--save", action="store_true", help="Submit dead URLs to Save Page Now")
    parser.add_argument("--limit", type=int, default=0, help="Limit to N URLs (for testing)")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    print(f"IDAHO-VAULT Wayback Audit — {date_str}")
    notes = find_vault_notes()
    print(f"Found {len(notes)} notes")

    url_notes = []
    for note in notes:
        content = note.read_text(encoding="utf-8", errors="replace")
        url = extract_url(content)
        if url:
            already_has_wayback = extract_wayback_field(content)
            url_notes.append({
                "path": note,
                "url": url,
                "content": content,
                "already_patched": already_has_wayback,
            })

    total_urls = len(url_notes)
    print(f"Found {total_urls} notes with URLs")

    if args.limit:
        url_notes = url_notes[:args.limit]
        print(f"Limiting to first {args.limit} URLs")

    live = []
    dead = []
    unreachable = []
    already_patched = []

    print("\nChecking live status...")

    for i, item in enumerate(url_notes, 1):
        note_name = item["path"].name
        url = item["url"]

        if item["already_patched"]:
            already_patched.append(item)
            print(f"  [{i}/{len(url_notes)}] SKIP (already patched) {note_name}")
            continue

        print(f"  [{i}/{len(url_notes)}] {note_name[:60]}", end=" ", flush=True)
        status = head_request(url)
        time.sleep(RATE_LIVE)

        if status is None:
            print("→ UNREACHABLE")
            unreachable.append({**item, "live_status": None})
        elif status in DEAD_STATUSES:
            print(f"→ DEAD ({status})")
            dead.append({**item, "live_status": status})
        else:
            print(f"→ OK ({status})")
            live.append({**item, "live_status": status})

    print(f"\nQuerying Wayback for {len(dead)} dead URLs...")

    patches = []
    no_archive = []

    for i, item in enumerate(dead, 1):
        note_name = item["path"].name
        url = item["url"]
        print(f"  [{i}/{len(dead)}] {note_name[:60]}", end=" ", flush=True)

        snapshot = cdx_lookup(url)
        time.sleep(RATE_CDX)

        if snapshot:
            print(f"→ snapshot {snapshot['timestamp']}")
            item["snapshot"] = snapshot
            patches.append(item)

            if args.save:
                print("    Submitting to Save Page Now...", end=" ", flush=True)
                saved = save_page_now(url)
                print("saved" if saved else "failed")
                if saved:
                    item["saved_url"] = saved
                time.sleep(RATE_SAVE)
        else:
            print("→ NO ARCHIVE FOUND")
            item["snapshot"] = None
            no_archive.append(item)

    ADMIN_DIR.mkdir(exist_ok=True)
    report_path = ADMIN_DIR / f"wayback-audit-{date_str}.md"
    patches_path = ADMIN_DIR / f"wayback-patches-{date_str}.md"

    report_lines = [
        f"# Wayback Audit — {date_str}", "",
        f"Scanned {total_urls} notes with URL fields.", "",
        "| Status | Count |", "|---|---|",
        f"| ✅ Live | {len(live)} |",
        f"| ❌ Dead — snapshot found | {len(patches)} |",
        f"| ❌ Dead — no archive | {len(no_archive)} |",
        f"| ⚠️ Unreachable (network error) | {len(unreachable)} |",
        f"| ⏭️ Already patched | {len(already_patched)} |",
        "", "---", "",
    ]

    if patches:
        report_lines += [
            "## Dead — Wayback Snapshot Found", "",
            "| Note | Original URL | Snapshot | Archived |",
            "|---|---|---|---|",
        ]
        for item in patches:
            snap = item["snapshot"]
            ts = snap["timestamp"]
            archived_date = f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]}"
            report_lines.append(
                f"| `{item['path'].name}` "
                f"| [{item['url'][:60]}]({item['url']}) "
                f"| [snapshot]({snap['snapshot_url']}) "
                f"| {archived_date} |"
            )
        report_lines.append("")

    if no_archive:
        report_lines += [
            "## Dead — No Archive Found", "",
            "| Note | Dead URL | HTTP Status |", "|---|---|---|",
        ]
        for item in no_archive:
            report_lines.append(
                f"| `{item['path'].name}` | {item['url'][:80]} | {item['live_status']} |"
            )
        report_lines.append("")

    if unreachable:
        report_lines += [
            "## Unreachable (Network Error)", "",
            "| Note | URL |", "|---|---|",
        ]
        for item in unreachable:
            report_lines.append(f"| `{item['path'].name}` | {item['url'][:80]} |")
        report_lines.append("")

    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nReport written to {report_path}")

    if patches:
        patch_lines = [
            f"# Wayback Patches — {date_str}", "",
            "Proposed `wayback:` frontmatter additions for notes with dead URLs.",
            "Insert the `wayback:` line directly after the `URL:` field.", "",
            "---", "",
        ]
        for item in patches:
            snap = item["snapshot"]
            rel_path = item["path"].relative_to(VAULT_ROOT)
            patch_lines += [
                f"### `{rel_path}`", "",
                "```",
                f"URL: {item['url']}",
                f"wayback: {snap['snapshot_url']}",
                "```", "",
            ]
        patches_path.write_text("\n".join(patch_lines), encoding="utf-8")
        print(f"Patches written to {patches_path}")

    print(f"\n{'─'*50}")
    print(f"Total URLs scanned:      {total_urls}")
    print(f"Live:                    {len(live)}")
    print(f"Dead (snapshot found):   {len(patches)}")
    print(f"Dead (no archive):       {len(no_archive)}")
    print(f"Unreachable:             {len(unreachable)}")
    print(f"Already patched:         {len(already_patched)}")


if __name__ == "__main__":
    main()
