"""
Test suite for incremental Word merger.
"""

import unittest
from pathlib import Path
import sys
import shutil

sys.path.insert(0, str(Path(__file__).parent.parent))

from document_merger import WordMerger
from tests.generate_test_files import create_sample_docx_files


class TestWordMerger(unittest.TestCase):
    """Test cases for incremental Word merger."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.test_dir = Path('tests/sample_docs')
        cls.output_dir = Path('tests/output')
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate test files
        if not cls.test_dir.exists():
            print("Generating test DOCX files...")
            create_sample_docx_files()
    
    def setUp(self):
        """Set up each test."""
        # Create a copy of document1 as master for testing
        self.master_docx = self.output_dir / 'test_master.docx'
        source_docx = self.test_dir / 'document1.docx'
        
        if source_docx.exists():
            shutil.copy(source_docx, self.master_docx)
    
    def tearDown(self):
        """Clean up after each test."""
        # Clean up test files
        if self.master_docx.exists():
            self.master_docx.unlink()
        backup = self.output_dir / 'test_master_backup.docx'
        if backup.exists():
            backup.unlink()
    
    def test_initialization(self):
        """Test WordMerger initialization with master DOCX."""
        if not self.master_docx.exists():
            self.skipTest("Master DOCX not found")
        
        merger = WordMerger(str(self.master_docx))
        self.assertIsNotNone(merger)
        self.assertGreater(merger.get_paragraph_count(), 0)
        print(f"✓ WordMerger initialized with {merger.get_paragraph_count()} paragraphs")
    
    def test_append_document(self):
        """Test appending a DOCX to master."""
        if not self.master_docx.exists():
            self.skipTest("Master DOCX not found")
        
        merger = WordMerger(str(self.master_docx))
        initial_count = merger.get_paragraph_count()
        
        doc2 = self.test_dir / 'document2.docx'
        if doc2.exists():
            merger.append_document(str(doc2), add_page_break=True)
            new_count = merger.get_paragraph_count()
            self.assertGreater(new_count, initial_count)
            print(f"✓ DOCX appended: {initial_count} -> {new_count} paragraphs")
    
    def test_append_multiple_documents(self):
        """Test appending multiple DOCXs sequentially."""
        if not self.master_docx.exists():
            self.skipTest("Master DOCX not found")
        
        merger = WordMerger(str(self.master_docx))
        initial_count = merger.get_paragraph_count()
        
        doc2 = self.test_dir / 'document2.docx'
        doc3 = self.test_dir / 'document3.docx'
        
        if doc2.exists():
            merger.append_document(str(doc2))
        if doc3.exists():
            merger.append_document(str(doc3))
        
        final_count = merger.get_paragraph_count()
        appended_count = merger.get_appended_paragraph_count()
        
        self.assertGreater(final_count, initial_count)
        self.assertGreater(appended_count, 0)
        print(f"✓ Multiple DOCXs appended: {appended_count} paragraphs added")
    
    def test_refresh_toc(self):
        """Test refreshing TOC."""
        if not self.master_docx.exists():
            self.skipTest("Master DOCX not found")
        
        merger = WordMerger(str(self.master_docx))
        toc = merger.refresh_toc(max_depth=2)
        self.assertIsInstance(toc, str)
        print(f"✓ TOC refreshed: {len(toc.split(chr(10)))} entries")
    
    def test_save(self):
        """Test saving master DOCX."""
        if not self.master_docx.exists():
            self.skipTest("Master DOCX not found")
        
        merger = WordMerger(str(self.master_docx))
        doc2 = self.test_dir / 'document2.docx'
        
        if doc2.exists():
            merger.append_document(str(doc2))
        
        original_size = self.master_docx.stat().st_size
        merger.save()
        new_size = self.master_docx.stat().st_size
        
        # File should be larger after appending
        self.assertGreater(new_size, original_size)
        print(f"✓ DOCX saved: {original_size} -> {new_size} bytes")
    
    def test_backup_creation(self):
        """Test that backup is created when saving."""
        if not self.master_docx.exists():
            self.skipTest("Master DOCX not found")
        
        merger = WordMerger(str(self.master_docx))
        doc2 = self.test_dir / 'document2.docx'
        
        if doc2.exists():
            merger.append_document(str(doc2))
            merger.save()
            
            backup = self.output_dir / 'test_master_backup.docx'
            self.assertTrue(backup.exists())
            print(f"✓ Backup created: {backup}")
    
    def test_method_chaining(self):
        """Test method chaining."""
        if not self.master_docx.exists():
            self.skipTest("Master DOCX not found")
        
        doc2 = self.test_dir / 'document2.docx'
        doc3 = self.test_dir / 'document3.docx'
        
        merger = WordMerger(str(self.master_docx))
        
        if doc2.exists() and doc3.exists():
            result = merger.append_document(str(doc2)).append_document(str(doc3))
            self.assertIsInstance(result, WordMerger)
            print(f"✓ Method chaining works")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
