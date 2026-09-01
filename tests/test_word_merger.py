"""
Unit tests for Word document merger functionality.
"""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from document_merger import WordMerger
from document_merger.config import Config
from docx import Document


class TestWordMerger(unittest.TestCase):
    """Test cases for WordMerger class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.test_dir = Path('tests/sample_docs')
        cls.output_dir = Path('tests/output')
        cls.output_dir.mkdir(parents=True, exist_ok=True)
    
    def setUp(self):
        """Set up test case."""
        self.merger = WordMerger()
    
    def tearDown(self):
        """Tear down test case."""
        self.merger.clear()
    
    def test_initialization(self):
        """Test WordMerger initialization."""
        merger = WordMerger()
        self.assertIsNone(merger.master_doc)
        self.assertEqual(len(merger.doc_files), 0)
        self.assertIsNotNone(merger.toc_manager)
    
    def test_add_document(self):
        """Test adding a Word document."""
        doc_path = self.test_dir / 'document1.docx'
        if doc_path.exists():
            self.merger.add_document(str(doc_path))
            self.assertEqual(len(self.merger.doc_files), 1)
    
    def test_add_multiple_documents(self):
        """Test adding multiple Word documents."""
        docs = [
            self.test_dir / 'document1.docx',
            self.test_dir / 'document2.docx',
            self.test_dir / 'document3.docx',
        ]
        
        for doc_path in docs:
            if doc_path.exists():
                self.merger.add_document(str(doc_path))
        
        self.assertGreater(len(self.merger.doc_files), 0)
    
    def test_merge(self):
        """Test merging documents."""
        doc_path = self.test_dir / 'document1.docx'
        if doc_path.exists():
            self.merger.add_document(str(doc_path))
            result = self.merger.merge()
            self.assertIsInstance(result, Document)
            self.assertIsNotNone(self.merger.master_doc)
    
    def test_method_chaining(self):
        """Test method chaining."""
        doc_path = self.test_dir / 'document1.docx'
        if doc_path.exists():
            result = self.merger.add_document(str(doc_path)).add_documents_batch([])
            self.assertIsInstance(result, WordMerger)
    
    def test_get_document(self):
        """Test getting master document."""
        doc_path = self.test_dir / 'document1.docx'
        if doc_path.exists():
            self.merger.add_document(str(doc_path))
            doc = self.merger.get_document()
            self.assertIsInstance(doc, Document)
    
    def test_save(self):
        """Test saving merged document."""
        doc_path = self.test_dir / 'document1.docx'
        if doc_path.exists():
            self.merger.add_document(str(doc_path))
            output_path = self.output_dir / 'test_merged.docx'
            self.merger.save(str(output_path))
            self.assertTrue(output_path.exists())
    
    def test_clear(self):
        """Test clearing merger state."""
        doc_path = self.test_dir / 'document1.docx'
        if doc_path.exists():
            self.merger.add_document(str(doc_path))
            self.assertGreater(len(self.merger.doc_files), 0)
            self.merger.clear()
            self.assertEqual(len(self.merger.doc_files), 0)
            self.assertIsNone(self.merger.master_doc)
    
    def test_config_initialization(self):
        """Test merger with custom config."""
        config = Config()
        merger = WordMerger(config)
        self.assertIsNotNone(merger.config)


class TestWordTOC(unittest.TestCase):
    """Test cases for Word TOC generation and refresh."""
    
    def setUp(self):
        """Set up test case."""
        self.merger = WordMerger()
        self.test_dir = Path('tests/sample_docs')
    
    def test_toc_generation(self):
        """Test TOC generation."""
        doc_path = self.test_dir / 'document1.docx'
        if doc_path.exists():
            self.merger.add_document(str(doc_path))
            toc = self.merger.generate_toc()
            self.assertIsInstance(toc, str)
    
    def test_refresh_toc(self):
        """Test TOC refresh."""
        doc_path = self.test_dir / 'document1.docx'
        if doc_path.exists():
            self.merger.add_document(str(doc_path))
            toc = self.merger.refresh_toc()
            self.assertIsInstance(toc, str)


if __name__ == '__main__':
    unittest.main()
