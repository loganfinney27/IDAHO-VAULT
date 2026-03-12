#!/usr/bin/env python3
"""
IDAHO-VAULT Sort Audit
Walks the vault tree and flags files that appear misplaced,
orphaned at a parent level, or inconsistently named.
Outputs a dated markdown report to !ADMINISTRATION/.
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path

# ── Vault root (relative to repo root when run via GitHub Actions) ──────────
VAULT_ROOT = Path(".")

# ── Folders to skip entirely ─────────────────────────────────────────────────
SKIP_DIRS = {".obsidian", "ATTACHMENTS", "!ADMINISTRATION", "X LABELER",
             "x hey you make sure to link these"}

# ── Known top-level folders and their expected content types ─────────────────
# Each entry: folder path fragment → human label for report
FOLDER_TAXONOMY = {
    # GOVERNMENTS
    "GOVERNMENTS/IDAHO - EXECUTIVE/AGRICULTURAL COMMISSIONS": "Idaho executive agricultural commission",
    "GOVERNMENTS/IDAHO - EXECUTIVE/CONSTITUTIONAL/OFFICERS":  "Idaho constitutional officer",
    "GOVERNMENTS/IDAHO - EXECUTIVE/COUNTIES & CITIES":        "Idaho county/city executive entity",
    "GOVERNMENTS/IDAHO - EXECUTIVE/DEPARTMENTS":              "Idaho executive department",
    "GOVERNMENTS/IDAHO - EXECUTIVE/HEALTH DISTRICTS":         "Idaho health district",
    "GOVERNMENTS/IDAHO - EXECUTIVE":                          "Idaho executive agency/board/commission",
    "GOVERNMENTS/IDAHO - JUDICIAL/COUNTY COURTHOUSES":        "Idaho county courthouse",
    "GOVERNMENTS/IDAHO - JUDICIAL/JUDICIAL DISTRICTS":        "Idaho judicial district",
    "GOVERNMENTS/IDAHO - JUDICIAL":                           "Idaho judicial entity",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS":                  "Idaho bill",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/DISTRICTS":              "Idaho legislative district",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/IDAHO HOUSE/HOUSE COMMITTEES": "Idaho House committee",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/IDAHO HOUSE":            "Idaho House member or entity",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/IDAHO SENATE/SENATE COMMITTEES": "Idaho Senate committee",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/IDAHO SENATE":           "Idaho Senate member or entity",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/JOINT COMMITTEES/PAST COMMITTEES/WORKING GROUPS": "JFAC/joint working group",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/JOINT COMMITTEES/PAST COMMITTEES": "past joint committee",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/JOINT COMMITTEES":       "joint legislative committee",
    "GOVERNMENTS/IDAHO - LEGISLATIVE/SESSIONS":               "Idaho legislative session",
    "GOVERNMENTS/IDAHO - LEGISLATIVE":                        "Idaho legislative entity",
    "GOVERNMENTS/USA - FEDERAL/CENSUS YEARS":                 "US Census year",
    "GOVERNMENTS/USA - FEDERAL/ENTITIES":                     "federal entity",
    "GOVERNMENTS/USA - FEDERAL/LEGISLATION":                  "federal legislation",
    "GOVERNMENTS/USA - FEDERAL/WILDLIFE REFUGES":             "federal wildlife refuge",
    "GOVERNMENTS/USA - FEDERAL":                              "federal government entity",
    "GOVERNMENTS/USA - TRIBES/TRIBES":                        "Idaho tribe",
    "GOVERNMENTS/USA - TRIBES":                               "tribal government entity",
    "GOVERNMENTS":                                            "government entity (unsorted)",
    # ORGANIZATIONS
    "ORGANIZATIONS/CHURCHES":      "church or religious organization",
    "ORGANIZATIONS/COMPANIES":     "company or business",
    "ORGANIZATIONS/DEVELOPMENT":   "development organization",
    "ORGANIZATIONS/EDUCATION":     "education organization",
    "ORGANIZATIONS/HOSPITALS":     "hospital or health system",
    "ORGANIZATIONS/LEGAL":         "legal organization",
    "ORGANIZATIONS/PARTIES/CENTRAL COMMITTEES": "party central committee",
    "ORGANIZATIONS/PARTIES/GROUPS": "party-affiliated group",
    "ORGANIZATIONS/PARTIES":       "political party",
    "ORGANIZATIONS/POLITICS":      "political organization",
    "ORGANIZATIONS/PUBLICATIONS":  "publication or media outlet",
    "ORGANIZATIONS/UNIONS":        "union or labor organization",
    "ORGANIZATIONS":               "organization (unsorted)",
    # PEOPLE
    "PEOPLE":                      "person",
    # PLACES
    "PLACES/CITIES":               "Idaho city",
    "PLACES/COMMUNITIES":          "Idaho community",
    "PLACES/COUNTIES":             "Idaho county",
    "PLACES/COUNTY JAILS":         "Idaho county jail",
    "PLACES/GAME UNITS":           "Idaho game management unit",
    "PLACES/GEOGRAPHY/LAND/NATIONAL FORESTS": "national forest",
    "PLACES/GEOGRAPHY/LAND":       "geographic land feature",
    "PLACES/GEOGRAPHY/WATER/DAMS": "dam",
    "PLACES/GEOGRAPHY/WATER/LAKES AND RESERVOIRS": "lake or reservoir",
    "PLACES/GEOGRAPHY/WATER/RIVERS AND CREEKS": "river or creek",
    "PLACES/GEOGRAPHY/WATER":      "geographic water feature",
    "PLACES/GEOGRAPHY":            "geographic feature (unsorted)",
    "PLACES/LIBRARIES":            "library",
    "PLACES/LOCATIONS":            "named location",
    "PLACES/OTHER/CITIES":         "out-of-state city",
    "PLACES/OTHER/COUNTIES":       "out-of-state county",
    "PLACES/OTHER/COUNTRIES":      "country",
    "PLACES/OTHER/STATES":         "US state",
    "PLACES/OTHER":                "non-Idaho place (unsorted)",
    "PLACES/REGIONS":              "region",
    "PLACES/RESERVATIONS":         "reservation",
    "PLACES/ROADS":                "road or highway",
    "PLACES/SCHOOL DISTRICTS":     "school district",
    "PLACES/SCHOOLS/COLLEGES AND UNIVERSITIES/COMMUNITY COLLEGES": "community college",
    "PLACES/SCHOOLS/COLLEGES AND UNIVERSITIES/PRIVATE COLLEGES":   "private college",
    "PLACES/SCHOOLS/COLLEGES AND UNIVERSITIES/STATE COLLEGES":     "state college/university",
    "PLACES/SCHOOLS/COLLEGES AND UNIVERSITIES": "college or university",
    "PLACES/SCHOOLS/PRIVATE SCHOOLS": "private school",
    "PLACES/SCHOOLS/PUBLIC SCHOOLS":  "public school",
    "PLACES/SCHOOLS":              "school (unsorted)",
    "PLACES/TAXING DISTRICTS/FIRE PROTECTION DISTRICTS": "fire protection district",
    "PLACES/TAXING DISTRICTS/HIGHWAY DISTRICTS": "highway district",
    "PLACES/TAXING DISTRICTS":     "taxing district (unsorted)",
    "PLACES":                      "place (unsorted)",
    # SOURCES
    "SOURCES/EDITORIALS/MAIN STREET IDAHO CAUCUS": "Main Street Idaho Caucus editorial",
    "SOURCES/EDITORIALS/MOON - CHAIRWOMAN'S COLUMN": "Moon chairwoman's column",
    "SOURCES/EDITORIALS":          "editorial",
    "SOURCES/HEARINGS/2020":       "2020 hearing",
    "SOURCES/HEARINGS/2021":       "2021 hearing",
    "SOURCES/HEARINGS/2022":       "2022 hearing",
    "SOURCES/HEARINGS/2023":       "2023 hearing",
    "SOURCES/HEARINGS/2024":       "2024 hearing",
    "SOURCES/HEARINGS/2025":       "2025 hearing",
    "SOURCES/HEARINGS":            "hearing (unsorted year)",
    "SOURCES/INTERVIEWS":          "interview",
    "SOURCES/LISTS":               "list",
    "SOURCES/NEWS MEDIA":          "news media article",
    "SOURCES/PODCASTS":            "podcast",
    "SOURCES/PRESS RELEASES":      "press release",
    "SOURCES/REPORTS":             "report",
    "SOURCES/RESOLUTIONS":         "resolution",
    "SOURCES":                     "source (unsorted)",
    # TOPICS
    "TOPICS/AGRICULTURE":          "agriculture topic",
    "TOPICS/CONCEPTS":             "concept",
    "TOPICS/ECONOMY/LABOR":        "labor/economy topic",
    "TOPICS/ECONOMY/RESIDENTIAL":  "residential/economy topic",
    "TOPICS/ECONOMY":              "economy topic",
    "TOPICS/EDUCATION/HIGHER EDUCATION": "higher education topic",
    "TOPICS/EDUCATION/K-12":       "K-12 education topic",
    "TOPICS/EDUCATION":            "education topic",
    "TOPICS/ELECTIONS/ELECTION YEARS": "election year",
    "TOPICS/ELECTIONS":            "elections topic",
    "TOPICS/FISCAL/FISCAL YEARS":  "fiscal year",
    "TOPICS/FISCAL":               "fiscal topic",
    "TOPICS/FUNDS":                "fund",
    "TOPICS/HEALTH/DISEASES":      "disease",
    "TOPICS/HEALTH":               "health topic",
    "TOPICS/IDLEG":                "Idaho Legislature topic",
    "TOPICS/INTERNET":             "internet topic",
    "TOPICS/LEGAL":                "legal topic",
    "TOPICS/PUBLIC SAFETY":        "public safety topic",
    "TOPICS/RESOURCES/WILDLIFE":   "wildlife topic",
    "TOPICS/RESOURCES":            "natural resources topic",
    "TOPICS/STATE AFFAIRS":        "state affairs topic",
    "TOPICS/TAXES/TAXING DISTRICTS": "taxing district topic",
    "TOPICS/TAXES":                "taxes topic",
    "TOPICS/TRANSPORTATION":       "transportation topic",
    "TOPICS":                      "topic (unsorted)",
}

# ── Patterns that suggest a file may be misplaced ────────────────────────────
# (name_pattern, likely_folder, reason)
MISPLACEMENT_HINTS = [
    # Bills
    (r"^(HB|SB|HCR|SCR|HJM|SJM|HR|SR)\s*\d+", "GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS",
     "looks like an Idaho bill"),
    (r"^(H|S)\.\s*(B\.|R\.|C\.R\.|J\.M\.)\s*\d+", "GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS",
     "looks like an Idaho bill"),
    # Hearing transcripts / committee minutes
    (r"^\d{4}-\d{2}-\d{2}.*(?:hearing|committee|subcommittee)", "SOURCES/HEARINGS",
     "looks like a hearing note"),
    # News articles with date prefix
    (r"^\d{4}-\d{2}-\d{2}\s*[-–]\s*.+\s*[-–]", "SOURCES/NEWS MEDIA",
     "looks like a dated news article"),
    # Idaho counties
    (r"^[A-Z][a-z]+ County$", "PLACES/COUNTIES",
     "looks like an Idaho county"),
    # US states
    (r"^(Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|"
     r"Georgia|Hawaii|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|"
     r"Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|"
     r"New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|"
     r"Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|"
     r"Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming)$",
     "PLACES/OTHER/STATES", "looks like a US state"),
]

# ── Naming convention checks ──────────────────────────────────────────────────
NEWS_MEDIA_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}\s*[-–]\s*.+\s*[-–]\s*.+\.md$"
)
HEARING_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}.*\.md$"
)


def relative_path(path: Path) -> str:
    return str(path.relative_to(VAULT_ROOT)).replace("\\", "/")


def folder_key(path: Path) -> str:
    """Return the path string relative to vault root, uppercase, for taxonomy lookup."""
    return str(path.parent.relative_to(VAULT_ROOT)).replace("\\", "/").upper()


def best_taxonomy_match(fkey: str) -> str:
    """Find the most specific taxonomy label for a folder key."""
    best = ""
    label = "unknown folder"
    for k, v in FOLDER_TAXONOMY.items():
        ku = k.upper()
        if fkey == ku or fkey.startswith(ku + "/") or fkey.startswith(ku + "\\"):
            if len(ku) > len(best):
                best = ku
                label = v
    return label


def check_misplacement(filename: str, fkey: str):
    """Return (suggested_folder, reason) if file looks misplaced, else None."""
    stem = Path(filename).stem
    for pattern, suggested, reason in MISPLACEMENT_HINTS:
        if re.search(pattern, stem, re.IGNORECASE):
            # Only flag if not already in the right place
            if not fkey.startswith(suggested.upper()):
                return suggested, reason
    return None


def audit():
    issues = []
    orphans = []  # .md files sitting directly in a parent folder that has subfolders
    naming = []   # naming convention inconsistencies

    for dirpath, dirnames, filenames in os.walk(VAULT_ROOT):
        # Skip unwanted dirs in-place
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

        for fname in sorted(md_files):
            fpath = path / fname
            rpath = relative_path(fpath)

            # 1. Misplacement check
            result = check_misplacement(fname, fkey)
            if result:
                suggested, reason = result
                issues.append({
                    "file": rpath,
                    "current_folder": rel or "(root)",
                    "reason": reason,
                    "suggested": suggested,
                })

            # 2. Orphan check — .md file in a folder that has subfolders
            # (may belong in one of the subfolders)
            if has_subdirs and rel:  # skip vault root level
                orphans.append({
                    "file": rpath,
                    "folder": rel,
                    "subfolders": sorted(dirnames),
                })

            # 3. Naming convention check for NEWS MEDIA
            if "SOURCES/NEWS MEDIA" in rel.upper():
                if not NEWS_MEDIA_PATTERN.match(fname):
                    naming.append({
                        "file": rpath,
                        "issue": "NEWS MEDIA file does not match expected "
                                 "YYYY-MM-DD - Outlet - Title.md pattern",
                    })

    return issues, orphans, naming


def render_report(issues, orphans, naming) -> str:
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    lines = []

    lines.append(f"# Vault Sort Audit — {date_str}")
    lines.append(f"\n_Generated {now.strftime('%Y-%m-%d %H:%M UTC')} by GitHub Actions_\n")
    lines.append("---\n")

    # Summary
    lines.append("## Summary\n")
    lines.append(f"| Check | Count |")
    lines.append(f"|---|---|")
    lines.append(f"| Likely misplaced files | {len(issues)} |")
    lines.append(f"| Files in parent folders with subfolders (potential orphans) | {len(orphans)} |")
    lines.append(f"| Naming convention issues | {len(naming)} |")
    lines.append("")

    # Misplaced files
    lines.append("---\n")
    lines.append("## Likely Misplaced Files\n")
    if issues:
        lines.append("These files match naming patterns suggesting they belong elsewhere.\n")
        lines.append("| File | Current Folder | Suggested Folder | Reason |")
        lines.append("|---|---|---|---|")
        for i in issues:
            lines.append(f"| `{i['file']}` | `{i['current_folder']}` | "
                         f"`{i['suggested']}` | {i['reason']} |")
    else:
        lines.append("_No likely misplaced files detected._")
    lines.append("")

    # Orphans
    lines.append("---\n")
    lines.append("## Files in Parent Folders (Potential Orphans)\n")
    lines.append("These files sit directly in a folder that also has subfolders. "
                 "They may belong in one of the subfolders listed.\n")
    if orphans:
        lines.append("| File | Folder | Available Subfolders |")
        lines.append("|---|---|---|")
        for o in orphans:
            subs = ", ".join(f"`{s}`" for s in o["subfolders"])
            lines.append(f"| `{o['file']}` | `{o['folder']}` | {subs} |")
    else:
        lines.append("_No orphaned files detected._")
    lines.append("")

    # Naming issues
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
    lines.append("_This report is generated automatically. "
                 "All suggested moves require human review before actioning._")

    return "\n".join(lines)


if __name__ == "__main__":
    issues, orphans, naming = audit()
    report = render_report(issues, orphans, naming)

    # Write to !ADMINISTRATION with date
    out_dir = VAULT_ROOT / "!ADMINISTRATION"
    out_dir.mkdir(exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = out_dir / f"sort-audit-{date_str}.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"Report written to {out_path}")

    # Also print to stdout for GitHub Actions summary
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(report)
        print("Summary written to GitHub Actions step summary.")
    else:
        print(report)
