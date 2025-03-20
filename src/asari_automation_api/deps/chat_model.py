from langchain_core.language_models import BaseChatModel
from langchain_groq import ChatGroq


def get_chat_model() -> BaseChatModel:
    return ChatGroq(model="llama3-70b-8192")
