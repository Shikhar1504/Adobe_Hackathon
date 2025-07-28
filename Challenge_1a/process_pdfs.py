import fitz  # PyMuPDF
import json
import re
from pathlib import Path


def extract_spans(pdf_path):
    doc = fitz.open(pdf_path)
    spans = []
    font_sizes = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        w, h = page.rect.width, page.rect.height
        prev_bottom = None
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text:
                        continue
                    font_size = span["size"]
                    bbox = span["bbox"]
                    is_bold = "Bold" in span.get("font", "")
                    is_all_caps = text.isupper()
                    x_centered = abs(((bbox[0] + bbox[2]) / 2) - w / 2) / w
                    indentation = bbox[0]  # left margin
                    font_family = span.get("font", "")
                    # Line spacing: vertical distance from previous span on the same page
                    line_spacing = None
                    if prev_bottom is not None:
                        line_spacing = bbox[1] - prev_bottom
                    prev_bottom = bbox[3]

                    spans.append({
                        "text": text,
                        "font_size": font_size,
                        "is_bold": is_bold,
                        "is_all_caps": is_all_caps,
                        "x_centered": x_centered,
                        "indentation": indentation,
                        "font_family": font_family,
                        "line_spacing": line_spacing if line_spacing is not None else 0.0,
                        "page": page_num,
                        "bbox": bbox
                    })
                    font_sizes.append(font_size)

    return spans, font_sizes


def assign_headings(spans, font_sizes):
    outline = []
    font_sizes = sorted(set(font_sizes), reverse=True)
    
    # Better font size thresholds based on debug output
    if len(font_sizes) >= 3:
        h1_threshold = font_sizes[1]  # Second largest font (16.0)
        h2_threshold = font_sizes[2]  # Third largest font (14.0)
    elif len(font_sizes) >= 2:
        h1_threshold = font_sizes[0]
        h2_threshold = font_sizes[1]
    else:
        h1_threshold = font_sizes[0] if font_sizes else 0
        h2_threshold = h1_threshold - 1

    # Improved patterns for heading detection
    h1_pattern = re.compile(r'^(\d+\.?\s+)?([A-Z][^.]*?)(\s*[-–]\s*[^.]*)?$')
    h2_pattern = re.compile(r'^(\d+\.\d+\s+)([^.]*?)(\s*[-–]\s*[^.]*)?$')
    
    # Known H1 titles
    known_h1_titles = {
        "revision history", "table of contents", "acknowledgements", 
        "references", "introduction to the foundation level extensions",
        "introduction to foundation level agile tester extension",
        "overview of the foundation level extension"
    }

    for span in spans:
        text = span["text"].strip()
        size = span["font_size"]
        page = span["page"]
        is_bold = span["is_bold"]

        # Skip very short or very long text
        if len(text) < 3 or len(text) > 150:
            continue

        # Skip text that's too centered (likely headers/footers)
        if span["x_centered"] > 0.3:
            continue

        # Check for known H1 titles
        is_known_h1 = any(title in text.lower() for title in known_h1_titles)
        
        # Check for numbered patterns
        h1_match = h1_pattern.match(text)
        h2_match = h2_pattern.match(text)
        
        # Determine heading level based on debug output
        if is_known_h1 or (h1_match and size >= h1_threshold and is_bold):
            outline.append({"level": "H1", "text": text, "page": page})
        elif h2_match and size >= h2_threshold:
            # H2 headings are not bold but have font size 14.0
            outline.append({"level": "H2", "text": text, "page": page})
        elif is_bold and size >= h1_threshold and page >= 2:
            # Additional H1 detection for bold, large text after page 1
            outline.append({"level": "H1", "text": text, "page": page})
        elif h1_match and size >= h1_threshold:
            # H1 numbered headings that might not be bold
            outline.append({"level": "H1", "text": text, "page": page})

    return outline


def process_pdf(pdf_path, output_path):
    spans, font_sizes = extract_spans(pdf_path)
    outline = assign_headings(spans, font_sizes)

    # Group first-page spans into lines by y-position (using bbox[1])
    first_page_spans = [span for span in spans if span["page"] == 0]
    if first_page_spans:
        max_font = max(span["font_size"] for span in first_page_spans)
        title_spans = [span for span in first_page_spans if abs(span["font_size"] - max_font) < 0.5]
        # Group by y-position (rounded to nearest int)
        lines = {}
        for span in title_spans:
            y = int(round(span["bbox"][1]))
            if y not in lines:
                lines[y] = []
            lines[y].append(span["text"].strip())
        # Sort lines by y (top to bottom)
        sorted_lines = [" ".join(lines[y]) for y in sorted(lines.keys())]
        # Filter lines: not all-caps, not too short, not known non-title
        non_title_patterns = ["copyright", "version", "notice", "board"]
        filtered = []
        for t in sorted_lines:
            t = t.strip()
            if t and len(t) > 8 and not t.isupper() and not any(pat in t.lower() for pat in non_title_patterns):
                filtered.append(t)
        # Only join the first 2 lines (adjust N as needed)
        title_text = "  ".join(filtered[:2]).strip() if filtered else "Document Title"
    else:
        title_text = "Document Title"
    # Exclude headings that match the title (case-insensitive, stripped), are too short, or are single characters
    clean_outline = [h for h in outline if len(h["text"].strip()) >= 8 and h["text"].strip().lower() != title_text.strip().lower()]

    # Clean and sort outline
    seen = set()
    final_outline = []
    for o in clean_outline:
        key = (o["text"].strip(), o["page"])
        if key not in seen:
            seen.add(key)
            final_outline.append(o)
    final_outline.sort(key=lambda x: (x["page"], x["text"]))

    result = {
        "title": title_text,
        "outline": final_outline
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Processed: {pdf_path.name} -> {output_path.name}")


if __name__ == "__main__":
    # input_dir = Path("sample_dataset/pdfs")
    # output_dir = Path("sample_dataset/outputs")
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")

    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_file in input_dir.glob("*.pdf"):
        out_path = output_dir / f"{pdf_file.stem}.json"
        process_pdf(pdf_file, out_path)