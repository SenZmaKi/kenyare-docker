import "dotenv/config";

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://kenyare-backend:8000";
// Update paths to be relative to container mount point
export const FINANCIAL_AUDITS_DIR = 'audits';
export const PROPOSAL_FORMS_DIR = 'proposals';
export const QUOTATIONS_DIR = 'quotations';
export const DELETE_UPLOADS = process.env.DELETE_UPLOADS === "1";
