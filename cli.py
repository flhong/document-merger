#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CLI interface for Document Merger.
"""

import sys
import click
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from document_merger import PDFMerger, WordMerger, HybridMerger
from document_merger.config import Config


@click.group()
def cli():
    """Document Merger - Merge PDF and Word documents with automatic TOC generation."""
    pass


@cli.command()
@click.option('--files', '-f', multiple=True, required=True, 
              help='PDF files to merge')
@click.option('--output', '-o', required=True, 
              help='Output PDF file path')
@click.option('--toc', is_flag=True, default=False,
              help='Generate table of contents')
@click.option('--bookmarks', '-b', multiple=True,
              help='Bookmark titles for each PDF (optional)')
@click.option('--style', type=click.Choice(['formal', 'simple', 'hierarchical']),
              default='formal', help='TOC style')
def merge_pdf(files, output, toc, bookmarks, style):
    """Merge multiple PDF files.
    
    Example:
        python cli.py merge-pdf -f doc1.pdf -f doc2.pdf -o merged.pdf --toc
    """
    try:
        merger = PDFMerger()
        
        click.echo(f"\n{click.style('Merging PDF files...', fg='cyan')}")
        
        for i, pdf_file in enumerate(files):
            bookmark = bookmarks[i] if i < len(bookmarks) else None
            merger.add_pdf(pdf_file, bookmark)
            click.echo(f"  {click.style('✓', fg='green')} Added: {pdf_file}")
        
        if toc:
            click.echo(f"\n{click.style('Generating TOC...', fg='cyan')}")
            toc_str = merger.generate_toc(style=style, add_to_pdf=True)
            click.echo(f"  {click.style('✓', fg='green')} TOC generated")
        
        click.echo(f"\n{click.style('Saving output...', fg='cyan')}")
        merger.save(output)
        click.echo(f"  {click.style('✓', fg='green')} Saved to: {output}")
        click.echo(f"\n{click.style('Success!', fg='green', bold=True)}")
        
    except Exception as e:
        click.echo(f"\n{click.style('Error:', fg='red', bold=True)} {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--files', '-f', multiple=True, required=True,
              help='Word files to merge')
@click.option('--output', '-o', required=True,
              help='Output Word file path')
@click.option('--toc', is_flag=True, default=False,
              help='Generate and insert table of contents')
@click.option('--page-breaks', is_flag=True, default=True,
              help='Add page breaks between documents')
def merge_word(files, output, toc, page_breaks):
    """Merge multiple Word documents.
    
    Example:
        python cli.py merge-word -f doc1.docx -f doc2.docx -o merged.docx --toc
    """
    try:
        merger = WordMerger()
        
        click.echo(f"\n{click.style('Merging Word documents...', fg='cyan')}")
        
        for docx_file in files:
            merger.add_document(docx_file, add_page_break=page_breaks)
            click.echo(f"  {click.style('✓', fg='green')} Added: {docx_file}")
        
        if toc:
            click.echo(f"\n{click.style('Generating and inserting TOC...', fg='cyan')}")
            toc_str = merger.generate_toc(insert_at_beginning=True)
            click.echo(f"  {click.style('✓', fg='green')} TOC generated")
        else:
            merger.merge()
        
        click.echo(f"\n{click.style('Saving output...', fg='cyan')}")
        merger.save(output)
        click.echo(f"  {click.style('✓', fg='green')} Saved to: {output}")
        click.echo(f"\n{click.style('Success!', fg='green', bold=True)}")
        
    except Exception as e:
        click.echo(f"\n{click.style('Error:', fg='red', bold=True)} {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--files', '-f', multiple=True, required=True,
              help='PDF or Word files to merge')
@click.option('--output', '-o', required=True,
              help='Output file path')
@click.option('--format', 'output_format', type=click.Choice(['pdf', 'docx']),
              default='pdf', help='Output format')
@click.option('--toc', is_flag=True, default=False,
              help='Generate table of contents')
@click.option('--style', type=click.Choice(['formal', 'simple', 'hierarchical']),
              default='formal', help='TOC style')
def merge_hybrid(files, output, output_format, toc, style):
    """Merge mixed PDF and Word documents.
    
    Example:
        python cli.py merge-hybrid -f doc1.docx -f doc2.pdf -o merged.pdf --toc
    """
    try:
        merger = HybridMerger(output_format=output_format)
        
        click.echo(f"\n{click.style('Merging documents...', fg='cyan')}")
        click.echo(f"  Output format: {output_format.upper()}")
        
        for doc_file in files:
            merger.add_document(doc_file)
            click.echo(f"  {click.style('✓', fg='green')} Added: {doc_file}")
        
        if toc:
            click.echo(f"\n{click.style('Generating TOC...', fg='cyan')}")
            toc_str = merger.generate_toc(style=style)
            click.echo(f"  {click.style('✓', fg='green')} TOC generated")
        
        click.echo(f"\n{click.style('Saving output...', fg='cyan')}")
        merger.save(output)
        click.echo(f"  {click.style('✓', fg='green')} Saved to: {output}")
        click.echo(f"\n{click.style('Success!', fg='green', bold=True)}")
        
    except Exception as e:
        click.echo(f"\n{click.style('Error:', fg='red', bold=True)} {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--output', '-o', default='tests/output',
              help='Output directory for test files')
def generate(output):
    """Generate sample test documents.
    
    Example:
        python cli.py generate
    """
    try:
        from tests.generate_test_files import create_sample_docx_files, create_sample_pdf_files
        
        click.echo(f"\n{click.style('Generating test documents...', fg='cyan')}")
        
        click.echo(f"\n  {click.style('Creating DOCX files...', fg='yellow')}")
        create_sample_docx_files()
        
        click.echo(f"\n  {click.style('Creating PDF files...', fg='yellow')}")
        create_sample_pdf_files()
        
        click.echo(f"\n{click.style('Test documents generated successfully!', fg='green', bold=True)}")
        
    except Exception as e:
        click.echo(f"\n{click.style('Error:', fg='red', bold=True)} {e}", err=True)
        sys.exit(1)


@cli.command()
def version():
    """Show version information."""
    from document_merger import __version__
    click.echo(f"Document Merger v{__version__}")


if __name__ == '__main__':
    cli()
