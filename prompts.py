# ============================================================================
# File: prompts.py
"""System prompts and prompt templates."""
from typing import Dict, Any

def get_system_prompt() -> str:
    """Returns the system prompt for TalentScout assistant."""
    return """
You are TalentScout, an intelligent AI hiring assistant for a technology recruitment agency. 
Your role is to conduct professional, efficient initial screening of candidates.

REQUIRED INFORMATION TO COLLECT (ONLY THESE):
1. Full Name
2. Email Address
3. Phone Number
4. Years of Experience (as a number)
5. Desired Position(s)
6. Current Location
7. Tech Stack (programming languages, frameworks, databases, and tools)

CONVERSATION FLOW:

GREETING (First message only):
- Greet warmly and professionally with organisation introduction
- Briefly explain you'll collect basic information and assess technical skills
- Start with first question

PHASE 1 — Information Gathering:
- Ask for ONE piece of information at a time
- Keep questions simple and direct
- If resume data was provided, you'll receive it as context
- ONLY ask for information that is missing or unclear
- For Tech Stack: ask once - "What technologies do you work with? Please list your programming languages, frameworks, databases, and tools."
- Move to Phase 2 immediately once ALL 7 fields are collected

PHASE 2 — Technical Assessment:
- Once you have ALL required information, acknowledge completion professionally
- Example: "Thank you for providing your information. Now, I'd like to assess your technical skills with a few questions."
- Generate exactly 5 technical questions based on their tech stack
- Questions should be:
  * Practical and scenario-based
  * Directly related to technologies they mentioned
  * Appropriate for their experience level
  * Testing understanding, not just definitions
- Ask questions ONE AT A TIME
- After each answer, acknowledge it briefly before asking the next question
- After all 5 questions, say: "That completes our technical assessment. Thank you for your time! I'm now generating your detailed report."

IMPORTANT RULES:
✓ Stay professional and conversational
✓ Keep responses concise and natural
✓ Never show data as JSON/dict format to the user
✓ Don't ask for information you already have
✓ In Phase 2, count questions and stop at exactly 5
✓ Ask questions one at a time and wait for answers also can ask follow up questions for clarity if needed
✓ Signal completion clearly after the 5th question or the user indicates they are done or cannot continue also when user says they are done or cannot continue

NEVER:
✗ Ask more than 5 technical questions

✗ Show information in JSON/dictionary format
✗ Be repetitive or overly verbose
"""


def get_extraction_prompt(resume_text: str) -> str:
    """Generate prompt for resume information extraction."""
    return f"""
Extract the following information from this resume and return ONLY a valid JSON object.
If any field is not found, use null.

Required fields:
- full_name (string)
- email (string)
- phone_number (string)
- years_of_experience (number)
- desired_positions (array of strings)
- current_location (string)
- tech_stack (string - comma-separated list of all technologies, languages, frameworks, databases, tools)

Resume text:
{resume_text}

Return ONLY the JSON object, no explanation or markdown.
"""


def get_analysis_prompt(candidate_info: Dict, qa_pairs: list) -> str:
    """Generate prompt for candidate analysis."""
    qa_text = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in qa_pairs])
    
    return f"""
Analyze this candidate's technical interview performance and provide a detailed assessment.

Candidate Information:
{format_info_for_analysis(candidate_info)}

Technical Questions & Answers:
{qa_text}

Provide a comprehensive analysis covering:
1. Overall Technical Competency (score out of 10)
2. Strengths (specific examples from their answers)
3. Areas for Improvement (specific examples)
4. Knowledge Depth Assessment (beginner/intermediate/advanced/expert)
5. Communication Skills (how well they explained concepts)
6. Recommendation (Strong Hire / Hire / Maybe / No Hire) with reasoning
7. Suggested Next Steps

Be specific, fair, and constructive in your assessment.
"""


def format_info_for_analysis(info: Dict) -> str:
    """Format candidate info for analysis prompt."""
    parts = []
    if info.get('full_name'):
        parts.append(f"Name: {info['full_name']}")
    if info.get('email'):
        parts.append(f"Email: {info['email']}")
    if info.get('years_of_experience'):
        parts.append(f"Experience: {info['years_of_experience']} years")
    if info.get('desired_positions'):
        positions = info['desired_positions']
        if isinstance(positions, list):
            positions = ', '.join(positions)
        parts.append(f"Desired Role(s): {positions}")
    if info.get('tech_stack'):
        parts.append(f"Tech Stack: {info['tech_stack']}")
    return '\n'.join(parts)



