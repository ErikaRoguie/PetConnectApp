# Contributing to Pet Connect

Thank you for your interest in contributing to Pet Connect! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to maintain a respectful and inclusive environment for everyone.

## Setting Up the Development Environment

1. Fork the Repl from [Replit](https://replit.com/@username/pet-connect)
2. The environment will automatically configure:
   - Python 3.11
   - PostgreSQL database
   - Required system dependencies

### Dependencies
The project uses the following main dependencies:
- Flask (^3.0.3)
- Flask-SQLAlchemy (^3.1.1)
- Flask-RestX (^1.3.0)
- psycopg2-binary (^2.9.9)

## Coding Standards

### Python Style Guide
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 79 characters

### JavaScript Style Guide
- Use ES6+ features where appropriate
- Follow camelCase naming convention
- Add comments for complex logic
- Use meaningful variable and function names
- Avoid global variables

### HTML/CSS Style Guide
- Use semantic HTML elements
- Follow BEM naming convention for CSS classes
- Maintain responsive design principles
- Keep CSS organized by component

## Development Workflow

### Creating Issues
1. Check existing issues to avoid duplicates
2. Use issue templates if available
3. Provide clear reproduction steps for bugs
4. Include expected vs actual behavior
5. Add relevant labels

### Pull Request Process
1. Create a feature branch from `main`
2. Make focused, atomic commits
3. Write clear commit messages
4. Update documentation as needed
5. Add tests for new features
6. Ensure all tests pass
7. Request review from maintainers

### Git Commit Guidelines
Format: `<type>(<scope>): <subject>`

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance tasks

Example: `feat(pets): add image upload validation`

## Testing Requirements

### Unit Tests
- Write tests for new features
- Maintain test coverage
- Use appropriate assertions
- Mock external dependencies

### Integration Tests
- Test API endpoints
- Verify database operations
- Check file operations
- Test frontend-backend integration

## Documentation Requirements

### Code Documentation
- Add docstrings to Python functions/classes
- Comment complex logic
- Update API documentation
- Keep README.md current

### API Documentation
- Document new endpoints in Swagger/OpenAPI
- Include request/response examples
- Document error responses
- Update API version when needed

## Submitting Changes

1. Push changes to your fork
2. Create a Pull Request to `main`
3. Fill out the PR template
4. Link related issues
5. Wait for review

## Getting Help

- Check existing documentation
- Search closed issues
- Ask questions in discussions
- Contact maintainers

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-RestX Documentation](https://flask-restx.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Recognition

Contributors will be added to the README.md acknowledgments section.

---

Thank you for contributing to Pet Connect! Your efforts help make this project better for everyone.
