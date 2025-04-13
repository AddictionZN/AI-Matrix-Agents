import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Dict, Any

from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# Environment & Logging Configuration
# -----------------------------------------------------------------------------
load_dotenv()

log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# FastAPI Lifespan
# -----------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Financial Agents API...")
    yield
    logger.info("Shutting down Financial Agents API...")

# -----------------------------------------------------------------------------
# Initialize FastAPI App
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Financial Agents API",
    description="API for generating cash flow analyses using AI agents",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[{"name": "cash-flow", "description": "Generate cash flow analysis"}]
)

# -----------------------------------------------------------------------------
# CORS Middleware Configuration
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# -----------------------------------------------------------------------------
# Exception Handling
# -----------------------------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "detail": exc.errors(),
            "body": exc.body,
            "message": "Invalid request format. Please check your input."
        })
    )

# -----------------------------------------------------------------------------
# Cash Flow Analysis Endpoint
# -----------------------------------------------------------------------------
@app.post(
    "/cash-flow",
    tags=["cash-flow"],
    response_model=CashFlowResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate cash flow analysis",
    description="Creates a cash flow analysis for the provided project details."
)
async def analyze_cash_flow(request_body: CashFlowRequest) -> CashFlowResponse:
    """
    Generate a cash flow analysis.

    - **project_name**: Name of the project (required)
    - **project_description**: Brief description of the project (required)
    - **industry**: Industry sector of the project (required)
    - **additional_context**: Any extra information to consider (optional)
    """
    try:
        logger.info(f"Received request for cash flow analysis of project: {request_body.project_name}")
        result: Dict[str, Any] = generate_cash_flow(
            project_name=request_body.project_name,
            project_description=request_body.project_description,
            industry=request_body.industry,
            additional_context=request_body.additional_context
        )
        return CashFlowResponse(
            project_name=request_body.project_name,
            success=result.get("success"),
            error=result.get("error"),
            intermediate_steps=result.get("intermediate_steps"),
            cash_flow_projection=result.get("cash_flow_projection")
        )
    except Exception as e:
        logger.error(f"Error processing cash flow request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

# -----------------------------------------------------------------------------
# Health Check Endpoint (optional)
# -----------------------------------------------------------------------------
@app.get("/health", tags=["health"])
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "Financial Agents API"}

# -----------------------------------------------------------------------------
# Application Entry Point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
