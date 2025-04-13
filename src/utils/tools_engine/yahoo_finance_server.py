import math
import logging
import numpy as np
import pandas as pd
import yfinance as yf
from typing import Dict, Any, List, Union


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YahooFinanceService:
    """
    A service for fetching and sanitizing financial data from Yahoo Finance.
    """

    def __init__(self) -> None:
        logger.info("Initializing Yahoo Finance Service")

    def _sanitize_data(self, data: Any) -> Any:
        """
        Recursively sanitize data to replace NaN and infinite values with None for JSON compatibility.

        Args:
            data: Any data structure that might contain problematic float values.

        Returns:
            The sanitized data structure.
        """
        if isinstance(data, float):
            if math.isnan(data) or math.isinf(data):
                return None
            return data
        elif isinstance(data, dict):
            return {k: self._sanitize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        elif isinstance(data, pd.DataFrame):
            # Replace NaN values with None and convert DataFrame to dict
            data_dict = data.where(pd.notna(data), None).to_dict()
            return self._sanitize_data(data_dict)
        elif isinstance(data, pd.Series):
            # Replace NaN values with None and convert Series to dict
            data_dict = data.where(pd.notna(data), None).to_dict()
            return self._sanitize_data(data_dict)
        elif isinstance(data, np.ndarray):
            data_list = data.tolist()
            return self._sanitize_data(data_list)
        return data

    def get_market_share_data(self, ticker: str) -> Dict[str, Any]:
        """
        (Stub) Get market share data for a ticker. Extend this method if more detailed logic is needed.

        Args:
            ticker: The stock ticker symbol.

        Returns:
            An empty dict (or market share data if implemented).
        """
        # Stub: Return an empty dict or implement your logic
        return {}

    def get_all_market_data(self, ticker: str) -> Dict[str, Any]:
        """
        Get comprehensive financial and market data for a ticker.

        Args:
            ticker: The stock ticker symbol.

        Returns:
            A dictionary containing all available market data.
        """
        try:
            logger.info(f"Fetching comprehensive market data for {ticker}")
            stock = yf.Ticker(ticker)
            result = {
                "info": stock.info,
                "market_share": self.get_market_share_data(ticker),
                "financials": self.get_financial_data(ticker),
                "peers": self.get_industry_peers(ticker)
            }
            return self._sanitize_data(result)
        except Exception as e:
            logger.error(f"Error fetching market data for {ticker}: {str(e)}", exc_info=True)
            return {"error": str(e), "ticker": ticker}

    def get_financial_data(self, ticker: str) -> Dict[str, Any]:
        """
        Get financial statements for a ticker.

        Args:
            ticker: The stock ticker symbol.

        Returns:
            A dictionary containing financial statement data.
        """
        try:
            logger.info(f"Fetching financial data for {ticker}")
            stock = yf.Ticker(ticker)

            # Income Statement
            income_stmt = {}
            if hasattr(stock, 'income_stmt') and stock.income_stmt is not None and not stock.income_stmt.empty:
                income_stmt = stock.income_stmt.where(pd.notna(stock.income_stmt), None).to_dict()

            # Balance Sheet
            balance_sheet = {}
            if hasattr(stock, 'balance_sheet') and stock.balance_sheet is not None and not stock.balance_sheet.empty:
                balance_sheet = stock.balance_sheet.where(pd.notna(stock.balance_sheet), None).to_dict()

            # Cash Flow
            cash_flow = {}
            if hasattr(stock, 'cashflow') and stock.cashflow is not None and not stock.cashflow.empty:
                cash_flow = stock.cashflow.where(pd.notna(stock.cashflow), None).to_dict()

            result = {
                "income_statement": income_stmt,
                "balance_sheet": balance_sheet,
                "cash_flow": cash_flow,
                "key_metrics": self.get_estimation_data(ticker),
                "resource_data": self.get_resource_allocation_data(ticker)
            }
            return self._sanitize_data(result)
        except Exception as e:
            logger.error(f"Error fetching financial data for {ticker}: {str(e)}", exc_info=True)
            return {"error": str(e), "ticker": ticker}

    def get_industry_peers(self, ticker: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get industry peers for a ticker.

        Args:
            ticker: The stock ticker symbol.
            limit: Maximum number of peers to return.

        Returns:
            A list of dictionaries containing peer data.
        """
        peers: List[Dict[str, Any]] = []
        try:
            logger.info(f"Getting industry peers for {ticker}")
            stock = yf.Ticker(ticker)
            info = stock.info

            if info and "recommendedSymbols" in info:
                recommended_symbols = info.get("recommendedSymbols", [])
                peers_list = recommended_symbols[:limit]

                for peer_ticker in peers_list:
                    try:
                        peer_stock = yf.Ticker(peer_ticker)
                        peer_info = peer_stock.info
                        peers.append({
                            "ticker": peer_ticker,
                            "name": peer_info.get("shortName"),
                            "sector": peer_info.get("sector"),
                            "industry": peer_info.get("industry"),
                            "market_cap": peer_info.get("marketCap")
                        })
                    except Exception as peer_err:
                        logger.warning(f"Error getting data for peer ticker {peer_ticker}: {peer_err}")
            return self._sanitize_data(peers)
        except Exception as e:
            logger.error(f"Error fetching industry peers for {ticker}: {str(e)}", exc_info=True)
            return [{"error": str(e), "ticker": ticker}]

    def get_cash_flow(self, ticker: str) -> Dict[str, Any]:
        """
        Get cash flow statement for a ticker.

        Args:
            ticker: The stock ticker symbol.

        Returns:
            A dictionary containing cash flow data.
        """
        try:
            logger.info(f"Fetching cash flow data for {ticker}")
            stock = yf.Ticker(ticker)
            cash_flow = stock.cashflow

            if cash_flow is None or cash_flow.empty:
                return {"error": "Cash flow data is empty", "ticker": ticker}

            cash_flow_dict = cash_flow.where(pd.notna(cash_flow), None).to_dict()
            return self._sanitize_data(cash_flow_dict)
        except Exception as e:
            logger.error(f"Error fetching cash flow data for {ticker}: {str(e)}", exc_info=True)
            return {"error": str(e), "ticker": ticker}

    def get_estimation_data(self, ticker: str) -> Dict[str, Any]:
        """
        Get key financial metrics for estimation purposes.

        Args:
            ticker: The stock ticker symbol.

        Returns:
            A dictionary containing key financial metrics.
        """
        try:
            logger.info(f"Fetching estimation data for {ticker}")
            stock = yf.Ticker(ticker)
            info = stock.info

            estimation_data = {
                "previous_close": info.get("previousClose"),
                "open": info.get("open"),
                "bid": info.get("bid"),
                "ask": info.get("ask"),
                "volume": info.get("volume"),
                "market_cap": info.get("marketCap"),
                "trailing_PE": info.get("trailingPE"),
                "forward_PE": info.get("forwardPE"),
                "price_to_book": info.get("priceToBook"),
                "dividend_yield": info.get("dividendYield"),
                "earnings_growth": info.get("earningsGrowth"),
                "revenue_growth": info.get("revenueGrowth"),
            }
            return self._sanitize_data(estimation_data)
        except Exception as e:
            logger.error(f"Error fetching estimation data for {ticker}: {str(e)}", exc_info=True)
            return {"error": str(e), "ticker": ticker}

    def get_resource_allocation_data(self, ticker: str) -> Dict[str, Any]:
        """
        Get resource-related data for a ticker.

        Args:
            ticker: The stock ticker symbol.

        Returns:
            A dictionary containing resource allocation data.
        """
        try:
            logger.info(f"Fetching resource allocation data for {ticker}")
            stock = yf.Ticker(ticker)
            info = stock.info

            resource_data = {
                "full_time_employees": info.get("fullTimeEmployees"),
                "company_summary": info.get("longBusinessSummary"),
                "industry": info.get("industry"),
                "sector": info.get("sector")
            }
            return self._sanitize_data(resource_data)
        except Exception as e:
            logger.error(f"Error fetching resource allocation data for {ticker}: {str(e)}", exc_info=True)
            return {"error": str(e), "ticker": ticker}
