import "dotenv/config";
import path from 'path';
import fs from 'fs';

const FLASK_PORT = process.env.FLASK_PORT ?? 8000;
const FLASK_HOST = process.env.FLASK_HOST ?? "http://127.0.0.1";
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://kenyare-backend:8000";
const UPLOADS_DIR = 'uploads';
export const FINANCIAL_AUDITS_DIR = '/api/static/uploads/audits';
export const PROPOSAL_FORMS_DIR = '/api/static/uploads/proposals';
export const QUOTATIONS_DIR = '/api/static/uploads/quotations';
export const DELETE_UPLOADS = process.env.DELETE_UPLOADS === "1";

if (!fs.existsSync(UPLOADS_DIR)) await fs.promises.mkdir(UPLOADS_DIR);
if (process.env.CLEAR_UPLOADS_DIR === "1") {
    await fs.promises.rm(UPLOADS_DIR, { recursive: true });
    await fs.promises.mkdir(UPLOADS_DIR);

}

if (!fs.existsSync(FINANCIAL_AUDITS_DIR)) await fs.promises.mkdir(FINANCIAL_AUDITS_DIR);
if (!fs.existsSync(PROPOSAL_FORMS_DIR)) await fs.promises.mkdir(PROPOSAL_FORMS_DIR);
