import os
import logging
from typing import Dict, Any, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from finance_service import YahooFinanceService

# Configure logging using environment variable
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create the Yahoo Finance service instance
yahoo_service = YahooFinanceService()

# Create FastAPI application
app = FastAPI(
    title="Yahoo Finance Market Data Service",
    description="A service for retrieving market data from Yahoo Finance for financial projections and market analysis",
    version="1.0.0",
    openapi_tags=[{"name": "finance", "description": "Financial data endpoints"}]
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Global exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": str(exc)}
    )

@app.post("/yahoo_market", tags=["finance"])
async def yahoo_market_data(ticker: str) -> Dict[str, Any]:
    """
    Retrieve comprehensive financial and market data for a ticker symbol.
    """
    logger.info(f"Processing market data request for ticker: {ticker}")
    try:
        # Retrieve and return all market data; data is sanitized in the service
        result = yahoo_service.get_all_market_data(ticker)
        return result
    except Exception as e:
        logger.error(f"Error retrieving market data for {ticker}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving market data: {str(e)}")

@app.get("/yahoo_market_financials/{ticker}", tags=["finance"])
async def get_financials(ticker: str) -> Dict[str, Any]:
    """
    Get detailed financial statements for a ticker.
    """
    logger.info(f"Retrieving financial data for {ticker}")
    try:
        result = yahoo_service.get_financial_data(ticker)
        return result
    except Exception as e:
        logger.error(f"Error retrieving financials for {ticker}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving financial data: {str(e)}")

@app.get("/market_sizing/{ticker}", tags=["finance"])
async def get_market_sizing(ticker: str) -> Dict[str, Any]:
    """
    Get market sizing estimates (TAM, SAM, SOM) for a ticker.
    """
    logger.info(f"Retrieving market sizing data for {ticker}")
    try:
        result = yahoo_service.get_market_share_data(ticker)
        if "error" in result:
            logger.warning(f"Warning for ticker {ticker}: {result.get('error')}")
        return result
    except Exception as e:
        logger.error(f"Error retrieving market sizing for {ticker}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving market sizing data: {str(e)}")

@app.get("/industry_peers/{ticker}", tags=["finance"])
async def get_industry_peers(ticker: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get information about industry peers (competitors) for market comparison.

    Args:
        ticker: Stock ticker symbol.
        limit: Maximum number of peers to return.
    """
    logger.info(f"Retrieving industry peers for {ticker} with limit {limit}")
    try:
        result = yahoo_service.get_industry_peers(ticker, limit)
        return result
    except Exception as e:
        logger.error(f"Error retrieving industry peers for {ticker}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving industry peers: {str(e)}")

@app.get("/health", tags=["health"])
async def health_check() -> Dict[str, str]:
    """
    Simple health check endpoint to verify the service is running.
    """
    return {"status": "healthy", "service": "yahoo-finance-market-data"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
