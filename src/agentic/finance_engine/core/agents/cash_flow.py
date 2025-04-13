import logging
from typing import Dict, Any, Optional, List

from base_agent import BaseAgent
from prompt_cash_flow import (
    SYSTEM_PROMPT_CASH_FLOW,
    build_cash_flow_prompt
)

# Example imports for tools; adjust as needed.
from tools.yahoo_finance import (
    yahoo_finance_market_data,
    yahoo_finance_financials,
    yahoo_market_sizing,
    yahoo_industry_peers
)

logger = logging.getLogger(__name__)

class CashFlowAgent(BaseAgent):
    """
    An agent specialized in generating cash flow projections.
    It uses external data sources to enrich the analysis.
    """

    def get_tools(self) -> List:
        """
        Returns a list of tools (functions) accessible by this agent for data gathering.
        Override if more tools are needed.
        """
        logger.info("Registering tools for CashFlowAgent.")
        return [
            yahoo_finance_market_data,
            yahoo_finance_financials,
            yahoo_market_sizing,
            yahoo_industry_peers
        ]

    def get_system_prompt(self) -> str:
        """
        Returns the system prompt guiding the LLM in producing the desired output.
        """
        return SYSTEM_PROMPT_CASH_FLOW

    def _format_input(
        self,
        project_name: str,
        project_description: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Formats the agent input using the build_cash_flow_prompt function.

        Args:
            project_name (str): The name of the project.
            project_description (str): Description of the project.
            additional_context (Optional[str]): Additional context or details.
        """
        logger.info(f"Formatting cash flow prompt for project: {project_name}")
        return build_cash_flow_prompt(
            project_name,
            project_description,
            additional_context
        )

def generate_cash_flow(
    project_name: str,
    project_description: str,
    additional_context: Optional[str] = None,
    streaming: bool = False
) -> Dict[str, Any]:
    """
    Convenience function to instantiate a CashFlowAgent and generate a cash flow projection.

    Args:
        project_name (str): Name of the project.
        project_description (str): A brief description of the project.
        additional_context (Optional[str]): Additional context details for the analysis.
        streaming (bool): Whether the LLM should stream responses or not.

    Returns:
        Dict[str, Any]: Dictionary containing the generated output and metadata.
    """
    agent = CashFlowAgent(streaming=streaming)
    return agent.generate(project_name, project_description, additional_context)
