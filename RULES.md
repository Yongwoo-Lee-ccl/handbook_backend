# Handbook Backend Rules

## 1. Rule-Based First
- Always attempt to extract content using deterministic rules (page geometry, font sizes, text-layer coordinates) before using AI.
- Use `pdfplumber` for coordinate-based layout analysis.

## 2. Specialized Local AI
- For complex elements where rules fail (equations, complex tables), use specialized open-source models:
  - **Equations:** Pix2Tex (LaTeX-OCR) or similar.
  - **Tables:** PaddleOCR or specialized table-transformers.
- Avoid calling LLMs for raw extraction tasks that can be done locally.

## 3. LLM for "Final Tailoring"
- LLMs (Gemini, OpenAI, etc.) should only be used for:
  - Fixing broken text flows.
  - Improving Markdown consistency.
  - Converting raw OCR output into semantic HTML/EPUB structures.
- Always include a cost-reduction strategy (minimal prompt, compressed context).

## 4. Testing & Branches
- Every new feature MUST have a corresponding branch.
- Every new feature MUST include automated tests.
- Tests must be runnable with a single command and include real papers from ArXiv/IACR.

## 6. Performance Note
- For clean, digitally-born PDFs, open-source tools (Pix2Tex, PaddleOCR, pdfplumber) are 95%+ accurate and much faster/cheaper than LLMs.
- LLMs should be reserved for "fixing" the 5% where rule-based or specialized local models fail.
