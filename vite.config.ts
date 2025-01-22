import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import "dotenv/config";

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		host: '0.0.0.0',
		port: 5173,
		hmr: {
			// Set proper HMR configuration
			clientPort: 5173,
			host: '206.189.134.228' // Your server's public IP
		}
	}
});
