# Document Merger 📄

A powerful Python tool for merging PDF and Word documents with automatic table of contents (TOC) generation and refresh capabilities.

## Features ✨

- **PDF Merging**: Combine multiple PDF files into a single document
- **Word Document Merging**: Merge DOCX files while preserving formatting
- **Automatic TOC Generation**: Generate table of contents from document headings
- **TOC Auto-Refresh**: Automatically update page numbers and links in the TOC
- **Bookmark Support**: Add clickable bookmarks/outlines to merged PDFs
- **Flexible Configuration**: Customize merge order, styling, and TOC format
- **Cross-Format Support**: Convert and merge PDFs and Word documents together

## Installation 📦

```bash
# Clone the repository
git clone https://github.com/flhong/document-merger.git
cd document-merger

# Install dependencies
pip install -r requirements.txt
```

## Quick Start 🚀

### Merge PDF Files

```python
from document_merger.pdf_merger import PDFMerger

merger = PDFMerger()
merger.add_pdf('document1.pdf')
merger.add_pdf('document2.pdf')
merger.add_pdf('document3.pdf')

# Generate TOC automatically
merger.generate_toc()

# Save merged document
merger.save('output.pdf')
```

### Merge Word Documents

```python
from document_merger.word_merger import WordMerger

merger = WordMerger()
merger.add_document('file1.docx')
merger.add_document('file2.docx')
merger.add_document('file3.docx')

# Auto-refresh TOC
merger.refresh_toc()

# Save merged document
merger.save('output.docx')
```

### Merge PDF and Word Documents

```python
from document_merger.hybrid_merger import HybridMerger

merger = HybridMerger(output_format='pdf')
merger.add_document('document.docx')
merger.add_document('file.pdf')
merger.add_document('another.docx')

# Generate comprehensive TOC
merger.generate_toc()

# Save as PDF
merger.save('output.pdf')
```

## Configuration 🔧

Create a `config.yaml` file to customize behavior:

```yaml
merge:
  output_format: pdf  # pdf or docx
  preserve_formatting: true
  
toc:
  auto_generate: true
  auto_refresh: true
  max_depth: 3
  include_page_numbers: true
  style: formal  # formal or simple
  
pdf:
  add_bookmarks: true
  bookmark_style: hierarchical
  page_numbering: true
  
word:
  keep_styles: true
  merge_styles: true
  update_fields: true
```

## Project Structure 📁

```
document-merger/
├── document_merger/
│   ├── __init__.py
│   ├── pdf_merger.py          # PDF merging logic
│   ├── word_merger.py         # Word merging logic
│   ├── hybrid_merger.py       # Cross-format merging
│   ├── toc_manager.py         # TOC generation & refresh
│   ├── bookmark_manager.py    # PDF bookmark handling
│   ├── config.py              # Configuration management
│   └── utils.py               # Utility functions
├── tests/
│   ├── test_pdf_merger.py
│   ├── test_word_merger.py
│   ├── test_hybrid_merger.py
│   └── test_toc_manager.py
├── examples/
│   ├── merge_pdfs.py
│   ├── merge_docs.py
│   └── hybrid_merge.py
├── requirements.txt
├── config.yaml
└── README.md
```

## Dependencies 📚

- `PyPDF2` - PDF manipulation and merging
- `python-docx` - Word document handling
- `reportlab` - PDF generation and TOC creation
- `pyyaml` - Configuration file parsing
- `docx2pdf` - Convert DOCX to PDF

## API Documentation 📖

### PDFMerger

```python
class PDFMerger:
    def add_pdf(file_path: str, bookmark: str = None)
    def generate_toc(style: str = 'formal', max_depth: int = 3)
    def add_bookmark(title: str, page_num: int, level: int = 0)
    def save(output_path: str)
    def get_page_count() -> int
```

### WordMerger

```python
class WordMerger:
    def add_document(file_path: str)
    def refresh_toc(max_depth: int = 3)
    def preserve_formatting(flag: bool)
    def save(output_path: str)
```

### HybridMerger

```python
class HybridMerger:
    def add_document(file_path: str, format: str = 'auto')
    def generate_toc(style: str = 'formal')
    def set_output_format(format: str)  # 'pdf' or 'docx'
    def save(output_path: str)
```

## Examples 💡

See the `examples/` directory for complete usage examples:
- Merging multiple PDF files with TOC
- Combining Word documents with automatic TOC refresh
- Converting and merging mixed format documents
- Customizing TOC styles and bookmarks

## Contributing 🤝

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 🆘

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation and examples

## Roadmap 🗺️

- [ ] GUI interface for document merging
- [ ] Batch processing support
- [ ] Advanced TOC styling options
- [ ] Support for additional formats (ODT, RTF)
- [ ] Watermark and security features
- [ ] Performance optimization for large files
- [ ] Cloud storage integration (Google Drive, OneDrive)

## Changelog 📝

### v0.1.0 (Initial Release)
- Basic PDF merging with TOC generation
- Word document merging with auto-refresh
- Hybrid merge support
- Configuration management

---

**Made with ❤️ by flhong**
