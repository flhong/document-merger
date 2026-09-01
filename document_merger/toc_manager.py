"""
Table of Contents management and generation.
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TOCStyle(Enum):
    """TOC style options."""
    FORMAL = 'formal'  # With page numbers and dots
    SIMPLE = 'simple'  # Simple list format
    HIERARCHICAL = 'hierarchical'  # Multi-level hierarchy


@dataclass
class TOCEntry:
    """Table of contents entry."""
    title: str
    page_num: int
    level: int = 1
    
    def __repr__(self) -> str:
        indent = '  ' * (self.level - 1)
        return f"{indent}{self.title} ...... {self.page_num}"


class TOCManager:
    """Manages table of contents generation and refresh."""
    
    def __init__(self):
        """Initialize TOC manager."""
        self.entries: List[TOCEntry] = []
        self.style = TOCStyle.FORMAL

    def add_entry(self, title: str, page_num: int, level: int = 1) -> None:
        """Add a TOC entry.
        
        Args:
            title: Entry title
            page_num: Page number
            level: Hierarchy level (1-6)
        """
        level = max(1, min(level, 6))  # Clamp level 1-6
        entry = TOCEntry(title, page_num, level)
        self.entries.append(entry)

    def add_entries_batch(self, entries: List[Tuple[str, int, int]]) -> None:
        """Add multiple TOC entries.
        
        Args:
            entries: List of (title, page_num, level) tuples
        """
        for title, page_num, level in entries:
            self.add_entry(title, page_num, level)

    def update_page_numbers(self, page_offset: int = 0) -> None:
        """Update all page numbers with offset (for auto-refresh).
        
        Args:
            page_offset: Number of pages to add to all entries
        """
        for entry in self.entries:
            entry.page_num += page_offset

    def refresh_toc(self, heading_page_map: List[Tuple[str, int]]) -> None:
        """Refresh TOC from document headings.
        
        Args:
            heading_page_map: List of (heading_text, page_num) tuples extracted from document
        """
        self.entries.clear()
        for i, (heading, page_num) in enumerate(heading_page_map):
            # Try to extract level from heading (e.g., 'Heading 1' -> 1)
            level = self._extract_level(heading)
            self.add_entry(heading, page_num, level)

    @staticmethod
    def _extract_level(heading: str) -> int:
        """Extract heading level from heading string.
        
        Args:
            heading: Heading text
            
        Returns:
            Heading level (1-6)
        """
        # Try to extract level from common heading formats
        import re
        
        # Pattern: "# " or "## " etc (Markdown style)
        match = re.match(r'^(#{1,6})\s', heading)
        if match:
            return len(match.group(1))
        
        # Pattern: "1. " or "1.1. " etc (Numbered style)
        match = re.match(r'^(\d+(\.\d+)*)\.\s', heading)
        if match:
            dots = match.group(1).count('.')
            return min(dots + 1, 6)
        
        # Default to level 1
        return 1

    def set_style(self, style: TOCStyle) -> None:
        """Set TOC style.
        
        Args:
            style: TOC style (FORMAL, SIMPLE, HIERARCHICAL)
        """
        self.style = style

    def format_toc(self) -> str:
        """Format TOC as string.
        
        Returns:
            Formatted TOC string
        """
        if self.style == TOCStyle.FORMAL:
            return self._format_formal()
        elif self.style == TOCStyle.SIMPLE:
            return self._format_simple()
        else:
            return self._format_hierarchical()

    def _format_formal(self) -> str:
        """Format TOC in formal style (with dots and page numbers).
        
        Returns:
            Formatted TOC string
        """
        lines = []
        for entry in self.entries:
            indent = '  ' * (entry.level - 1)
            dots_count = max(1, 60 - len(entry.title) - len(str(entry.page_num)))
            dots = '.' * dots_count
            line = f"{indent}{entry.title} {dots} {entry.page_num}"
            lines.append(line)
        return '\n'.join(lines)

    def _format_simple(self) -> str:
        """Format TOC in simple style.
        
        Returns:
            Formatted TOC string
        """
        lines = []
        for entry in self.entries:
            indent = '  ' * (entry.level - 1)
            line = f"{indent}{entry.title} ({entry.page_num})"
            lines.append(line)
        return '\n'.join(lines)

    def _format_hierarchical(self) -> str:
        """Format TOC in hierarchical style.
        
        Returns:
            Formatted TOC string
        """
        return self._format_formal()  # Same as formal for now

    def get_entries(self) -> List[TOCEntry]:
        """Get all TOC entries.
        
        Returns:
            List of TOC entries
        """
        return self.entries.copy()

    def clear(self) -> None:
        """Clear all TOC entries."""
        self.entries.clear()

    def get_max_level(self) -> int:
        """Get maximum heading level in TOC.
        
        Returns:
            Maximum level (1-6)
        """
        if not self.entries:
            return 1
        return max(entry.level for entry in self.entries)

    def filter_by_level(self, max_level: int) -> 'TOCManager':
        """Create a filtered TOC with max level.
        
        Args:
            max_level: Maximum level to include
            
        Returns:
            New TOCManager with filtered entries
        """
        filtered = TOCManager()
        filtered.style = self.style
        filtered.entries = [e for e in self.entries if e.level <= max_level]
        return filtered

    def __repr__(self) -> str:
        """String representation."""
        return f"TOCManager({len(self.entries)} entries, style={self.style.value})"
