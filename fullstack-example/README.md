# Fullstack Example

A simple fullstack application with a React frontend and Express.js backend. The frontend features a button that sends an API request to the backend and displays the response.

## Project Structure

```
fullstack-example/
├── backend/             # Express.js backend
│   ├── server.js        # Backend server implementation
│   └── package.json     # Backend dependencies
├── frontend/            # React frontend
│   ├── src/             # Source files
│   │   ├── App.jsx      # Main application component
│   │   ├── main.jsx     # Application entry point
│   │   └── styles.css   # Application styles
│   ├── index.html       # HTML entry point
│   ├── vite.config.js   # Vite configuration
│   └── package.json     # Frontend dependencies
└── README.md            # Project documentation
```

## Getting Started

### Prerequisites

- Node.js (v14 or later)
- npm (v6 or later)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fullstack-example
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   npm install
   ```

3. Install frontend dependencies:
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   npm start
   ```
   The server will run on http://localhost:8000

2. In a new terminal, start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```
   The frontend will run on http://localhost:3000

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Click the "Fetch Data from API" button
3. The application will make a request to the backend API and display the response

## Features

- React frontend with a clean, responsive UI
- Express.js backend with a simple API endpoint
- Loading and error states for API requests
- Proper MDC documentation for all components

## Technologies Used

- **Frontend**:
  - React
  - Vite (for build and development)
  - CSS (for styling)

- **Backend**:
  - Express.js
  - CORS middleware

## Documentation

All components and files are documented using MDC (Markdown Cursor) files located in the `.cursor/rules/` directory. These files provide detailed information about each component's purpose, usage, dependencies, and maintenance guidelines.

## License

MIT 