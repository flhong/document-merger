"""
Document Merger - Merge PDF and Word documents with automatic TOC generation and refresh.
"""

__version__ = '0.1.0'
__author__ = 'flhong'
__email__ = 'flhong@example.com'
__license__ = 'MIT'

from .pdf_merger import PDFMerger
from .word_merger import WordMerger
from .hybrid_merger import HybridMerger
from .toc_manager import TOCManager
from .config import Config

__all__ = [
    'PDFMerger',
    'WordMerger',
    'HybridMerger',
    'TOCManager',
    'Config',
]
