# Challenge 1b: Multi-Collection PDF Analysis

## Overview
Advanced PDF analysis solution that processes multiple document collections and extracts relevant content based on specific personas and use cases. The solution is containerized for reproducibility and leverages both rule-based and machine learning (TF-IDF, cosine similarity) techniques for content extraction and ranking.

## Project Structure
```
Challenge_1b/
├── Collection 1/                    # Travel Planning
│   ├── PDFs/                       # South of France guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # (Output: analysis results, if present)
├── Collection 2/                    # Adobe Acrobat Learning
│   ├── PDFs/                       # Acrobat tutorials
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # (Output: analysis results, if present)
├── Collection 3/                    # Recipe Collection
│   ├── PDFs/                       # Cooking guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # (Output: analysis results, if present)
├── analyze_pdfs.py                  # Main analysis script
├── fix_titles.py                    # Section title/paragraph refinement
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container configuration
└── README.md                        # This file
```

## Collections

### Collection 1: Travel Planning
- **Challenge ID:** round_1b_002
- **Persona:** Travel Planner
- **Task:** Plan a 4-day trip for 10 college friends to South of France
- **Documents:** 7 travel guides

### Collection 2: Adobe Acrobat Learning
- **Challenge ID:** round_1b_003
- **Persona:** HR Professional
- **Task:** Create and manage fillable forms for onboarding and compliance
- **Documents:** 15 Acrobat guides

### Collection 3: Recipe Collection
- **Challenge ID:** round_1b_001
- **Persona:** Food Contractor
- **Task:** Prepare vegetarian buffet-style dinner menu for corporate gathering
- **Documents:** 9 cooking guides

## Input/Output Format

### Input JSON Structure
```json
{
  "challenge_info": {
    "challenge_id": "round_1b_XXX",
    "test_case_name": "specific_test_case"
  },
  "documents": [{"filename": "doc.pdf", "title": "Title"}],
  "persona": {"role": "User Persona"},
  "job_to_be_done": {"task": "Use case description"}
}
```

### Output JSON Structure
```json
{
  "metadata": {
    "input_documents": ["list"],
    "persona": "User Persona",
    "job_to_be_done": "Task description"
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "section_title": "Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Content",
      "page_number": 1
    }
  ]
}
```

## Key Features
- Persona-based content analysis
- Importance ranking of extracted sections
- Multi-collection document processing
- Structured JSON output with metadata

## Libraries and Dependencies

### Python Libraries
- **PyMuPDF (fitz):** PDF parsing and text extraction.
- **scikit-learn:** TF-IDF vectorization and cosine similarity for content ranking.
- **json, pathlib, collections, hashlib, datetime:** Standard Python libraries for data handling, file operations, and deduplication.

### System Libraries (Dockerfile)
- **libgl1, poppler-utils:** Required for PDF rendering and parsing in Linux environments.

### requirements.txt
```
PyMuPDF
scikit-learn
```

## How to Run the Code

### Using Docker (Recommended)
1. **Build the Docker Image**
   ```sh
   docker build -t pdf-analyzer-b .
   ```
2. **Run the Container**
   ```sh
   docker run --rm -v "$(cd "$(pwd)"; pwd | sed 's|^/c|C:|' | sed 's|/|\\|g'):/app" pdf-analyzer-b
   ```
   - This mounts the project directory and runs the analysis. Output JSON files will be created in `/app/output` inside the container (create this directory if needed).

### Running Locally (Without Docker)
1. **Install Python 3.10+**
2. **Install System Dependencies** (Linux)
   ```sh
   sudo apt-get update && sudo apt-get install -y libgl1 poppler-utils
   ```
3. **Install Python Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the Script**
   ```sh
   python analyze_pdfs.py
   ```
   - By default, the script expects `/app/Collection*` and outputs to `/app/output`. For local runs, you may need to adjust paths or mount directories accordingly.

## Solution and Model Explanation

- **Text Extraction:** Uses PyMuPDF to extract text from each page of each PDF in the collections.
- **Content Ranking:** Uses TF-IDF vectorization and cosine similarity (scikit-learn) to rank sections of text by relevance to the persona and job-to-be-done.
- **Section and Subsection Analysis:** Top-ranked sections are selected, refined, and deduplicated using additional heuristics and the `fix_titles.py` script.
- **Output Generation:** Results are written as structured JSON files for each collection, containing metadata, extracted sections, and refined content.

## Example Usage

```sh
docker build -t pdf-analyzer-b .
docker run --rm -v "$(cd "$(pwd)"; pwd | sed 's|^/c|C:|' | sed 's|/|\\|g'):/app" pdf-analyzer-b
```

## Notes
- Output files are generated in `/app/output` (create this directory if it does not exist).
- All dependencies are open source.
- The solution is designed for extensibility and can be adapted for new personas, tasks, or document types.
