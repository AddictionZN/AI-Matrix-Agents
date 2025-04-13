import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import BaseTool

from config.load_model import get_llm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base Agent class that defines common interfaces and shared functionality for all financial analysis agents.
    """

    def __init__(self, streaming: bool = False):
        """
        Initialize the base agent with common parameters.

        Args:
            streaming (bool): Whether to stream output.
        """
        self.streaming = streaming
        self.agent_executor = self._create_agent()

    def _create_agent(self) -> AgentExecutor:
        """
        Create the agent executor with appropriate tools and prompts.
        Child classes can override parts of the agent creation process if needed.

        Returns:
            AgentExecutor: The agent executor instance.
        """
        # Initialize the language model.
        llm = get_llm(streaming=self.streaming)

        # Get tools and system prompt from the child class.
        tools = self.get_tools()
        system_prompt = self.get_system_prompt()

        # Build a prompt following LangChain best practices.
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Create and return the agent executor.
        agent = create_openai_tools_agent(llm, tools, prompt)
        return AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=4,
            early_stopping_method="generate",
            return_intermediate_steps=True
        )

    def get_tools(self) -> List[BaseTool]:
        """
        Return the list of tools to be used by the agent.

        Returns:
            List[BaseTool]: A list of BaseTool instances (empty by default).
        """
        return []

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for the agent.

        Returns:
            str: The system prompt as a string.
        """
        raise NotImplementedError

    @abstractmethod
    def _format_input(
        self,
        project_name: str,
        project_description: str,
        industry: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Format the input for the agent task.

        Args:
            project_name (str): Name of the project.
            project_description (str): Description of the project.
            industry (str): Industry sector.
            additional_context (Optional[str]): Extra context information.

        Returns:
            str: A formatted input string.
        """
        raise NotImplementedError

    def generate(
        self,
        project_name: str,
        project_description: str,
        industry: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate output based on the provided project information.

        Args:
            project_name (str): Name of the project.
            project_description (str): Description of the project.
            industry (str): Industry sector.
            additional_context (Optional[str]): Extra context to consider.

        Returns:
            Dict[str, Any]: A dictionary containing the generated output.
        """
        try:
            # Format the agent's input.
            agent_input = self._format_input(
                project_name, project_description, industry, additional_context
            )
            logger.info(f"Generating output for project: {project_name}")
            result = self.agent_executor.invoke({"input": agent_input})
            output = result.get("output", "")
            return self._prepare_response(
                project_name=project_name,
                output=output,
                result=result,
                success=True
            )
        except Exception as e:
            logger.error(f"Error generating output: {str(e)}", exc_info=True)
            return self._prepare_error_response(
                project_name=project_name, error=str(e)
            )

    def _prepare_response(
        self,
        project_name: str,
        output: str,
        result: Dict[str, Any],
        success: bool
    ) -> Dict[str, Any]:
        """
        Prepare a successful response.

        Args:
            project_name (str): Name of the project.
            output (str): Generated output.
            result (Dict[str, Any]): Full result including intermediate steps.
            success (bool): Indicator of success.

        Returns:
            Dict[str, Any]: A dictionary containing the response.
        """
        intermediate_steps = result.get("intermediate_steps", []) if self.streaming else None
        return {
            "project_name": project_name,
            "output": output,
            "success": success,
            "intermediate_steps": intermediate_steps,
        }

    def _prepare_error_response(self, project_name: str, error: str) -> Dict[str, Any]:
        """
        Prepare an error response.

        Args:
            project_name (str): Name of the project.
            error (str): Error message.

        Returns:
            Dict[str, Any]: A dictionary containing the error response.
        """
        return {
            "project_name": project_name,
            "output": "An error occurred during generation.",
            "success": False,
            "error": error,
        }
