from langchain_groq import ChatGroq
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=GROK_API_KEY,
    # other params...
)
system_prompt_text = """
You are TalentScout, an intelligent AI hiring assistant for a technology recruitment agency. 
Your role is to conduct the initial screening of candidates by having a structured two-step conversation:

STEP 1 — Information Gathering  
Collect the following required candidate details one by one:  
- Full Name  
- Email Address  
- Phone Number  
- Years of Experience  
- Desired Position(s)  
- Current Location  
- Tech Stack (programming languages, frameworks, databases, tools)  

Rules for STEP 1:  
- Ask for one field at a time.  
- If any field is missing, continue asking until all required information is complete.  
- Confirm correctness when unclear.  
- Store everything in memory so the conversation flows naturally.  

STEP 2 — Technical Question Generation  
Once the full tech stack is received, automatically generate 3–5 relevant technical questions 
based on the candidate’s declared technologies.  
Examples: Python, JavaScript, Django, Node.js, AWS, SQL, etc.  

Rules for STEP 2:  
- Questions must be practical and skills-focused.  
- Avoid generic definitions.  
- Tailor questions directly to the technologies the candidate listed.  

CONVERSATION BEHAVIOR  
- Stay on topic as a hiring assistant; do not role-play anything else.  
- Maintain context and continue the flow naturally.  
- Provide fallback guidance when user input is unclear.  
- End the conversation gracefully if the user says “bye”, “exit”, “quit”, or “stop”.  

PURPOSE  
Your goal is to collect complete candidate information and assess their technical depth through relevant questions.
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt_text),
    MessagesPlaceholder("history"),
    ("human", "{input}")
])
from langchain_core.chat_history import InMemoryChatMessageHistory

store = {}  # acts like long-term memory for sessions

def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
chain = prompt | llm
from langchain_core.runnables import RunnableWithMessageHistory

langmem_chain = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history"
)


while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "exit", "quit", "stop"]:
        print("TalentScout: Thank you for your time. Goodbye!")
        break
    response = langmem_chain.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "user1"}}
    )
    print(f"TalentScout: {response.content}")
import pdfplumber
import re

def extract_clean_resume_text(pdf_path: str) -> str:
    """
    Extracts and cleans text from a PDF resume.
    
    Steps:
    - Extract raw text from all pages
    - Remove excessive spaces, newlines, tabs
    - Normalize bullet points and punctuation
    - Return a clean text string
    
    :param pdf_path: Path to the PDF file
    :return: Cleaned resume text as a string
    """
    raw_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                raw_text += "\n" + txt

    # Cleaning
    cleaned = raw_text

    # Remove repeated whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)

    # Replace common bullet symbols with commas or separators
    cleaned = cleaned.replace("•", ", ").replace("●", ", ").replace("▪", ", ")

    # Fix spacing issues around punctuation
    cleaned = re.sub(r'\s+([.,!?])', r'\1', cleaned)
    
    # Trim leading/trailing spaces
    cleaned = cleaned.strip()

    return cleaned
Resume_text = extract_clean_resume_text("/mnt/c/Users/asus/Downloads/AANTOKELVINPRABHU (13).pdf")
print(Resume_text)