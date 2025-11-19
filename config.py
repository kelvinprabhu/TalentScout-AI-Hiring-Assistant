# File: config.py
"""Configuration settings for TalentScout application."""

import streamlit as st
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AppConfig:
    """Application configuration."""
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    TEMPERATURE: float = 0
    MAX_RETRIES: int = 2
    REPORTS_FOLDER: str = "Reports"
    
    # Required candidate information fields
    REQUIRED_FIELDS = [
        "full_name",
        "email",
        "phone_number",
        "years_of_experience",
        "desired_positions",
        "current_location",
        "tech_stack"
    ]


def initialize_session_state():
    """Initialize all session state variables."""
    defaults = {
        "messages": [],
        "chat_history": None,
        "candidate_info": {},
        "mode_selected": False,
        "input_mode": None,
        "resume_processed": False,
        "qa_pairs": [],
        "assessment_complete": False,
        "voice_enabled": False,
        "question_phase": False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
