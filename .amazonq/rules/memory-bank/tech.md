# Technology Stack and Development Setup

## Programming Languages and Versions

### Python
- **Primary Language**: Python 3.10+
- **Type Hints**: Extensive use of Python type annotations
- **Async/Await**: Asynchronous programming with FastAPI

## Core Technologies

### Web Framework
- **FastAPI**: Modern, fast web framework for building APIs
  - Automatic API documentation (Swagger UI, ReDoc)
  - Built-in data validation with Pydantic
  - Native async support
  - OAuth2 and JWT integration

### Database Stack
- **SQLAlchemy**: Python SQL toolkit and ORM
  - Declarative model definitions
  - Relationship management
  - Query building and execution
- **SQLite**: Lightweight, file-based database
  - Development and testing database
  - Zero-configuration setup
- **Alembic**: Database migration tool
  - Schema version control
  - Automatic migration generation

### Data Validation and Serialization
- **Pydantic**: Data validation using Python type annotations
  - Request/response model validation
  - Automatic JSON schema generation
  - Type conversion and validation

### Authentication and Security
- **Passlib**: Password hashing library
  - Bcrypt algorithm for secure password storage
  - Password verification utilities
- **Python-JOSE**: JWT token handling
  - Token creation and validation
  - OAuth2 implementation support

### Testing Framework
- **Pytest**: Testing framework
  - Test discovery and execution
  - Fixture management
  - Parametrized testing
- **TestClient**: FastAPI testing utilities
  - HTTP client for endpoint testing
  - Database isolation for tests

### Development Tools
- **Uvicorn**: ASGI server for development
  - Hot reload during development
  - Production-ready deployment
- **Pylint**: Code quality and style checking
  - Configuration via .pylintrc
  - Import error resolution

## Dependencies and Build System

### Core Dependencies (requirements.txt)
```
fastapi          # Web framework
uvicorn          # ASGI server
sqlalchemy       # ORM and database toolkit
passlib[bcrypt]  # Password hashing
pydantic         # Data validation
python-multipart # Form data handling
jose             # JWT token handling
pytest           # Testing framework
```

### Development Commands

#### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Database Management
```bash
# Run migrations
alembic upgrade head

# Generate new migration
alembic revision --autogenerate -m "description"
```

#### Development Server
```bash
# Start development server with hot reload
uvicorn main:app --reload

# Access API documentation
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

#### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_user.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=.
```

## Configuration Files

### Alembic Configuration (alembic.ini)
- Database connection settings
- Migration file templates
- Logging configuration

### Pylint Configuration (.pylintrc)
- Code style rules
- Import path configuration
- Error suppression settings

### Git Configuration (.gitignore)
- Python cache files exclusion
- Database files exclusion
- Environment-specific files

## Development Environment

### IDE Support
- Type hints for better IDE integration
- Automatic API documentation generation
- Hot reload for rapid development

### Database Development
- SQLite for local development
- Alembic for schema migrations
- Test database isolation

### API Development
- Automatic OpenAPI schema generation
- Interactive API documentation
- Request/response validation