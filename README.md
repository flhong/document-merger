"""
README - Document Merger

Incremental PDF and Word document merging with automatic TOC refresh.
"""

# Document Merger 📄

A Python tool for **incrementally appending** PDF and Word documents to a master file with **automatic table of contents (TOC) refresh**.

## Key Features ✨

✅ **Incremental Merging**: Append documents to existing master file (not creating new ones)  
✅ **Automatic TOC Refresh**: Update page numbers and heading references automatically  
✅ **Backup Creation**: Automatic backup of original files before modification  
✅ **PDF Support**: PyPDF2-based PDF merging with bookmark management  
✅ **Word Support**: python-docx based document merging with formatting preservation  
✅ **Easy API**: Simple, fluent interface with method chaining  
✅ **CLI Interface**: Command-line tools for batch operations  
✅ **Configuration**: YAML-based customization  

## What's Different from Traditional Merge?

### Traditional Approach ❌
```python
# Creates a NEW file, loses original master structure
merger = PDFMerger()
merger.add_pdf('file1.pdf')
merger.add_pdf('file2.pdf')
merger.save('output.pdf')  # New file
```

### This Tool's Approach ✅
```python
# Appends to EXISTING master file, updates in place
merger = PDFMerger('master.pdf')  # Start with existing file
merger.append_pdf('file2.pdf')    # Append to master
merger.refresh_toc()               # Update TOC
merger.save()                       # Overwrites master.pdf
```

## Installation 📦

```bash
# Clone the repository
git clone https://github.com/flhong/document-merger.git
cd document-merger

# Install dependencies
pip install -r requirements.txt
```

## Quick Start 🚀

### PDF Merging (Append to Master)

```python
from document_merger import PDFMerger

# Start with existing master PDF
merger = PDFMerger('master.pdf')

# Append new PDF files
merger.append_pdf('document2.pdf', bookmark='Chapter 2')
merger.append_pdf('document3.pdf', bookmark='Chapter 3')

# Refresh TOC with updated page numbers
toc = merger.refresh_toc(max_depth=2)
print(toc)  # Print updated TOC

# Save (overwrites master.pdf)
merger.save()
```

### Word Document Merging (Append to Master)

```python
from document_merger import WordMerger

# Start with existing master DOCX
merger = WordMerger('master.docx')

# Append new Word documents
merger.append_document('document2.docx', add_page_break=True)
merger.append_document('document3.docx', add_page_break=True)

# Refresh TOC with updated headings
toc = merger.refresh_toc(max_depth=2)
print(toc)  # Print updated TOC

# Save (overwrites master.docx)
merger.save()
```

## Usage Examples 💡

### Example 1: Daily Log Update

```python
from document_merger import PDFMerger
from datetime import datetime

# Master file contains all previous days' logs
merger = PDFMerger('daily_logs.pdf')

# Append today's log
today = datetime.now().strftime('%Y-%m-%d')
merger.append_pdf(f'logs/{today}.pdf', bookmark=f'Day: {today}')

# Refresh TOC to show all days
merger.refresh_toc()

# Save to the same file
merger.save()
print(f"Daily log appended and TOC refreshed")
```

### Example 2: Report Compilation

```python
from document_merger import WordMerger

# Master report with company overview
merger = WordMerger('annual_report.docx')

# Append department reports
merger.append_document('departments/sales.docx', add_page_break=True)
merger.append_document('departments/marketing.docx', add_page_break=True)
merger.append_document('departments/it.docx', add_page_break=True)

# Refresh TOC
toc = merger.refresh_toc(max_depth=3)
print(f"Report sections:\n{toc}")

# Save updated report
merger.save()
```

### Example 3: Book Assembly

```python
from document_merger import PDFMerger

# Book master containing chapters 1-5
merger = PDFMerger('book.pdf')

print(f"Current pages: {merger.get_page_count()}")

# Append new chapters
merger.append_pdf('chapters/chapter_6.pdf', bookmark='Chapter 6')
merger.append_pdf('chapters/chapter_7.pdf', bookmark='Chapter 7')

print(f"New pages: {merger.get_page_count()}")
print(f"Appended: {merger.get_appended_page_count()} pages")

# Refresh TOC to include new chapters
toc = merger.refresh_toc()
print(f"Updated TOC:\n{toc}")

# Save
merger.save()
```

## API Reference 📚

### PDFMerger

```python
class PDFMerger:
    # Initialize with master PDF
    def __init__(master_pdf_path: str, config: Optional[Config] = None)
    
    # Append a PDF file
    def append_pdf(file_path: str, bookmark: Optional[str] = None) -> PDFMerger
    
    # Refresh TOC with current page numbers
    def refresh_toc(max_depth: int = 3) -> str
    
    # Get page counts
    def get_page_count() -> int
    def get_appended_page_count() -> int
    
    # Save changes (overwrites master file)
    def save() -> None
```

### WordMerger

```python
class WordMerger:
    # Initialize with master DOCX
    def __init__(master_docx_path: str, config: Optional[Config] = None)
    
    # Append a Word document
    def append_document(file_path: str, add_page_break: bool = True) -> WordMerger
    
    # Refresh TOC with current headings
    def refresh_toc(max_depth: int = 3) -> str
    
    # Get paragraph counts
    def get_paragraph_count() -> int
    def get_appended_paragraph_count() -> int
    
    # Save changes (overwrites master file)
    def save() -> None
```

## Configuration 🔧

Edit `config.yaml` to customize behavior:

```yaml
merge:
  preserve_formatting: true
  page_numbering: true

toc:
  auto_refresh: true
  max_depth: 3
  include_page_numbers: true
  style: formal  # formal, simple, or hierarchical

pdf:
  add_bookmarks: true
  
word:
  keep_styles: true
```

## Command-Line Interface 💻

```bash
# Append PDF to master
python cli.py append-pdf master.pdf document.pdf --bookmark "Chapter 2" --save

# Append Word doc to master
python cli.py append-word master.docx document.docx --save

# Refresh TOC
python cli.py refresh-toc master.pdf --depth 2 --save

# Check document info
python cli.py info master.pdf
```

## Interactive Mode 🎮

```bash
python main.py

# Follow the interactive menu to:
# 1. Append PDFs to a master
# 2. Append Word docs to a master  
# 3. Refresh TOC
# 4. View document info
```

## Important Notes ⚠️

1. **Automatic Backup**: The tool creates a backup (`_backup.pdf/docx`) before modifying the master file
2. **Overwrites Master**: `save()` overwrites the original master file - backups are available if needed
3. **Page Numbers**: TOC is automatically refreshed based on current document structure
4. **Formatting**: Word formatting is preserved during append operations
5. **Bookmarks**: PDF bookmarks/outlines are extracted and maintained

## Testing 🧪

```bash
# Generate test documents
python tests/generate_test_files.py

# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=document_merger --cov-report=html

# Run examples
python examples/merge_pdfs.py
python examples/merge_docs.py
```

## Troubleshooting 🔍

### Issue: "File not found"
- Ensure the master file exists before calling `PDFMerger()` or `WordMerger()`
- Use absolute paths for reliability

### Issue: "TOC not updating"
- Call `refresh_toc()` explicitly after appending documents
- Check that documents have proper heading styles

### Issue: "Backup files accumulating"
- Backups are created once per master file
- Safe to delete old backups after verifying the master file

### Issue: "Permission denied when saving"
- Close the file in any PDF/Word viewers
- Ensure write permissions on the directory
- Check that the file is not read-only

## Contributing 🤝

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License 📄

MIT License - see [LICENSE](LICENSE) file for details.

## Changelog 📝

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Support 💬

- Open an issue for bug reports
- Check existing issues before creating new ones
- See examples in `examples/` directory

---

**Made with ❤️ by flhong**
