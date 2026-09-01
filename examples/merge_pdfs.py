"""
Example: Merge multiple PDF files with automatic TOC generation.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from document_merger import PDFMerger


def main():
    """Merge PDF files example."""
    print("="*60)
    print("PDF Merger Example")
    print("="*60)
    
    # Create merger instance
    merger = PDFMerger()
    
    # Add PDF files (with optional bookmarks)
    print("\n1. Adding PDF files...")
    test_pdfs = [
        ('tests/sample_pdfs/document1.pdf', 'Chapter 1: Introduction'),
        ('tests/sample_pdfs/document2.pdf', 'Chapter 2: Main Content'),
        ('tests/sample_pdfs/document3.pdf', 'Chapter 3: Conclusion'),
    ]
    
    for pdf_path, bookmark in test_pdfs:
        if Path(pdf_path).exists():
            try:
                merger.add_pdf(pdf_path, bookmark)
                print(f"  ✓ Added: {pdf_path}")
            except Exception as e:
                print(f"  ✗ Error adding {pdf_path}: {e}")
        else:
            print(f"  ⚠ File not found: {pdf_path}")
    
    # Generate TOC
    print(f"\n2. Generating Table of Contents...")
    print(f"  Total pages: {merger.get_page_count()}")
    print(f"  Total PDFs: {merger.get_pdf_count()}")
    
    try:
        toc = merger.generate_toc(style='formal', max_depth=3, add_to_pdf=False)
        print(f"  ✓ TOC generated")
        if toc:
            print(f"\n  Contents:\n{toc}")
    except Exception as e:
        print(f"  ✗ Error generating TOC: {e}")
    
    # Save merged PDF
    print(f"\n3. Saving merged PDF...")
    output_path = 'tests/output/merged_pdfs.pdf'
    try:
        merger.save(output_path)
        print(f"  ✓ Saved to: {output_path}")
    except Exception as e:
        print(f"  ✗ Error saving: {e}")
    
    print("\n" + "="*60)
    print("PDF Merge Complete!")
    print("="*60)


if __name__ == '__main__':
    main()
