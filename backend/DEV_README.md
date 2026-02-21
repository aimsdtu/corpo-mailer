# Corpo Mailer Backend

## DEV Readme:

### Architecture Overview

**Project Structure:**
- `app/` - Application code
    - `api/` - Routes, models (Pydantic validation), and services (business logic)
    - `agents/` - LLM and mail agent implementations
    - `core/` - Configuration, logging, and prompts
    - `db/` - Database layer with protocol-based abstraction

### Adding a New Endpoint

1. **Create the Model** (`app/api/models/resource.py`)
     - Define Pydantic schemas for request/response validation

2. **Create Database Queries** (`app/db/sql/resourcequeries.py`)
     - Add SQL queries for your resource
     - Update `app/db/schema.py` with table definitions

3. **Create the Service** (`app/api/services/resourceservice.py`)
     - Implement business logic using queries from `resourcequeries.py`

4. **Create the Route** (`app/api/routes/resource.py`)
     - Define endpoints using the service
     - Apply RBAC decorators from `dependencies/auth.py`
     - Keep implementations slim

5. **Register Route** (`app/api/main.py`)
     - Import and include your router

### Database Management

- Store SQL queries in `app/db/sql/resourcequeries.py` (one file per resource)
- Database queries are used by services in `app/api/services/`
- Supabase implements the `protocol.py` interface - hotswap for other databases
- Update `schema.py` when adding tables; modify `session.py` only for schema changes

### Authentication & Authorization

- Use `dependencies/auth.py` for auth injection in routes
- Apply role-based decorators to routes for access control
- Roles are easily added/removed via route decorators

### Configuration & Utilities

- Environment config: `app/core/config.py`
- Logging setup: `app/core/logging.py`
- Prompts: `app/core/prompts.yaml`
## Step-by-Step Development Guide

### Step 1: Plan Your Resource
- Identify what data your resource will manage
- Define the database schema (tables, columns, data types)
- List all API operations needed (GET, POST, PUT, DELETE, etc.)
- Determine access control requirements (which roles can perform each operation)

### Step 2: Set Up Database Layer
- Create SQL migration file for your new table in the database
- Add table definition to `app/db/schema.py`
- Create `app/db/sql/resourcequeries.py` with all CRUD operations:
    - SELECT queries (list all, get by ID, filter)
    - INSERT queries (create new records)
    - UPDATE queries (modify existing records)
    - DELETE queries (remove records)
- Test each query directly in your database before proceeding
    - SELECT queries (list all, get by ID, filter)
    - INSERT queries (create new records)
    - UPDATE queries (modify existing records)
    - DELETE queries (remove records)
- Test each query directly in your database before proceeding

### Step 3: Create Data Models
- In `app/api/models/resource.py`, define Pydantic models:
    - `ResourceCreate` - for POST request validation
    - `ResourceUpdate` - for PUT request validation
    - `ResourceResponse` - for API response format
- Include field validation, type hints, and descriptions
- Add examples to model configurations for documentation

### Step 4: Implement Business Logic
- Create `app/api/services/resourceservice.py`
- Write class methods that:
    - Call database queries from `resourcequeries.py`
    - Validate business rules
    - Handle transformations
    - Raise appropriate exceptions for error cases
- Include error handling for missing records, invalid operations, and permission checks

### Step 5: Define API Routes
- Create `app/api/routes/resource.py`
- Define endpoint functions with:
    - Proper HTTP methods and paths
    - Request/response Pydantic models
    - Auth dependency injection
    - Role-based access control decorators
    - Clear docstrings and status codes
- Keep route logic minimal; delegate to service layer

### Step 6: Register Routes
- Import your router in `app/api/main.py`
- Include it with `app.include_router()` using an appropriate prefix

### Step 7: Test & Validate
- Write unit tests for your service logic
- Test endpoints with curl, Postman, or FastAPI docs
- Verify role-based access restrictions work correctly
- Test error cases and edge conditions
