"""
Example: Append Word documents to master with automatic TOC refresh.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from document_merger import WordMerger


def main():
    """Append Word documents to master example."""
    print("="*70)
    print("Word Document Incremental Merge Example")
    print("Append to master.docx and refresh TOC")
    print("="*70)
    
    test_dir = Path('tests/sample_docs')
    master_docx = test_dir / 'master.docx'
    
    # Check if test files exist
    if not test_dir.exists():
        print("\n✗ Test directory not found. Run: python tests/generate_test_files.py")
        return 1
    
    # Create master DOCX if it doesn't exist
    if not master_docx.exists():
        print(f"\n1. Creating master DOCX from document1.docx...")
        source = test_dir / 'document1.docx'
        if source.exists():
            import shutil
            shutil.copy(source, master_docx)
            print(f"   ✓ Master created: {master_docx}")
        else:
            print(f"   ✗ Source file not found: {source}")
            return 1
    else:
        print(f"\n1. Master DOCX exists: {master_docx}")
    
    try:
        # Initialize merger with master DOCX
        print(f"\n2. Loading master DOCX...")
        merger = WordMerger(str(master_docx))
        print(f"   ✓ Loaded successfully")
        print(f"   Current paragraphs: {merger.get_paragraph_count()}")
        
        # Append second document
        print(f"\n3. Appending document2.docx...")
        doc2 = test_dir / 'document2.docx'
        if doc2.exists():
            merger.append_document(str(doc2), add_page_break=True)
            print(f"   ✓ Appended successfully")
            print(f"   New paragraph count: {merger.get_paragraph_count()}")
            print(f"   Paragraphs added: {merger.get_appended_paragraph_count()}")
        else:
            print(f"   ⚠ File not found: {doc2}")
        
        # Append third document
        print(f"\n4. Appending document3.docx...")
        doc3 = test_dir / 'document3.docx'
        if doc3.exists():
            merger.append_document(str(doc3), add_page_break=True)
            print(f"   ✓ Appended successfully")
            print(f"   Final paragraph count: {merger.get_paragraph_count()}")
            print(f"   Total paragraphs appended: {merger.get_appended_paragraph_count()}")
        else:
            print(f"   ⚠ File not found: {doc3}")
        
        # Refresh TOC
        print(f"\n5. Refreshing Table of Contents...")
        toc = merger.refresh_toc(max_depth=2)
        print(f"   ✓ TOC refreshed")
        if toc:
            print(f"\n   Contents:\n{toc}")
        
        # Save master
        print(f"\n6. Saving master DOCX...")
        merger.save()
        print(f"   ✓ Master DOCX saved and updated")
        
        print(f"\n" + "="*70)
        print("Word Document Incremental Merge Complete!")
        print("="*70)
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
