# Handbook Backend TODO

## Phase 1: Infrastructure & Data
- [ ] Setup `download_samples.py` for ArXiv/IACR.
- [ ] Initialize `pytest` suite.
- [ ] Create `PDFProcessor` skeleton.

## Phase 2: Layout Analysis (Rule-Based)
- [ ] Implement Page Segmentation (Header/Footer/Main).
- [ ] Implement Column Detection (Single vs. Double).
- [ ] Implement Block Detection (Text, Figure, Table, Equation).

## Phase 3: Specialized Extraction
- [ ] Integrate local Math OCR (LaTeX-OCR).
- [ ] Integrate local Table Extraction (PaddleOCR).
- [ ] Handle Figure extraction (save images + captions).

## Phase 4: LLM Refinement
- [ ] Create LLM Client interface (Gemini/OpenAI).
- [ ] Implement "Contextual Repair" (fixing flow across columns/pages).

## Phase 5: EPUB Assembly
- [ ] Implement EPUB generator using `EbookLib`.
- [ ] Create default CSS for academic papers.

## Phase 6: Automation
- [ ] Create a "Run All" script that processes a paper and validates output.
