"""
Utility functions for Document Merger.
"""

import os
from pathlib import Path
from typing import List, Tuple
from datetime import datetime


def validate_file_path(file_path: str, required_extension: str = None) -> bool:
    """Validate if file exists and has correct extension.
    
    Args:
        file_path: Path to file
        required_extension: Required file extension (e.g., '.pdf', '.docx')
        
    Returns:
        True if file is valid
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    if required_extension and not str(path).lower().endswith(required_extension.lower()):
        raise ValueError(f"File must have {required_extension} extension: {file_path}")
    
    return True


def get_file_extension(file_path: str) -> str:
    """Get file extension.
    
    Args:
        file_path: Path to file
        
    Returns:
        File extension (lowercase, with dot)
    """
    return Path(file_path).suffix.lower()


def is_pdf(file_path: str) -> bool:
    """Check if file is PDF.
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file is PDF
    """
    return get_file_extension(file_path) == '.pdf'


def is_docx(file_path: str) -> bool:
    """Check if file is DOCX.
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file is DOCX
    """
    return get_file_extension(file_path) == '.docx'


def create_output_directory(output_path: str) -> None:
    """Create output directory if it doesn't exist.
    
    Args:
        output_path: Path to output file
    """
    output_dir = Path(output_path).parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)


def get_file_size(file_path: str) -> int:
    """Get file size in bytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in bytes
    """
    return Path(file_path).stat().st_size


def format_file_size(size_bytes: int) -> str:
    """Format file size to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_timestamp() -> str:
    """Get current timestamp in ISO format.
    
    Returns:
        Timestamp string
    """
    return datetime.now().isoformat()


def generate_backup_path(file_path: str) -> str:
    """Generate backup file path.
    
    Args:
        file_path: Original file path
        
    Returns:
        Backup file path
    """
    path = Path(file_path)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return str(path.parent / f"{path.stem}_backup_{timestamp}{path.suffix}")


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"|?*\\'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def extract_headings_from_docx(docx_path: str) -> List[Tuple[str, int]]:
    """Extract headings from DOCX file.
    
    Args:
        docx_path: Path to DOCX file
        
    Returns:
        List of tuples (heading_text, heading_level)
    """
    try:
        from docx import Document
        doc = Document(docx_path)
        headings = []
        
        for para in doc.paragraphs:
            style_name = para.style.name
            if style_name.startswith('Heading'):
                level = int(style_name.split()[-1])
                headings.append((para.text, level))
        
        return headings
    except Exception as e:
        print(f"Error extracting headings from {docx_path}: {e}")
        return []


def extract_headings_from_pdf(pdf_path: str) -> List[Tuple[str, int]]:
    """Extract headings from PDF file (from outline/bookmarks).
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        List of tuples (heading_text, heading_level)
    """
    try:
        from PyPDF2 import PdfReader
        
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            outlines = reader.outline
            
            headings = []
            _extract_outlines(outlines, headings, 0)
            return headings
    except Exception as e:
        print(f"Error extracting headings from {pdf_path}: {e}")
        return []


def _extract_outlines(outlines, headings: List, level: int = 0) -> None:
    """Recursively extract outlines/bookmarks.
    
    Args:
        outlines: PDF outlines/bookmarks
        headings: List to append headings to
        level: Current hierarchy level
    """
    for outline in outlines:
        if isinstance(outline, list):
            _extract_outlines(outline, headings, level + 1)
        else:
            try:
                title = outline.title if hasattr(outline, 'title') else str(outline)
                headings.append((title, level))
            except:
                pass
