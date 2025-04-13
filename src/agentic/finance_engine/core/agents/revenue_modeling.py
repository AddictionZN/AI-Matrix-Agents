import logging
from typing import Dict, Any, Optional, List

from base_agent import BaseAgent
from prompts.prompt_revenue_modeling import (
    REVENUE_MODELING_SYSTEM_PROMPT,
    get_revenue_modeling_prompt
)

# Example data-gathering tools; replace or extend as needed.
from tools.yahoo_finance import (
    yahoo_finance_market_data,
    yahoo_finance_financials,
    yahoo_market_sizing,
    yahoo_industry_peers
)

logger = logging.getLogger(__name__)

class RevenueModelingAgent(BaseAgent):
    """
    Agent specialized in generating revenue models, pricing strategies,
    and selecting a recommended strategy for a given project.
    """

    def get_tools(self) -> List:
        """
        Returns a list of data-gathering tools for market analysis and competitor research.
        """
        logger.info("Registering tools for RevenueModelingAgent.")
        return [
            yahoo_finance_market_data,
            yahoo_finance_financials,
            yahoo_market_sizing,
            yahoo_industry_peers
        ]

    def get_system_prompt(self) -> str:
        """
        The system prompt instructing the LLM on how to build revenue models.
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
        Format the prompt input. BaseAgent requires these parameters,
        but project_description and industry may not be used if not needed.
        """
        logger.info(f"Creating revenue modeling prompt for project: {project_name}.")
        return get_revenue_modeling_prompt(project_name, additional_context)

def generate_revenue_models(
    project_name: str,
    additional_context: Optional[str] = None,
    streaming: bool = False
) -> Dict[str, Any]:
    """
    High-level function to create revenue models for the specified project.

    Args:
        project_name (str): The name of the project.
        additional_context (Optional[str]): Additional context or instructions.
        streaming (bool): Whether to stream the model's output.

    Returns:
        Dict[str, Any]: A dictionary containing the generated revenue models, recommendation, etc.
    """
    agent = RevenueModelingAgent(streaming=streaming)
    return agent.generate(
        project_name=project_name,
        project_description="",
        industry="",
        additional_context=additional_context
    )
