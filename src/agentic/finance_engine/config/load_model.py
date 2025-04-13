import os
import logging
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import CallbackManager

logger = logging.getLogger(__name__)

load_dotenv()

# Load environment variables

def get_llm(streaming=False):
    callbacks = [StreamingStdOutCallbackHandler()] if streaming else None

    # Check if required env vars exist
    required_vars = ["AZURE_OPENAI_MODEL", "AZURE_OPENAI_BASE", "AZURE_OPENAI_KEY", "AZURE_OPENAI_VERSION"]
    for var in required_vars:
        if var not in os.environ:
            logger.error(f"Missing required environment variable: {var}")
            raise ValueError(f"Missing required environment variable: {var}")

    model_name = os.environ["AZURE_OPENAI_MODEL"].split(",")[1]
    logger.info(f"Using Azure OpenAI model: {model_name}")

    base_url = os.environ["AZURE_OPENAI_BASE"]
    if not base_url.endswith("/"):
        base_url += "/"
    base_url += "openai/deployments/"

    logger.info(f"Using Azure endpoint: {base_url}")

    try:
        llm = AzureChatOpenAI(
            openai_api_key=os.environ["AZURE_OPENAI_KEY"],
            openai_api_base=base_url,
            deployment_name=os.environ["AZURE_OPENAI_MODEL"],
            openai_api_type="azure",
            openai_api_version=os.environ["AZURE_OPENAI_VERSION"],
            streaming=streaming,
            callbacks=callbacks,
            request_timeout=300,
        )
        return llm

    except Exception as ex:
        logger.error(f"Error initializing Azure OpenAI: {str(ex)}")
        raise
