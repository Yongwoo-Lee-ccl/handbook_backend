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
2. Activate virtual environment:
   - Linux/macOS: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Download test samples: `python3 scripts/download_samples.py`

## Usage

### Basic Conversion
Run the main script providing the input PDF and desired EPUB output path:
```bash
python3 src/main.py data/samples/attention_is_all_you_need.pdf output.epub
```

### Advanced Usage
The converter automatically performs the following steps:
1.  **Layout Detection**: Identifies if the paper is single or double column.
2.  **Equation Analysis**: Scans for mathematical formulas.
    -   **OCR Strategy**: For simple equations, it flags them for future OCR processing.
    -   **Image Strategy**: For complex equations (high character density), it recommends cropping them as images to preserve accuracy.
3.  **Refinement**: Hyphens at line breaks are automatically removed, and basic whitespace cleaning is performed.

### Example
To convert the ResNet paper:
```bash
python3 src/main.py data/samples/resnet.pdf resnet.epub
```
The console will output the number of detected equations and tables per page, helping you monitor the extraction quality.

## Testing
Run all tests and sample conversions:
`./scripts/run_all_tests.sh`
