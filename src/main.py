import sys
import os

# Add the project root to sys.path to allow running as a script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.processor import PDFProcessor
from src.epub_generator import EPUBGenerator
from src.llm_client import LLMClient

def convert_pdf_to_epub(pdf_path, output_path):
    print(f"Processing {pdf_path}...")
    
    # Ensure images directory exists
    img_dir = "data/images"
    os.makedirs(img_dir, exist_ok=True)
    
    # 1. Load and Analyze
    processor = PDFProcessor(pdf_path).load()
    title = processor.metadata.get("Title", os.path.basename(pdf_path))
    author = processor.metadata.get("Author", "Unknown Author")
    
    # 2. Extract and Refine
    llm = LLMClient()
    html_sections = []
    
    # Process first few pages for demo
    max_pages = min(len(processor.pdf.pages), 10)
    for i in range(max_pages):
        print(f"  Processing Page {i+1}...")
        
        # Extract text first
        page_text = processor.extract_text(i)
        refined_text = llm.refine_content(page_text)
        
        # Convert text to HTML paragraphs
        page_html = "".join([f"<p>{p.strip()}</p>" for p in refined_text.split("\n\n") if p.strip()])
        
        # Identify and insert equations as images or placeholders
        equations = processor.identify_equations(i)
        for idx, eq in enumerate(equations):
            if eq['strategy'] == 'image':
                img_name = f"page_{i+1}_eq_{idx+1}.png"
                img_path = os.path.join(img_dir, img_name)
                processor.extract_equation_image(i, eq, img_path)
                page_html += f'<div class="equation"><img src="{img_path}" alt="Equation" /></div>'
            else:
                page_html += f'<p class="equation-placeholder">[Equation Block {idx+1}]</p>'
        
        html_sections.append(page_html)
        
    # 3. Generate EPUB
    print(f"Generating EPUB...")
    gen = EPUBGenerator(title, author)
    full_content = "\n".join(html_sections)
    gen.add_chapter("Main Content", full_content)
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
