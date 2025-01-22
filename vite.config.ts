import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import "dotenv/config";

export default defineConfig({
    plugins: [sveltekit()],
    server: {
        host: '0.0.0.0',
        port: 5173,
        strictPort: true,
        hmr: {
            protocol: 'ws',
            host: '206.189.134.228',
            port: 5173,
            clientPort: 5173
        }
    }
});
