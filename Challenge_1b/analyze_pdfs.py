import os, json
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fix_titles import fix_outputs
from collections import defaultdict

def select_diverse_top_indices(all_sections, scores, top_k=10, min_unique_docs=5):
    sorted_indices = scores.argsort()[::-1]
    seen_docs = set()
    doc_counts = defaultdict(int)
    result = []

    for idx in sorted_indices:
        doc = all_sections[idx]["filename"]

        if len(seen_docs) < min_unique_docs:
            if doc not in seen_docs:
                result.append(idx)
                seen_docs.add(doc)
                doc_counts[doc] += 1
        elif doc_counts[doc] < 2:  # allow up to 2 from the same doc
            result.append(idx)
            doc_counts[doc] += 1

        if len(result) >= top_k:
            break

    return result


def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 30]
        for line in lines:
            sections.append({
                "text": line,
                "page": page_num,
                "filename": pdf_path.name
            })
    return sections


def analyze_collection(collection_path):
    pdf_dir = collection_path / "PDFs"
    query_file = collection_path / "challenge1b_input.json"

    with open(query_file, encoding="utf-8") as f:
        query = json.load(f)

    persona = query["persona"]["role"]
    task = query["job_to_be_done"]["task"]
    task_query = f"{persona} - {task}"

    all_sections = []
    for pdf in pdf_dir.glob("*.pdf"):
        all_sections.extend(extract_sections(pdf))

    if not all_sections:
        return {}

    texts = [sec["text"] for sec in all_sections]
    vectorizer = TfidfVectorizer().fit(texts + [task_query])
    query_vec = vectorizer.transform([task_query])
    doc_vecs = vectorizer.transform(texts)
    scores = cosine_similarity(query_vec, doc_vecs).flatten()

    # top_indices = scores.argsort()[::-1][:5]
    top_indices = select_diverse_top_indices(all_sections, scores, top_k=8, min_unique_docs=4)


    metadata = {
        "input_documents": sorted({s["filename"] for s in all_sections}),
        "persona": persona,
        "job_to_be_done": task,
        "processing_timestamp": datetime.utcnow().isoformat()
    }

    extracted_sections = []
    subsection_analysis = []

    for rank, idx in enumerate(top_indices, 1):
        sec = all_sections[idx]
        extracted_sections.append({
            "document": sec["filename"],
            "section_title": sec["text"],  # raw line, will fix later
            "importance_rank": rank,
            "page_number": sec["page"]
        })

        subsection_analysis.append({
            "document": sec["filename"],
            "refined_text": sec["text"],
            "page_number": sec["page"]
        })

    # 🔧 Fix section titles & paragraphs using external script
    extracted_sections, subsection_analysis = fix_outputs(
        extracted_sections, subsection_analysis, pdf_dir
    )

    return {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }


def main():
    base = Path("/app")
    output_dir = base / "output"
    output_dir.mkdir(exist_ok=True)

    for coll in base.glob("Collection*"):
        result = analyze_collection(coll)
        if result:
            with open(output_dir / f"{coll.name}.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
