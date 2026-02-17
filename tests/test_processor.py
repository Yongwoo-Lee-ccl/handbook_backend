import pytest
from src.processor import PDFProcessor
import os

def test_load_pdf():
    pdf_path = "data/samples/attention_is_all_you_need.pdf"
    if not os.path.exists(pdf_path):
        pytest.skip("Sample PDF not found")
        
    processor = PDFProcessor(pdf_path)
    processor.load()
    assert len(processor.pdf.pages) > 0
    assert "Title" in processor.metadata or "Author" in processor.metadata
    processor.close()

    # Test Double Column (Attention)
    pdf_path = "data/samples/attention_is_all_you_need.pdf"
    if os.path.exists(pdf_path):
        processor = PDFProcessor(pdf_path).load()
        layout = processor.analyze_layout(2) # Try page 3
        print(f"Attention Layout P3: {layout}")
        assert layout["is_double_column"] is True, f"Attention P3 should be double column, got {layout}"
        processor.close()

    # Test Single Column
    pdf_path = "data/samples/dilithium.pdf"
    if os.path.exists(pdf_path):
        processor = PDFProcessor(pdf_path).load()
        layout = processor.analyze_layout(1)
        print(f"Dilithium Layout: {layout}")
        assert layout["is_double_column"] is False, f"Dilithium should be single column, got {layout}"
        processor.close()
