# ============================================================================
# File: llm_handler.py
"""LLM initialization and chain creation."""
from typing import Dict, Any

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from config import AppConfig


def initialize_llm(api_key: str) -> ChatGroq:
    """Initialize the ChatGroq LLM with given API key."""
    config = AppConfig()
    return ChatGroq(
        model=config.MODEL_NAME,
        temperature=config.TEMPERATURE,
        max_tokens=None,
        timeout=None,
        max_retries=config.MAX_RETRIES,
        api_key=api_key,
    )


def create_chain(llm, chat_history):
    """Create the LangChain conversation chain."""
    from prompts import get_system_prompt
    
    system_prompt = get_system_prompt()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("history"),
        ("human", "{input}")
    ])
    
    chain = prompt | llm
    
    langmem_chain = RunnableWithMessageHistory(
        chain,
        lambda session_id: chat_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    
    return langmem_chain


def extract_info_from_resume(resume_text: str, llm) -> Dict[str, Any]:
    """Use LLM to extract structured candidate information from resume text."""
    from prompts import get_extraction_prompt
    
    extraction_prompt = get_extraction_prompt(resume_text)
    response = llm.invoke([{"role": "user", "content": extraction_prompt}])
    
    from utils import parse_json_from_response
    return parse_json_from_response(response.content)


def generate_candidate_analysis(candidate_info: Dict, qa_pairs: list, llm) -> str:
    """Generate detailed analysis of candidate performance."""
    from prompts import get_analysis_prompt
    
    analysis_prompt = get_analysis_prompt(candidate_info, qa_pairs)
    response = llm.invoke([{"role": "user", "content": analysis_prompt}])
    
    return response.content
