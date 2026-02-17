import sys
import os
from src.processor import PDFProcessor
from src.epub_generator import EPUBGenerator
from src.llm_client import LLMClient

def convert_pdf_to_epub(pdf_path, output_path):
    print(f"Processing {pdf_path}...")
    
    # 1. Load and Analyze
    processor = PDFProcessor(pdf_path).load()
    title = processor.metadata.get("Title", os.path.basename(pdf_path))
    author = processor.metadata.get("Author", "Unknown Author")
    
    # 2. Extract and Refine
    llm = LLMClient()
    full_refined_text = ""
    
    # Process first few pages for demo
    max_pages = min(len(processor.pdf.pages), 5)
    for i in range(max_pages):
        print(f"  Extracting Page {i+1}...")
        raw_text = processor.extract_text(i)
        refined_text = llm.refine_content(raw_text)
        full_refined_text += f"\n\n<!-- Page {i+1} -->\n" + refined_text
        
    # 3. Generate EPUB
    print(f"Generating EPUB...")
    gen = EPUBGenerator(title, author)
    # Simple conversion to HTML paragraphs
    html_content = "".join([f"<p>{line}</p>" for line in full_refined_text.split("\n") if line.strip()])
    gen.add_chapter("Main Content", html_content)
    gen.generate(output_path)
    
    processor.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        # Default for testing
        pdf = "data/samples/attention_is_all_you_need.pdf"
        out = "output.epub"
    else:
        pdf = sys.argv[1]
        out = sys.argv[2]
        
    convert_pdf_to_epub(pdf, out)
