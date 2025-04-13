import logging
from typing import Dict, Any, Optional, List

from prompts.prompt_cash_flow import CASH_FLOW_SYSTEM_PROMPT, get_cash_flow_human_prompt
from base_agent import BaseAgent

from tools.bing_search import bing_search
from tools.yahoo_finance import (
    yahoo_finance_market_data,
    yahoo_finance_financials,
    yahoo_market_sizing,
    yahoo_industry_peers
)

logger = logging.getLogger(__name__)


class CashFlowAgent(BaseAgent):
    """
    Agent responsible for generating cash flow projections.
    Leverages LangChain's agent executor with a structured prompt and output parser.
    """

    def get_tools(self) -> List:
        """
        Return tools for gathering industry and company-specific financial data.
        """
        logger.info("Registering tools with CashFlowAgent")
        return [
            bing_search,
            yahoo_finance_market_data,
            yahoo_finance_financials,
            yahoo_market_sizing,
            yahoo_industry_peers
        ]

    def get_system_prompt(self) -> str:
        """
        Return the system prompt defined in prompt_cash_flow.py.
        """
        return CASH_FLOW_SYSTEM_PROMPT

    def _format_input(
        self,
        project_name: str,
        project_description: str,
        industry: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Build the input prompt using the human prompt template.
        """
        logger.info(f"Creating cash flow prompt for project: {project_name} in industry: {industry}")
        return get_cash_flow_human_prompt(project_name, project_description, industry, additional_context)


def generate_cash_flow(
    project_name: str,
    project_description: str,
    industry: str,
    additional_context: Optional[str] = None,
    streaming: bool = False
) -> Dict[str, Any]:
    """
    Convenience function to generate a cash flow projection.
    Uses various tools to gather current market data and company-specific financials before projecting cash flows.

    Args:
        project_name (str): Name of the project.
        project_description (str): Description of the project.
        industry (str): Industry sector.
        additional_context (Optional[str]): Additional context.
        streaming (bool): Whether to stream output.

    Returns:
        Dict[str, Any]: The generated cash flow projection.
    """
    agent = CashFlowAgent(streaming=streaming)
    return agent.generate(project_name, project_description, industry, additional_context)
