import "dotenv/config";
import path from 'path';
import fs from 'fs';

const FLASK_PORT = import.meta.env.VITE_FLASK_PORT ?? 8000;
const FLASK_HOST = import.meta.env.VITE_FLASK_HOST ?? "http://127.0.0.1";
export const API_BASE_URL = `${FLASK_HOST}:${FLASK_PORT}`;

// Remove Node.js specific file system operations as they won't work in browser
export const FINANCIAL_AUDITS_DIR = 'financial-audits';
export const PROPOSAL_FORMS_DIR = 'proposal-forms';
