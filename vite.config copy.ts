import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import "dotenv/config";

export default defineConfig({
	plugins: [sveltekit()],
	envPrefix: 'VITE_',
	preview: {
		host: '0.0.0.0',
		port: parseInt(process.env.VITE_PROD_PORT ?? "5173")
	},
	server: {
		host: '0.0.0.0',
		port: parseInt(process.env.VITE_DEV_PORT ?? "5173")
	}
});
