from ebooklib import epub
import os

class EPUBGenerator:
    def __init__(self, title, author):
        self.book = epub.EpubBook()
        self.book.set_title(title)
        self.book.set_language('en')
        self.book.add_author(author)
        
        self.chapters = []
        self.content_parts = []

    def add_chapter(self, title, content_html, filename=None):
        if filename is None:
            filename = f"chapter_{len(self.chapters) + 1}.xhtml"
            
        chapter = epub.EpubHtml(title=title, file_name=filename, lang='en')
        chapter.content = f"<html><body><h1>{title}</h1>{content_html}</body></html>"
        
        self.book.add_item(chapter)
        self.chapters.append(chapter)
        return chapter

    def generate(self, output_path):
        # Add basic navigation
        self.book.toc = tuple(self.chapters)
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        
        # Define spine
        self.book.spine = ['nav'] + self.chapters
        
        epub.write_epub(output_path, self.book, {})
        print(f"EPUB saved to {output_path}")

if __name__ == "__main__":
    gen = EPUBGenerator("Test Paper", "Author Name")
    gen.add_chapter("Introduction", "<p>This is a test introduction.</p>")
    gen.generate("test.epub")
