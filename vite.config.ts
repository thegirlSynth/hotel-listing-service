import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
// import swc from 'vite-plugin-swc';

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),  
  ],
})
