# Contribution Guidelines

Thank you for considering contributing to Document Merger! Here are some guidelines to help you get started.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/document-merger.git
   cd document-merger
   ```
3. **Create** a branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Install** development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8
   ```

## Development Workflow

### Code Style

- Follow PEP 8 guidelines
- Use `black` for formatting: `black document_merger/`
- Use `flake8` for linting: `flake8 document_merger/`
- Add docstrings to all public methods and classes

### Testing

- Write unit tests for new features
- Ensure existing tests pass: `python -m pytest tests/`
- Aim for >80% code coverage
- Run tests before submitting PR: `python -m pytest tests/ -v --cov=document_merger`

### Documentation

- Update README.md for user-facing changes
- Update API docstrings for code changes
- Add examples for new features
- Update CHANGELOG.md

## Submitting Changes

1. **Commit** your changes with clear messages:
   ```bash
   git commit -am "Add feature: clear description of changes"
   ```

2. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create** a Pull Request on GitHub with:
   - Clear title and description
   - Reference to any related issues
   - List of changes made
   - Screenshots/examples if applicable

## Reporting Issues

Before opening an issue:
- Check existing issues to avoid duplicates
- Use clear, descriptive titles
- Provide minimal code examples to reproduce
- Include Python version and OS information
- Include full error traceback if applicable

## Questions?

- Open a discussion in GitHub Discussions
- Check existing documentation
- Review examples in the `examples/` directory

## Code of Conduct

- Be respectful and inclusive
- Welcome feedback and different perspectives
- Focus on the code, not the person
- Help others learn and grow

Thank you for contributing!
