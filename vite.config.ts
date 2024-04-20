import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  root: './src/frontend',
  envDir: '../../',
  server: {
    host: true,
    port: 5001,
    strictPort: true,
    watch: {
      ignored: [
        './src/*.py',
        './src/**/*.py'
      ]
    }
  }
})
