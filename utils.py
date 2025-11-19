# ============================================================================
# File: utils.py
"""Utility functions for file processing and data formatting."""
from typing import Dict, Any

import pdfplumber
import re
import json
from typing import Dict, Any
from datetime import datetime


def extract_clean_resume_text(pdf_file) -> str:
    """
    Extracts and cleans text from an uploaded PDF resume.
    
    :param pdf_file: Streamlit UploadedFile object
    :return: Cleaned resume text as a string
    """
    raw_text = ""
    
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                raw_text += "\n" + txt
    
    # Cleaning
    cleaned = raw_text
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.replace("•", ", ").replace("●", ", ").replace("▪", ", ")
    cleaned = re.sub(r'\s+([.,!?])', r'\1', cleaned)
    cleaned = cleaned.strip()
    
    return cleaned


def format_candidate_info_natural(info: Dict) -> str:
    """Convert candidate info dict to natural language."""
    parts = []
    
    if info.get('full_name'):
        parts.append(f"Name: {info['full_name']}")
    if info.get('email'):
        parts.append(f"Email: {info['email']}")
    if info.get('phone_number'):
        parts.append(f"Phone: {info['phone_number']}")
    if info.get('years_of_experience'):
        parts.append(f"Experience: {info['years_of_experience']} years")
    if info.get('desired_positions'):
        positions = info['desired_positions']
        if isinstance(positions, list):
            positions = ', '.join(positions)
        parts.append(f"Desired Role(s): {positions}")
    if info.get('current_location'):
        parts.append(f"Location: {info['current_location']}")
    if info.get('tech_stack'):
        tech = info['tech_stack']
        if isinstance(tech, dict):
            all_tech = []
            for category, items in tech.items():
                if isinstance(items, list):
                    all_tech.extend(items)
                else:
                    all_tech.append(str(items))
            tech = ', '.join(all_tech)
        parts.append(f"Tech Stack: {tech}")
    
    return '\n'.join(parts)


def generate_filename(candidate_name: str, extension: str) -> str:
    """Generate filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r'[^\w\s-]', '', candidate_name).strip().replace(' ', '_')
    return f"{safe_name}_{timestamp}.{extension}"


def parse_json_from_response(content: str) -> Dict:
    """Extract JSON object from LLM response."""
    try:
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {}
    except Exception:
        return {}

