# Contributing to gh0sty

Thank you for showing interest in improving the **gh0sty** framework! We welcome all contributions, including bug fixes, new modules, security checks, documentation updates, and pull requests.

## Code of Conduct

Please behave professionally and treat all contributors with respect. This project is built for ethical, authorized target auditing only.

## Development Setup

To configure your development environment:

1. Clone this repository:
   ```bash
   git clone https://github.com/jacksonfb/gh0sty.git
   cd gh0sty
   ```

2. Setup virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Guidelines

Before opening a pull request, ensure your code respects our quality guidelines:

- **Type Hints**: All functions and classes must be statically typed.
- **Docstrings**: Use PEP 257 Google style docstrings.
- **Formatting**: Format your code using `black` (line limit: 100):
  ```bash
  black .
  ```
- **Linting**: Keep code clean of warnings using `ruff`:
  ```bash
  ruff check .
  ```
- **Static Analysis**: Verify typing correctness with `mypy`:
  ```bash
  mypy gh0sty tests
  ```
- **Testing**: Ensure all tests pass:
  ```bash
  pytest
  ```

Thank you for keeping **gh0sty** clean, secure, and professional!
