---
description: Documentation for the Vite configuration file with Express.js backend integration
globs: fullstack-example/frontend/vite.config.js
---
# Vite Configuration Documentation

## Purpose
This file configures the Vite build tool for the React frontend application. It sets up the development server, plugins, build options, and proxy configuration for seamless integration with the Express.js backend.

## Usage
The Vite configuration is used automatically when running the following npm scripts:

```bash
# Start the development server
npm run dev

# Build for production
npm run build

# Preview the production build
npm run preview
```

## Dependencies
List of dependencies and relationships with other files/components:

- `vite`: The build tool and development server
- `@vitejs/plugin-react`: Plugin for React support in Vite
- React application files: Processed according to this configuration
- Express.js backend: Integrated via proxy configuration

## Configuration Options

### Development Server
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
});
```

### Proxy Configuration
The proxy configuration allows the frontend to communicate with the backend during development without CORS issues:

- All requests to `/api/*` are forwarded to the Express.js server running on port 8000
- `changeOrigin: true` ensures the host header is properly set
- `secure: false` allows for HTTP connections (for development only)

### Build Options
```javascript
build: {
  outDir: 'dist',
  assetsDir: 'assets',
  sourcemap: process.env.NODE_ENV !== 'production',
  minify: process.env.NODE_ENV === 'production',
  rollupOptions: {
    output: {
      manualChunks: {
        vendor: ['react', 'react-dom'],
        // Add other vendor chunks as needed
      }
    }
  }
}
```

## Maintenance
Guidelines for maintaining and updating this file:

- Update the port configuration if needed (currently set to 3000)
- Adjust proxy settings if API endpoints or backend port changes
- Add additional plugins as project requirements evolve
- Configure build options for production optimization
- Update manual chunks configuration as dependencies change

## Additional Notes

### Port Configuration
The development server runs on port 3000 by default, following the port standardization guidelines. This aligns with the standard port for frontend applications and works in conjunction with the Express.js backend on port 8000.

### Environment Variables
Vite supports environment variables through `.env` files:

- `.env`: Loaded in all environments
- `.env.development`: Development-specific variables
- `.env.production`: Production-specific variables

Example `.env` file:
```
VITE_API_URL=http://localhost:8000/api
VITE_APP_TITLE=My Fullstack App
```

Access in code: `import.meta.env.VITE_API_URL`

### Performance Considerations
- Use code splitting for larger applications
- Configure asset handling and optimization
- Consider using `import.meta.glob` for dynamic imports
- Implement proper caching strategies for production builds 