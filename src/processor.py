import pdfplumber
import os

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf = None
        self.metadata = {}

    def load(self):
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")
        
        self.pdf = pdfplumber.open(self.pdf_path)
        self.metadata = self.pdf.metadata
        return self

    def close(self):
        if self.pdf:
            self.pdf.close()

    def analyze_layout(self, page_index):
        if not self.pdf:
            self.load()
            
        page = self.pdf.pages[page_index]
        width = page.width
        height = page.height
        
        chars = page.chars
        if not chars:
            return {"width": width, "height": height, "is_double_column": False, "char_count": 0}

        # Check for a vertical gutter in the middle
        # Divide the vertical space into 100 cells
        num_v_cells = 100
        v_cell_height = height / num_v_cells
        empty_v_cells = 0
        
        gutter_x_min = width * 0.48
        gutter_x_max = width * 0.52
        
        for i in range(num_v_cells):
            v_top = i * v_cell_height
            v_bottom = (i + 1) * v_cell_height
            
            # Check if any char overlaps this cell in the gutter zone
            cell_occupied = any(
                c['top'] < v_bottom and c['bottom'] > v_top and
                c['x0'] < gutter_x_max and c['x1'] > gutter_x_min
                for c in chars
            )
            if not cell_occupied:
                empty_v_cells += 1
        
        is_double_column = empty_v_cells > (num_v_cells * 0.6)
        
        return {
            "width": width,
            "height": height,
            "is_double_column": is_double_column,
            "empty_v_cells": empty_v_cells
        }

    def extract_equation_image(self, page_index, bbox, output_path):
        page = self.pdf.pages[page_index]
        # Crop to the equation bounding box (x0, top, x1, bottom)
        cropped = page.crop((bbox['x0'], bbox['top'], bbox['x1'], bbox['bottom']))
        img = cropped.to_image(resolution=300)
        img.save(output_path)
        return output_path

    def identify_equations(self, page_index):
        page = self.pdf.pages[page_index]
        math_fonts = ['CMMI', 'CMSY', 'Math']
        
        math_chars = [c for c in page.chars if any(mf in (c['fontname'] or "") for mf in math_fonts)]
        
        if not math_chars:
            return []
            
        # Group math characters into blocks (simple y-based grouping)
        blocks = []
        for c in sorted(math_chars, key=lambda x: x['top']):
            added = False
            for b in blocks:
                # If close vertically and horizontally
                if abs(c['top'] - b['bottom']) < 5 or abs(c['top'] - b['top']) < 5:
                    b['x0'] = min(b['x0'], c['x0'])
                    b['x1'] = max(b['x1'], c['x1'])
                    b['top'] = min(b['top'], c['top'])
                    b['bottom'] = max(b['bottom'], c['bottom'])
                    b['char_count'] = b.get('char_count', 0) + 1
                    added = True
                    break
            if not added:
                blocks.append({
                    'x0': c['x0'], 'x1': c['x1'], 
                    'top': c['top'], 'bottom': c['bottom'],
                    'char_count': 1
                })
        
        # Determine strategy and filter by size
        results = []
        for b in blocks:
            if (b['x1'] - b['x0']) < 15: continue
            
            # Heuristic for confidence: very long math blocks are harder to OCR
            if b['char_count'] > 60:
                b['strategy'] = 'image'
                b['confidence'] = 0.4
            else:
                b['strategy'] = 'ocr'
                b['confidence'] = 0.8
            results.append(b)
            
        return results

    def identify_tables(self, page_index):
        page = self.pdf.pages[page_index]
        return page.find_tables()

    def extract_text(self, page_index):
        layout = self.analyze_layout(page_index)
        page = self.pdf.pages[page_index]
        
        equations = self.identify_equations(page_index)
        if equations:
            ocr_count = len([e for e in equations if e['strategy'] == 'ocr'])
            img_count = len([e for e in equations if e['strategy'] == 'image'])
            print(f"  DEBUG: Found {len(equations)} equations on page {page_index} (OCR: {ocr_count}, Image: {img_count})")
            
        tables = self.identify_tables(page_index)
        if tables:
            print(f"  DEBUG: Found {len(tables)} tables on page {page_index}")

        if not layout["is_double_column"]:
            return page.extract_text(x_tolerance=1)
        
        # Double column extraction
        width = page.width
        mid = width / 2
        
        # Crop left and right columns
        # We use a small margin to avoid cutting off characters
        left_bbox = (0, 0, mid, page.height)
        right_bbox = (mid, 0, page.width, page.height)
        
        left_text = page.crop(left_bbox).extract_text(x_tolerance=1) or ""
        right_text = page.crop(right_bbox).extract_text(x_tolerance=1) or ""
        
        return left_text + "\n" + right_text

if __name__ == "__main__":
    # Quick test
    processor = PDFProcessor("data/samples/attention_is_all_you_need.pdf")
    processor.load()
    layout = processor.analyze_layout(0)
    print(f"Page 0 Layout: {layout}")
