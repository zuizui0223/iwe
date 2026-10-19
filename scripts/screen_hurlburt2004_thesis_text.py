"""Reproducible, source-only text triage of recovered Hurlburt thesis.

Scans the exact original PDF's existing text layer (never OCR, never
invents missing IDs) and reports candidate **physical PDF pages** for
a human check. Page selection is not evidence that the fruit-to-flower
join exists. Selected original pages are rendered as unreviewed previews.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

MARKED = re.compile(r"mark(?:ed|ing)?|tagg?ed|label(?:led|ed)|identifi(?:ed|cation)", re.I)
FRUITS = re.compile(r"fruit|seed|dissect|viab(?:le|ility)", re.I)
TIME = re.compile(r"flower|date|day|week|phenolog|timing", re.I)
JOIN = re.compile(r"inflorescen|clone|individual|cohort|tag|marked", re.I)
PROVENANCE = "10.7939/r3-fe1d-kj80"


def score_page(text: str) -> tuple[int, list[str]]:
    present = {
        "marked_units": bool(MARKED.search(text)),
        "fruit_or_seeds": bool(FRUITS.search(text)),
        "timing": bool(TIME.search(text)),
        "potential_unit_key": bool(JOIN.search(text)),
    }
    score = (3 * present["marked_units"] +
             3 * present["fruit_or_seeds"] +
             2 * present["timing"] +
             2 * present["potential_unit_key"])
    if all(present.values()):
        score += 6
    return score, [k for k, v in present.items() if v]


def short_context(text: str, limit: int = 220) -> str:
    """Display small original-context leads, not transcript or effect data."""
    trimmed = re.sub(r"\s+", " ", text).strip()
    for pat in (r"marked.{0,90}(?:fruit|seed|inflorescen)",
                r"(?:fruit|seed).{0,90}(?:mark|identif|date|cohort)",
                r"(?:clone|inflorescen).{0,90}(?:fruit|seed)"):
        hit = re.search(pat, trimmed, re.I)
        if hit:
            return trimmed[max(0, hit.start()-30):hit.end()+30][:limit]
    return trimmed[:limit]


def rank_pages(pages: list[str], max_pages: int = 12) -> list[dict]:
    ranked = []
    for index, page in enumerate(pages):
        score, tokens = score_page(page)
        if score >= 10 and len(page.strip()) >= 100:
            ranked.append({
                "physical_pdf_page": index + 1,
                "score": score,
                "keyword_groups": tokens,
                "text_layer_character_count": len(page),
                "lead_only": short_context(page),
                "join_verified": False,
            })
    return sorted(ranked, key=lambda r: (-r["score"], r["physical_pdf_page"]))[:max_pages]


def screen_pdf(pdf: Path, outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    if not pdf.is_file():
        raise ValueError("original PDF file missing")
    import fitz  # PyMuPDF; use existing PDF text layer without OCR
    with fitz.open(str(pdf)) as document:
        pages = [page.get_text("text", sort=True) for page in document]
    ranked = rank_pages(pages)
    summary = {
        "schema": "iwe_hurlburt2004_pdf_text_leads_v1",
        "thesis_doi": PROVENANCE,
        "physical_pages_found": len(pages),
        "pages_with_text_layer": sum(len(x.strip()) > 50 for x in pages),
        "candidate_pages": ranked,
        "original_pdf_visually_verified": False,
        "original_marked_fruit_linkage_verified": False,
        "original_mature_seed_by_date_verified": False,
        "strict_h1_promoted": False,
        "use": "source-level review pointers only, never source-linked quantitative extraction",
    }
    (outdir / "page_review_leads.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    )
    print(f"Thesis physical pages: {len(pages)}; text pages: {summary['pages_with_text_layer']}")
    print("Top candidate *physical PDF* pages (not a verified unit join):")
    for p in ranked[:12]:
        print(f"PDF page {p['physical_pdf_page']}: score={p['score']}; "
              f"excerpt={p['lead_only']}")
    # These source Methods/result pages contain the most plausible marked
    # flower -> fruit dissection design details and need visual verification.
    focus_pages = (83, 84, 85, 86, 87, 88, 119, 120, 121, 122)
    focus_terms = (
        "marked flower", "fruit dissection", "mature fruit",
        "flower was collected", "oviposition", "individual",
        "seed", "fruit"
    )
    targeted = []
    for n in focus_pages:
        if n > len(pages):
            continue
        flat = re.sub(r"\\s+", " ", pages[n - 1]).strip()
        snippets = []
        for term in focus_terms:
            pos = flat.lower().find(term)
            if pos >= 0:
                snippet = flat[max(0, pos - 100):pos + 450]
                if snippet not in snippets:
                    snippets.append(snippet)
            if len(snippets) >= 3:
                break
        targeted.append({
            "physical_pdf_page": n,
            "keywords_found": [w for w in focus_terms if w in flat.lower()],
            "source_excerpt_candidates": snippets,
            "visually_verified": False,
            "joined_raw_rows_verified": False
        })
        print(f"FOCUS PDF physical page {n}: " +
              " | ".join(snippets[:2]))
    summary["source_methods_targeted_pages"] = targeted
    (outdir / "page_review_leads.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\\n"
    )
    if ranked:
        preview = outdir / "original_page_previews_unreviewed"
        preview.mkdir(exist_ok=True)
        with fitz.open(str(pdf)) as document:
            for page_no in sorted(set(
                [p["physical_pdf_page"] for p in ranked[:5]] + [85, 86, 121]
            )):
                page = document[page_no - 1]
                image = page.get_pixmap(matrix=fitz.Matrix(1.25, 1.25),
                                        alpha=False)
                image.save(str(preview / f"pdf_physical_page_{page_no}.png"))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    x = ap.parse_args()
    screen_pdf(x.pdf, x.outdir)


if __name__ == "__main__":
    main()
