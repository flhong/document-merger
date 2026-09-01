"""
PDF document merging functionality.
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple
from PyPDF2 import PdfReader, PdfWriter
from .toc_manager import TOCManager, TOCStyle
from .bookmark_manager import BookmarkManager
from .utils import validate_file_path, is_pdf, create_output_directory
from .config import Config


class PDFMerger:
    """Merge multiple PDF files into a single document with TOC and bookmarks."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize PDF merger.
        
        Args:
            config: Configuration object (optional)
        """
        self.config = config or Config()
        self.pdf_files: List[str] = []
        self.pdf_reader: List[PdfReader] = []
        self.pdf_writer = PdfWriter()
        self.toc_manager = TOCManager()
        self.bookmark_manager = BookmarkManager()
        self.current_page = 0
        self.page_count = 0

    def add_pdf(self, file_path: str, bookmark: Optional[str] = None) -> 'PDFMerger':
        """Add a PDF file to merge queue.
        
        Args:
            file_path: Path to PDF file
            bookmark: Optional bookmark title for this PDF
            
        Returns:
            Self for method chaining
        """
        validate_file_path(file_path, '.pdf')
        
        # Open and read PDF
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            
            # Add all pages from this PDF
            for page_num, page in enumerate(reader.pages):
                self.pdf_writer.add_page(page)
            
            # Add bookmark if provided
            if bookmark:
                self.bookmark_manager.add_bookmark(
                    bookmark, 
                    self.current_page,
                    level=0
                )
            
            self.pdf_files.append(file_path)
            self.current_page += len(reader.pages)
            self.page_count += len(reader.pages)
        
        return self

    def add_pdfs_batch(self, file_paths: List[str], bookmarks: Optional[List[str]] = None) -> 'PDFMerger':
        """Add multiple PDF files at once.
        
        Args:
            file_paths: List of PDF file paths
            bookmarks: Optional list of bookmark titles (must match file count)
            
        Returns:
            Self for method chaining
        """
        for i, file_path in enumerate(file_paths):
            bookmark = bookmarks[i] if bookmarks and i < len(bookmarks) else None
            self.add_pdf(file_path, bookmark)
        
        return self

    def generate_toc(self, style: str = 'formal', max_depth: int = 3, 
                    add_to_pdf: bool = False) -> str:
        """Generate table of contents from PDF outlines.
        
        Args:
            style: TOC style ('formal', 'simple', 'hierarchical')
            max_depth: Maximum heading depth to include
            add_to_pdf: Whether to add TOC as first page (requires reportlab)
            
        Returns:
            Formatted TOC string
        """
        self.toc_manager.set_style(TOCStyle[style.upper()])
        
        # Extract outlines from PDFs
        self._extract_outlines()
        
        # Filter by max depth if needed
        if max_depth < self.toc_manager.get_max_level():
            self.toc_manager = self.toc_manager.filter_by_level(max_depth)
        
        toc_str = self.toc_manager.format_toc()
        
        if add_to_pdf:
            try:
                self._add_toc_page(toc_str)
            except ImportError:
                print("Warning: reportlab required to add TOC page. Install with: pip install reportlab")
        
        return toc_str

    def _extract_outlines(self) -> None:
        """Extract outlines/bookmarks from the merged PDF."""
        for pdf_file in self.pdf_files:
            try:
                with open(pdf_file, 'rb') as f:
                    reader = PdfReader(f)
                    if reader.outline:
                        self._process_outline(reader.outline, 0)
            except Exception as e:
                print(f"Warning: Could not extract outline from {pdf_file}: {e}")

    def _process_outline(self, outline, level: int = 0, page_offset: int = 0) -> None:
        """Process PDF outline recursively.
        
        Args:
            outline: PDF outline/bookmark
            level: Current hierarchy level
            page_offset: Page offset for this PDF
        """
        for item in outline:
            if isinstance(item, list):
                self._process_outline(item, level + 1, page_offset)
            else:
                try:
                    title = item.title if hasattr(item, 'title') else str(item)
                    # Try to get page number
                    page_num = self._get_page_number(item, page_offset)
                    self.toc_manager.add_entry(title, page_num, level + 1)
                except Exception as e:
                    print(f"Warning: Could not process outline item: {e}")

    @staticmethod
    def _get_page_number(item, offset: int = 0) -> int:
        """Extract page number from outline item.
        
        Args:
            item: Outline item
            offset: Page offset
            
        Returns:
            Page number
        """
        try:
            if hasattr(item, 'page'):
                return item.page + offset
            return offset
        except:
            return offset

    def add_bookmark(self, title: str, page_num: int, level: int = 0) -> 'PDFMerger':
        """Add a bookmark manually.
        
        Args:
            title: Bookmark title
            page_num: Page number (0-indexed)
            level: Hierarchy level
            
        Returns:
            Self for method chaining
        """
        self.bookmark_manager.add_bookmark(title, page_num, level)
        return self

    def add_bookmarks_batch(self, bookmarks: List[Tuple[str, int, int]]) -> 'PDFMerger':
        """Add multiple bookmarks.
        
        Args:
            bookmarks: List of (title, page_num, level) tuples
            
        Returns:
            Self for method chaining
        """
        self.bookmark_manager.add_bookmarks_batch(bookmarks)
        return self

    def refresh_toc(self) -> None:
        """Refresh TOC with updated page numbers."""
        self._extract_outlines()

    def _add_toc_page(self, toc_content: str) -> None:
        """Add TOC as first page (requires reportlab).
        
        Args:
            toc_content: Formatted TOC content
        """
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.units import inch
        from io import BytesIO
        
        # Create TOC PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Add title
        title_style = ParagraphStyle(
            'CustomTitle',
            fontSize=16,
            textColor='black',
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph("Table of Contents", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Add TOC content
        normal_style = ParagraphStyle(
            'CustomNormal',
            fontSize=10,
            textColor='black',
            spaceAfter=6,
        )
        
        for line in toc_content.split('\n'):
            if line.strip():
                story.append(Paragraph(line, normal_style))
        
        doc.build(story)
        
        # Read TOC PDF and insert at beginning
        buffer.seek(0)
        toc_reader = PdfReader(buffer)
        
        # Create new writer with TOC first
        new_writer = PdfWriter()
        
        # Add TOC pages
        for page in toc_reader.pages:
            new_writer.add_page(page)
        
        # Add original pages with offset bookmarks
        for i, page in enumerate(self.pdf_writer.pages):
            new_writer.add_page(page)
        
        # Update writer
        self.pdf_writer = new_writer
        self.current_page = len(toc_reader.pages)

    def get_page_count(self) -> int:
        """Get total page count.
        
        Returns:
            Total number of pages
        """
        return self.page_count

    def get_pdf_count(self) -> int:
        """Get number of PDFs added.
        
        Returns:
            Number of PDF files
        """
        return len(self.pdf_files)

    def save(self, output_path: str) -> None:
        """Save merged PDF to file.
        
        Args:
            output_path: Path to output PDF file
        """
        create_output_directory(output_path)
        
        # Apply bookmarks
        self.bookmark_manager.apply_to_pdf(self.pdf_writer)
        
        # Write to file
        with open(output_path, 'wb') as f:
            self.pdf_writer.write(f)
        
        print(f"✓ Merged PDF saved to: {output_path}")
        print(f"  Total pages: {len(self.pdf_writer.pages)}")
        print(f"  Total PDFs: {len(self.pdf_files)}")

    def clear(self) -> None:
        """Clear all data and reset merger."""
        self.pdf_files.clear()
        self.pdf_reader.clear()
        self.pdf_writer = PdfWriter()
        self.toc_manager.clear()
        self.bookmark_manager.clear()
        self.current_page = 0
        self.page_count = 0

    def __repr__(self) -> str:
        """String representation."""
        return f"PDFMerger({len(self.pdf_files)} files, {self.page_count} pages)"
