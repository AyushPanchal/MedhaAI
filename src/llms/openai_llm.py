from langchain_openai import ChatOpenAI
from src.config.settings import OPENAI_API_KEY


def get_openai_chat_model(model: str = "gpt-3.5-turbo", temperature: float = 0.1) -> ChatOpenAI:
    """
    Returns a configured ChatOpenAI model instance.
    
    Args:
        model (str): The OpenAI model to use (e.g., 'gpt-4o', 'gpt-3.5-turbo').
        temperature (float): Sampling temperature.
    
    Returns:
        ChatOpenAI: A ready-to-use LangChain ChatOpenAI object.
    """
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=OPENAI_API_KEY,
    )
