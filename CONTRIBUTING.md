# Contributing to EEMCARS

Thank you for your interest in contributing to EEMCARS! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/eemcars.git
   cd eemcars
   ```

2. **Install dependencies:**
   ```bash
   make install
   ```

3. **Start development environment:**
   ```bash
   make dev
   ```

## Code Style

### Python (Backend)
- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use type hints where applicable
- Write docstrings for all public functions and classes

### JavaScript/React (Frontend)
- Follow [Airbnb React Style Guide](https://github.com/airbnb/javascript/tree/master/react)
- Use functional components with hooks
- Use meaningful variable and function names

## Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Run tests before submitting PR:
  ```bash
  make test
  ```

## Pull Request Process

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** and commit with clear messages
3. **Update documentation** if needed
4. **Add tests** for new functionality
5. **Run linters and tests:**
   ```bash
   make lint
   make test
   ```
6. **Submit a pull request** with a clear description

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
feat: add new assessment endpoint
fix: correct maturity calculation bug
docs: update API documentation
test: add tests for scoring engine
chore: update dependencies
```

## Bug Reports

When reporting bugs, include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, versions)
- Relevant logs or screenshots

## Feature Requests

For feature requests, please:
- Describe the feature and its use case
- Explain why it would be valuable
- Provide examples if possible

## Code Review

All submissions require code review. We use GitHub pull requests for this purpose.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
