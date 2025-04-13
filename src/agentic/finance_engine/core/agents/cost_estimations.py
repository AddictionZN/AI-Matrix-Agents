import logging
from typing import Dict, Any, Optional, List

from prompts.prompt_cost_estatimations import ESTIMATIONS_SYSTEM_PROMPT, get_estimations_human_prompt
from base_agent import BaseAgent

from tools.yahoo_finance import (
    yahoo_finance_market_data,
    yahoo_finance_financials,
    yahoo_market_sizing,
    yahoo_industry_peers
)

logger = logging.getLogger(__name__)


class EstimationsAgent(BaseAgent):
    """
    Agent responsible for generating cost estimations using a structured JSON approach.
    Inherits from BaseAgent and provides the specialized system prompt and input formatting.
    """

    def get_tools(self) -> List:
        """
        Return a list of tools used for gathering market pricing data and financial information.
        
        Returns:
            List: A list of tool instances.
        """
        logger.info("Registering tools with EstimationsAgent")
        return [
            yahoo_finance_market_data,
            yahoo_finance_financials,
            yahoo_market_sizing,
            yahoo_industry_peers
        ]

    def get_system_prompt(self) -> str:
        """
        Return the specialized system prompt for generating cost estimations.

        Returns:
            str: The system prompt.
        """
        return ESTIMATIONS_SYSTEM_PROMPT

    def _format_input(
        self,
        project_name: str,
        project_description: str,
        industry: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Create the final string prompt that the agent will process.

        Note:
            For consistency with BaseAgent, we receive 'project_description' and 'industry' parameters.
            Here, we treat:
              - 'project_description' as the estimate date.
              - 'industry' as the expiration date of the estimate.

        Args:
            project_name (str): Name of the project.
            project_description (str): The estimate date.
            industry (str): The expiration date.
            additional_context (Optional[str]): Additional context for the estimation.

        Returns:
            str: The formatted prompt for cost estimation.
        """
        date_str = project_description  # Estimate date
        expiration_date_str = industry   # Expiration date
        logger.info(f"Creating estimation prompt for project: {project_name}")
        return get_estimations_human_prompt(
            project_name=project_name,
            date=date_str,
            expiration_date=expiration_date_str,
            additional_context=additional_context
        )

def generate_estimations(
    project_name: str,
    date: str,
    expiration_date: str,
    additional_context: Optional[str] = None,
    streaming: bool = False
) -> Dict[str, Any]:
    """
    Convenience function to generate a cost estimation.

    The BaseAgent expects the following parameters:
      - project_name
      - project_description (mapped to date)
      - industry (mapped to expiration_date)
      - additional_context

    Args:
        project_name (str): Name of the project.
        date (str): Date of the estimate (mapped as project_description).
        expiration_date (str): Expiration date of the estimate (mapped as industry).
        additional_context (Optional[str]): Extra context or details.
        streaming (bool): Whether to stream the output.

    Returns:
        Dict[str, Any]: The generated cost estimation.
    """
    logger.info(f"Generating estimation for project: {project_name}")
    agent = EstimationsAgent(streaming=streaming)
    return agent.generate(
        project_name=project_name,
        project_description=date,
        industry=expiration_date,
        additional_context=additional_context
    )
