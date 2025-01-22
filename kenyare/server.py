import os
import shutil
import uuid
import logging
from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from kenyare.quotation.excel import make_excel
from kenyare.quotation.openai import run_prompt
from kenyare.quotation.output import get_quotation_output

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Update base paths to use shared volume
BASE_UPLOADS_DIR = "/app/static/uploads"
PROPOSAL_FORMS_DIR = f"{BASE_UPLOADS_DIR}/proposals"
FINANCIAL_AUDITS_DIR = f"{BASE_UPLOADS_DIR}/audits"
QUOTATIONS_DIR = f"{BASE_UPLOADS_DIR}/quotations"

# Create required directories
for directory in [PROPOSAL_FORMS_DIR, FINANCIAL_AUDITS_DIR, QUOTATIONS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Clear quotations directory if environment variable is set
if os.getenv("CLEAR_QUOTATIONS_DIR") == "1":
    shutil.rmtree(QUOTATIONS_DIR)
    os.makedirs(QUOTATIONS_DIR)

# Create FastAPI app and router
app = FastAPI()
router = APIRouter(prefix="/api")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request validation
class QuotationInputRequest(BaseModel):
    proposal_path: str
    audit_paths: list[str]

class QuotationOutputRequest(BaseModel):
    quotation_input: dict

@router.post("/quotation/input")
async def quotation_upload(request: QuotationInputRequest):
    logger.info("Processing quotation input request")
    logger.debug(f"Input parameters: proposal_path={request.proposal_path}, audit_paths={request.audit_paths}")
    
    # Adjust paths to be relative to the container's mount point
    proposal_path = os.path.join("/app", request.proposal_path.lstrip('/'))
    audit_paths = [os.path.join("/app", path.lstrip('/')) for path in request.audit_paths]
    
    # Verify files exist in shared volume
    if not os.path.exists(proposal_path):
        logger.error(f"Proposal file not found: {proposal_path}")
        raise HTTPException(status_code=404, detail="Proposal file not found")
    
    for audit_path in audit_paths:
        if not os.path.exists(audit_path):
            logger.error(f"Audit file not found: {audit_path}")
            raise HTTPException(status_code=404, detail=f"Audit file not found: {audit_path}")

    try:
        quotation_input = run_prompt([*audit_paths, proposal_path])
        logger.info("Successfully processed quotation input")
        return {"data": {"quotation_input": quotation_input}}
    except Exception as e:
        logger.error(f"Error processing quotation input: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quotation/output")
async def quotation_output(request: QuotationOutputRequest):
    logger.info("Processing quotation output request")
    try:
        quotation_input = request.quotation_input
        logger.debug(f"Quotation input: {quotation_input}")
        
        quotation_output = get_quotation_output(quotation_input)
        excel_filename = f"{uuid.uuid4()}.xlsx"
        excel_path = f"{QUOTATIONS_DIR}/{excel_filename}"
        excel_download_url = f"/quotations/{excel_filename}"
        
        logger.info(f"Generating Excel file: {excel_filename}")
        make_excel(
            quotation_input["reinsured_name"],
            quotation_input["broker_name"],
            quotation_input["insured_name"],
            quotation_output,
            excel_path,
        )
        
        quotation_output["excel_download_url"] = excel_download_url
        logger.info("Successfully processed quotation output")
        return {"data": {"quotation_output": quotation_output}}
    except Exception as e:
        logger.error(f"Error processing quotation output: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/health")
async def health_check():
    logger.debug("Health check requested")
    return {"status": "healthy"}

@router.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {"status": "KenyaRE FASTAPI Server is running!"}

# Include router in app
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "kenyare.server:app", 
        host=os.getenv("SERVER_HOST", "localhost"),
        port=int(os.getenv("SERVER_PORT", "8000")),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )