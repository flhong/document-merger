"""
Unit tests for hybrid document merger functionality.
"""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from document_merger import HybridMerger
from document_merger.config import Config


class TestHybridMerger(unittest.TestCase):
    """Test cases for HybridMerger class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.test_docs_dir = Path('tests/sample_docs')
        cls.test_pdfs_dir = Path('tests/sample_pdfs')
        cls.output_dir = Path('tests/output')
        cls.output_dir.mkdir(parents=True, exist_ok=True)
    
    def setUp(self):
        """Set up test case."""
        self.merger = HybridMerger(output_format='pdf')
    
    def tearDown(self):
        """Tear down test case."""
        self.merger.clear()
    
    def test_initialization(self):
        """Test HybridMerger initialization."""
        merger = HybridMerger(output_format='pdf')
        self.assertEqual(merger.output_format, 'pdf')
        self.assertEqual(len(merger.documents), 0)
    
    def test_invalid_output_format(self):
        """Test invalid output format raises error."""
        with self.assertRaises(ValueError):
            HybridMerger(output_format='invalid')
    
    def test_add_docx_document(self):
        """Test adding DOCX document."""
        doc_path = self.test_docs_dir / 'document1.docx'
        if doc_path.exists():
            self.merger.add_document(str(doc_path))
            self.assertEqual(self.merger.get_document_count(), 1)
            self.assertEqual(self.merger.get_docx_count(), 1)
    
    def test_add_pdf_document(self):
        """Test adding PDF document."""
        pdf_path = self.test_pdfs_dir / 'document1.pdf'
        if pdf_path.exists():
            self.merger.add_document(str(pdf_path))
            self.assertEqual(self.merger.get_document_count(), 1)
            self.assertEqual(self.merger.get_pdf_count(), 1)
    
    def test_add_mixed_documents(self):
        """Test adding mixed PDF and DOCX documents."""
        doc_path = self.test_docs_dir / 'document1.docx'
        pdf_path = self.test_pdfs_dir / 'document1.pdf'
        
        if doc_path.exists():
            self.merger.add_document(str(doc_path))
        if pdf_path.exists():
            self.merger.add_document(str(pdf_path))
        
        self.assertGreater(self.merger.get_document_count(), 0)
    
    def test_set_output_format(self):
        """Test setting output format."""
        self.merger.set_output_format('docx')
        self.assertEqual(self.merger.output_format, 'docx')
    
    def test_invalid_format_setting(self):
        """Test invalid format setting raises error."""
        with self.assertRaises(ValueError):
            self.merger.set_output_format('invalid')
    
    def test_method_chaining(self):
        """Test method chaining."""
        doc_path = self.test_docs_dir / 'document1.docx'
        if doc_path.exists():
            result = self.merger.add_document(str(doc_path)).set_output_format('pdf')
            self.assertIsInstance(result, HybridMerger)
    
    def test_get_counts(self):
        """Test document count methods."""
        doc_path = self.test_docs_dir / 'document1.docx'
        pdf_path = self.test_pdfs_dir / 'document1.pdf'
        
        if doc_path.exists():
            self.merger.add_document(str(doc_path))
        if pdf_path.exists():
            self.merger.add_document(str(pdf_path))
        
        self.assertEqual(self.merger.get_docx_count() + self.merger.get_pdf_count(), 
                        self.merger.get_document_count())
    
    def test_clear(self):
        """Test clearing merger state."""
        doc_path = self.test_docs_dir / 'document1.docx'
        if doc_path.exists():
            self.merger.add_document(str(doc_path))
            self.assertGreater(self.merger.get_document_count(), 0)
            self.merger.clear()
            self.assertEqual(self.merger.get_document_count(), 0)
    
    def test_config_initialization(self):
        """Test merger with custom config."""
        config = Config()
        merger = HybridMerger(config=config)
        self.assertIsNotNone(merger.config)


if __name__ == '__main__':
    unittest.main()
