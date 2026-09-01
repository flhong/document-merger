#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick start script for Document Merger.
Generates test documents and runs example merge operations.
"""

import sys
import os
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tests.generate_test_files import main as generate_test_files


def main():
    """Main entry point."""
    print("\n" + "="*70)
    print("Document Merger - Quick Start")
    print("="*70)
    
    print("\nStep 1: Generating test documents...")
    print("-" * 70)
    try:
        generate_test_files()
        print("\n✓ Test documents generated successfully!")
    except Exception as e:
        print(f"\n✗ Error generating test documents: {e}")
        return 1
    
    print("\n" + "="*70)
    print("Step 2: Running examples...")
    print("-" * 70)
    
    examples = [
        ('examples/merge_pdfs.py', 'PDF Merge Example'),
        ('examples/merge_docs.py', 'Word Document Merge Example'),
        ('examples/hybrid_merge.py', 'Hybrid (PDF + Word) Merge Example'),
    ]
    
    for example_file, description in examples:
        example_path = project_root / example_file
        if example_path.exists():
            print(f"\n>>> Running: {description}")
            print("-" * 70)
            try:
                import runpy
                runpy.run_path(str(example_path))
            except Exception as e:
                print(f"✗ Error running {example_file}: {e}")
        else:
            print(f"✗ Example file not found: {example_file}")
    
    print("\n" + "="*70)
    print("Step 3: Running unit tests...")
    print("-" * 70)
    
    import unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_modules = [
        'tests.test_pdf_merger',
        'tests.test_word_merger',
        'tests.test_hybrid_merger',
        'tests.test_toc_manager',
    ]
    
    for test_module in test_modules:
        try:
            suite.addTests(loader.loadTestsFromName(test_module))
        except Exception as e:
            print(f"✗ Error loading {test_module}: {e}")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print("Quick Start Complete!")
    print("="*70)
    print("\nGenerated files:")
    print(f"  - Test PDFs: tests/sample_pdfs/")
    print(f"  - Test Documents: tests/sample_docs/")
    print(f"  - Output: tests/output/")
    
    print("\nNext steps:")
    print("  1. Check the output files in tests/output/")
    print("  2. Review the examples in examples/ directory")
    print("  3. Run individual tests: python -m pytest tests/")
    print("  4. Read the README.md for API documentation")
    print("\n" + "="*70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
