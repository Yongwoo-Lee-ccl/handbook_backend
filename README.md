# Handbook Backend

A PDF-to-EPUB converter optimized for academic papers.

## Features
- **Rule-Based Layout Analysis:** Detects single vs. double column layouts using vertical gutter clearance.
- **Column-Aware Extraction:** Preserves reading order by extracting text from columns separately.
- **Equation Detection:** Identifies mathematical content using math-font heuristics.
- **LLM Refinement:** Uses a modular client to polish text and fix flow issues (minimal cost approach).
- **EPUB Generation:** Produces valid EPUB files with semantic structure.

## Setup
1. Create virtual environment: `python3 -m venv venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Download test samples: `python3 scripts/download_samples.py`

## Usage
`python3 src/main.py <input_pdf> <output_epub>`

## Testing
Run all tests and sample conversions:
`./scripts/run_all_tests.sh`
