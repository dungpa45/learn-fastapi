# Project Structure and Architecture

## Directory Organization

### Root Structure
```
learn-python/
├── crud/                    # Basic CRUD operations learning
├── fastapi-test/           # FastAPI experimentation and examples
├── learn-fastapi/          # Main learning projects
│   └── todo-app/          # Comprehensive todo application
├── practice/              # Practice scripts and experiments
└── .amazonq/              # Amazon Q configuration and rules
```

## Core Components and Relationships

### 1. Todo App Architecture (Main Project)
```
todo-app/
├── models/                 # Database models (SQLAlchemy)
│   ├── __init__.py
│   └── base.py            # User, Task, Company models
├── routers/               # API route handlers
│   ├── auth.py           # Authentication endpoints
│   ├── company.py        # Company CRUD operations
│   ├── task.py           # Task management
│   └── user.py           # User management
├── schemas/               # Pydantic models for validation
│   ├── auth.py           # Authentication schemas
│   ├── company.py        # Company request/response models
│   ├── task.py           # Task data models
│   └── user.py           # User data models
├── tests/                 # Comprehensive test suite
│   ├── conftest.py       # Test configuration and fixtures
│   ├── test_company.py   # Company endpoint tests
│   ├── test_task.py      # Task endpoint tests
│   └── test_user.py      # User endpoint tests
├── utils/                 # Utility functions
│   └── auth_user.py      # Authentication helpers
├── versions/              # Alembic migration files
├── main.py               # FastAPI application entry point
├── database.py           # Database configuration
└── requirements.txt      # Project dependencies
```

### 2. Component Relationships

#### Database Layer
- **Models**: SQLAlchemy ORM models defining database schema
- **Database**: Connection management and session handling
- **Migrations**: Alembic for schema version control

#### API Layer
- **Routers**: Modular endpoint organization by entity type
- **Schemas**: Pydantic models for request/response validation
- **Authentication**: JWT-based security with OAuth2

#### Business Logic
- **CRUD Operations**: Create, Read, Update, Delete for all entities
- **Authentication Flow**: User registration, login, token management
- **Authorization**: Company-based access control

#### Testing Layer
- **Unit Tests**: Individual endpoint testing
- **Integration Tests**: Full workflow testing
- **Fixtures**: Reusable test data setup

## Architectural Patterns

### 1. Layered Architecture
- **Presentation Layer**: FastAPI routers and endpoints
- **Business Layer**: Service logic and validation
- **Data Layer**: SQLAlchemy models and database operations

### 2. Dependency Injection
- Database session management through FastAPI dependencies
- Authentication middleware for protected endpoints
- Modular component injection for testing

### 3. Repository Pattern
- Database operations abstracted through SQLAlchemy ORM
- Model-based data access with relationship management
- Migration-based schema evolution

### 4. MVC-like Structure
- **Models**: Database entities and relationships
- **Views**: API endpoints and response formatting
- **Controllers**: Router functions handling business logic

## Learning Progression

### Basic Level (practice/, crud/)
- Simple FastAPI applications
- Basic CRUD operations
- Database connectivity

### Intermediate Level (fastapi-test/)
- Authentication implementation
- Advanced routing
- Error handling

### Advanced Level (learn-fastapi/todo-app/)
- Complete application architecture
- Testing frameworks
- Database migrations
- Security best practices
- Multi-entity relationships