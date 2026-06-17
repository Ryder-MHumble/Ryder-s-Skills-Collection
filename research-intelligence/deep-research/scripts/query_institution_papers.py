#!/usr/bin/env python3
"""
Institution Paper Tracker — API Query Engine
Queries OpenAlex + CrossRef APIs for papers from target institutions,
filters by affiliation match, and writes results to /tmp/paper_results.json.

Usage: python3 query_apis.py

Configure the variables below before running.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

try:
    from openpyxl import Workbook  # noqa: F401 — not used here but validates env
except ImportError:
    pass  # Not needed for query phase

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURATION — Edit these before running
# ═══════════════════════════════════════════════════════════════════════

INSTITUTIONS = [
    {
        "cn_name": "中关村人工智能研究院",
        "en_name": "Zhongguancun Institute of Artificial Intelligence",
        "keywords": ["zhongguancun", "institute", "artificial", "intelligence"],
        "person_type": "导师",  # default classification
    },
    {
        "cn_name": "北京中关村学院",
        "en_name": "Zhongguancun Academy",
        "keywords": ["zhongguancun", "academy"],
        "person_type": "导师",
    },
]

DATE_FROM = "2026-03"  # YYYY-MM or YYYY-MM-DD
DATE_TO = "2026-06"    # YYYY-MM or YYYY-MM-DD

OUTPUT_JSON = "/tmp/paper_results.json"

# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def http_get_json(url, timeout=30):
    """GET request, return parsed JSON."""
    req = urllib.request.Request(url, headers={"User-Agent": "InstitutionPaperTracker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def http_get_xml(url, timeout=30):
    """GET request, return parsed XML ElementTree."""
    req = urllib.request.Request(url, headers={"User-Agent": "InstitutionPaperTracker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return ET.fromstring(resp.read())


def is_affiliation_match(aff_string, keywords):
    """Check if affiliation string matches all keywords of target institution."""
    aff_lower = aff_string.lower()
    # False positive filter: addresses on Zhongguancun Road
    false_positive_markers = ["zhongguancun east road", "zhongguancun south street",
                              "zhongguancun south st", "zhongguancun north first street"]
    for marker in false_positive_markers:
        if marker in aff_lower and "academy" not in aff_lower and "institute" not in aff_lower:
            return False
    # Must contain ALL keywords
    return all(kw.lower() in aff_lower for kw in keywords)


def extract_arxiv_id_from_doi(doi):
    """Try to infer arXiv ID from DOI (e.g. 10.48550/arXiv.xxxx)."""
    if doi and "arxiv" in doi.lower():
        parts = doi.split(".")
        for p in parts:
            if p.startswith("2") and len(p) >= 8:
                return p
    return ""


# ═══════════════════════════════════════════════════════════════════════
# CROSSREF QUERY
# ═══════════════════════════════════════════════════════════════════════

def query_crossref(inst, date_from, date_to, max_rows=50):
    """Search CrossRef by affiliation."""
    encoded = urllib.parse.quote(inst["en_name"])
    url = (f"https://api.crossref.org/works?"
           f"query.affiliation={encoded}"
           f"&filter=from-pub-date:{date_from},until-pub-date:{date_to}"
           f"&rows={max_rows}")
    try:
        data = http_get_json(url)
    except Exception as e:
        print(f"  CrossRef error: {e}")
        return []

    items = data.get("message", {}).get("items", [])
    results = []

    for r in items:
        titles = r.get("title", [])
        title = titles[0] if titles else "N/A"
        date_parts = r.get("published", {}).get("date-parts", [[""]])
        date_str = "-".join(str(x) for x in date_parts[0]) if date_parts else ""
        doi = r.get("DOI", "")

        for a in r.get("author", []):
            author_name = (a.get("given", "") + " " + a.get("family", "")).strip()
            for aff in a.get("affiliation", []):
                aff_name = aff.get("name", "")
                if is_affiliation_match(aff_name, inst["keywords"]):
                    # Check if arXiv DOI
                    arxiv_id = extract_arxiv_id_from_doi(doi)
                    arxiv_url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ""

                    # Full author list
                    all_authors = []
                    for au in r.get("author", []):
                        all_authors.append((au.get("given", "") + " " + au.get("family", "")).strip())
                    authors_str = "; ".join(all_authors)

                    results.append({
                        "person_type": inst.get("person_type", "学生"),
                        "name": author_name,
                        "institution": inst["cn_name"],
                        "title": title,
                        "date": date_str,
                        "arxiv_id": arxiv_id,
                        "arxiv_url": arxiv_url,
                        "doi": doi,
                        "authors": authors_str,
                        "source": "CrossRef",
                    })
                    break  # Don't double-count same author with multiple matching affs
    return results


# ═══════════════════════════════════════════════════════════════════════
# OPENALEX QUERY
# ═══════════════════════════════════════════════════════════════════════

def query_openalex(inst, date_from, max_per_query=25):
    """Search OpenAlex by full-text, then filter by raw_affiliation_strings."""
    encoded = urllib.parse.quote(inst["en_name"])
    url = (f"https://api.openalex.org/works?"
           f"search={encoded}"
           f"&filter=from_publication_date:{date_from}"
           f"&per_page={max_per_query}"
           f"&sort=publication_date:desc"
           f"&select=id,title,publication_date,doi")
    try:
        data = http_get_json(url)
    except Exception as e:
        print(f"  OpenAlex error: {e}")
        return []

    results = []
    seen_dois = set()

    for r in data.get("results", []):
        title = r.get("title", "N/A")
        date_str = r.get("publication_date", "")
        doi = r.get("doi", "") or ""
        work_id = r.get("id", "").split("/")[-1]

        # Fetch full work for authorships
        try:
            detail = http_get_json(
                f"https://api.openalex.org/works/{work_id}?select=id,title,authorships"
            )
        except Exception:
            continue

        for a in detail.get("authorships", []):
            author_name = a["author"]["display_name"]
            raw_affs = a.get("raw_affiliation_strings", [])
            inst_names = [i["display_name"] for i in a.get("institutions", [])]

            matched = False
            for aff in raw_affs + inst_names:
                if is_affiliation_match(aff, inst["keywords"]):
                    matched = True
                    break

            if not matched:
                continue

            # Extract arXiv ID from DOI if available
            arxiv_id = ""
            arxiv_url = ""
            if doi and "arxiv" in doi.lower():
                arxiv_id = doi.split("/")[-1]
                arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"

            # Full author list
            all_authors = [au["author"]["display_name"] for au in detail.get("authorships", [])]
            authors_str = "; ".join(all_authors)

            # Dedup by DOI+author
            dedup_key = (doi or title, author_name)
            if dedup_key in seen_dois:
                continue
            seen_dois.add(dedup_key)

            results.append({
                "person_type": inst.get("person_type", "学生"),
                "name": author_name,
                "institution": inst["cn_name"],
                "title": title,
                "date": date_str,
                "arxiv_id": arxiv_id,
                "arxiv_url": arxiv_url,
                "doi": doi,
                "authors": authors_str,
                "source": "OpenAlex",
            })

    return results


# ═══════════════════════════════════════════════════════════════════════
# ARXIV QUERY (supplementary — for known author names)
# ═══════════════════════════════════════════════════════════════════════

def query_arxiv(author_name, max_results=20):
    """Search arXiv by author name, return papers."""
    encoded = urllib.parse.quote(author_name)
    url = (f"http://export.arxiv.org/api/query?"
           f"search_query=au:{encoded}"
           f"&start=0&max_results={max_results}"
           f"&sortBy=submittedDate&sortOrder=descending")
    try:
        root = http_get_xml(url)
    except Exception as e:
        print(f"  arXiv error for '{author_name}': {e}")
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    results = []

    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
        published = entry.find("atom:published", ns).text[:10]  # YYYY-MM-DD
        entry_id = entry.find("atom:id", ns).text
        # Extract arXiv ID
        arxiv_id = entry_id.split("/abs/")[-1]
        # Remove version suffix
        if "v" in arxiv_id:
            base = arxiv_id.rsplit("v", 1)[0]
        else:
            base = arxiv_id

        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]

        results.append({
            "title": title,
            "date": published,
            "arxiv_id": base,
            "arxiv_url": f"https://arxiv.org/abs/{base}",
            "authors": "; ".join(authors),
        })

    return results


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    all_papers = []
    seen_keys = set()

    for inst in INSTITUTIONS:
        print(f"\n{'='*60}")
        print(f"Querying: {inst['cn_name']} ({inst['en_name']})")
        print(f"{'='*60}")

        # CrossRef
        print("  → CrossRef ...")
        cr_results = query_crossref(inst, DATE_FROM, DATE_TO)
        for p in cr_results:
            key = (p.get("doi", "") or p["title"], p["name"])
            if key not in seen_keys:
                seen_keys.add(key)
                all_papers.append(p)

        # OpenAlex
        print("  → OpenAlex ...")
        oa_results = query_openalex(inst, DATE_FROM)
        for p in oa_results:
            key = (p.get("doi", "") or p["title"], p["name"])
            if key not in seen_keys:
                seen_keys.add(key)
                all_papers.append(p)

        time.sleep(1)  # Rate limiting

    # Sort
    type_order = {"学生": 0, "导师": 1}
    all_papers.sort(
        key=lambda p: (type_order.get(p["person_type"], 9), p["date"]),
        reverse=False
    )

    # Save
    output = {"papers": all_papers}
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Total papers saved: {len(all_papers)}")
    print(f"   Output: {OUTPUT_JSON}")

    # Summary
    for inst in INSTITUTIONS:
        count = len([p for p in all_papers if p["institution"] == inst["cn_name"]])
        print(f"   {inst['cn_name']}: {count} papers")


if __name__ == "__main__":
    main()