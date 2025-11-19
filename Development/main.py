import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
import pdfplumber
import re
import json
from typing import Dict, Any, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = InMemoryChatMessageHistory()
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {}
if "mode_selected" not in st.session_state:
    st.session_state.mode_selected = False
if "input_mode" not in st.session_state:
    st.session_state.input_mode = None
if "resume_processed" not in st.session_state:
    st.session_state.resume_processed = False

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

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


def initialize_llm(api_key: str) -> ChatGroq:
    """Initialize the ChatGroq LLM with given API key."""
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=api_key,
    )


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
- Greet warmly and professionally
- Briefly explain you'll collect basic information and assess technical skills
- Start with first question

PHASE 1 — Information Gathering:
- Ask for ONE piece of information at a time
- Keep questions simple and direct
- If resume data was provided, you'll receive it as context
- ONLY ask for information that is missing or unclear
- For Tech Stack: ask once - "What technologies do you work with? Please list your programming languages, frameworks, databases, and tools."
- Move to Phase 2 immediately once ALL 7 fields are collected
- NEVER present information as JSON or dictionaries - always use natural, professional language

PHASE 2 — Technical Assessment:
- Once you have ALL required information, acknowledge completion professionally
- Example: "Thank you for providing your information. Now, I'd like to assess your technical skills with a few questions."
- Generate exactly 3-5 technical questions based on their tech stack
- Questions should be:
  * Practical and scenario-based
  * Directly related to technologies they mentioned
  * Appropriate for their experience level
  * Testing understanding, not just definitions
  
Example questions:
- Python: "Can you explain the difference between lists and tuples, and when you'd use each?"
- Django: "How do you handle database migrations in Django when working in a team?"
- React: "What's your approach to state management in larger React applications?"
- AWS: "Which AWS services have you used, and can you describe a project where you implemented them?"

IMPORTANT RULES:
✓ Stay professional and conversational
✓ Keep responses concise and natural
✓ Never show data as JSON/dict format to the user
✓ Don't ask for information you already have
✓ Don't ask unnecessary follow-up questions
✓ When presenting collected info, use natural language:
  Example: "Great! I've noted that you're [Name], with [X] years of experience, looking for [Position] roles in [Location]. You work with [Technologies]."
✓ Don't repeat or summarize tech stack unnecessarily
✓ Stay focused on the hiring screening purpose
✓ Exit gracefully when user says: "bye", "exit", "quit", or "stop"

NEVER:
✗ Ask for overly detailed technical breakdowns upfront
✗ Request information beyond the 7 required fields
✗ Show information in JSON/dictionary format
✗ Be repetitive or overly verbose
✗ Deviate from recruitment purpose
"""


def create_chain(llm):
    """Create the LangChain conversation chain."""
    system_prompt = get_system_prompt()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("history"),
        ("human", "{input}")
    ])
    
    chain = prompt | llm
    
    langmem_chain = RunnableWithMessageHistory(
        chain,
        lambda session_id: st.session_state.chat_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    
    return langmem_chain


def extract_info_from_resume(resume_text: str, llm) -> Dict[str, Any]:
    """
    Use LLM to extract structured candidate information from resume text.
    """
    extraction_prompt = f"""
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
    
    response = llm.invoke([{"role": "user", "content": extraction_prompt}])
    
    try:
        content = response.content
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            extracted_data = json.loads(json_match.group())
            return extracted_data
        else:
            return {}
    except Exception as e:
        st.error(f"Error extracting information: {str(e)}")
        return {}


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
            # Flatten nested tech stack
            all_tech = []
            for category, items in tech.items():
                if isinstance(items, list):
                    all_tech.extend(items)
                else:
                    all_tech.append(str(items))
            tech = ', '.join(all_tech)
        parts.append(f"Tech Stack: {tech}")
    
    return '\n'.join(parts)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.set_page_config(
        page_title="TalentScout - AI Hiring Assistant",
        page_icon="🎯",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1E88E5;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #666;
            text-align: center;
            margin-bottom: 2rem;
        }
        .info-box {
            background-color: #E3F2FD;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .stButton>button {
            width: 100%;
            background-color: #1E88E5;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">🎯 TalentScout</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Hiring Assistant</div>', unsafe_allow_html=True)
    
    # Sidebar for API Key
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("Groq API Key", type="password", help="Enter your Groq API key")
        
        if api_key:
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Please enter your Groq API key")
        
        st.markdown("---")
        st.markdown("### 📋 Information Collected")
        if st.session_state.candidate_info:
            for key, value in st.session_state.candidate_info.items():
                if value:
                    # Format key nicely
                    formatted_key = key.replace('_', ' ').title()
                    # Format value
                    if isinstance(value, list):
                        formatted_value = ', '.join(str(v) for v in value)
                    elif isinstance(value, dict):
                        formatted_value = ', '.join(str(v) for items in value.values() for v in (items if isinstance(items, list) else [items]))
                    else:
                        formatted_value = str(value)
                    st.write(f"**{formatted_key}:** {formatted_value}")
        else:
            st.info("No information collected yet")
        
        st.markdown("---")
        if st.button("🔄 Reset Conversation"):
            st.session_state.messages = []
            st.session_state.chat_history = InMemoryChatMessageHistory()
            st.session_state.candidate_info = {}
            st.session_state.mode_selected = False
            st.session_state.input_mode = None
            st.session_state.resume_processed = False
            st.rerun()
    
    if not api_key:
        st.warning("👈 Please enter your Groq API Key in the sidebar to continue")
        return
    
    # Initialize LLM
    llm = initialize_llm(api_key)
    chain = create_chain(llm)
    
    # Mode Selection
    if not st.session_state.mode_selected:
        st.markdown("### 👋 Welcome! How would you like to proceed?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class="info-box">
                    <h4>💬 Chat Mode</h4>
                    <p>Answer questions interactively through a conversational interface</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Start Chat", key="chat_mode"):
                st.session_state.mode_selected = True
                st.session_state.input_mode = "chat"
                # Add initial greeting
                greeting = "Hello! I'm TalentScout, your AI hiring assistant. I'll help you through our initial screening process by collecting some basic information and assessing your technical skills. Let's get started!\n\nWhat's your full name?"
                st.session_state.messages.append({"role": "assistant", "content": greeting})
                st.rerun()
        
        with col2:
            st.markdown("""
                <div class="info-box">
                    <h4>📄 Resume Upload</h4>
                    <p>Upload your resume and let AI extract your information automatically</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Upload Resume", key="resume_mode"):
                st.session_state.mode_selected = True
                st.session_state.input_mode = "resume"
                st.rerun()
    
    # Resume Upload Mode
    elif st.session_state.input_mode == "resume" and not st.session_state.resume_processed:
        st.markdown("### 📄 Upload Your Resume")
        
        uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
        
        if uploaded_file is not None:
            with st.spinner("🔍 Analyzing your resume..."):
                # Extract text from resume
                resume_text = extract_clean_resume_text(uploaded_file)
                
                # Use LLM to extract structured information
                extracted_info = extract_info_from_resume(resume_text, llm)
                
                if extracted_info:
                    st.session_state.candidate_info = extracted_info
                    st.success("✅ Resume processed successfully!")
                    
                    # Prepare initial message with extracted info in natural language
                    info_natural = format_candidate_info_natural(extracted_info)
                    
                    greeting = f"""Hello! I'm TalentScout, your AI hiring assistant. I've analyzed your resume and extracted the following information:

{info_natural}

Let me verify if I have everything I need, and I'll ask for any missing details."""
                    
                    st.session_state.messages.append({"role": "assistant", "content": greeting})
                    st.session_state.resume_processed = True
                    
                    st.rerun()
                else:
                    st.error("❌ Could not extract information from resume. Please try chat mode instead.")
    
    # Chat Interface
    if st.session_state.mode_selected:
        st.markdown("### 💬 Conversation")
        
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Special handling for resume mode first verification
        if st.session_state.input_mode == "resume" and st.session_state.resume_processed and len(st.session_state.messages) == 1:
            info_natural = format_candidate_info_natural(st.session_state.candidate_info)
            
            initial_query = f"""
I have extracted the following information from the candidate's resume:

{info_natural}

Please review this information and:
1. Check if ALL 7 required fields are present (Full Name, Email, Phone Number, Years of Experience, Desired Position(s), Current Location, Tech Stack)
2. If anything is missing or unclear, ask for it naturally and professionally
3. If everything is complete, acknowledge it professionally and move to technical questions
4. DO NOT show the information as JSON or dictionary format
5. Be conversational and natural

Start your response directly.
"""
            
            with st.spinner("Reviewing information..."):
                response = chain.invoke(
                    {"input": initial_query},
                    config={"configurable": {"session_id": "user_session"}}
                )
                
                assistant_message = response.content
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                st.rerun()
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Check for exit keywords
            if prompt.lower() in ["bye", "exit", "quit", "stop"]:
                farewell = "Thank you for your time! Your information has been recorded. Our recruitment team will review your profile and get back to you within 2-3 business days. Have a great day! 👋"
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.messages.append({"role": "assistant", "content": farewell})
                st.rerun()
            
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Get response from LLM
            with st.spinner("Thinking..."):
                response = chain.invoke(
                    {"input": prompt},
                    config={"configurable": {"session_id": "user_session"}}
                )
                
                assistant_message = response.content
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            
            st.rerun()


if __name__ == "__main__":
    main()