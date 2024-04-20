import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig(({command, mode}) => {
  const env = loadEnv(mode, process.cwd())
  return {
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
    },
    define: {
      BACKEND_HOST: JSON.stringify(env.VITE_BACKEND_HOST)
    }
  }
})
