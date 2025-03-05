/**
 * @fileoverview Vite Configuration - Configuration for Vite bundler
 * @author Claude
 * @created 2023-11-08
 * 
 * Documentation: .cursor/rules/javascript/vite-config.mdc
 */

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  }
}); 