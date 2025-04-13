import logging
from typing import Dict, Any, Optional, List

from base_agent import BaseAgent
from prompts.prompt_revenue_modeling import (
    REVENUE_MODELING_SYSTEM_PROMPT,
    get_revenue_modeling_prompt
)

# Example tool imports if they exist in your codebase:
from tools.bing_search import bing_search
from tools.yahoo_finance import (
    yahoo_finance_market_data,
    yahoo_finance_financials,
    yahoo_market_sizing,
    yahoo_industry_peers
)

logger = logging.getLogger(__name__)


class RevenueModelingAgent(BaseAgent):
    """
    Agent specialized in generating revenue modeling and pricing strategies.
    """

    def get_tools(self) -> List:
        """
        Return tools for gathering market data, competitor revenue patterns, and pricing benchmarks.
        """
        logger.info("Registering tools with RevenueModelingAgent")
        return [
            bing_search,
            yahoo_finance_market_data,
            yahoo_finance_financials,
            yahoo_market_sizing,
            yahoo_industry_peers
        ]

    def get_system_prompt(self) -> str:
        """
        Return the specialized system prompt for revenue modeling.
        """
        return REVENUE_MODELING_SYSTEM_PROMPT

    def _format_input(
        self,
        project_name: str,
        project_description: str,
        industry: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Format the input for the revenue modeling agent.

        Note:
          - project_description and industry are inherited from BaseAgent
            but not necessarily used here. Use them if relevant to add context.
        """
        logger.info(f"Creating revenue modeling prompt for project: {project_name}")
        return get_revenue_modeling_prompt(project_name, additional_context)


def generate_revenue_models(
    project_name: str,
    additional_context: Optional[str] = None,
    streaming: bool = False
) -> Dict[str, Any]:
    """
    Convenience function to generate multiple revenue models and a final recommendation.

    Args:
        project_name (str): Name of the project.
        additional_context (Optional[str]): Extra context or details for the modeling.
        streaming (bool): Whether to stream output.

    Returns:
        Dict[str, Any]: The generated revenue models and recommended strategy.
    """
    agent = RevenueModelingAgent(streaming=streaming)
    return agent.generate(
        project_name=project_name,
        project_description="",  # Not used, but required by BaseAgent
        industry="",            # Not used, but required by BaseAgent
        additional_context=additional_context
    )
