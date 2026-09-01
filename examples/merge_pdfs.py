"""
Example: Append PDF files to master with automatic TOC refresh.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from document_merger import PDFMerger


def main():
    """Append PDFs to master example."""
    print("="*70)
    print("PDF Incremental Merge Example")
    print("Append to master.pdf and refresh TOC")
    print("="*70)
    
    test_dir = Path('tests/sample_pdfs')
    master_pdf = test_dir / 'master.pdf'
    
    # Check if test files exist
    if not test_dir.exists():
        print("\n✗ Test directory not found. Run: python tests/generate_test_files.py")
        return 1
    
    # Create master PDF if it doesn't exist
    if not master_pdf.exists():
        print(f"\n1. Creating master PDF from document1.pdf...")
        source = test_dir / 'document1.pdf'
        if source.exists():
            import shutil
            shutil.copy(source, master_pdf)
            print(f"   ✓ Master created: {master_pdf}")
        else:
            print(f"   ✗ Source file not found: {source}")
            return 1
    else:
        print(f"\n1. Master PDF exists: {master_pdf}")
    
    try:
        # Initialize merger with master PDF
        print(f"\n2. Loading master PDF...")
        merger = PDFMerger(str(master_pdf))
        print(f"   ✓ Loaded successfully")
        print(f"   Current pages: {merger.get_page_count()}")
        
        # Append second PDF
        print(f"\n3. Appending document2.pdf...")
        doc2 = test_dir / 'document2.pdf'
        if doc2.exists():
            merger.append_pdf(str(doc2), bookmark='Document 2')
            print(f"   ✓ Appended successfully")
            print(f"   New page count: {merger.get_page_count()}")
            print(f"   Pages added: {merger.get_appended_page_count()}")
        else:
            print(f"   ⚠ File not found: {doc2}")
        
        # Append third PDF
        print(f"\n4. Appending document3.pdf...")
        doc3 = test_dir / 'document3.pdf'
        if doc3.exists():
            merger.append_pdf(str(doc3), bookmark='Document 3')
            print(f"   ✓ Appended successfully")
            print(f"   Final page count: {merger.get_page_count()}")
            print(f"   Total pages appended: {merger.get_appended_page_count()}")
        else:
            print(f"   ⚠ File not found: {doc3}")
        
        # Refresh TOC
        print(f"\n5. Refreshing Table of Contents...")
        toc = merger.refresh_toc(max_depth=2)
        print(f"   ✓ TOC refreshed")
        if toc:
            print(f"\n   Contents:\n{toc}")
        
        # Save master
        print(f"\n6. Saving master PDF...")
        merger.save()
        print(f"   ✓ Master PDF saved and updated")
        
        print(f"\n" + "="*70)
        print("PDF Incremental Merge Complete!")
        print("="*70)
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
