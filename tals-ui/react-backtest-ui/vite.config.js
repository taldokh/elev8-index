import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ['elev8.cs.colman.ac.il'],
    host: true, // this allows exposure to the network (equivalent to --host)
  },
})
