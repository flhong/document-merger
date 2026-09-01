"""
Example: Merge multiple Word documents with automatic TOC refresh.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from document_merger import WordMerger


def main():
    """Merge Word documents example."""
    print("="*60)
    print("Word Document Merger Example")
    print("="*60)
    
    # Create merger instance
    merger = WordMerger()
    
    # Add Word documents
    print("\n1. Adding Word documents...")
    test_docs = [
        'tests/sample_docs/document1.docx',
        'tests/sample_docs/document2.docx',
        'tests/sample_docs/document3.docx',
    ]
    
    for doc_path in test_docs:
        if Path(doc_path).exists():
            try:
                merger.add_document(doc_path, add_page_break=True)
                print(f"  ✓ Added: {doc_path}")
            except Exception as e:
                print(f"  ✗ Error adding {doc_path}: {e}")
        else:
            print(f"  ⚠ File not found: {doc_path}")
    
    # Merge documents
    print(f"\n2. Merging documents...")
    try:
        merged_doc = merger.merge()
        print(f"  ✓ Documents merged")
        print(f"  Total paragraphs: {len(merged_doc.paragraphs)}")
        print(f"  Total documents: {len(test_docs)}")
    except Exception as e:
        print(f"  ✗ Error merging: {e}")
        return
    
    # Generate and insert TOC
    print(f"\n3. Generating and inserting Table of Contents...")
    try:
        toc = merger.generate_toc(max_depth=3, insert_at_beginning=True)
        print(f"  ✓ TOC generated and inserted")
        if toc:
            print(f"\n  Contents:\n{toc}")
    except Exception as e:
        print(f"  ✗ Error generating TOC: {e}")
    
    # Refresh TOC
    print(f"\n4. Refreshing Table of Contents...")
    try:
        updated_toc = merger.refresh_toc(max_depth=3)
        print(f"  ✓ TOC refreshed")
    except Exception as e:
        print(f"  ✗ Error refreshing TOC: {e}")
    
    # Save merged document
    print(f"\n5. Saving merged document...")
    output_path = 'tests/output/merged_documents.docx'
    try:
        merger.save(output_path)
        print(f"  ✓ Saved to: {output_path}")
    except Exception as e:
        print(f"  ✗ Error saving: {e}")
    
    print("\n" + "="*60)
    print("Word Document Merge Complete!")
    print("="*60)


if __name__ == '__main__':
    main()
