# Development Guidelines and Patterns

## Code Quality Standards

### Import Organization
- **Standard Library First**: Import Python standard library modules first
- **Third-Party Libraries**: Import external packages (FastAPI, SQLAlchemy, etc.)
- **Local Imports**: Import project-specific modules last
- **Specific Imports**: Use specific imports (`from fastapi import APIRouter`) over wildcard imports

### Documentation Standards
- **Triple Quote Docstrings**: Use `'''` for module and function documentation
- **Inline Comments**: Use `#` for section separators and explanations
- **Function Documentation**: Include purpose and parameter descriptions
- **Module Headers**: Start files with descriptive module docstrings

### Naming Conventions
- **Snake Case**: Use `snake_case` for variables, functions, and file names
- **Pascal Case**: Use `PascalCase` for class names (User, Company, Task)
- **Descriptive Names**: Use clear, descriptive names (`create_user` not `cu`)
- **Prefix Conventions**: Use `db_` prefix for database objects (`db_user`, `db_company`)

## Structural Conventions

### Router Organization (10/10 files follow this pattern)
```python
router = APIRouter(
    prefix="/endpoint",
    tags=["endpoint"],
    responses={404: {"description": "Not found"}}
)
```

### CRUD Operation Structure (8/10 files follow this pattern)
- **Create**: POST endpoints with validation and duplicate checking
- **Read**: GET endpoints for single items and lists
- **Update**: PUT endpoints with partial update support
- **Delete**: DELETE endpoints with confirmation messages

### Section Separators (9/10 files use this pattern)
```python
#==========================
# Next Section
#==========================
```

### Error Handling Pattern (10/10 files follow this)
```python
if not db_object:
    raise HTTPException(404, detail="Object not found")
```

## Database Patterns

### Model Definitions (Frequency: 10/10)
- **SQLAlchemy Declarative Base**: All models inherit from `Base`
- **Relationship Definitions**: Use `relationship()` with `back_populates`
- **Foreign Key Constraints**: Explicit foreign key definitions with proper references
- **Index Creation**: Add indexes on frequently queried columns

### Database Session Management (10/10 files)
```python
def endpoint(db: Session = Depends(get_db)):
    # Database operations
    db.add(object)
    db.commit()
    db.refresh(object)
    return object
```

### Migration Patterns (Alembic Standard)
- **Auto-generated Migrations**: Use `alembic revision --autogenerate`
- **Upgrade/Downgrade Functions**: Include both upgrade and downgrade operations
- **Index Management**: Proper index creation and removal in migrations

## Authentication and Security Patterns

### Password Handling (8/10 files with auth)
```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_pw = pwd_context.hash(password)
```

### JWT Token Management (5/10 files)
```python
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### Dependency Injection for Auth (7/10 files)
```python
async def protected_endpoint(current_user: User = Depends(get_current_user)):
    return current_user
```

## Testing Patterns

### Test Structure (8/10 test files follow this)
- **Arrange-Act-Assert**: Clear separation of test phases
- **Descriptive Test Names**: `test_operation_condition_expected_result`
- **Fixture Usage**: Leverage pytest fixtures for test data setup

### Database Testing (10/10 test files)
```python
@pytest.fixture(autouse=True, scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
```

### Test Client Pattern (10/10 test files)
```python
client = TestClient(app)
response = client.post("/endpoint/", json=data)
assert response.status_code == 200
```

## API Design Patterns

### Response Model Usage (10/10 router files)
```python
@router.post("/", response_model=schemas.ResponseModel, status_code=status.HTTP_200_OK)
async def create_item(item: schemas.CreateModel, db: Session = Depends(get_db)):
```

### Status Code Standards (9/10 files)
- **200**: Successful operations (GET, PUT, DELETE)
- **400**: Client errors (validation, duplicates)
- **404**: Resource not found
- **401**: Authentication required

### Validation Patterns (10/10 schema files)
```python
class UpdateModel(BaseModel):
    field: Optional[str] = None
    
# In router:
for key, value in update_data.model_dump(exclude_unset=True).items():
    if value is not None:
        setattr(db_object, key, value)
```

## Common Code Idioms

### Database Query Pattern (10/10 database files)
```python
db_object = db.query(Model).filter(Model.id == object_id).first()
if not db_object:
    raise HTTPException(404, detail="Object not found")
```

### Async Function Definitions (8/10 router files)
```python
async def endpoint_function():
    # Async operations
```

### Type Hints Usage (10/10 files)
- **Function Parameters**: Always include type hints
- **Return Types**: Specify return types for functions
- **Optional Types**: Use `Optional[Type]` for nullable fields

## Configuration Patterns

### Environment Configuration
- **Secret Management**: Use environment variables for sensitive data
- **Database URLs**: Configurable database connection strings
- **Token Expiration**: Configurable timeout values

### Logging Standards (3/10 files with logging)
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Operation completed")
```

## Best Practices Adherence

### Security Best Practices (10/10 applicable files)
- **Password Hashing**: Never store plain text passwords
- **JWT Tokens**: Proper token validation and expiration
- **Input Validation**: Pydantic model validation on all inputs

### Database Best Practices (10/10 database files)
- **Transaction Management**: Proper commit/rollback handling
- **Connection Pooling**: Use SQLAlchemy session management
- **Migration Control**: Version-controlled schema changes

### Testing Best Practices (10/10 test files)
- **Test Isolation**: Each test uses fresh database
- **Comprehensive Coverage**: Test both success and failure cases
- **Fixture Reuse**: Common test data through fixtures