Here’s a polished **README.md** you can drop into your GitHub repo:

---

# Persona-Driven PDF Outline Extractor

Extracts a structured outline (Title, H1, H2, H3) from PDFs using lightweight, font-size–based heuristics. Designed for **CPU-only**, **offline** execution with **no ML model weights**.

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-blue">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-ready-brightgreen">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-lightgrey">
</p>

---

## Table of Contents

* [Approach](#approach)
* [Libraries Used](#libraries-used)
* [Project Structure](#project-structure)
* [Quick Start](#quick-start)

  * [Run with Docker](#run-with-docker)
  * [Run Locally (Python)](#run-locally-python)
* [Input/Output](#inputoutput)
* [Example Output](#example-output)
* [Performance & Constraints](#performance--constraints)
* [Troubleshooting](#troubleshooting)
* [Roadmap](#roadmap)
* [License](#license)

---

## Approach

A simple, robust heuristic pipeline:

1. **Parse PDF pages** via `PyMuPDF` (`fitz`) to obtain text blocks, spans, and **font sizes**.
2. **Group lines by font size**:

   * The **largest font** lines are concatenated as the **document title**.
   * The next three descending font sizes are labeled **H1**, **H2**, **H3**.
3. **Emit JSON** with `title` and an `outline` list of `{ level, text, page }`.

Why this works:

* Most documents encode hierarchy through typography (size, weight).
* No heavyweight models required → fast, portable, offline.

---

## Libraries Used

* **PyMuPDF (fitz)** — PDF parsing and text span metadata.
* **Python stdlib** — `os`, `json`, `collections`.

No external ML models or network calls.

---

## Project Structure

```
.
├── input/                  # Put your PDFs here (mounted in Docker)
├── output/                 # JSON files are written here
├── main.py                 # Orchestrates batch processing
├── utils.py                # Heading extraction logic
├── requirements.txt        # PyMuPDF
├── Dockerfile              # Build + run container
└── README.md               # This file
```

---

## Quick Start

### Run with Docker

1. **Build** the image:

   ```bash
   docker build -t pdf-outline-extractor .
   ```

2. **Prepare folders** (host machine):

   ```bash
   mkdir -p input output
   # copy your PDFs into ./input
   ```

3. **Run**:

   ```bash
   docker run --rm \
     -v "$PWD/input:/app/input" \
     -v "$PWD/output:/app/output" \
     pdf-outline-extractor
   ```

> **Note (Windows PowerShell):**
>
> ```powershell
> docker run --rm `
>   -v "${PWD}\input:/app/input" `
>   -v "${PWD}\output:/app/output" `
>   pdf-outline-extractor
> ```

### Run Locally (Python)

> Requires Python 3.10+.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

mkdir -p input output
# copy PDFs into ./input

python main.py
```

---

## Input/Output

* **Input**: All `*.pdf` files placed in `./input`.
* **Output**: For each `file.pdf`, a corresponding `file.json` is written to `./output`.

File naming is preserved (just the extension changes to `.json`).

---

## Example Output

```json
{
  "title": "2024 Annual Financial Report",
  "outline": [
    { "level": "H1", "text": "Revenue Overview", "page": 1 },
    { "level": "H2", "text": "Quarterly Breakdown", "page": 2 },
    { "level": "H3", "text": "Q1 Highlights", "page": 3 }
  ]
}
```

---

## Performance & Constraints

* **CPU-only**, **offline**: No GPU, no internet access required.
* **Lightweight**: Only `PyMuPDF` + stdlib; Docker image based on `python:3.10-slim`.
* **Speed**: Heuristic, font-based parsing is typically **≲10 seconds for \~50 pages** (document-dependent).
* **Resource limits**: Should run comfortably on 8 vCPUs / 16 GB RAM.

> Your solution runs directly via the commands above; no extra orchestration is required.

---

## Troubleshooting

* **No output files**

  * Ensure PDFs are actually in `./input`.
  * Check container volume mounts (`-v` paths) and permissions.
* **Title looks duplicated or too long**

  * Some PDFs repeat large-font headers per page; the current approach concatenates them. Consider post-filtering (e.g., dedup or take first page only).
* **Heading levels seem off**

  * PDFs with irregular typography may require custom thresholds (e.g., skip tiny/huge outliers). See `utils.py` to tune:

    * Number of heading levels considered (`sorted_sizes[1:4]`).
    * Minimum line length filter (`len(line_text) >= 5`).

---

## Roadmap

* Weight/italic cues to refine heading detection.
* Deduplicate repeating headers/footers.
* Optional heuristics for multi-column layouts.
* Configurable levels (H1–H4) and size thresholds via CLI flags or env vars.
* Optional persona-aware post-filtering downstream (kept out of this extractor for simplicity).

---
