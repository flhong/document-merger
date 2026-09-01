"""
Auto test runner for Document Merger.
Generates test files and runs all tests.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def run_tests():
    """Run all tests with detailed output."""
    print("\n" + "="*70)
    print("Document Merger - Auto Test Runner")
    print("="*70)
    
    # Step 1: Generate test files
    print("\nStep 1: Generating test files...")
    print("-" * 70)
    try:
        from tests.generate_test_files import create_sample_pdf_files, create_sample_docx_files
        create_sample_docx_files()
        create_sample_pdf_files()
        print("\n✓ Test files generated successfully")
    except Exception as e:
        print(f"\n✗ Error generating test files: {e}")
        return False
    
    # Step 2: Run examples
    print("\n" + "="*70)
    print("Step 2: Running examples...")
    print("-" * 70)
    
    examples = [
        ('examples/merge_pdfs.py', 'PDF Merge Example'),
        ('examples/merge_docs.py', 'Word Document Merge Example'),
    ]
    
    for example_file, description in examples:
        example_path = Path(example_file)
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
    
    # Step 3: Run unit tests
    print("\n" + "="*70)
    print("Step 3: Running unit tests...")
    print("-" * 70)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_modules = [
        'tests.test_pdf_merger',
        'tests.test_word_merger',
        'tests.test_toc_manager',
    ]
    
    for test_module in test_modules:
        try:
            suite.addTests(loader.loadTestsFromName(test_module))
        except Exception as e:
            print(f"✗ Error loading {test_module}: {e}")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✓ All tests passed!")
        return True
    else:
        print("\n✗ Some tests failed.")
        return False


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
