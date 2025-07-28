# Adobe India Hackathon 2025

## Welcome to the "Connecting the Dots" Challenge

### Rethink Reading. Rediscover Knowledge

What if every time you opened a PDF, it didn't just sit there—it spoke to you, connected ideas, and narrated meaning across your entire library?

That's the future we're building — and we want you to help shape it.

In the Connecting the Dots Challenge, your mission is to reimagine the humble PDF as an intelligent, interactive experience—one that understands structure, surfaces insights, and responds to you like a trusted research companion.

---

## The Journey Ahead

**Round 1:** Kick things off by building the brains — extract structured outlines from raw PDFs with blazing speed and pinpoint accuracy. Then, power it up with on-device intelligence that understands sections and links related ideas together.

**Round 2:** It's showtime! Build a beautiful, intuitive reading webapp using Adobe's PDF Embed API. You will be using your Round 1 work to design a futuristic webapp.

---

## Why This Matters

In a world flooded with documents, what wins is not more content — it's context. You're not just building tools — you're building the future of how we read, learn, and connect. No matter your background — ML hacker, UI builder, or insight whisperer — this is your stage.

Are you in?

It's time to read between the lines. Connect the dots. And build a PDF experience that feels like magic. Let's go.

---

## Challenge Solutions

### Challenge 1a: PDF Processing Solution
Basic PDF processing with Docker containerization and structured data extraction.
- Extracts structured outlines from PDFs at high speed and accuracy
- Containerized for reproducibility and easy deployment
- See [`Challenge_1a/README.md`](./Challenge_1a/README.md) for full technical details

### Challenge 1b: Multi-Collection PDF Analysis
Advanced persona-based content analysis across multiple document collections.
- Analyzes and ranks content based on user persona and task
- Uses machine learning (TF-IDF, cosine similarity) for intelligent section extraction
- See [`Challenge_1b/README.md`](./Challenge_1b/README.md) for full technical details

> **Note:** Each challenge directory contains detailed documentation and implementation details. Please refer to the individual README files for comprehensive information about each solution.

---

## Key Libraries, Frameworks, and System Dependencies

### Python Libraries
- **PyMuPDF (fitz):** Fast, robust PDF parsing and text extraction
- **scikit-learn:** Machine learning for text vectorization and similarity analysis (Challenge 1b)
- **Standard Python libraries:** json, pathlib, collections, hashlib, datetime, re

### System Dependencies (via Docker)
- **libglib2.0-0, libxext6, libsm6, libxrender1:** Required for PyMuPDF (Challenge 1a)
- **libgl1, poppler-utils:** Required for PDF rendering and parsing (Challenge 1b)

### Containerization
- **Docker:** All solutions are containerized for reproducibility, security, and ease of deployment
- **Python 3.10-slim:** Lightweight, modern Python base image

---

## Solution Approach

This project is our answer to the "Connecting the Dots" challenge: transforming static PDFs into dynamic, intelligent companions for research and learning. We:
- Extract structure and meaning from raw PDFs with high performance
- Analyze and rank content based on user context and persona
- Use open source tools and containerization for transparency and reproducibility
- Lay the groundwork for a future-ready, interactive PDF reading experience

Explore each challenge's README for technical deep-dives, usage instructions, and implementation details.

---

**Let's connect the dots and build the future of reading—together.**

---

## TEAM MEMBERS:
- SHIKHAR SINHA
- SANSKAR DUBEY
- SACHIN KUMAR
