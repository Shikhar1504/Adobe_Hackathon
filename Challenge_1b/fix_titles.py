import fitz  # PyMuPDF
from pathlib import Path
import hashlib
from collections import defaultdict


def get_full_paragraph(page, match_line):
    """Get the full paragraph containing the matched line."""
    text = page.get_text("text")
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 40]
    for para in paragraphs:
        if match_line.strip() in para:
            return para.strip()
    return match_line.strip()


def get_nearby_title(page, match_line):
    """Guess a title/heading by font or proximity."""
    blocks = page.get_text("dict")["blocks"]
    candidate = match_line.strip().lower()

    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            line_text = " ".join([span["text"] for span in line["spans"]])
            if not line_text.strip():
                continue
            if candidate in line_text.lower():
                continue
            for span in line["spans"]:
                if "bold" in span.get("font", "").lower() or span["size"] > 12:
                    return line_text.strip()
    return ""


def fallback_title_from_text(text):
    """Extract a reasonable title candidate from refined_text."""
    lines = [l.strip("•:- ") for l in text.split("\n") if l.strip()]
    for line in lines:
        if (
            3 <= len(line) <= 70 and
            line[0].isupper() and
            not line.lower().startswith(("instructions", "ingredients", "conclusion"))
        ):
            return line
    return "Untitled Section"


def looks_like_bad_title(text):
    """Detect if a title is just a sentence fragment, not a real heading."""
    if not text:
        return True
    words = text.strip().split()
    return (
        len(words) > 12 or
        text.strip().endswith((".", ":", ";")) or
        text.strip()[0].islower() or
        "," in text
    )


def dedup_key_section(sec):
    """Hash key for deduplication of extracted_sections."""
    base = f"{sec['document']}|{sec['page_number']}|{sec.get('section_title', '')[:80]}"
    return hashlib.md5(base.encode()).hexdigest()


def dedup_key_subsection(sec):
    """Hash key for deduplication of subsection_analysis."""
    base = f"{sec['document']}|{sec['page_number']}|{sec.get('refined_text', '')[:100]}"
    return hashlib.md5(base.encode()).hexdigest()


def select_diverse_sections(sections, max_sections=8, min_unique_docs=4):
    """Select diverse sections from different documents."""
    selected = []
    doc_counts = defaultdict(int)

    for sec in sections:
        doc = sec["document"]
        selected_docs = set(s["document"] for s in selected)

        if len(selected_docs) < min_unique_docs:
            if doc not in selected_docs:
                selected.append(sec)
                doc_counts[doc] += 1
        else:
            if doc_counts[doc] < 2:
                selected.append(sec)
                doc_counts[doc] += 1

        if len(selected) >= max_sections:
            break

    return selected


def fix_outputs(extracted_sections, subsection_analysis, pdf_folder):
    """Fix section titles, clean paragraphs, and deduplicate."""
    pdf_cache = {}
    seen_section_keys = set()
    seen_subsection_keys = set()
    clean_extracted = []
    clean_subsections = []

    # Fix and deduplicate extracted_sections
    for sec in extracted_sections:
        doc = sec["document"]
        page_num = sec["page_number"]

        if doc not in pdf_cache:
            pdf_cache[doc] = fitz.open(Path(pdf_folder) / doc)
        page = pdf_cache[doc][page_num - 1]

        raw_title = sec.get("section_title", "").strip()
        if looks_like_bad_title(raw_title):
            nearby = get_nearby_title(page, raw_title)
            if not nearby:
                related_text = next(
                    (s["refined_text"] for s in subsection_analysis
                     if s["document"] == doc and s["page_number"] == page_num),
                    ""
                )
                nearby = fallback_title_from_text(related_text)
            raw_title = nearby or fallback_title_from_text(raw_title)

        sec["section_title"] = raw_title.strip().rstrip(".") + "."

        key = dedup_key_section(sec)
        if key not in seen_section_keys:
            seen_section_keys.add(key)
            clean_extracted.append(sec)

    # Fix and deduplicate subsection_analysis
    for sec in subsection_analysis:
        doc = sec["document"]
        page_num = sec["page_number"]

        if doc not in pdf_cache:
            pdf_cache[doc] = fitz.open(Path(pdf_folder) / doc)
        page = pdf_cache[doc][page_num - 1]

        match_text = sec.get("refined_text", "").strip()
        paragraph = get_full_paragraph(page, match_text)
        sec["refined_text"] = paragraph

        key = dedup_key_subsection(sec)
        if key not in seen_subsection_keys:
            seen_subsection_keys.add(key)
            clean_subsections.append(sec)

    return clean_extracted, clean_subsections
