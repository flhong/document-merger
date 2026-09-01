#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main entry point for Document Merger.
Provides a simple interface to merge documents.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from document_merger import PDFMerger, WordMerger, HybridMerger
from document_merger.utils import is_pdf, is_docx


def main():
    """
    Interactive menu for document merging.
    """
    print("\n" + "="*70)
    print("Document Merger - Interactive Mode")
    print("="*70)
    
    while True:
        print("\nSelect merge type:")
        print("  1. Merge PDF files")
        print("  2. Merge Word documents")
        print("  3. Merge mixed documents (PDF + Word)")
        print("  4. Generate test documents")
        print("  5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            merge_pdfs_interactive()
        elif choice == '2':
            merge_words_interactive()
        elif choice == '3':
            merge_hybrid_interactive()
        elif choice == '4':
            generate_test_files_interactive()
        elif choice == '5':
            print("\nGoodbye!")
            break
        else:
            print("\n✗ Invalid choice. Please try again.")


def merge_pdfs_interactive():
    """Interactive PDF merge."""
    print("\n--- PDF Merge ---")
    
    merger = PDFMerger()
    pdf_files = []
    
    print("\nEnter PDF file paths (one per line, empty line to finish):")
    while True:
        file_path = input("> ").strip()
        if not file_path:
            break
        if Path(file_path).exists() and is_pdf(file_path):
            merger.add_pdf(file_path)
            pdf_files.append(file_path)
            print(f"  ✓ Added: {file_path}")
        else:
            print(f"  ✗ File not found or invalid: {file_path}")
    
    if not pdf_files:
        print("\n✗ No PDF files added. Canceling merge.")
        return
    
    # TOC generation
    toc_choice = input("\nGenerate table of contents? (y/n): ").strip().lower()
    if toc_choice == 'y':
        style = input("TOC style (formal/simple/hierarchical) [formal]: ").strip() or 'formal'
        toc = merger.generate_toc(style=style, add_to_pdf=True)
        print(f"\n✓ TOC generated")
        if toc:
            print(f"\nPreview:\n{toc}")
    
    # Output
    output_path = input("\nOutput file path [merged.pdf]: ").strip() or 'merged.pdf'
    try:
        merger.save(output_path)
        print(f"\n✓ Saved to: {output_path}")
    except Exception as e:
        print(f"\n✗ Error saving: {e}")


def merge_words_interactive():
    """Interactive Word merge."""
    print("\n--- Word Document Merge ---")
    
    merger = WordMerger()
    doc_files = []
    
    print("\nEnter Word document paths (one per line, empty line to finish):")
    while True:
        file_path = input("> ").strip()
        if not file_path:
            break
        if Path(file_path).exists() and is_docx(file_path):
            merger.add_document(file_path)
            doc_files.append(file_path)
            print(f"  ✓ Added: {file_path}")
        else:
            print(f"  ✗ File not found or invalid: {file_path}")
    
    if not doc_files:
        print("\n✗ No Word documents added. Canceling merge.")
        return
    
    # TOC generation
    toc_choice = input("\nGenerate and insert table of contents? (y/n): ").strip().lower()
    if toc_choice == 'y':
        toc = merger.generate_toc(insert_at_beginning=True)
        print(f"\n✓ TOC generated and inserted")
    else:
        merger.merge()
    
    # Output
    output_path = input("\nOutput file path [merged.docx]: ").strip() or 'merged.docx'
    try:
        merger.save(output_path)
        print(f"\n✓ Saved to: {output_path}")
    except Exception as e:
        print(f"\n✗ Error saving: {e}")


def merge_hybrid_interactive():
    """Interactive hybrid merge."""
    print("\n--- Hybrid Document Merge (PDF + Word) ---")
    
    format_choice = input("\nOutput format (pdf/docx) [pdf]: ").strip().lower() or 'pdf'
    merger = HybridMerger(output_format=format_choice)
    
    doc_files = []
    print("\nEnter document paths (PDF or Word, one per line, empty line to finish):")
    while True:
        file_path = input("> ").strip()
        if not file_path:
            break
        if Path(file_path).exists() and (is_pdf(file_path) or is_docx(file_path)):
            merger.add_document(file_path)
            doc_files.append(file_path)
            file_type = "PDF" if is_pdf(file_path) else "Word"
            print(f"  ✓ Added ({file_type}): {file_path}")
        else:
            print(f"  ✗ File not found or invalid: {file_path}")
    
    if not doc_files:
        print("\n✗ No documents added. Canceling merge.")
        return
    
    print(f"\nDocuments to merge:")
    print(f"  PDFs: {merger.get_pdf_count()}")
    print(f"  Word docs: {merger.get_docx_count()}")
    print(f"  Output format: {format_choice.upper()}")
    
    # TOC generation
    toc_choice = input("\nGenerate table of contents? (y/n): ").strip().lower()
    if toc_choice == 'y':
        style = input("TOC style (formal/simple/hierarchical) [formal]: ").strip() or 'formal'
        toc = merger.generate_toc(style=style)
        print(f"\n✓ TOC generated")
    
    # Output
    default_ext = '.pdf' if format_choice == 'pdf' else '.docx'
    output_path = input(f"\nOutput file path [merged{default_ext}]: ").strip() or f'merged{default_ext}'
    try:
        merger.save(output_path)
        print(f"\n✓ Saved to: {output_path}")
    except Exception as e:
        print(f"\n✗ Error saving: {e}")


def generate_test_files_interactive():
    """Generate test files interactively."""
    print("\n--- Generate Test Documents ---")
    
    try:
        from tests.generate_test_files import create_sample_docx_files, create_sample_pdf_files
        
        print("\nGenerating test documents...")
        print("  Creating Word documents...")
        create_sample_docx_files()
        print("  Creating PDF documents...")
        create_sample_pdf_files()
        print("\n✓ Test documents generated successfully!")
        print("\nLocations:")
        print("  PDFs: tests/sample_pdfs/")
        print("  Word docs: tests/sample_docs/")
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
