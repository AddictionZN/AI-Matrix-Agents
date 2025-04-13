from abc import ABC, abstractmethod
import logging
from typing import Dict, Any, Optional, List

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import BaseTool

from config.load_model import get_llm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base Agent class for financial analysis requests.
    Provides a common interface for generating outputs using LangChain agents
    and enforces structured input formatting.
    """

    def __init__(self, streaming: bool = False):
        self.streaming = streaming
        self.agent_executor = self._create_agent()

    def _create_agent(self) -> AgentExecutor:
        """
        Create an AgentExecutor with the language model, tools, and prompt.
        """
        llm = get_llm(streaming=self.streaming)
        tools = self.get_tools()
        system_prompt = self.get_system_prompt()

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

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
        Return a list of tools available to the agent.
        Override in subclass as needed.
        """
        return []

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Return the system prompt for the agent.
        """
        raise NotImplementedError

    @abstractmethod
    def _format_input(
        self,
        project_name: str,
        project_description: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Format the input prompt for the agent.

        Args:
            project_name (str): Name of the project.
            project_description (str): Brief description of the project.
            additional_context (Optional[str]): Extra context details.

        Returns:
            str: Formatted input string.
        """
        raise NotImplementedError

    def generate(
        self,
        project_name: str,
        project_description: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate an output based on the project details.

        Args:
            project_name (str): Name of the project.
            project_description (str): Project description.
            additional_context (Optional[str]): Supplementary context in string format.

        Returns:
            Dict[str, Any]: Dictionary with generated output and additional info.
        """
        try:
            agent_input = self._format_input(project_name, project_description, additional_context)
            logger.info(f"Generating output for project: {project_name}")
            result = self.agent_executor.invoke({"input": agent_input})
            output = result.get("output", "")
            return self._prepare_response(project_name, output, result, success=True)
        except Exception as e:
            logger.error(f"Error generating output: {str(e)}", exc_info=True)
            return self._prepare_error_response(project_name, str(e))

    def _prepare_response(
        self,
        project_name: str,
        output: str,
        result: Dict[str, Any],
        success: bool
    ) -> Dict[str, Any]:
        """
        Prepare a successful response.
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
        """
        return {
            "project_name": project_name,
            "output": "An error occurred during generation.",
            "success": False,
            "error": error,
        }
