"""
Unit tests for PDF merger functionality.
"""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from document_merger import PDFMerger
from document_merger.config import Config


class TestPDFMerger(unittest.TestCase):
    """Test cases for PDFMerger class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.test_dir = Path('tests/sample_pdfs')
        cls.output_dir = Path('tests/output')
        cls.output_dir.mkdir(parents=True, exist_ok=True)
    
    def setUp(self):
        """Set up test case."""
        self.merger = PDFMerger()
    
    def tearDown(self):
        """Tear down test case."""
        self.merger.clear()
    
    def test_initialization(self):
        """Test PDFMerger initialization."""
        merger = PDFMerger()
        self.assertEqual(merger.page_count, 0)
        self.assertEqual(merger.get_pdf_count(), 0)
        self.assertIsNotNone(merger.toc_manager)
        self.assertIsNotNone(merger.bookmark_manager)
    
    def test_add_pdf(self):
        """Test adding a PDF file."""
        pdf_path = self.test_dir / 'document1.pdf'
        if pdf_path.exists():
            self.merger.add_pdf(str(pdf_path))
            self.assertEqual(self.merger.get_pdf_count(), 1)
            self.assertGreater(self.merger.page_count, 0)
    
    def test_add_multiple_pdfs(self):
        """Test adding multiple PDF files."""
        pdfs = [
            self.test_dir / 'document1.pdf',
            self.test_dir / 'document2.pdf',
            self.test_dir / 'document3.pdf',
        ]
        
        for pdf_path in pdfs:
            if pdf_path.exists():
                self.merger.add_pdf(str(pdf_path))
        
        self.assertGreaterEqual(self.merger.get_pdf_count(), 1)
    
    def test_add_pdf_with_bookmark(self):
        """Test adding PDF with bookmark."""
        pdf_path = self.test_dir / 'document1.pdf'
        if pdf_path.exists():
            self.merger.add_pdf(str(pdf_path), bookmark='Test Chapter')
            self.assertEqual(self.merger.get_pdf_count(), 1)
    
    def test_method_chaining(self):
        """Test method chaining."""
        pdf_path = self.test_dir / 'document1.pdf'
        if pdf_path.exists():
            result = self.merger.add_pdf(str(pdf_path)).add_bookmark('Chapter 1', 0)
            self.assertIsInstance(result, PDFMerger)
    
    def test_clear(self):
        """Test clearing merger state."""
        pdf_path = self.test_dir / 'document1.pdf'
        if pdf_path.exists():
            self.merger.add_pdf(str(pdf_path))
            self.assertGreater(self.merger.get_pdf_count(), 0)
            self.merger.clear()
            self.assertEqual(self.merger.get_pdf_count(), 0)
            self.assertEqual(self.merger.page_count, 0)
    
    def test_save(self):
        """Test saving merged PDF."""
        pdf_path = self.test_dir / 'document1.pdf'
        if pdf_path.exists():
            self.merger.add_pdf(str(pdf_path))
            output_path = self.output_dir / 'test_output.pdf'
            self.merger.save(str(output_path))
            self.assertTrue(output_path.exists())
            self.assertGreater(output_path.stat().st_size, 0)
    
    def test_config_initialization(self):
        """Test merger with custom config."""
        config = Config()
        merger = PDFMerger(config)
        self.assertIsNotNone(merger.config)


class TestPDFTOC(unittest.TestCase):
    """Test cases for PDF TOC generation."""
    
    def setUp(self):
        """Set up test case."""
        self.merger = PDFMerger()
    
    def test_toc_generation(self):
        """Test TOC generation."""
        test_dir = Path('tests/sample_pdfs')
        pdf_path = test_dir / 'document1.pdf'
        
        if pdf_path.exists():
            self.merger.add_pdf(str(pdf_path))
            toc = self.merger.generate_toc()
            self.assertIsInstance(toc, str)
    
    def test_add_bookmark(self):
        """Test adding bookmarks."""
        self.merger.add_bookmark('Chapter 1', 0)
        bookmarks = self.merger.bookmark_manager.get_bookmarks()
        self.assertEqual(len(bookmarks), 1)
        self.assertEqual(bookmarks[0].title, 'Chapter 1')


if __name__ == '__main__':
    unittest.main()
