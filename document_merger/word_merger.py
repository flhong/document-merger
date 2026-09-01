"""
Incremental Word document merging functionality.
Appends Word documents to a master document and refreshes TOC.
"""

import os
from pathlib import Path
from typing import Optional
from docx import Document
from .toc_manager import TOCManager
from .utils import validate_file_path, is_docx, extract_headings_from_docx
from .config import Config


class WordMerger:
    """Incrementally append Word documents to a master document and refresh TOC."""
    
    def __init__(self, master_docx_path: str, config: Optional[Config] = None):
        """Initialize Word merger with a master document.
        
        Args:
            master_docx_path: Path to master DOCX file to append to
            config: Configuration object (optional)
        """
        validate_file_path(master_docx_path, '.docx')
        
        self.config = config or Config()
        self.master_docx_path = master_docx_path
        self.master_doc = Document(master_docx_path)
        self.toc_manager = TOCManager()
        self.original_paragraph_count = len(self.master_doc.paragraphs)
        self.preserve_styles = self.config.get('word.keep_styles', True)
        
        # Extract initial TOC
        self._extract_toc()

    def _extract_toc(self) -> None:
        """Extract TOC from master document."""
        self.toc_manager.clear()
        for para in self.master_doc.paragraphs:
            style_name = para.style.name if para.style else ''
            if style_name.startswith('Heading'):
                try:
                    level = int(style_name.split()[-1])
                    self.toc_manager.add_entry(para.text, 0, level)
                except (ValueError, IndexError):
                    pass

    def append_document(self, file_path: str, add_page_break: bool = True) -> 'WordMerger':
        """Append a Word document to master document.
        
        Args:
            file_path: Path to DOCX file to append
            add_page_break: Whether to add page break before appending
            
        Returns:
            Self for method chaining
        """
        validate_file_path(file_path, '.docx')
        
        source_doc = Document(file_path)
        
        # Add page break if requested and master has content
        if add_page_break and self.master_doc.paragraphs:
            self.master_doc.add_page_break()
        
        # Append paragraphs
        for para in source_doc.paragraphs:
            new_para = self.master_doc.add_paragraph()
            new_para.style = para.style
            new_para.alignment = para.alignment
            
            # Copy runs (text with formatting)
            for run in para.runs:
                new_run = new_para.add_run(run.text)
                self._copy_run_formatting(run, new_run)
        
        # Append tables
        for table in source_doc.tables:
            self._copy_table(table)
        
        return self

    def _copy_run_formatting(self, source_run, target_run) -> None:
        """Copy formatting from source run to target run.
        
        Args:
            source_run: Source run object
            target_run: Target run object
        """
        try:
            if source_run.font.bold is not None:
                target_run.font.bold = source_run.font.bold
            if source_run.font.italic is not None:
                target_run.font.italic = source_run.font.italic
            if source_run.font.underline is not None:
                target_run.font.underline = source_run.font.underline
            if source_run.font.size is not None:
                target_run.font.size = source_run.font.size
            if source_run.font.color.rgb is not None:
                target_run.font.color.rgb = source_run.font.color.rgb
            if source_run.font.name is not None:
                target_run.font.name = source_run.font.name
        except Exception as e:
            print(f"Warning: Could not copy formatting: {e}")

    def _copy_table(self, table) -> None:
        """Copy a table to master document.
        
        Args:
            table: Table object to copy
        """
        try:
            new_table = self.master_doc.add_table(rows=len(table.rows),
                                                   cols=len(table.columns))
            new_table.style = table.style
            
            for i, row in enumerate(table.rows):
                for j, cell in enumerate(row.cells):
                    new_table.rows[i].cells[j].text = cell.text
                    try:
                        new_table.rows[i].cells[j].width = cell.width
                    except:
                        pass
        except Exception as e:
            print(f"Warning: Could not copy table: {e}")

    def refresh_toc(self, max_depth: int = 3, insert_at_beginning: bool = False) -> str:
        """Refresh table of contents.
        
        Args:
            max_depth: Maximum heading depth to include
            insert_at_beginning: Whether to insert fresh TOC at beginning
            
        Returns:
            Formatted TOC string
        """
        # Extract fresh TOC from current document
        self._extract_toc()
        
        # Filter by max depth if needed
        if max_depth < self.toc_manager.get_max_level():
            self.toc_manager = self.toc_manager.filter_by_level(max_depth)
        
        return self.toc_manager.format_toc()

    def get_paragraph_count(self) -> int:
        """Get total paragraph count of master document.
        
        Returns:
            Total number of paragraphs
        """
        return len(self.master_doc.paragraphs)

    def get_appended_paragraph_count(self) -> int:
        """Get number of paragraphs appended.
        
        Returns:
            Number of appended paragraphs
        """
        return self.get_paragraph_count() - self.original_paragraph_count

    def save(self) -> None:
        """Save updated master Word document (overwrites original file)."""
        # Create backup of original
        backup_path = str(self.master_docx_path).rsplit('.', 1)[0] + '_backup.docx'
        if Path(self.master_docx_path).exists() and not Path(backup_path).exists():
            import shutil
            shutil.copy(self.master_docx_path, backup_path)
        
        # Save to master file (overwrites)
        self.master_doc.save(self.master_docx_path)
        
        print(f"✓ Master Word document updated: {self.master_docx_path}")
        print(f"  Total paragraphs: {self.get_paragraph_count()}")
        print(f"  Paragraphs appended: {self.get_appended_paragraph_count()}")
        if Path(backup_path).exists():
            print(f"  Backup saved: {backup_path}")

    def get_toc_manager(self) -> TOCManager:
        """Get TOC manager for direct access.
        
        Returns:
            TOCManager instance
        """
        return self.toc_manager

    def get_document(self) -> Document:
        """Get the master document object.
        
        Returns:
            Master Document object
        """
        return self.master_doc

    def __repr__(self) -> str:
        """String representation."""
        return f"WordMerger(master={Path(self.master_docx_path).name}, paragraphs={self.get_paragraph_count()})"
