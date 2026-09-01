"""
Hybrid document merging for PDF and Word documents.
"""

from pathlib import Path
from typing import List, Optional
from .pdf_merger import PDFMerger
from .word_merger import WordMerger
from .toc_manager import TOCManager
from .utils import is_pdf, is_docx, validate_file_path, create_output_directory
from .config import Config


class HybridMerger:
    """Merge mixed PDF and Word documents with automatic TOC generation."""
    
    def __init__(self, output_format: str = 'pdf', config: Optional[Config] = None):
        """Initialize hybrid merger.
        
        Args:
            output_format: Output format ('pdf' or 'docx')
            config: Configuration object (optional)
        """
        if output_format.lower() not in ('pdf', 'docx'):
            raise ValueError("output_format must be 'pdf' or 'docx'")
        
        self.output_format = output_format.lower()
        self.config = config or Config()
        self.documents: List[tuple] = []  # (file_path, doc_type, bookmark)
        self.pdf_merger = PDFMerger(config)
        self.word_merger = WordMerger(config)
        self.toc_manager = TOCManager()

    def add_document(self, file_path: str, bookmark: Optional[str] = None) -> 'HybridMerger':
        """Add a document (PDF or Word) to merge queue.
        
        Args:
            file_path: Path to document file
            bookmark: Optional bookmark/heading title
            
        Returns:
            Self for method chaining
        """
        validate_file_path(file_path)
        
        if is_pdf(file_path):
            doc_type = 'pdf'
            self.pdf_merger.add_pdf(file_path, bookmark)
        elif is_docx(file_path):
            doc_type = 'docx'
            self.word_merger.add_document(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        
        self.documents.append((file_path, doc_type, bookmark))
        return self

    def add_documents_batch(self, file_paths: List[str], 
                           bookmarks: Optional[List[str]] = None) -> 'HybridMerger':
        """Add multiple documents at once.
        
        Args:
            file_paths: List of document file paths
            bookmarks: Optional list of bookmarks (must match file count)
            
        Returns:
            Self for method chaining
        """
        for i, file_path in enumerate(file_paths):
            bookmark = bookmarks[i] if bookmarks and i < len(bookmarks) else None
            self.add_document(file_path, bookmark)
        return self

    def set_output_format(self, output_format: str) -> 'HybridMerger':
        """Set output format.
        
        Args:
            output_format: 'pdf' or 'docx'
            
        Returns:
            Self for method chaining
        """
        if output_format.lower() not in ('pdf', 'docx'):
            raise ValueError("output_format must be 'pdf' or 'docx'")
        self.output_format = output_format.lower()
        return self

    def generate_toc(self, style: str = 'formal', max_depth: int = 3) -> str:
        """Generate table of contents.
        
        Args:
            style: TOC style ('formal', 'simple', 'hierarchical')
            max_depth: Maximum heading depth
            
        Returns:
            Formatted TOC string
        """
        if self.output_format == 'pdf':
            return self.pdf_merger.generate_toc(style, max_depth, add_to_pdf=True)
        else:
            return self.word_merger.generate_toc(max_depth, insert_at_beginning=True)

    def merge(self) -> None:
        """Perform the merge operation."""
        if self.output_format == 'pdf':
            # If output is PDF but we have Word docs, convert them first
            if any(doc_type == 'docx' for _, doc_type, _ in self.documents):
                print("Note: Converting Word documents to PDF for merging...")
                self._convert_docx_to_pdf()
        else:
            # If output is DOCX, merge Word docs and skip PDF handling
            if self.documents:
                self.word_merger.merge()

    def _convert_docx_to_pdf(self) -> None:
        """Convert Word documents to PDF for merging."""
        try:
            from docx2pdf import convert
            import tempfile
            
            temp_dir = tempfile.mkdtemp()
            
            for file_path, doc_type, bookmark in self.documents:
                if doc_type == 'docx':
                    pdf_path = Path(temp_dir) / f"{Path(file_path).stem}.pdf"
                    convert(file_path, str(pdf_path))
                    self.pdf_merger.add_pdf(str(pdf_path), bookmark)
        except ImportError:
            print("Error: docx2pdf not installed. Install with: pip install docx2pdf")
            print("Falling back to Word-only merge...")

    def save(self, output_path: str) -> None:
        """Save merged document to file.
        
        Args:
            output_path: Path to output file
        """
        create_output_directory(output_path)
        
        # Ensure correct extension
        if self.output_format == 'pdf' and not output_path.lower().endswith('.pdf'):
            output_path = output_path.rsplit('.', 1)[0] + '.pdf'
        elif self.output_format == 'docx' and not output_path.lower().endswith('.docx'):
            output_path = output_path.rsplit('.', 1)[0] + '.docx'
        
        # Perform merge if not already done
        self.merge()
        
        # Save based on format
        if self.output_format == 'pdf':
            self.pdf_merger.save(output_path)
        else:
            self.word_merger.save(output_path)

    def get_document_count(self) -> int:
        """Get total number of documents added.
        
        Returns:
            Number of documents
        """
        return len(self.documents)

    def get_pdf_count(self) -> int:
        """Get number of PDF documents.
        
        Returns:
            Number of PDFs
        """
        return sum(1 for _, doc_type, _ in self.documents if doc_type == 'pdf')

    def get_docx_count(self) -> int:
        """Get number of Word documents.
        
        Returns:
            Number of DOCX files
        """
        return sum(1 for _, doc_type, _ in self.documents if doc_type == 'docx')

    def clear(self) -> None:
        """Clear all data and reset merger."""
        self.documents.clear()
        self.pdf_merger.clear()
        self.word_merger.clear()
        self.toc_manager.clear()

    def __repr__(self) -> str:
        """String representation."""
        return (f"HybridMerger({len(self.documents)} docs, "
                f"{self.get_pdf_count()} PDFs, "
                f"{self.get_docx_count()} DOCX, output={self.output_format})")
