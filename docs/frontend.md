# Frontend Setup

## Prerequisites
- Node.js (v14 or higher)
- npm (v6 or higher)

## Installation Steps

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## Project Structure
frontend/
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   ├── styles/
│   ├── utils/
│   ├── middleware.tsx
│   └── app/
│       ├── layout.tsx
│       └── pages/
│           └── app.tsx
├── .eslintrc.json
├── .prettierrc
├── next.config.js
└── package.json

## Key Components

- **components/**: Reusable React components.
- **pages/**: Next.js pages.
- **styles/**: CSS and styling files.
- **utils/**: Utility functions.
- **middleware.tsx**: Middleware for handling requests.

## Running Tests

1. Install testing dependencies:
   ```bash
   npm install --save-dev jest @testing-library/react
   ```

2. Run tests:
   ```bash
   npm test
   ```

## Linting and Formatting

1. Run ESLint:
   ```bash
   npm run lint
   ```

2. Run Prettier:
   ```bash
   npm run format
   ```

## Deployment

1. Build the project:
   ```bash
   npm run build
   ```

2. Start the production server:
   ```bash
   npm start
   ```

For more detailed information, refer to the Next.js documentation.