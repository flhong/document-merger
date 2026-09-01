"""
Example: Merge mixed PDF and Word documents with automatic TOC.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from document_merger import HybridMerger


def main():
    """Hybrid merge example."""
    print("="*60)
    print("Hybrid Document Merger Example (PDF + Word)")
    print("="*60)
    
    # Create hybrid merger for PDF output
    print("\n--- Merging to PDF ---")
    merger_pdf = HybridMerger(output_format='pdf')
    
    print("\n1. Adding mixed documents (PDF + Word)...")
    documents = [
        ('tests/sample_docs/document1.docx', 'Part 1: Word Document'),
        ('tests/sample_pdfs/document1.pdf', 'Part 2: PDF Document'),
        ('tests/sample_docs/document2.docx', 'Part 3: Another Word Doc'),
    ]
    
    for doc_path, bookmark in documents:
        if Path(doc_path).exists():
            try:
                merger_pdf.add_document(doc_path, bookmark)
                print(f"  ✓ Added: {doc_path}")
            except Exception as e:
                print(f"  ✗ Error adding {doc_path}: {e}")
        else:
            print(f"  ⚠ File not found: {doc_path}")
    
    print(f"\n2. Document summary:")
    print(f"  Total documents: {merger_pdf.get_document_count()}")
    print(f"  PDFs: {merger_pdf.get_pdf_count()}")
    print(f"  Word docs: {merger_pdf.get_docx_count()}")
    print(f"  Output format: {merger_pdf.output_format.upper()}")
    
    # Generate TOC
    print(f"\n3. Generating Table of Contents...")
    try:
        toc = merger_pdf.generate_toc(style='formal', max_depth=2)
        print(f"  ✓ TOC generated")
        if toc:
            print(f"\n  Contents:\n{toc}")
    except Exception as e:
        print(f"  ✗ Error generating TOC: {e}")
    
    # Save to PDF
    print(f"\n4. Saving merged document...")
    try:
        merger_pdf.save('tests/output/hybrid_merged.pdf')
        print(f"  ✓ Saved to: tests/output/hybrid_merged.pdf")
    except Exception as e:
        print(f"  ✗ Error saving: {e}")
    
    # Also create Word version
    print(f"\n--- Merging to Word ---")
    merger_word = HybridMerger(output_format='docx')
    
    print("\n5. Adding documents for Word output...")
    for doc_path, bookmark in documents:
        if Path(doc_path).exists():
            try:
                merger_word.add_document(doc_path, bookmark)
                print(f"  ✓ Added: {doc_path}")
            except Exception as e:
                print(f"  ✗ Error adding {doc_path}: {e}")
    
    print(f"\n6. Saving to Word format...")
    try:
        merger_word.save('tests/output/hybrid_merged.docx')
        print(f"  ✓ Saved to: tests/output/hybrid_merged.docx")
    except Exception as e:
        print(f"  ✗ Error saving: {e}")
    
    print("\n" + "="*60)
    print("Hybrid Merge Complete!")
    print("="*60)


if __name__ == '__main__':
    main()
