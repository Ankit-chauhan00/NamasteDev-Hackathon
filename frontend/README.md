# Frontend

This folder contains the Next.js frontend for the AI Personalizer Agent.

## Tech stack

- Next.js
- React
- TypeScript
- Tailwind CSS
- Three.js for visual components

## Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```

The app will be available at http://localhost:3000.

## Environment

Set the backend URL before running the app:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Useful scripts

- `npm run dev` - start the local dev server
- `npm run build` - create a production build
- `npm run lint` - run ESLint
