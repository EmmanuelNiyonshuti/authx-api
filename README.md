# AUTHX-API

A simple user authentication and management REST API built with FastAPI for learning purposes.

## Features

- **Authentication**: JWT-based login system
- **User Management**: Register, login, and profile endpoints
- **Database**: SQLite for data storage
- **Testing**: Pytest integration

## Endpoints

- `POST /api/auth/register` - Create new user
- `POST /api/auth/login` - User login (returns JWT token)
- `GET /api/users/me` - Get user profile (requires auth)

## Getting Started


```bash
clone the project with:
git clone 'git@github.com:EmmanuelNiyonshuti/authx-api.git'
# Install dependencies
Getting Started
# Install dependencies
uv sync

# Navigate to app directory and run the server
cd app
fastapi dev
# or
uvicorn main:app --reload
Access the interactive API docs at http://localhost:8000/docs
```
Testing
```bash
pytest
```
## Coming Soon

Additional user management endpoints
Role-based access control (RBAC)
Docker support