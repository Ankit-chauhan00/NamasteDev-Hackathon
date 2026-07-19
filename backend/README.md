# Backend

This folder contains the FastAPI backend for the AI Personalizer Agent.

## Tech stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- LangGraph and LangChain
- PostgreSQL

## Setup

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (or use `uv`):
   ```bash
   uv sync
   ```
3. Start the API server:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

The API will be available at http://localhost:8000.

## Database

Run migrations with:

```bash
uv run alembic upgrade head
```

## Testing

Run the test suite with:

```bash
uv run pytest
```
