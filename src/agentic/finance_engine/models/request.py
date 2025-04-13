from agentic.finance_engine.shared.base_scheme import BaseFinancialRequest


class CashFlowRequest(BaseFinancialRequest):
    """Request model for cash flow analysis."""
    pass


class EstimationsRequest(BaseFinancialRequest):
    """Request model for cost estimations."""
    pass


class FinancialAnalysisRequest(BaseFinancialRequest):
    """Request model for comprehensive financial statements."""
    pass
