# Challenge 1a: PDF Processing Solution

## Overview
This is a sample solution for Challenge 1a of the Adobe India Hackathon 2025. The challenge requires implementing a PDF processing solution that extracts structured data from PDF documents and outputs JSON files. The solution is containerized using Docker and meets specific performance and resource constraints.

## Official Challenge Guidelines
### Submission Requirements
- **GitHub Project:** Complete code repository with working solution
- **Dockerfile:** Present in the root directory and functional
- **README.md:** Documentation explaining the solution, models, and libraries used

### Build Command
```sh
docker build --platform linux/amd64 -t pdf-processor .
```

### Run Command
```sh
docker run --rm \
  -v "$(pwd -W)/sample_dataset/pdfs:/app/input:ro" \
  -v "$(pwd -W)/sample_dataset/outputs:/app/output" \
  --network none \
  pdf-processor
```

### Critical Constraints
- **Execution Time:** ≤ 10 seconds for a 50-page PDF
- **Model Size:** ≤ 200MB (if using ML models)
- **Network:** No internet access allowed during runtime execution
- **Runtime:** Must run on CPU (amd64) with 8 CPUs and 16 GB RAM
- **Architecture:** Must work on AMD64, not ARM-specific

### Key Requirements
- **Automatic Processing:** Process all PDFs from `/app/input` directory
- **Output Format:** Generate `filename.json` for each `filename.pdf`
- **Input Directory:** Read-only access only
- **Open Source:** All libraries, models, and tools must be open source
- **Cross-Platform:** Test on both simple and complex PDFs

## Sample Solution Structure
```
Challenge_1a/
├── sample_dataset/
│   ├── pdfs/            # Input PDF files
│   ├── outputs/         # Output JSON files (generated after running the script; may be empty initially)
│   ├── schema/          # Output schema definition
│   │   └── output_schema.json
├── Dockerfile           # Docker container configuration
├── process_pdfs.py      # PDF processing script
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Libraries and Dependencies
### Python Libraries
- **PyMuPDF (fitz)**: `pymupdf==1.22.0`
  - Used for parsing and extracting text, font, and layout information from PDF files.
  - Provides access to low-level PDF structure, enabling extraction of spans, font sizes, and bounding boxes.
- **json**: Standard Python library for reading and writing JSON files.
- **re**: Standard Python library for regular expressions, used for heading detection.
- **pathlib**: Standard Python library for filesystem path operations.

### System Libraries (Installed via Dockerfile)
- **libglib2.0-0, libxext6, libsm6, libxrender1**: Required by PyMuPDF for rendering and PDF parsing support in Linux environments.

### requirements.txt
```
pymupdf==1.22.0
```

## How to Run the Code
### Using Docker (Recommended)
1. **Build the Docker Image**
   ```sh
   docker build --platform linux/amd64 -t pdf-processor .
   ```
2. **Run the Container**
   ```sh
   docker run --rm \
   -v "$(pwd -W)/sample_dataset/pdfs:/app/input:ro" \
   -v "$(pwd -W)/sample_dataset/outputs:/app/output" \
   --network none \
   pdf-processor
   ```
   - This mounts the input PDFs and output directory, and runs the script in a secure, reproducible environment.
   - Output JSON files will appear in `sample_dataset/outputs/`.

### Running Locally (Without Docker)
1. **Install Python 3.10+** (recommended for compatibility)
2. **Install System Dependencies** (Linux only)
   ```sh
   sudo apt-get update && sudo apt-get install -y libglib2.0-0 libxext6 libsm6 libxrender1
   ```
3. **Install Python Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the Script**
   ```sh
   python process_pdfs.py
   ```
   - By default, the script expects `/app/input` and `/app/output` directories (as in Docker). For local runs, you may need to modify the script to use `sample_dataset/pdfs` and `sample_dataset/outputs` as input/output paths, or create symlinks.

## Solution and Model Explanation
- **No ML Model Used:** This solution does not use a machine learning model, but rather rule-based extraction and heuristics for heading detection and document structure parsing.
- **Text Extraction:** Uses PyMuPDF to extract all text spans, font sizes, and layout features from each page.
- **Heading Detection:** Applies regular expressions and font size/boldness heuristics to identify H1 and H2 headings.
- **Output Generation:** Assembles a document outline and title, and writes a JSON file for each PDF, conforming to the schema in `sample_dataset/schema/output_schema.json`.

## Sample Implementation
### Current Sample Solution
The provided `process_pdfs.py` script demonstrates:
- PDF file scanning from the input directory
- Extraction of text spans, font sizes, and headings
- Generation of structured JSON output for each PDF
- Output file creation in the specified format (in `sample_dataset/outputs/`)

#### Main Processing Logic (`process_pdfs.py`)
- Uses [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) for PDF parsing
- Extracts text, font size, boldness, and layout features from each PDF page
- Detects headings (H1, H2) using font size, boldness, and regex patterns
- Assembles a document outline and title
- Outputs a JSON file for each PDF, matching the required schema

#### Example Code Snippet
```python
input_dir = Path("/app/input")
output_dir = Path("/app/output")
output_dir.mkdir(parents=True, exist_ok=True)
for pdf_file in input_dir.glob("*.pdf"):
    out_path = output_dir / f"{pdf_file.stem}.json"
    process_pdf(pdf_file, out_path)
```

### Docker Configuration
- Uses `python:3.10-slim` (AMD64) as the base image
- Installs system dependencies for PyMuPDF
- Installs Python dependencies from `requirements.txt`
- Copies the processing script and sample data structure
- Runs the script on container start

#### Dockerfile Excerpt
```dockerfile
FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY process_pdfs.py .
COPY sample_dataset/ sample_dataset/
CMD ["python", "process_pdfs.py"]
```

### Python Dependencies
- `pymupdf==1.22.0`

## Expected Output Format
Each PDF generates a corresponding JSON file that must conform to the schema defined in `sample_dataset/schema/output_schema.json` and is saved in the `sample_dataset/outputs/` directory.

#### Required JSON Structure
```json
{
  "title": "<Document Title>",
  "outline": [
    { "level": "H1", "text": "Section Title", "page": 0 },
    { "level": "H2", "text": "Subsection Title", "page": 1 }
    // ...
  ]
}
```

#### Schema Excerpt
- `title`: string, the document's main title
- `outline`: array of objects, each with:
  - `level`: string (e.g., "H1", "H2")
  - `text`: string (section heading)
  - `page`: integer (page number)

## Implementation Guidelines
### Performance Considerations
- **Memory Management:** Efficient handling of large PDFs
- **Processing Speed:** Optimized for sub-10-second execution
- **Resource Usage:** Stays within 16GB RAM constraint
- **CPU Utilization:** Efficient use of 8 CPU cores

### Testing Strategy
- **Simple PDFs:** Test with basic PDF documents
- **Complex PDFs:** Test with multi-column layouts, images, tables
- **Large PDFs:** Verify 50-page processing within time limit

### Local Testing
```sh
docker build --platform linux/amd64 -t pdf-processor .
docker run --rm \
  -v "$(pwd -W)/sample_dataset/pdfs:/app/input:ro" \
  -v "$(pwd -W)/sample_dataset/outputs:/app/output" \
  --network none \
  pdf-processor
```

## Validation Checklist
- All PDFs in input directory are processed
- JSON output files are generated for each PDF (in `sample_dataset/outputs/`)
- Output format matches required structure
- Output conforms to schema in `sample_dataset/schema/output_schema.json`
- Processing completes within 10 seconds for 50-page PDFs
- Solution works without internet access
- Memory usage stays within 16GB limit
- Compatible with AMD64 architecture

---
