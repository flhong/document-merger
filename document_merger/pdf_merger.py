"""
Incremental PDF document merging functionality.
Appends PDF files to a master document and refreshes TOC.
"""

import os
from pathlib import Path
from typing import Optional
from PyPDF2 import PdfReader, PdfWriter
from .toc_manager import TOCManager, TOCStyle
from .bookmark_manager import BookmarkManager
from .utils import validate_file_path, is_pdf, extract_headings_from_pdf
from .config import Config


class PDFMerger:
    """Incrementally append PDF files to a master document and refresh TOC."""
    
    def __init__(self, master_pdf_path: str, config: Optional[Config] = None):
        """Initialize PDF merger with a master document.
        
        Args:
            master_pdf_path: Path to master PDF file to append to
            config: Configuration object (optional)
        """
        validate_file_path(master_pdf_path, '.pdf')
        
        self.config = config or Config()
        self.master_pdf_path = master_pdf_path
        self.pdf_writer = None
        self.toc_manager = TOCManager()
        self.bookmark_manager = BookmarkManager()
        self.original_page_count = 0
        self._load_master_pdf()

    def _load_master_pdf(self) -> None:
        """Load master PDF into writer."""
        with open(self.master_pdf_path, 'rb') as f:
            reader = PdfReader(f)
            self.pdf_writer = PdfWriter()
            
            # Copy all pages from master
            for page in reader.pages:
                self.pdf_writer.add_page(page)
            
            # Store original page count
            self.original_page_count = len(reader.pages)
            
            # Extract existing outlines
            if reader.outline:
                self._extract_outlines(reader.outline, 0)

    def append_pdf(self, file_path: str, bookmark: Optional[str] = None) -> 'PDFMerger':
        """Append a PDF file to master document.
        
        Args:
            file_path: Path to PDF file to append
            bookmark: Optional bookmark title for this PDF
            
        Returns:
            Self for method chaining
        """
        validate_file_path(file_path, '.pdf')
        
        current_page = len(self.pdf_writer.pages)
        
        # Open and read PDF to append
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            
            # Add all pages from this PDF
            for page in reader.pages:
                self.pdf_writer.add_page(page)
            
            # Add bookmark if provided
            if bookmark:
                self.bookmark_manager.add_bookmark(
                    bookmark, 
                    current_page,
                    level=0
                )
            
            # Extract and store headings for TOC refresh
            headings = extract_headings_from_pdf(file_path)
            for heading, level in headings:
                self.toc_manager.add_entry(heading, current_page, level)
        
        return self

    def refresh_toc(self, max_depth: int = 3) -> str:
        """Refresh table of contents with current page numbers.
        
        This reads the master PDF, extracts headings, and updates page numbers.
        
        Args:
            max_depth: Maximum heading depth to include
            
        Returns:
            Formatted TOC string
        """
        # Clear and rebuild TOC from scratch
        self.toc_manager.clear()
        
        # Extract headings from master PDF
        headings = extract_headings_from_pdf(self.master_pdf_path)
        for heading, level in headings:
            self.toc_manager.add_entry(heading, 0, level)
        
        # Filter by max depth if needed
        if max_depth < self.toc_manager.get_max_level():
            self.toc_manager = self.toc_manager.filter_by_level(max_depth)
        
        return self.toc_manager.format_toc()

    def add_bookmark(self, title: str, page_num: int, level: int = 0) -> 'PDFMerger':
        """Add a bookmark to the document.
        
        Args:
            title: Bookmark title
            page_num: Page number (0-indexed)
            level: Hierarchy level
            
        Returns:
            Self for method chaining
        """
        self.bookmark_manager.add_bookmark(title, page_num, level)
        return self

    def get_page_count(self) -> int:
        """Get total page count of master PDF.
        
        Returns:
            Total number of pages
        """
        return len(self.pdf_writer.pages) if self.pdf_writer else 0

    def get_appended_page_count(self) -> int:
        """Get number of pages appended (not including original).
        
        Returns:
            Number of appended pages
        """
        return self.get_page_count() - self.original_page_count

    def save(self) -> None:
        """Save updated master PDF (overwrites original file)."""
        if not self.pdf_writer:
            raise ValueError("No PDF writer initialized")
        
        # Apply bookmarks
        self.bookmark_manager.apply_to_pdf(self.pdf_writer)
        
        # Create backup of original
        backup_path = str(self.master_pdf_path).rsplit('.', 1)[0] + '_backup.pdf'
        if Path(self.master_pdf_path).exists() and not Path(backup_path).exists():
            import shutil
            shutil.copy(self.master_pdf_path, backup_path)
        
        # Write to master file (overwrites)
        with open(self.master_pdf_path, 'wb') as f:
            self.pdf_writer.write(f)
        
        print(f"✓ Master PDF updated: {self.master_pdf_path}")
        print(f"  Total pages: {self.get_page_count()}")
        print(f"  Pages appended: {self.get_appended_page_count()}")
        if Path(backup_path).exists():
            print(f"  Backup saved: {backup_path}")

    def get_toc_manager(self) -> TOCManager:
        """Get TOC manager for direct access.
        
        Returns:
            TOCManager instance
        """
        return self.toc_manager

    def __repr__(self) -> str:
        """String representation."""
        return f"PDFMerger(master={Path(self.master_pdf_path).name}, pages={self.get_page_count()})"
