#!/usr/bin/env python3
"""
IDAHO-VAULT Sort Audit — v2
Walks the vault tree and flags files that appear misplaced,
orphaned at a parent level, or inconsistently named.
Outputs a dated markdown report to !ADMINISTRATION/.

Changes from v1:
- Dated files in EDITORIALS, PODCASTS, PRESS RELEASES etc. no longer flagged as NEWS MEDIA
- Out-of-state county folders exempt from Idaho county check
- FLAT_OK set suppresses orphan warnings for intentionally flat folders
- Org-sounding names in TOPICS root flagged as potential misfiles
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path

VAULT_ROOT = Path(".")

SKIP_DIRS = {".obsidian", "ATTACHMENTS", "!ADMINISTRATION", "X LABELER",
             "x hey you make sure to link these"}

OUT_OF_STATE_COUNTY_FOLDERS = {
    "PLACES/OTHER/COUNTIES",
    "PLACES/OTHER",
}

FLAT_OK = {
    "TOPICS",
    "TOPICS/ECONOMY",
    "TOPICS/EDUCATION",
    "TOPICS/ELECTIONS",
    "TOPICS/FISCAL",
    "TOPICS/HEALTH",
    "TOPICS/RESOURCES",
    "TOPICS/TAXES",
    "ORGANIZATIONS",
    "ORGANIZATIONS/PARTIES",
    "GOVERNMENTS/IDAHO - EXECUTIVE",
    "GOVERNMENTS/IDAHO - JUDICIAL",
    "GOVERNMENTS/IDAHO - LEGISLATIVE",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/IDAHO HOUSE",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/IDAHO SENATE",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/JOINT COMMITTEES",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/JOINT COMMITTEES/PAST COMMITTEES",
    "GOVERNMENTS/USA - FEDERAL",
    "GOVERNMENTS/IDAHO - EXECUTIVE/CONSTITUTIONAL",
    "PLACES/GEOGRAPHY/LAND",
    "PLACES/GEOGRAPHY/WATER",
    "PLACES/SCHOOLS",
    "PLACES/TAXING DISTRICTS",
    "SOURCES/EDITORIALS",
    "SOURCES/PODCASTS",
    "SOURCES/PRESS RELEASES",
    "SOURCES/RESOLUTIONS",
    "SOURCES/REPORTS",
    "SOURCES/INTERVIEWS",
    "SOURCES/HEARINGS",
}

KNOWN_ORGS = [
    r"Kaiser Family Foundation",
    r"Foundation$",
    r"Institute$",
    r"Association$",
    r"Coalition$",
    r"Alliance$",
    r"Federation$",
    r"Society$",
    r"Center for ",
]

MISPLACEMENT_HINTS = [
    (r"^(HB|SB|HCR|SCR|HJM|SJM|HR|SR)\s*\d+",
     "GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS", "looks like an Idaho bill"),
    (r"^[A-Z][a-z]+ County$",
     "PLACES/COUNTIES", "looks like an Idaho county"),
    (r"^(Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|"
     r"Georgia|Hawaii|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|"
     r"Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|"
     r"New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|"
     r"Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|"
     r"Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming)$",
     "PLACES/OTHER/STATES", "looks like a US state"),
]

NEWS_MEDIA_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}\s*[-–]\s*.+\s*[-–]\s*.+\.md$"
)

def relative_path(path):
    return str(path.relative_to(VAULT_ROOT)).replace("\\", "/")

def check_misplacement(filename, fkey, rel_folder):
    stem = Path(filename).stem
    for hint_pattern, suggested, reason in MISPLACEMENT_HINTS:
        if re.search(hint_pattern, stem, re.IGNORECASE):
            if "County" in stem and rel_folder.upper() in {
                f.upper() for f in OUT_OF_STATE_COUNTY_FOLDERS
            }:
                continue
            if not fkey.startswith(suggested.upper()):
                return suggested, reason
    if fkey == "TOPICS":
        for pat in KNOWN_ORGS:
            if re.search(pat, stem, re.IGNORECASE):
                return "ORGANIZATIONS", "looks like an organization, not a topic"
    return None

def audit():
    issues = []
    orphans = []
    naming = []

    for dirpath, dirnames, filenames in os.walk(VAULT_ROOT):
        dirnames[:] = [d for d in sorted(dirnames)
                       if d not in SKIP_DIRS and not d.startswith('.')]

        path = Path(dirpath)
        rel = str(path.relative_to(VAULT_ROOT)).replace("\\", "/")
        if rel == ".":
            rel = ""

        fkey = rel.upper()
        md_files = [f for f in filenames if f.endswith(".md")]
        if not md_files:
            continue

        has_subdirs = bool(dirnames)
        is_flat_ok = rel.upper() in {f.upper() for f in FLAT_OK} or not rel

        for fname in sorted(md_files):
            fpath = path / fname
            rpath = relative_path(fpath)

            result = check_misplacement(fname, fkey, rel)
            if result:
                suggested, reason = result
                issues.append({
                    "file": rpath,
                    "current_folder": rel or "(root)",
                    "reason": reason,
                    "suggested": suggested,
                })

            if has_subdirs and rel and not is_flat_ok:
                orphans.append({
                    "file": rpath,
                    "folder": rel,
                    "subfolders": sorted(dirnames),
                })

            if "SOURCES/NEWS MEDIA" in rel.upper():
                if not NEWS_MEDIA_PATTERN.match(fname):
                    naming.append({
                        "file": rpath,
                        "issue": "does not match expected YYYY-MM-DD - Outlet - Title.md pattern",
                    })

    return issues, orphans, naming

def render_report(issues, orphans, naming):
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    lines = []

    lines.append(f"# Vault Sort Audit — {date_str}")
    lines.append(f"\n_Generated {now.strftime('%Y-%m-%d %H:%M UTC')} by GitHub Actions — v2_\n")
    lines.append("---\n")
    lines.append("## Summary\n")
    lines.append("| Check | Count |")
    lines.append("|---|---|")
    lines.append(f"| Likely misplaced files | {len(issues)} |")
    lines.append(f"| Files in parent folders with subfolders (potential orphans) | {len(orphans)} |")
    lines.append(f"| Naming convention issues | {len(naming)} |")
    lines.append("")

    lines.append("---\n")
    lines.append("## Likely Misplaced Files\n")
    if issues:
        lines.append("| File | Current Folder | Suggested Folder | Reason |")
        lines.append("|---|---|---|---|")
        for i in issues:
            lines.append(f"| `{i['file']}` | `{i['current_folder']}` | `{i['suggested']}` | {i['reason']} |")
    else:
        lines.append("_No likely misplaced files detected._")
    lines.append("")

    lines.append("---\n")
    lines.append("## Files in Parent Folders (Potential Orphans)\n")
    lines.append("Files in folders with subfolders that are not designated as intentionally flat.\n")
    if orphans:
        lines.append("| File | Folder | Available Subfolders |")
        lines.append("|---|---|---|")
        for o in orphans:
            subs = ", ".join(f"`{s}`" for s in o["subfolders"])
            lines.append(f"| `{o['file']}` | `{o['folder']}` | {subs} |")
    else:
        lines.append("_No orphaned files detected._")
    lines.append("")

    lines.append("---\n")
    lines.append("## Naming Convention Issues\n")
    if naming:
        lines.append("| File | Issue |")
        lines.append("|---|---|")
        for n in naming:
            lines.append(f"| `{n['file']}` | {n['issue']} |")
    else:
        lines.append("_No naming convention issues detected._")
    lines.append("")

    lines.append("---\n")
    lines.append("_This report is generated automatically. All suggested moves require human review._")
    return "\n".join(lines)

if __name__ == "__main__":
    issues, orphans, naming = audit()
    report = render_report(issues, orphans, naming)

    out_dir = VAULT_ROOT / "!ADMINISTRATION"
    out_dir.mkdir(exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = out_dir / f"sort-audit-{date_str}.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"Report written to {out_path}")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(report)
        print("Summary written to GitHub Actions step summary.")
    else:
        print(report)
