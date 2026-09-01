"""
Bookmark/Outline management for PDF documents.
"""

from typing import List, Optional, Tuple
from PyPDF2 import PdfWriter


class BookmarkEntry:
    """Represents a bookmark entry."""
    
    def __init__(self, title: str, page_num: int, level: int = 0, parent=None):
        """Initialize bookmark entry.
        
        Args:
            title: Bookmark title
            page_num: Page number (0-indexed)
            level: Hierarchy level
            parent: Parent bookmark
        """
        self.title = title
        self.page_num = page_num
        self.level = level
        self.parent = parent
        self.children = []


class BookmarkManager:
    """Manages PDF bookmarks/outlines."""
    
    def __init__(self):
        """Initialize bookmark manager."""
        self.bookmarks: List[BookmarkEntry] = []
        self._bookmark_stack = []  # For hierarchical bookmarks

    def add_bookmark(self, title: str, page_num: int, level: int = 0) -> None:
        """Add a bookmark.
        
        Args:
            title: Bookmark title
            page_num: Page number (0-indexed)
            level: Hierarchy level (0 = root)
        """
        bookmark = BookmarkEntry(title, page_num, level)
        
        # Maintain hierarchy
        while self._bookmark_stack and self._bookmark_stack[-1].level >= level:
            self._bookmark_stack.pop()
        
        if self._bookmark_stack:
            parent = self._bookmark_stack[-1]
            bookmark.parent = parent
            parent.children.append(bookmark)
        else:
            self.bookmarks.append(bookmark)
        
        self._bookmark_stack.append(bookmark)

    def add_bookmarks_batch(self, bookmarks: List[Tuple[str, int, int]]) -> None:
        """Add multiple bookmarks.
        
        Args:
            bookmarks: List of (title, page_num, level) tuples
        """
        for title, page_num, level in bookmarks:
            self.add_bookmark(title, page_num, level)

    def apply_to_pdf(self, pdf_writer: PdfWriter) -> None:
        """Apply bookmarks to PDF writer.
        
        Args:
            pdf_writer: PyPDF2 PdfWriter instance
        """
        for bookmark in self.bookmarks:
            self._apply_bookmark_recursive(pdf_writer, bookmark)

    def _apply_bookmark_recursive(self, pdf_writer: PdfWriter, 
                                   bookmark: BookmarkEntry, 
                                   parent=None) -> None:
        """Recursively apply bookmark and children.
        
        Args:
            pdf_writer: PyPDF2 PdfWriter instance
            bookmark: Bookmark entry to apply
            parent: Parent bookmark in PDF
        """
        # Add this bookmark
        outline_item = pdf_writer.add_outline_item(
            bookmark.title,
            bookmark.page_num,
            parent=parent
        )
        
        # Add children
        for child in bookmark.children:
            self._apply_bookmark_recursive(pdf_writer, child, outline_item)

    def clear(self) -> None:
        """Clear all bookmarks."""
        self.bookmarks.clear()
        self._bookmark_stack.clear()

    def get_bookmarks(self) -> List[BookmarkEntry]:
        """Get all bookmarks.
        
        Returns:
            List of bookmark entries
        """
        return self.bookmarks.copy()

    def to_list(self) -> List[Tuple[str, int, int]]:
        """Convert bookmarks to list format.
        
        Returns:
            List of (title, page_num, level) tuples
        """
        result = []
        
        def traverse(bookmark: BookmarkEntry):
            result.append((bookmark.title, bookmark.page_num, bookmark.level))
            for child in bookmark.children:
                traverse(child)
        
        for bookmark in self.bookmarks:
            traverse(bookmark)
        
        return result

    def __repr__(self) -> str:
        """String representation."""
        return f"BookmarkManager({len(self.bookmarks)} bookmarks)"
