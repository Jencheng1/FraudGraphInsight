# Contributing to FraudGraphInsight

Thank you for your interest in contributing to FraudGraphInsight! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and considerate of others.

## How to Contribute

1. **Fork the Repository**
   - Fork the repository to your GitHub account
   - Clone your fork locally

2. **Create a Branch**
   - Create a new branch for your feature or bugfix
   - Use a descriptive name (e.g., `feature/add-new-fraud-pattern` or `fix/transaction-validation`)

3. **Make Changes**
   - Follow the project's coding style
   - Write clear, concise commit messages
   - Include tests for new features
   - Update documentation as needed

4. **Submit a Pull Request**
   - Push your changes to your fork
   - Create a pull request to the main repository
   - Provide a clear description of your changes

## Development Setup

1. **Environment Setup**
   ```bash
   # Clone the repository
   git clone https://github.com/your-username/fraud-graph-insight.git
   cd fraud-graph-insight

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Running Tests**
   ```bash
   # Run all tests
   python -m pytest

   # Run specific test file
   python -m pytest tests/test_file.py
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose

## Documentation

- Update README.md for significant changes
- Add comments for complex logic
- Document new features and APIs
- Keep the documentation up-to-date

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Include test cases for edge cases
- Maintain good test coverage

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation
3. Add tests for new features
4. Ensure the test suite passes
5. The PR will be reviewed by maintainers

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have any questions, please open an issue or contact the maintainers. 