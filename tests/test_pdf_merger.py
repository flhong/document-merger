"""
Test suite for incremental PDF merger.
"""

import unittest
from pathlib import Path
import sys
import shutil

sys.path.insert(0, str(Path(__file__).parent.parent))

from document_merger import PDFMerger
from tests.generate_test_files import create_sample_pdf_files


class TestPDFMerger(unittest.TestCase):
    """Test cases for incremental PDF merger."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.test_dir = Path('tests/sample_pdfs')
        cls.output_dir = Path('tests/output')
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate test files
        if not cls.test_dir.exists():
            print("Generating test PDF files...")
            create_sample_pdf_files()
    
    def setUp(self):
        """Set up each test."""
        # Create a copy of document1 as master for testing
        self.master_pdf = self.output_dir / 'test_master.pdf'
        source_pdf = self.test_dir / 'document1.pdf'
        
        if source_pdf.exists():
            shutil.copy(source_pdf, self.master_pdf)
    
    def tearDown(self):
        """Clean up after each test."""
        # Clean up test files
        if self.master_pdf.exists():
            self.master_pdf.unlink()
        backup = self.output_dir / 'test_master_backup.pdf'
        if backup.exists():
            backup.unlink()
    
    def test_initialization(self):
        """Test PDFMerger initialization with master PDF."""
        if not self.master_pdf.exists():
            self.skipTest("Master PDF not found")
        
        merger = PDFMerger(str(self.master_pdf))
        self.assertIsNotNone(merger)
        self.assertGreater(merger.get_page_count(), 0)
        print(f"✓ PDFMerger initialized with {merger.get_page_count()} pages")
    
    def test_append_pdf(self):
        """Test appending a PDF to master."""
        if not self.master_pdf.exists():
            self.skipTest("Master PDF not found")
        
        merger = PDFMerger(str(self.master_pdf))
        initial_count = merger.get_page_count()
        
        doc2 = self.test_dir / 'document2.pdf'
        if doc2.exists():
            merger.append_pdf(str(doc2))
            new_count = merger.get_page_count()
            self.assertGreater(new_count, initial_count)
            print(f"✓ PDF appended: {initial_count} -> {new_count} pages")
    
    def test_append_multiple_pdfs(self):
        """Test appending multiple PDFs sequentially."""
        if not self.master_pdf.exists():
            self.skipTest("Master PDF not found")
        
        merger = PDFMerger(str(self.master_pdf))
        initial_count = merger.get_page_count()
        
        doc2 = self.test_dir / 'document2.pdf'
        doc3 = self.test_dir / 'document3.pdf'
        
        if doc2.exists():
            merger.append_pdf(str(doc2))
        if doc3.exists():
            merger.append_pdf(str(doc3))
        
        final_count = merger.get_page_count()
        appended_count = merger.get_appended_page_count()
        
        self.assertGreater(final_count, initial_count)
        self.assertGreater(appended_count, 0)
        print(f"✓ Multiple PDFs appended: {appended_count} pages added")
    
    def test_refresh_toc(self):
        """Test refreshing TOC."""
        if not self.master_pdf.exists():
            self.skipTest("Master PDF not found")
        
        merger = PDFMerger(str(self.master_pdf))
        toc = merger.refresh_toc(max_depth=2)
        self.assertIsInstance(toc, str)
        print(f"✓ TOC refreshed: {len(toc.split(chr(10)))} entries")
    
    def test_save(self):
        """Test saving master PDF."""
        if not self.master_pdf.exists():
            self.skipTest("Master PDF not found")
        
        merger = PDFMerger(str(self.master_pdf))
        doc2 = self.test_dir / 'document2.pdf'
        
        if doc2.exists():
            merger.append_pdf(str(doc2))
        
        original_size = self.master_pdf.stat().st_size
        merger.save()
        new_size = self.master_pdf.stat().st_size
        
        # File should be larger after appending
        self.assertGreater(new_size, original_size)
        print(f"✓ PDF saved: {original_size} -> {new_size} bytes")
    
    def test_backup_creation(self):
        """Test that backup is created when saving."""
        if not self.master_pdf.exists():
            self.skipTest("Master PDF not found")
        
        merger = PDFMerger(str(self.master_pdf))
        doc2 = self.test_dir / 'document2.pdf'
        
        if doc2.exists():
            merger.append_pdf(str(doc2))
            merger.save()
            
            backup = self.output_dir / 'test_master_backup.pdf'
            self.assertTrue(backup.exists())
            print(f"✓ Backup created: {backup}")
    
    def test_method_chaining(self):
        """Test method chaining."""
        if not self.master_pdf.exists():
            self.skipTest("Master PDF not found")
        
        doc2 = self.test_dir / 'document2.pdf'
        doc3 = self.test_dir / 'document3.pdf'
        
        merger = PDFMerger(str(self.master_pdf))
        
        if doc2.exists() and doc3.exists():
            result = merger.append_pdf(str(doc2)).append_pdf(str(doc3))
            self.assertIsInstance(result, PDFMerger)
            print(f"✓ Method chaining works")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
