import logging
from typing import Dict, Any, Optional, List

from base_agent import BaseAgent
from prompt_cost_estimations import (
    SYSTEM_PROMPT_ESTIMATIONS,
    build_estimations_prompt
)

from tools.yahoo_finance import (
    yahoo_finance_market_data,
    yahoo_finance_financials,
    yahoo_market_sizing,
    yahoo_industry_peers
)

logger = logging.getLogger(__name__)

class EstimationsAgent(BaseAgent):
    """
    Agent specialized in generating cost estimations.
    It uses external data sources to gather market rates and relevant benchmarks.
    """

    def get_tools(self) -> List:
        """
        Returns a list of tools (functions) accessible by this agent for data gathering.
        Override if more tools are needed.
        """
        logger.info("Registering tools for EstimationsAgent.")
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
        return SYSTEM_PROMPT_ESTIMATIONS

    def _format_input(
        self,
        project_name: str,
        project_description: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Formats the agent input using the build_estimations_prompt function.

        Note:
            In this agent, 'project_description' is used as the 'date' parameter for
            the cost estimation. Modify as needed if a different approach is required.

        Args:
            project_name (str): The name of the project.
            project_description (str): Used here as the date for the estimation.
            additional_context (Optional[str]): Additional context or details.
        """
        logger.info(f"Formatting cost estimations prompt for project: {project_name}")
        # Adjust the expiration date as needed; here it's set to "N/A" for demonstration.
        return build_estimations_prompt(
            project_name=project_name,
            company_name="Example Company",
            company_address="1234 Example St, City, Country",
            date=project_description,
            expiration_date="N/A",
            additional_context=additional_context
        )

def generate_estimations(
    project_name: str,
    estimation_date: str,
    additional_context: Optional[str] = None,
    streaming: bool = False
) -> Dict[str, Any]:
    """
    Convenience function to instantiate an EstimationsAgent and generate cost estimations.

    Args:
        project_name (str): Name of the project.
        estimation_date (str): Date of the estimation (or project description).
        additional_context (Optional[str]): Additional context or details.
        streaming (bool): Whether the LLM should stream responses or not.

    Returns:
        Dict[str, Any]: Dictionary containing the generated output and metadata.
    """
    agent = EstimationsAgent(streaming=streaming)
    return agent.generate(project_name, estimation_date, additional_context)
