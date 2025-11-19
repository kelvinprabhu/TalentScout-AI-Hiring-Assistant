# ============================================================================
# File: main.py (app.py)
"""Main Streamlit application."""
from typing import Dict, Any

import streamlit as st
from langchain_core.chat_history import InMemoryChatMessageHistory
from config import initialize_session_state, AppConfig
from llm_handler import initialize_llm, create_chain, extract_info_from_resume, generate_candidate_analysis
from utils import extract_clean_resume_text, format_candidate_info_natural
from voice_handler import get_voice_input
from report_generator import generate_reports
import re


def detect_assessment_complete(message: str) -> bool:
    """Detect if the assessment has been completed based on LLM response."""
    completion_phrases = [
        "that completes our technical assessment",
        "thank you for your time",
        "generating your detailed report",
        "concludes our technical assessment",
        "finished with the technical questions",
        "completed the assessment"
    ]
    
    message_lower = message.lower()
    return any(phrase in message_lower for phrase in completion_phrases)


def detect_question_in_message(message: str) -> bool:
    """Detect if message contains a question."""
    # Check for question mark
    if '?' in message:
        return True
    
    # Check for question keywords
    question_starters = ['what', 'how', 'why', 'when', 'where', 'can you', 'could you', 'would you', 'explain', 'describe', 'tell me']
    message_lower = message.lower()
    
    return any(message_lower.strip().startswith(starter) for starter in question_starters)


def main():
    st.set_page_config(
        page_title="TalentScout - AI Hiring Assistant",
        page_icon="🎯",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
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
        .success-box {
            background-color: #C8E6C9;
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
    
    # Sidebar
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
                    formatted_key = key.replace('_', ' ').title()
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
        
        # Voice input toggle (only show during question phase)
        if st.session_state.question_phase:
            st.markdown("### 🎤 Voice Input")
            voice_enabled = st.checkbox("Enable Voice Input", value=st.session_state.voice_enabled)
            st.session_state.voice_enabled = voice_enabled
            
            if voice_enabled:
                st.info("💡 Voice input is active during technical questions")
        
        st.markdown("---")
        if st.button("🔄 Reset Conversation"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    if not api_key:
        st.warning("👈 Please enter your Groq API Key in the sidebar to continue")
        return
    
    # Initialize LLM and chain
    if st.session_state.chat_history is None:
        st.session_state.chat_history = InMemoryChatMessageHistory()
    
    llm = initialize_llm(api_key)
    chain = create_chain(llm, st.session_state.chat_history)
    
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
                resume_text = extract_clean_resume_text(uploaded_file)
                extracted_info = extract_info_from_resume(resume_text, llm)
                
                if extracted_info:
                    st.session_state.candidate_info = extracted_info
                    st.success("✅ Resume processed successfully!")
                    
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
    if st.session_state.mode_selected and not st.session_state.assessment_complete:
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
                
                # Check if question phase started
                if "technical" in assistant_message.lower() and "question" in assistant_message.lower():
                    st.session_state.question_phase = True
                
                st.rerun()
        
        # Chat input with voice option
        user_input = None
        
        # Voice input during question phase
        if st.session_state.question_phase and st.session_state.voice_enabled:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                text_input = st.chat_input("Type your answer or use voice input...")
            
            with col2:
                if st.button("🎤 Record Voice", use_container_width=True):
                    with st.spinner("Recording..."):
                        voice_text = get_voice_input(duration=15)
                        if voice_text:
                            st.success(f"Transcribed: {voice_text}")
                            user_input = voice_text
            
            if text_input:
                user_input = text_input
        else:
            # Regular text input
            user_input = st.chat_input("Type your message here...")
        
        if user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Store Q&A if in question phase
            if st.session_state.question_phase and len(st.session_state.messages) >= 2:
                last_assistant_msg = None
                for msg in reversed(st.session_state.messages[:-1]):
                    if msg["role"] == "assistant":
                        last_assistant_msg = msg["content"]
                        break
                
                if last_assistant_msg and detect_question_in_message(last_assistant_msg):
                    st.session_state.qa_pairs.append({
                        "question": last_assistant_msg,
                        "answer": user_input
                    })
            
            # Get response from LLM
            with st.spinner("Thinking..."):
                response = chain.invoke(
                    {"input": user_input},
                    config={"configurable": {"session_id": "user_session"}}
                )
                
                assistant_message = response.content
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
                # Detect if entering question phase
                if not st.session_state.question_phase:
                    if "technical" in assistant_message.lower() and "question" in assistant_message.lower():
                        st.session_state.question_phase = True
                
                # Detect if assessment is complete
                if detect_assessment_complete(assistant_message):
                    st.session_state.assessment_complete = True
            
            st.rerun()
    
    # Assessment Complete - Generate Reports
    elif st.session_state.assessment_complete:
        st.markdown("### ✅ Assessment Complete!")
        
        with st.spinner("🔄 Generating comprehensive analysis and reports..."):
            # Generate AI analysis
            analysis = generate_candidate_analysis(
                st.session_state.candidate_info,
                st.session_state.qa_pairs,
                llm
            )
            
            # Generate reports
            pdf_path, json_path = generate_reports(
                st.session_state.candidate_info,
                st.session_state.qa_pairs,
                analysis
            )
        
        st.markdown("""
            <div class="success-box">
                <h3>🎉 Reports Generated Successfully!</h3>
                <p>Your comprehensive assessment report has been created and saved.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Display analysis
        with st.expander("📊 View Candidate Analysis", expanded=True):
            st.markdown(analysis)
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_file,
                    file_name=pdf_path.split('/')[-1],
                    mime="application/pdf",
                    use_container_width=True
                )
        
        with col2:
            with open(json_path, "rb") as json_file:
                st.download_button(
                    label="📥 Download JSON Report",
                    data=json_file,
                    file_name=json_path.split('/')[-1],
                    mime="application/json",
                    use_container_width=True
                )
        
        st.info(f"📁 Reports saved to: `{pdf_path}` and `{json_path}`")
        
        # New candidate button
        st.markdown("---")
        if st.button("🔄 Screen New Candidate", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        # Show conversation summary
        with st.expander("💬 View Full Conversation"):
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])


if __name__ == "__main__":
    main()
