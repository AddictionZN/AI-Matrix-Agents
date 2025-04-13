import os
import logging
import requests
from typing import List, Dict, Any
from langchain.tools import tool


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def yahoo_finance_market_data(ticker: str) -> Dict[str, Any]:
    """
    Retrieve comprehensive market data for a company ticker symbol.
    Use this to get financial metrics, valuation data, and market positioning.

    Args:
        ticker: The stock ticker symbol (e.g., "AAPL" for Apple Inc.)

    Returns:
        Dictionary containing comprehensive market data for the specified company.
    """
    try:
        logger.info(f"Fetching Yahoo Finance market data for: {ticker}")
        protocol_url = os.environ.get('YAHOO_FINANCE_PROTOCOL_URL')
        if not protocol_url:
            error_msg = "YAHOO_FINANCE_PROTOCOL_URL environment variable not set"
            logger.error(error_msg)
            return {"error": error_msg, "ticker": ticker}

        response = requests.post(
            f"{protocol_url}/yahoo_market",
            json={"ticker": ticker},
            timeout=30
        )
        if response.status_code == 200:
            market_data = response.json()
            # Check if the response contains error data
            if isinstance(market_data, dict) and "error" in market_data:
                logger.error(f"Error in response: {market_data.get('error')}")
                return market_data
            return market_data
        else:
            error_msg = f"Failed to get market data. Status code: {response.status_code}"
            logger.error(error_msg)
            return {"error": error_msg, "ticker": ticker}
    except Exception as e:
        error_msg = f"Error calling Yahoo Finance service: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "ticker": ticker}


@tool
def yahoo_finance_financials(ticker: str) -> Dict[str, Any]:
    """
    Retrieve financial statements (income statement, balance sheet, cash flow) for a company.
    Use this to analyze financial health, profitability, and trends.

    Args:
        ticker: The stock ticker symbol (e.g., "AAPL" for Apple Inc.)

    Returns:
        Dictionary containing financial statement data.
    """
    try:
        logger.info(f"Fetching financial statements for: {ticker}")
        protocol_url = os.environ.get('YAHOO_FINANCE_PROTOCOL_URL')
        if not protocol_url:
            error_msg = "YAHOO_FINANCE_PROTOCOL_URL environment variable not set"
            logger.error(error_msg)
            return {"error": error_msg, "ticker": ticker}

        response = requests.get(
            f"{protocol_url}/yahoo_market/financials/{ticker}",
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = f"Failed to get financial data. Status code: {response.status_code}"
            logger.error(error_msg)
            return {"error": error_msg, "ticker": ticker}
    except Exception as e:
        error_msg = f"Error calling Yahoo Finance service: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "ticker": ticker}


@tool
def yahoo_market_sizing(ticker: str) -> Dict[str, Any]:
    """
    Get market sizing estimates for a company including sector, industry position,
    and growth metrics. Use this to understand a company's market position and potential TAM/SAM/SOM.

    Args:
        ticker: The stock ticker symbol (e.g., "AAPL" for Apple Inc.)

    Returns:
        Dictionary containing market sizing data.
    """
    try:
        logger.info(f"Fetching market sizing data for: {ticker}")
        protocol_url = os.environ.get('YAHOO_FINANCE_PROTOCOL_URL')
        if not protocol_url:
            error_msg = "YAHOO_FINANCE_PROTOCOL_URL environment variable not set"
            logger.error(error_msg)
            return {"error": error_msg, "ticker": ticker}

        response = requests.get(
            f"{protocol_url}/market_sizing/{ticker}",
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = f"Failed to get market sizing data. Status code: {response.status_code}"
            logger.error(error_msg)
            return {"error": error_msg, "ticker": ticker}
    except Exception as e:
        error_msg = f"Error calling Yahoo Finance service: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "ticker": ticker}


@tool
def yahoo_industry_peers(ticker: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve industry peers (competitors) for market comparison.
    Use this to compare a company against its competitors in the same sector.

    Args:
        ticker: The stock ticker symbol (e.g., "AAPL" for Apple Inc.)
        limit: Maximum number of peers to return (default: 5)

    Returns:
        List of peer companies with basic financial metrics.
    """
    try:
        logger.info(f"Fetching industry peers for: {ticker}")
        protocol_url = os.environ.get('YAHOO_FINANCE_PROTOCOL_URL')
        if not protocol_url:
            error_msg = "YAHOO_FINANCE_PROTOCOL_URL environment variable not set"
            logger.error(error_msg)
            return [{"error": error_msg, "ticker": ticker}]

        response = requests.get(
            f"{protocol_url}/industry_peers/{ticker}",
            params={"limit": limit},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = f"Failed to get industry peers. Status code: {response.status_code}"
            logger.error(error_msg)
            return [{"error": error_msg, "ticker": ticker}]
    except Exception as e:
        error_msg = f"Error calling Yahoo Finance service: {str(e)}"
        logger.error(error_msg)
        return [{"error": error_msg, "ticker": ticker}]
