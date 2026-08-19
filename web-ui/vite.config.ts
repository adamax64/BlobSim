import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { readFileSync } from 'fs';
import { execSync } from 'child_process';

// Build version used for cache-busting of assets fetched at runtime
// (e.g. i18next-http-backend translation files). Changes every build so
// updated translations are picked up after a deploy instead of being
// served from the browser's disk cache.
const buildVersion = (() => {
  try {
    return execSync('git rev-parse --short HEAD').toString().trim() || 'dev';
  } catch {
    try {
      return readFileSync('package.json', 'utf8').match(/"version":\s*"([^"]+)"/)?.[1] ?? 'dev';
    } catch {
      return 'dev';
    }
  }
})();

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    'import.meta.env.VITE_BUILD_VERSION': JSON.stringify(buildVersion),
  },
  optimizeDeps: {
    include: ['@mui/material', '@mui/icons-material'],
  },
  build: {
    rollupOptions: {
      external: [],
    },
    chunkSizeWarningLimit: 1000,
  },
});
