# AI Personalizer Agent

This repository contains a full-stack application for an AI Personalizer Agent with:

- a FastAPI backend for business logic, authentication, and AI workflows
- a Next.js frontend for the user interface

## Project structure

- `backend/` - Python/FastAPI backend
- `frontend/` - Next.js frontend

## Getting started

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Default URLs

- Frontend: https://namaste-dev-hackathon.vercel.app/
- Backend: https://namastedev-hackathon.onrender.com

## Notes

Make sure the frontend environment points to the backend API URL before running the app.
