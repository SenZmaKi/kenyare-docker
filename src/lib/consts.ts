export const API_BASE_URL = process.env.NODE_ENV === 'development' 
    ? 'http://kenyare-backend:8000'
    : import.meta.env.VITE_API_BASE_URL;
export const FINANCIAL_AUDITS_DIR = 'audits';
export const PROPOSAL_FORMS_DIR = 'proposals';
export const QUOTATIONS_DIR = 'quotations';
// export const DELETE_UPLOADS = import.meta.env.VITE_DELETE_UPLOADS === "1";
