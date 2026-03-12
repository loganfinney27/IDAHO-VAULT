#!/usr/bin/env python3
"""
Idaho Legislature Bill Scraper
================================
Scrapes https://legislature.idaho.gov/sessioninfo/<YEAR>/legislation/
and writes Obsidian-formatted markdown notes to:
  GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/

Usage:
  python3 idaho_leg_scraper.py [--year YEAR] [--force] [--bill BILLID] [--members] [--dry-run]

Options:
  --year YEAR    Session year to scrape (default: 2026)
  --force        Re-fetch and overwrite all bills, even finalized ones
  --bill BILLID  Scrape only one specific bill (e.g. H0001, S0042, HCR001)
  --members      Also scrape House/Senate member profiles
  --dry-run      Parse and print output without writing files
  --verbose      Enable debug-level logging

Exit codes:
  0  Success (new or updated files written, or nothing changed)
  1  Fatal error (could not fetch bill list)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEGISLATURE.IDAHO.GOV — SITE STRUCTURE REFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session-scoped pages  (BASE = /sessioninfo/{YEAR})
  {BASE}/                                   2026 session overview
  {BASE}/legislation/                       full bill listing (DataTables JS)
  {BASE}/legislation/minidata/              plain HTML bill table  ← PRIMARY TARGET
  {BASE}/legislation/{CODE}/                individual bill detail
    Bill code format:
      House Bills         H0001 – H0999   (e.g. H0024  = House Bill 24)
      Senate Bills        S1001 – S1999   (e.g. S1365  = Senate Bill 1365)
      House Concur. Res.  HCR001 –        (e.g. HCR001)
      Senate Concur. Res. SCR001 –
      House Joint Mem.    HJM001 –
      Senate Joint Mem.   SJM001 –        (e.g. SJM114)
      House Resolution    HR001  –
      Senate Resolution   SR001  –
      House Joint Res.    HJR001 –
      Senate Joint Res.   SJR001 –
      House Proclamation  HP001  –
      Senate Proclamation SP001  –
  {BASE}/standingcommittees/{CODE}/         committee page
    Known House codes: HAPP HBUS HEDU HENV HETH HHEA HJUD HLOC HREV HSTA HTRAN HWRC HCOM
    Known Senate codes: SAPP SEDU SENV SHEA SJUD SLGT SHW SJR SREV SSTA STRAN SCOM
  {BASE}/joint/{CODE}/                      joint committee
    Known codes: jfac  jloc  mill
  {BASE}/agenda/                            reading calendars & agendas
  {BASE}/agenda/hagenda/                    House committee agendas
  {BASE}/agenda/sagenda/                    Senate committee agendas

Non-session-scoped pages
  /legislators/membership/{YEAR}/id{ID}/   individual member profile
    Fields: name, party, district, term, address, phone, email, occupation, committees
    Example: /legislators/membership/2026/id3524/  →  Sen. Kelly Anthon
  /legislators/                            legislators index
  /house/membership/                       full House member listing (table)
  /senate/membership/                      full Senate member listing (table)
  /committees/housecommittees/             House committees overview
  /committees/senatecommittees/            Senate committees overview
  /committee-calendar/                     standing committee calendar

Data reliability notes
  - The /minidata/ page is a plain static HTML table — no JavaScript required.
    It is the most reliable scraping target and should be preferred over the
    main /legislation/ page (which uses DataTables and may be JS-rendered).
  - Individual bill pages are plain HTML served by WordPress; no JS required.
  - Member profile IDs persist across years (same ID used in 2024 and 2026).
  - The site does NOT use a robots.txt disallow for /sessioninfo/ paths.
  - Requests should include a descriptive User-Agent; no API key required.
  - Rate-limit to ≥1 request/second to avoid overloading the state servers.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import argparse
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Tag

# ── TODO: LEVELSET REPORTS ────────────────────────────────────────────────────
# FLAG: This scraper needs to be integrated with / clued in on LEVELSET REPORTS.
# Context pending — revisit when more information is available.
# ─────────────────────────────────────────────────────────────────────────────

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("idleg")

# ── Vault paths ───────────────────────────────────────────────────────────────
VAULT_ROOT = Path(__file__).resolve().parents[2]
BILLS_DIR = VAULT_ROOT / "GOVERNMENTS" / "IDAHO - LEGISLATIVE" / "BILLS"

# ── Scraper settings ──────────────────────────────────────────────────────────
DEFAULT_YEAR = "2026"
REQUEST_DELAY = 1.2        # seconds between individual bill fetches
MAX_RETRIES = 4
RETRY_BACKOFF = [3, 6, 12, 24]  # seconds per retry attempt
REQUEST_TIMEOUT = 30

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; IDAHO-VAULT-bot/1.0; "
        "+https://github.com/loganfinney27/IDAHO-VAULT)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# ── Bill type display names ───────────────────────────────────────────────────
BILL_TYPE_NAMES: dict[str, str] = {
    "HB":  "House Bill",
    "SB":  "Senate Bill",
    "HCR": "House Concurrent Resolution",
    "SCR": "Senate Concurrent Resolution",
    "HJM": "House Joint Memorial",
    "SJM": "Senate Joint Memorial",
    "HR":  "House Resolution",
    "SR":  "Senate Resolution",
    "HJR": "House Joint Resolution",
    "SJR": "Senate Joint Resolution",
    "HP":  "House Proclamation",
    "SP":  "Senate Proclamation",
}

# URL prefix fragments → normalised bill-type abbreviation
URL_PREFIX_MAP: dict[str, str] = {
    "HCR": "HCR",
    "SCR": "SCR",
    "HJM": "HJM",
    "SJM": "SJM",
    "HJR": "HJR",
    "SJR": "SJR",
    "HR":  "HR",
    "SR":  "SR",
    "HP":  "HP",
    "SP":  "SP",
    "H":   "HB",
    "S":   "SB",
}

# Terminal statuses — bills in these states won't change further
FINAL_ACTIONS = frozenset([
    "signed by governor",
    "vetoed by governor",
    "became law without signature",
    "failed in the house",
    "failed in the senate",
    "died in committee",
    "withdrawn",
    "adjourned",
    "session law chapter",
])


# ─────────────────────────────────────────────────────────────────────────────
# HTTP helpers
# ─────────────────────────────────────────────────────────────────────────────

def _fetch(url: str) -> requests.Response | None:
    """GET url with retry/backoff. Returns Response or None on total failure."""
    for attempt, wait in enumerate(RETRY_BACKOFF[:MAX_RETRIES], start=1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return resp
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else "?"
            log.warning("HTTP %s for %s (attempt %d/%d)", status, url, attempt, MAX_RETRIES)
            if status in (404, 410):
                log.error("Permanent error %s — skipping %s", status, url)
                return None
        except requests.RequestException as exc:
            log.warning("Request error for %s: %s (attempt %d/%d)", url, exc, attempt, MAX_RETRIES)
        if attempt < MAX_RETRIES:
            time.sleep(wait)
    log.error("All %d retries failed for %s", MAX_RETRIES, url)
    return None


def get_soup(url: str) -> BeautifulSoup | None:
    resp = _fetch(url)
    if resp is None:
        return None
    return BeautifulSoup(resp.text, "lxml")


# ─────────────────────────────────────────────────────────────────────────────
# Bill ID normalisation
# ─────────────────────────────────────────────────────────────────────────────

def parse_bill_id(raw: str) -> tuple[str, str, str, str]:
    """
    Convert a raw bill identifier (URL fragment or display text) into its
    components.

    Returns (bill_type, number, alias, url_fragment)
      bill_type    → 'HB', 'SB', 'HCR', …
      number       → '1', '42', '1365', … (no leading zeros, for display)
      alias        → 'HB 1', 'SB 42', 'HCR 1', …
      url_fragment → 'H0001', 'S1365', 'HCR001', 'SJM114', …  (as used in URLs)

    Padding rules on the Idaho legislature site:
      Single-char URL prefix (H, S): always 4-digit zero-padded → H0001, S1365
      Multi-char URL prefix (HCR, SJM, …): original digits preserved → HCR001, SJM114

    Display-form aliases like "HB 24" or "H.B. 24" are normalised to the
    URL-form prefix ("H") before processing.
    """
    raw = raw.strip().upper()
    # Collapse spaces and dots: "H. B. 24" → "HB24", "H 0024" → "H0024"
    raw = re.sub(r'[\s.]+', '', raw)

    match = re.fullmatch(r'([A-Z]+)(\d+)', raw)
    if not match:
        log.debug("Could not parse bill ID: %r", raw)
        return raw, "", raw, raw

    prefix, num_str = match.groups()

    # Normalise display-form prefixes to their URL-form equivalents
    # e.g. "HB" (display) → "H" (URL prefix); "SB" → "S"
    _DISPLAY_TO_URL: dict[str, str] = {"HB": "H", "SB": "S"}
    url_prefix = _DISPLAY_TO_URL.get(prefix, prefix)

    bill_type = URL_PREFIX_MAP.get(url_prefix, url_prefix)
    number = str(int(num_str))   # strip leading zeros for human-readable display

    # Single-char prefixes use 4-digit zero-padding; multi-char preserve original
    if len(url_prefix) == 1:
        padded = num_str.zfill(4)
    else:
        padded = num_str         # e.g. "001" stays "001", "114" stays "114"

    url_fragment = f"{url_prefix}{padded}"
    alias = f"{bill_type} {number}"
    return bill_type, number, alias, url_fragment


def bill_url(year: str, url_fragment: str) -> str:
    return (
        f"https://legislature.idaho.gov/sessioninfo/{year}/legislation/"
        f"{url_fragment.lower()}/"
    )


def bill_filename(year: str, bill_type: str, number: str) -> str:
    """Return the vault filename for a bill: '(2026) House Bill 1.md'"""
    full_name = BILL_TYPE_NAMES.get(bill_type, bill_type)
    return f"({year}) {full_name} {number}.md"


# ─────────────────────────────────────────────────────────────────────────────
# Minidata page — bill list
# ─────────────────────────────────────────────────────────────────────────────

def get_bill_list(year: str) -> list[dict]:
    """
    Scrape the minidata page for the complete bill listing.

    Returns a list of dicts, each with keys:
      id, url, title, sponsor, committee, last_action
    """
    minidata_url = (
        f"https://legislature.idaho.gov/sessioninfo/{year}/legislation/minidata/"
    )
    log.info("Fetching bill list from %s", minidata_url)

    soup = get_soup(minidata_url)
    if soup is None:
        log.error("Could not fetch minidata page")
        return []

    # The minidata page renders a plain HTML table.
    # Find the first <table> that contains bill links.
    table = _find_bill_table(soup)
    if table is None:
        # Fallback: try the full legislation page
        log.warning("No bill table on minidata; trying main legislation page")
        table = _find_bill_table(
            get_soup(
                f"https://legislature.idaho.gov/sessioninfo/{year}/legislation/"
            )
        )

    if table is None:
        log.error("Could not find bill table on either minidata or main page")
        return []

    bills = _parse_bill_table(table, year)
    log.info("Found %d bills in listing", len(bills))
    return bills


def _find_bill_table(soup: BeautifulSoup | None) -> Tag | None:
    """
    Return the first <table> that has multiple rows linking to individual bill
    pages (e.g. /legislation/h0001/ or /legislation/scr001/).

    Requires at least 3 bill links to avoid matching incidental navigation
    elements that happen to contain a single bill reference.
    """
    if soup is None:
        return None
    # Match paths like /legislation/h0001/ or /legislation/scr042/ —
    # one or more letters followed by 3–4 digits, not "minidata" or bare "/legislation/"
    bill_link_re = re.compile(r'/legislation/[a-z]{1,4}\d{3,4}/', re.I)
    for table in soup.find_all("table"):
        matches = table.find_all("a", href=bill_link_re)
        if len(matches) >= 3:
            return table
    return None


def _parse_bill_table(table: Tag, year: str) -> list[dict]:
    """
    Parse a bill listing table.

    Idaho legislature tables use these column orderings (varies by page):
    Minidata:   Bill | RS# | Title | Introduced By | Status
    Main page:  Bill | Title | Sponsors | Committee | Status/Last Action
    """
    rows = table.find_all("tr")
    if not rows:
        return []

    # Detect column positions from header row
    header_row = rows[0]
    headers = [th.get_text(strip=True).lower() for th in header_row.find_all(["th", "td"])]
    log.debug("Table headers: %s", headers)

    col_bill     = _col_index(headers, ["bill", "bill number", "#"])
    col_title    = _col_index(headers, ["title", "short title", "subject"])
    col_sponsor  = _col_index(headers, ["introduced by", "sponsor", "sponsors", "author"])
    col_cmte     = _col_index(headers, ["committee", "assigned to"])
    col_status   = _col_index(headers, ["status", "last action", "action"])

    bills = []
    base_url = "https://legislature.idaho.gov"

    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue

        # Bill number + URL
        bill_cell = cells[col_bill] if col_bill is not None and col_bill < len(cells) else cells[0]
        link = bill_cell.find("a")
        if not link:
            continue

        raw_id = link.get_text(strip=True)
        href = link.get("href", "")
        if href and not href.startswith("http"):
            href = base_url + href

        # If we have a URL fragment, extract the bill ID from there (more reliable)
        frag_match = re.search(r'/legislation/([a-z0-9]+)/', href, re.I)
        if frag_match:
            raw_id_from_url = frag_match.group(1)
        else:
            raw_id_from_url = raw_id

        bill_type, number, alias, url_fragment = parse_bill_id(raw_id_from_url)
        if not number:
            continue

        canonical_url = bill_url(year, url_fragment) if not href else href

        def _cell_text(idx):
            if idx is not None and idx < len(cells):
                return cells[idx].get_text(" ", strip=True)
            return ""

        title      = _cell_text(col_title)
        sponsor    = _cell_text(col_sponsor)
        committee  = _cell_text(col_cmte)
        last_action = _cell_text(col_status)

        bills.append({
            "id":          raw_id_from_url.upper(),
            "bill_type":   bill_type,
            "number":      number,
            "alias":       alias,
            "url":         canonical_url,
            "title":       title,
            "sponsor":     sponsor,
            "committee":   committee,
            "last_action": last_action,
        })

    return bills


def _col_index(headers: list[str], candidates: list[str]) -> int | None:
    for c in candidates:
        try:
            return headers.index(c)
        except ValueError:
            pass
    # Partial match fallback
    for c in candidates:
        for i, h in enumerate(headers):
            if c in h:
                return i
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Individual bill page parser
# ─────────────────────────────────────────────────────────────────────────────

def parse_bill_page(soup: BeautifulSoup, base_info: dict) -> dict:
    """
    Parse a full bill detail page.

    Returns an enriched copy of base_info with added keys:
      introduced_by, description, history (list of dicts), sponsors (list),
      committees (list), effective_dates (list), session_law
    """
    data = dict(base_info)
    data.setdefault("introduced_by", "")
    data.setdefault("description", "")
    data.setdefault("history", [])
    data.setdefault("sponsors", [])
    data.setdefault("committees", [])
    data.setdefault("effective_dates", [])
    data.setdefault("session_law", "")

    # ── Pull sponsor links from the page ─────────────────────────────────────
    sponsors = _extract_sponsors(soup)
    if sponsors:
        data["sponsors"] = sponsors

    # ── Pull "Introduced by / committee" line ────────────────────────────────
    intro, description = _extract_intro_and_description(soup)
    if intro:
        data["introduced_by"] = intro
    if description and not data.get("title"):
        data["description"] = description
    elif description:
        data["description"] = description

    # ── Parse action-history table ────────────────────────────────────────────
    history = _extract_action_history(soup)
    if history:
        data["history"] = history

    # ── Extract effective dates and session law from history ──────────────────
    for entry in data["history"]:
        action_lower = entry.get("action", "").lower()
        if "effective" in action_lower:
            data["effective_dates"].append(entry["action"])
        if "session law" in action_lower or (
            "chapter" in action_lower and "session" in action_lower
        ):
            data["session_law"] = entry["action"]

    return data


def _extract_sponsors(soup: BeautifulSoup) -> list[str]:
    """Return list of sponsor names found in the bill header."""
    sponsors: list[str] = []

    # Look for elements labelled "Sponsor" or "Introduced by" near a list of links
    for label in soup.find_all(string=re.compile(r'sponsor', re.I)):
        parent = label.parent
        if parent is None:
            continue
        # Try the parent's parent (wrapper element)
        container = parent.parent or parent
        for a in container.find_all("a"):
            name = a.get_text(strip=True)
            if name and len(name) > 2:
                sponsors.append(name)
        if sponsors:
            return sponsors

    # Fallback: look for the by-line "by NAME, NAME" near the top of the page
    body = soup.find("body") or soup
    for tag in body.find_all(["p", "div", "td", "span"], limit=50):
        text = tag.get_text(strip=True)
        if re.match(r'^by\s+', text, re.I) and len(text) < 200:
            # Extract names from the by-line
            name_part = re.sub(r'^by\s+', '', text, flags=re.I)
            # Remove parenthetical committee refs
            name_part = re.sub(r'\([^)]+\)', '', name_part)
            raw_names = re.split(r',\s*|\s+and\s+', name_part)
            for n in raw_names:
                n = n.strip()
                if n and len(n) > 2:
                    sponsors.append(n)
            if sponsors:
                return sponsors

    return sponsors


def _extract_intro_and_description(soup: BeautifulSoup) -> tuple[str, str]:
    """
    Return (introduced_by_line, description_text).

    On Idaho legislature pages, the bill body usually looks like:
      <div ...>
        <p>by COMMITTEE NAME</p>
        <p>SUBJECT MATTER – Description of what the bill does.</p>
      </div>
    """
    intro = ""
    description = ""

    # Try to find a block that starts with "by " or "BY "
    body = soup.find("body") or soup
    for tag in body.find_all(["p", "div", "td", "span"], limit=100):
        # Only look at direct text content, not deeply nested blocks
        direct_text = "".join(
            str(s) for s in tag.children
            if isinstance(s, str)
        ).strip()
        if not direct_text:
            direct_text = tag.get_text(strip=True)

        if not intro and re.match(r'^by\b', direct_text, re.I) and len(direct_text) < 300:
            intro = direct_text
            continue

        # Once we have the intro, the next substantial text is the description
        if intro and not description:
            text = tag.get_text(strip=True)
            # Filter out navigation / boilerplate
            if (text and len(text) > 15
                    and not re.match(r'^(home|about|contact|search|menu)', text, re.I)
                    and "legislature.idaho.gov" not in text.lower()):
                description = text
                break

    return intro, description


def _extract_action_history(soup: BeautifulSoup) -> list[dict]:
    """
    Parse the bill's legislative action history from any table on the page
    that contains date-formatted entries.

    Handles these Idaho legislature date formats:
      MM/DD           e.g. "1/13" or "01/13"   (most common)
      MM/DD/YYYY      e.g. "1/13/2026"          (occasionally used)
    """
    history: list[dict] = []
    # Accept MM/DD or MM/DD/YYYY; capture only MM/DD for normalised output
    date_re = re.compile(r'^(\d{1,2}/\d{1,2})(?:/\d{2,4})?$')

    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        candidate_entries: list[dict] = []

        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) < 2:
                continue

            # Check if first cell looks like a date (MM/DD or MM/DD/YYYY)
            cell0 = cells[0].get_text(strip=True)
            date_match = date_re.match(cell0)
            if not date_match:
                continue

            date_str = date_match.group(1)  # normalised MM/DD only
            action_text = cells[1].get_text(" ", strip=True)

            entry: dict = {"date": date_str, "action": action_text}

            # Look for vote detail rows: AYES/NAYS lines are often in sub-cells
            # or follow in the same row as additional cells
            vote_lines: list[str] = []
            for cell in cells[2:]:
                ct = cell.get_text(" ", strip=True)
                if ct:
                    vote_lines.append(ct)

            # Also look for bold/strong text within the action cell for vote tallies
            for strong in cells[1].find_all(["strong", "b"]):
                label = strong.get_text(strip=True)
                if label and label not in action_text:
                    vote_lines.append(label)

            if vote_lines:
                entry["votes"] = " | ".join(vote_lines)

            # Check for AYES/NAYS lines as sibling rows (continuation rows)
            # These rows typically have no date in cell 0
            candidate_entries.append(entry)

        # A valid history table needs at least 2 date-based entries
        if len(candidate_entries) >= 2:
            history = candidate_entries
            break  # Use first matching table

    # If we still have no history, try to parse structured text blocks
    if not history:
        history = _extract_history_from_text(soup)

    # Post-process: attach continuation rows (AYES/NAYS) to previous entries
    history = _attach_vote_continuations(soup, history)

    return history


def _extract_history_from_text(soup: BeautifulSoup) -> list[dict]:
    """Fallback: parse date-prefixed lines from raw page text."""
    history: list[dict] = []
    date_re = re.compile(r'^(\d{1,2}/\d{1,2})\s+(.+)$')

    for line in soup.get_text(separator="\n").splitlines():
        line = line.strip()
        m = date_re.match(line)
        if m:
            history.append({"date": m.group(1), "action": m.group(2)})

    return history


def _attach_vote_continuations(soup: BeautifulSoup, history: list[dict]) -> list[dict]:
    """
    Idaho legislature pages list AYES/NAYS as separate paragraphs or rows
    after the passage/failure entry. Attach them to the appropriate entry.
    """
    if not history:
        return history

    # Collect all bold/strong labelled vote lines from the page
    vote_blocks: list[str] = []
    for tag in soup.find_all(["strong", "b"]):
        text = tag.get_text(strip=True)
        if re.match(r'^(AYES|NAYS|Absent)', text, re.I):
            # Get the surrounding context
            parent = tag.parent
            if parent:
                block = parent.get_text(" ", strip=True)
                if block not in vote_blocks:
                    vote_blocks.append(block)

    if not vote_blocks:
        return history

    # Attach vote blocks to the nearest "PASSED"/"FAILED" entry
    for i, entry in enumerate(history):
        action_upper = entry["action"].upper()
        if "PASSED" in action_upper or "FAILED" in action_upper:
            if "votes" not in entry and vote_blocks:
                entry["votes"] = vote_blocks.pop(0)
            if not vote_blocks:
                break

    return history


# ─────────────────────────────────────────────────────────────────────────────
# Obsidian markdown generation
# ─────────────────────────────────────────────────────────────────────────────

def bill_to_markdown(data: dict, year: str) -> str:
    """Convert a parsed bill data dict to Obsidian-formatted markdown."""
    bill_type  = data.get("bill_type",  "")
    number     = data.get("number",     "")
    alias      = data.get("alias",      "")
    url        = data.get("url",        "")
    title      = data.get("title",      "")
    sponsor    = data.get("sponsor",    "")    # from minidata (plain text)
    sponsors   = data.get("sponsors",   [])    # from bill page (parsed names)
    committee  = data.get("committee",  "")    # from minidata
    committees = data.get("committees", [])    # from bill page
    history    = data.get("history",    [])
    last_action = data.get("last_action", "")
    intro      = data.get("introduced_by", "")
    description = data.get("description", "")

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # ── Frontmatter ───────────────────────────────────────────────────────────
    lines: list[str] = ["---"]

    lines.append("tags:")
    lines.append("  - bills")
    lines.append(f"  - {year}/session")

    lines.append("aliases:")
    lines.append(f"  - {alias}")

    # Committee(s)
    if committees:
        lines.append("cmte:")
        for c in committees:
            lines.append(f'  - "[[{c}]]"')
    elif committee:
        lines.append("cmte:")
        lines.append(f'  - "{committee}"')

    if url:
        lines.append(f"URL: {url}")

    # Sponsors (prefer parsed names from bill page over minidata text)
    active_sponsors = sponsors if sponsors else ([sponsor] if sponsor else [])
    if active_sponsors:
        lines.append("sponsor:")
        for s in active_sponsors:
            lines.append(f'  - "[[{s}]]"')

    # last_action stored verbatim so last_action_changed() can exact-match it
    if last_action:
        lines.append(f'last_action: "{last_action}"')
    lines.append(f'scraped: "{now_str}"')
    lines.append("---")
    lines.append("")

    # ── Body ──────────────────────────────────────────────────────────────────
    # "by COMMITTEE" intro line
    if intro:
        lines.append(intro)
        lines.append("")

    # Bill description / title
    display_title = description if description else title
    if display_title:
        lines.append(display_title)
        lines.append("")

    # Action history
    if history:
        lines.append(">")
        for entry in history:
            if not isinstance(entry, dict):
                lines.append(str(entry))
                continue
            date = entry.get("date", "")
            action = entry.get("action", "")
            votes = entry.get("votes", "")
            if date and action:
                lines.append(f"{date} \t{action}")
            elif action:
                lines.append(action)
            if votes:
                # Format vote blocks as bold-prefixed lines (matching existing vault style)
                for vline in votes.split(" | "):
                    vline = vline.strip()
                    if vline:
                        lines.append(f"\t**{vline}**")
    elif last_action:
        lines.append(f"> Last action: {last_action}")

    lines.append("")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Staleness / finality checks
# ─────────────────────────────────────────────────────────────────────────────

def is_bill_finalized(filepath: Path) -> bool:
    """
    Return True if the existing markdown file describes a bill that has
    reached a terminal legislative state (signed, vetoed, failed, died).
    """
    if not filepath.exists():
        return False
    text = filepath.read_text(encoding="utf-8").lower()
    return any(phrase in text for phrase in FINAL_ACTIONS)


def last_action_changed(filepath: Path, new_last_action: str) -> bool:
    """
    Return True if the last_action from the minidata listing differs from
    what is stored in the existing markdown file's last-action frontmatter key.

    We write `last_action: "..."` into the frontmatter on every save so we can
    do an exact-match comparison here rather than a loose substring search.
    """
    if not filepath.exists():
        return True  # File doesn't exist → needs creation
    existing = filepath.read_text(encoding="utf-8")
    # Look for the exact frontmatter key we write
    stored_m = re.search(r'^last_action:\s*"(.+)"', existing, re.M)
    if not stored_m:
        # Older file without the key — treat as changed so we refresh it
        return True
    return stored_m.group(1).strip() != new_last_action.strip()


# ─────────────────────────────────────────────────────────────────────────────
# Main scrape loop
# ─────────────────────────────────────────────────────────────────────────────

def scrape_bills(
    year: str,
    force: bool = False,
    target_bill: str | None = None,
    dry_run: bool = False,
) -> tuple[int, int, int, int]:
    """
    Scrape bills for the given session year.

    Returns (new, updated, unchanged, errors).
    """
    BILLS_DIR.mkdir(parents=True, exist_ok=True)

    bill_list = get_bill_list(year)
    if not bill_list:
        log.error("Empty bill list — cannot continue")
        return 0, 0, 0, 1

    # Filter to a single bill if requested
    if target_bill:
        _, _, _, url_frag = parse_bill_id(target_bill)
        bill_list = [b for b in bill_list
                     if b["id"].upper() == url_frag.upper()
                     or b["alias"].upper() == target_bill.upper()]
        if not bill_list:
            log.error("Bill %s not found in listing", target_bill)
            return 0, 0, 0, 1
        log.info("Targeting single bill: %s", target_bill)

    new_count = updated_count = unchanged_count = error_count = 0
    total = len(bill_list)

    for idx, bill_info in enumerate(bill_list, start=1):
        bill_type = bill_info["bill_type"]
        number    = bill_info["number"]
        alias     = bill_info["alias"]
        url       = bill_info["url"]
        last_action = bill_info.get("last_action", "")

        filename = bill_filename(year, bill_type, number)
        filepath = BILLS_DIR / filename

        log.debug("[%d/%d] %s", idx, total, alias)

        # ── Skip logic ────────────────────────────────────────────────────────
        if not force:
            if is_bill_finalized(filepath):
                log.debug("  Skipping finalized bill: %s", alias)
                unchanged_count += 1
                continue

            if filepath.exists() and not last_action_changed(filepath, last_action):
                log.debug("  No change detected for: %s", alias)
                unchanged_count += 1
                continue

        # ── Fetch and parse bill page ─────────────────────────────────────────
        log.info("[%d/%d] Scraping %s — %s", idx, total, alias, url)
        soup = get_soup(url)

        if soup is None:
            log.warning("  Could not fetch %s — using minidata info only", alias)
            data = bill_info
            error_count += 1
        else:
            data = parse_bill_page(soup, bill_info)

        # ── Generate markdown ─────────────────────────────────────────────────
        markdown = bill_to_markdown(data, year)

        if dry_run:
            log.info("  [DRY RUN] Would write: %s", filename)
            print(f"\n{'='*60}")
            print(f"FILE: {filepath}")
            print('='*60)
            print(markdown)
            new_count += 1
        else:
            if filepath.exists():
                old = filepath.read_text(encoding="utf-8")
                # Compare ignoring volatile frontmatter lines (timestamp only;
                # last_action IS intentionally included so status changes register)
                _strip = lambda t: re.sub(r'^scraped:.*$', '', t, flags=re.M)
                old_body = _strip(old)
                new_body = _strip(markdown)
                if old_body == new_body:
                    log.debug("  Content unchanged: %s", filename)
                    unchanged_count += 1
                else:
                    filepath.write_text(markdown, encoding="utf-8")
                    log.info("  Updated: %s", filename)
                    updated_count += 1
            else:
                filepath.write_text(markdown, encoding="utf-8")
                log.info("  Created: %s", filename)
                new_count += 1

        # Rate limit between fetches
        if soup is not None and idx < total:
            time.sleep(REQUEST_DELAY)

    return new_count, updated_count, unchanged_count, error_count


# ─────────────────────────────────────────────────────────────────────────────
# Member profile scraper
# ─────────────────────────────────────────────────────────────────────────────

MEMBERS_DIR_HOUSE  = VAULT_ROOT / "GOVERNMENTS" / "IDAHO - LEGISLATIVE" / "IDAHO HOUSE"
MEMBERS_DIR_SENATE = VAULT_ROOT / "GOVERNMENTS" / "IDAHO - LEGISLATIVE" / "IDAHO SENATE"


def get_member_list(chamber: str, year: str) -> list[dict]:
    """
    Scrape the House or Senate membership listing page.

    chamber: 'house' or 'senate'
    Returns list of dicts: {name, district, party, email, url}
    """
    url = f"https://legislature.idaho.gov/{chamber}/membership/"
    log.info("Fetching %s member list from %s", chamber, url)
    soup = get_soup(url)
    if soup is None:
        log.error("Could not fetch %s membership page", chamber)
        return []

    members: list[dict] = []
    # Membership pages use a table with columns: Name | District | Party | Email
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if len(rows) < 5:
            continue
        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            if len(cells) < 2:
                continue
            link = cells[0].find("a")
            if not link:
                continue
            name = link.get_text(strip=True)
            href = link.get("href", "")
            if not href.startswith("http"):
                href = "https://legislature.idaho.gov" + href
            district = cells[1].get_text(strip=True) if len(cells) > 1 else ""
            party    = cells[2].get_text(strip=True) if len(cells) > 2 else ""
            email    = cells[3].get_text(strip=True) if len(cells) > 3 else ""
            members.append({
                "name": name, "district": district,
                "party": party, "email": email, "url": href,
                "chamber": chamber,
            })
        if members:
            break

    log.info("Found %d %s members", len(members), chamber)
    return members


def parse_member_page(soup: BeautifulSoup, base_info: dict) -> dict:
    """
    Parse an individual member profile page.
    Returns enriched dict with: name, party, district, term, address,
    phone_home, phone_session, email, occupation, committees, bio.
    """
    data = dict(base_info)
    data.setdefault("term", "")
    data.setdefault("address", "")
    data.setdefault("phone_home", "")
    data.setdefault("phone_session", "")
    data.setdefault("occupation", "")
    data.setdefault("bio", "")
    data.setdefault("committees", [])

    full_text = soup.get_text(separator="\n", strip=True)

    # Extract fields from the page text using common label patterns
    field_map = {
        "term":             r'(?:Term|Terms?):\s*(.+)',
        "address":          r'(?:Mailing\s+)?Address:\s*(.+)',
        "phone_home":       r'(?:Home|Phone):\s*([\d\s\(\)\-\.]+)',
        "phone_session":    r'(?:Statehouse|Session)\s+(?:Phone)?:\s*([\d\s\(\)\-\.]+)',
        "occupation":       r'(?:Occupation|Profession):\s*(.+)',
    }
    for field, pattern in field_map.items():
        m = re.search(pattern, full_text, re.I)
        if m and not data.get(field):
            data[field] = m.group(1).strip()

    # Extract committee memberships
    cmte_section = soup.find(string=re.compile(r'committee', re.I))
    if cmte_section:
        container = cmte_section.parent
        if container:
            for item in container.find_next_siblings(["li", "td", "p"], limit=20):
                text = item.get_text(strip=True)
                if text and len(text) < 100:
                    data["committees"].append(text)
                elif not text:
                    break

    # Extract bio paragraph (usually the longest text block on the page)
    paragraphs = [
        p.get_text(strip=True) for p in soup.find_all("p")
        if len(p.get_text(strip=True)) > 100
    ]
    if paragraphs:
        data["bio"] = max(paragraphs, key=len)

    return data


def member_to_markdown(data: dict, year: str) -> str:
    """Convert parsed member data to Obsidian-format markdown."""
    name      = data.get("name", "Unknown")
    chamber   = data.get("chamber", "")
    district  = data.get("district", "")
    party     = data.get("party", "")
    term      = data.get("term", "")
    address   = data.get("address", "")
    phone_s   = data.get("phone_session", "")
    email     = data.get("email", "")
    occ       = data.get("occupation", "")
    bio       = data.get("bio", "")
    cmtes     = data.get("committees", [])
    url       = data.get("url", "")
    now_str   = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Determine chamber tag
    chamber_tag = "idaho-house" if chamber == "house" else "idaho-senate"

    lines: list[str] = ["---"]
    lines.append("tags:")
    lines.append(f"  - {chamber_tag}")
    lines.append(f"  - {year}/session")

    if district:
        lines.append(f"district: \"{district}\"")
    if party:
        lines.append(f"party: \"{party}\"")
    if email:
        lines.append(f"email: {email}")
    if phone_s:
        lines.append(f"phone: \"{phone_s.strip()}\"")
    if url:
        lines.append(f"URL: {url}")
    lines.append(f'scraped: "{now_str}"')
    lines.append("---")
    lines.append("")

    # Header
    chamber_label = "Rep." if chamber == "house" else "Sen."
    lines.append(f"{chamber_label} {name}")
    lines.append("")

    if district:
        lines.append(f"**District:** {district}")
    if party:
        lines.append(f"**Party:** {party}")
    if term:
        lines.append(f"**Term:** {term}")
    if occ:
        lines.append(f"**Occupation:** {occ}")
    if address:
        lines.append(f"**Address:** {address}")
    lines.append("")

    if cmtes:
        lines.append("**Committees:**")
        for c in cmtes:
            lines.append(f"- [[{c}]]")
        lines.append("")

    if bio:
        lines.append(bio)
        lines.append("")

    return "\n".join(lines)


def scrape_members(year: str, dry_run: bool = False) -> tuple[int, int, int]:
    """
    Scrape House and Senate member profiles.
    Returns (new, updated, unchanged).
    """
    MEMBERS_DIR_HOUSE.mkdir(parents=True, exist_ok=True)
    MEMBERS_DIR_SENATE.mkdir(parents=True, exist_ok=True)

    new_count = updated_count = unchanged_count = 0

    for chamber in ("house", "senate"):
        members = get_member_list(chamber, year)
        members_dir = MEMBERS_DIR_HOUSE if chamber == "house" else MEMBERS_DIR_SENATE
        total = len(members)

        for idx, member_info in enumerate(members, start=1):
            name = member_info["name"]
            # Sanitize name for filename: remove title prefixes
            clean_name = re.sub(r'^(Rep\.|Sen\.)\s*', '', name, flags=re.I).strip()
            filename = f"{clean_name}.md"
            filepath = members_dir / filename

            log.info("[%d/%d %s] Scraping %s", idx, total, chamber.upper(), name)

            soup = get_soup(member_info["url"])
            if soup:
                data = parse_member_page(soup, member_info)
            else:
                data = member_info

            markdown = member_to_markdown(data, year)

            if dry_run:
                log.info("  [DRY RUN] Would write: %s", filename)
                new_count += 1
            elif filepath.exists():
                old = filepath.read_text(encoding="utf-8")
                old_body = re.sub(r'^scraped:.*$', '', old, flags=re.M)
                new_body = re.sub(r'^scraped:.*$', '', markdown, flags=re.M)
                if old_body == new_body:
                    unchanged_count += 1
                else:
                    filepath.write_text(markdown, encoding="utf-8")
                    updated_count += 1
            else:
                filepath.write_text(markdown, encoding="utf-8")
                new_count += 1

            if soup is not None and idx < total:
                time.sleep(REQUEST_DELAY)

    return new_count, updated_count, unchanged_count


# ─────────────────────────────────────────────────────────────────────────────
# Session note updater
# ─────────────────────────────────────────────────────────────────────────────

def _idaho_legislature_number(year: int) -> tuple[int, int]:
    """
    Return (legislature_number, session_ordinal) for a given year.

    Idaho Legislature numbering:
      64th  2017-2018   (1st session = 2017, 2nd = 2018)
      65th  2019-2020
      66th  2021-2022
      67th  2023-2024
      68th  2025-2026
      69th  2027-2028  …
    Each legislature spans two calendar years; odd years = 1st session,
    even years = 2nd session.
    """
    # 64th legislature started in 2017
    offset = year - 2017
    legislature = 64 + offset // 2
    session_ordinal = 1 if year % 2 == 1 else 2
    return legislature, session_ordinal


_ORDINAL = {1: "1st", 2: "2nd", 3: "3rd"}


def ensure_session_note(year: str) -> None:
    """Create the session note for *year* if it doesn't already exist."""
    sessions_dir = VAULT_ROOT / "GOVERNMENTS" / "IDAHO - LEGISLATIVE" / "SESSIONS"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    session_file = sessions_dir / f"{year} legislative session.md"

    if session_file.exists():
        log.debug("Session note already exists: %s", session_file.name)
        return

    yr = int(year)
    leg_num, sess_ord = _idaho_legislature_number(yr)
    sess_label = _ORDINAL.get(sess_ord, f"{sess_ord}th")
    # Idaho regular sessions convene the second Monday of January
    content = (
        f"---\n"
        f"tags:\n"
        f"  - {year}/session\n"
        f"---\n"
        f"{sess_label} [[legislative session|Regular Session]] "
        f"of the {leg_num}th [[Idaho Legislature]]\n\n"
        f"Session convened: January {year}\n"
    )
    session_file.write_text(content, encoding="utf-8")
    log.info("Created session note: %s", session_file.name)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scrape Idaho Legislature bills into Obsidian vault markdown files."
    )
    parser.add_argument(
        "--year", default=DEFAULT_YEAR,
        help=f"Session year to scrape (default: {DEFAULT_YEAR})"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Re-fetch all bills, including finalized ones"
    )
    parser.add_argument(
        "--bill", metavar="BILLID",
        help="Scrape only one bill (e.g. H0001, S0042, HCR001)"
    )
    parser.add_argument(
        "--members", action="store_true",
        help="Also scrape House and Senate member profiles"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print output without writing any files"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable debug logging"
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    log.info("Idaho Legislature Scraper — year=%s  force=%s  members=%s  dry_run=%s",
             args.year, args.force, args.members, args.dry_run)

    if not args.dry_run:
        ensure_session_note(args.year)

    start = datetime.now(timezone.utc)
    new, updated, unchanged, errors = scrape_bills(
        year=args.year,
        force=args.force,
        target_bill=args.bill,
        dry_run=args.dry_run,
    )

    if args.members:
        m_new, m_updated, m_unchanged = scrape_members(
            year=args.year,
            dry_run=args.dry_run,
        )
        log.info("Members — New: %d  Updated: %d  Unchanged: %d",
                 m_new, m_updated, m_unchanged)

    elapsed = (datetime.now(timezone.utc) - start).total_seconds()

    # Summary
    log.info("─" * 50)
    log.info("Scrape complete in %.1fs", elapsed)
    log.info("  New:       %d", new)
    log.info("  Updated:   %d", updated)
    log.info("  Unchanged: %d", unchanged)
    log.info("  Errors:    %d", errors)
    log.info("─" * 50)

    # Write GitHub Actions step summary if available
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(f"# Idaho Legislature Scraper — {date_str}\n\n")
            f.write(f"| Metric | Count |\n|---|---|\n")
            f.write(f"| New bills | {new} |\n")
            f.write(f"| Updated bills | {updated} |\n")
            f.write(f"| Unchanged bills | {unchanged} |\n")
            f.write(f"| Fetch errors | {errors} |\n")
            f.write(f"\nTotal processed: {new + updated + unchanged}\n")
            f.write(f"Elapsed: {elapsed:.1f}s\n")

    return 1 if errors > (new + updated + unchanged) else 0


if __name__ == "__main__":
    sys.exit(main())
