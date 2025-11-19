# 📁 TalentScout - Complete File Structure

## 🗂️ Directory Layout

```
talentscout/
│
├── 📄 main.py                      # Main Streamlit application (entry point)
├── 📄 config.py                    # Configuration and session state management
├── 📄 prompts.py                   # All AI prompts and templates
├── 📄 utils.py                     # Utility functions (PDF, formatting, etc.)
├── 📄 llm_handler.py              # LLM initialization and operations
├── 📄 voice_handler.py            # Voice input with Google Speech Recognition
├── 📄 report_generator.py         # PDF and JSON report generation
│
├── 📄 requirements.txt             # Python dependencies
├── 📄 README.md                    # Documentation and setup guide
│
├── 📂 Reports/                     # Auto-generated (created on first report)
│   ├── 📄 John_Doe_20241119_143022.pdf
│   ├── 📄 John_Doe_20241119_143022.json
│   ├── 📄 Jane_Smith_20241119_150815.pdf
│   ├── 📄 Jane_Smith_20241119_150815.json
│   └── ...
│
└── 📂 .streamlit/                  # Optional: Streamlit config
    └── 📄 config.toml              # Optional: App configuration
```

---

## 📋 File Breakdown with Code Sections

### 1️⃣ **config.py** (Lines 1-60)
```
Purpose: Application configuration and session state initialization
Size: ~60 lines
Key Components:
  - AppConfig dataclass
  - Session state defaults
  - Required fields definition
Dependencies: streamlit, dataclasses
```

### 2️⃣ **prompts.py** (Lines 61-200)
```
Purpose: All AI prompts and prompt generation functions
Size: ~140 lines
Key Components:
  - get_system_prompt() - Main assistant prompt
  - get_extraction_prompt() - Resume parsing
  - get_analysis_prompt() - Candidate evaluation
  - format_info_for_analysis() - Data formatting
Dependencies: typing
```

### 3️⃣ **utils.py** (Lines 201-310)
```
Purpose: Utility functions for file processing and formatting
Size: ~110 lines
Key Components:
  - extract_clean_resume_text() - PDF text extraction
  - format_candidate_info_natural() - Data formatting
  - generate_filename() - Timestamped filenames
  - parse_json_from_response() - JSON extraction
Dependencies: pdfplumber, re, json, datetime
```

### 4️⃣ **llm_handler.py** (Lines 311-400)
```
Purpose: LLM initialization and chain operations
Size: ~90 lines
Key Components:
  - initialize_llm() - Groq LLM setup
  - create_chain() - LangChain conversation chain
  - extract_info_from_resume() - Resume data extraction
  - generate_candidate_analysis() - AI analysis
Dependencies: langchain_groq, langchain_core, prompts, utils
```

### 5️⃣ **voice_handler.py** (Lines 401-510)
```
Purpose: Voice input handling with Google Speech Recognition
Size: ~110 lines
Key Components:
  - initialize_recognizer() - SR setup
  - record_audio() - Microphone recording
  - transcribe_audio() - Speech-to-text
  - get_voice_input() - Complete flow
Dependencies: streamlit, speech_recognition
```

### 6️⃣ **report_generator.py** (Lines 511-780)
```
Purpose: PDF and JSON report generation
Size: ~270 lines
Key Components:
  - ensure_reports_folder() - Directory creation
  - generate_pdf_report() - PDF with ReportLab
  - generate_json_report() - Structured JSON
  - generate_reports() - Complete report flow
Dependencies: os, json, datetime, reportlab, config
```

### 7️⃣ **main.py** (Lines 781-1050)
```
Purpose: Main Streamlit application and UI
Size: ~270 lines
Key Components:
  - main() - Application entry point
  - Mode selection UI
  - Chat interface
  - Voice input integration
  - Report display
Dependencies: All above modules + streamlit
```

### 8️⃣ **requirements.txt**
```
streamlit>=1.28.0
langchain-groq>=0.1.0
langchain-core>=0.1.0
pdfplumber>=0.10.0
reportlab>=4.0.0
SpeechRecognition>=3.10.0
PyAudio>=0.2.13
```

### 9️⃣ **README.md**
```
Complete documentation:
  - Features overview
  - Installation instructions
  - Usage guide
  - Voice input setup
  - Report format details
  - Troubleshooting
  - Module descriptions
```

---

## 🔄 Module Dependencies Graph

```
main.py
  ├── config.py
  ├── prompts.py
  ├── utils.py
  │     └── pdfplumber
  ├── llm_handler.py
  │     ├── langchain_groq
  │     ├── langchain_core
  │     ├── prompts.py
  │     └── utils.py
  ├── voice_handler.py
  │     ├── streamlit
  │     └── speech_recognition
  └── report_generator.py
        ├── reportlab
        ├── config.py
        └── utils.py
```

---

## 📦 How to Create the Structure

### **Step 1: Create Project Folder**
```bash
mkdir talentscout
cd talentscout
```

### **Step 2: Create All Python Files**
```bash
touch config.py
touch prompts.py
touch utils.py
touch llm_handler.py
touch voice_handler.py
touch report_generator.py
touch main.py
```

### **Step 3: Create Supporting Files**
```bash
touch requirements.txt
touch README.md
```

### **Step 4: Copy Code to Each File**

**From the artifact above, copy each section:**

#### **config.py** - Copy lines 1-60
```python
# File: config.py
"""Configuration settings for TalentScout application."""
...
```

#### **prompts.py** - Copy lines 61-200
```python
# File: prompts.py
"""System prompts and prompt templates."""
...
```

#### **utils.py** - Copy lines 201-310
```python
# File: utils.py
"""Utility functions for file processing and data formatting."""
...
```

#### **llm_handler.py** - Copy lines 311-400
```python
# File: llm_handler.py
"""LLM initialization and chain creation."""
...
```

#### **voice_handler.py** - Copy lines 401-510
```python
# File: voice_handler.py
"""Voice input handling using Google Speech Recognition."""
...
```

#### **report_generator.py** - Copy lines 511-780
```python
# File: report_generator.py
"""PDF and JSON report generation."""
...
```

#### **main.py** - Copy lines 781-end
```python
# File: main.py (app.py)
"""Main Streamlit application."""
...
```

---

## 🎯 File Size Reference

| File | Lines | Size (approx) | Complexity |
|------|-------|---------------|------------|
| config.py | ~60 | 2 KB | Low |
| prompts.py | ~140 | 5 KB | Low |
| utils.py | ~110 | 4 KB | Medium |
| llm_handler.py | ~90 | 3 KB | Medium |
| voice_handler.py | ~110 | 4 KB | Medium |
| report_generator.py | ~270 | 10 KB | High |
| main.py | ~270 | 10 KB | High |
| **Total** | **~1,050** | **~38 KB** | - |

---

## 🚀 Quick Start Commands

```bash
# 1. Create structure
mkdir talentscout && cd talentscout

# 2. Create all files at once (Unix/Mac/Linux)
touch config.py prompts.py utils.py llm_handler.py voice_handler.py report_generator.py main.py requirements.txt README.md

# 3. Windows PowerShell
New-Item config.py, prompts.py, utils.py, llm_handler.py, voice_handler.py, report_generator.py, main.py, requirements.txt, README.md

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
streamlit run main.py
```

---

## 📊 Reports Folder Structure

**Auto-generated after first report:**
```
Reports/
├── 📄 Candidate1_20241119_143022.pdf
├── 📄 Candidate1_20241119_143022.json
├── 📄 Candidate2_20241119_150815.pdf
├── 📄 Candidate2_20241119_150815.json
├── 📄 Candidate3_20241119_163544.pdf
└── 📄 Candidate3_20241119_163544.json
```

**Naming Pattern:**
```
{CandidateName}_{YYYYMMDD}_{HHMMSS}.{extension}

Examples:
- John_Doe_20241119_143022.pdf
- Jane_Smith_20241120_091530.json
- Robert_Johnson_20241121_154820.pdf
```

---

## 🔍 File Content Summary

### **Configuration Files**
- `config.py` - Settings, session state, constants
- `requirements.txt` - Python packages
- `README.md` - Full documentation

### **Core Logic Files**
- `prompts.py` - AI prompt templates
- `utils.py` - Helper functions
- `llm_handler.py` - AI/LLM operations

### **Feature Files**
- `voice_handler.py` - Voice recognition
- `report_generator.py` - Report creation

### **Application File**
- `main.py` - UI and app flow

---

## ✅ Verification Checklist

After creating structure, verify:

- [ ] All 7 Python files created
- [ ] requirements.txt exists
- [ ] README.md exists
- [ ] Code copied to each file correctly
- [ ] No syntax errors (run `python -m py_compile *.py`)
- [ ] Dependencies installed
- [ ] Can import modules: `python -c "import config, prompts, utils"`
- [ ] Streamlit runs: `streamlit run main.py`

---

## 🎨 Optional: Streamlit Configuration

Create `.streamlit/config.toml` for custom styling:

```toml
[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 10
```

---

**Your complete modular TalentScout application is ready! 🚀**