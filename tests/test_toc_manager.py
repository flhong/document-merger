"""
Unit tests for TOC manager functionality.
"""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from document_merger import TOCManager
from document_merger.toc_manager import TOCStyle, TOCEntry


class TestTOCManager(unittest.TestCase):
    """Test cases for TOCManager class."""
    
    def setUp(self):
        """Set up test case."""
        self.toc = TOCManager()
    
    def tearDown(self):
        """Tear down test case."""
        self.toc.clear()
    
    def test_initialization(self):
        """Test TOCManager initialization."""
        self.assertEqual(len(self.toc.entries), 0)
        self.assertEqual(self.toc.style, TOCStyle.FORMAL)
    
    def test_add_entry(self):
        """Test adding TOC entry."""
        self.toc.add_entry('Chapter 1', 1, level=1)
        self.assertEqual(len(self.toc.entries), 1)
        self.assertEqual(self.toc.entries[0].title, 'Chapter 1')
    
    def test_add_multiple_entries(self):
        """Test adding multiple TOC entries."""
        self.toc.add_entry('Chapter 1', 1, level=1)
        self.toc.add_entry('Section 1.1', 2, level=2)
        self.toc.add_entry('Chapter 2', 5, level=1)
        self.assertEqual(len(self.toc.entries), 3)
    
    def test_level_clamping(self):
        """Test that levels are clamped between 1-6."""
        self.toc.add_entry('Title', 1, level=0)
        self.assertEqual(self.toc.entries[0].level, 1)
        
        self.toc.add_entry('Title', 2, level=10)
        self.assertEqual(self.toc.entries[1].level, 6)
    
    def test_set_style(self):
        """Test setting TOC style."""
        self.toc.set_style(TOCStyle.SIMPLE)
        self.assertEqual(self.toc.style, TOCStyle.SIMPLE)
    
    def test_format_formal(self):
        """Test formal TOC formatting."""
        self.toc.add_entry('Chapter 1', 1, level=1)
        self.toc.set_style(TOCStyle.FORMAL)
        formatted = self.toc.format_toc()
        self.assertIn('Chapter 1', formatted)
        self.assertIn('1', formatted)  # Page number
    
    def test_format_simple(self):
        """Test simple TOC formatting."""
        self.toc.add_entry('Chapter 1', 1, level=1)
        self.toc.set_style(TOCStyle.SIMPLE)
        formatted = self.toc.format_toc()
        self.assertIn('Chapter 1', formatted)
        self.assertIn('(1)', formatted)  # Page number in parentheses
    
    def test_get_max_level(self):
        """Test getting maximum level."""
        self.toc.add_entry('Chapter 1', 1, level=1)
        self.toc.add_entry('Section 1.1', 2, level=2)
        self.toc.add_entry('Subsection 1.1.1', 3, level=3)
        self.assertEqual(self.toc.get_max_level(), 3)
    
    def test_filter_by_level(self):
        """Test filtering TOC by level."""
        self.toc.add_entry('Chapter 1', 1, level=1)
        self.toc.add_entry('Section 1.1', 2, level=2)
        self.toc.add_entry('Subsection 1.1.1', 3, level=3)
        
        filtered = self.toc.filter_by_level(2)
        self.assertEqual(len(filtered.entries), 2)
    
    def test_clear(self):
        """Test clearing TOC."""
        self.toc.add_entry('Chapter 1', 1, level=1)
        self.assertGreater(len(self.toc.entries), 0)
        self.toc.clear()
        self.assertEqual(len(self.toc.entries), 0)
    
    def test_update_page_numbers(self):
        """Test updating page numbers with offset."""
        self.toc.add_entry('Chapter 1', 1, level=1)
        self.toc.add_entry('Chapter 2', 5, level=1)
        
        self.toc.update_page_numbers(offset=2)
        self.assertEqual(self.toc.entries[0].page_num, 3)
        self.assertEqual(self.toc.entries[1].page_num, 7)
    
    def test_add_entries_batch(self):
        """Test batch adding entries."""
        entries = [
            ('Chapter 1', 1, 1),
            ('Section 1.1', 2, 2),
            ('Chapter 2', 5, 1),
        ]
        self.toc.add_entries_batch(entries)
        self.assertEqual(len(self.toc.entries), 3)
    
    def test_get_entries(self):
        """Test getting entries."""
        self.toc.add_entry('Chapter 1', 1, level=1)
        entries = self.toc.get_entries()
        self.assertEqual(len(entries), 1)
        self.assertIsInstance(entries[0], TOCEntry)


if __name__ == '__main__':
    unittest.main()
