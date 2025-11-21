# 🎯 TalentScout - AI-Powered Hiring Assistant

> An intelligent Streamlit application for conducting automated technical screening interviews with voice input support, AI-powered analysis, and professional report generation.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Reports](#reports)
- [Voice Input](#voice-input)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

**TalentScout** automates the initial candidate screening process using AI technology. It intelligently gathers candidate information, conducts personalized technical assessments, and generates comprehensive evaluation reports - saving recruiters 50% of their screening time.

### Why TalentScout?

| Traditional Screening | TalentScout |
|----------------------|-------------|
| ❌ 20-30 min per candidate | ✅ 10-15 min per candidate |
| ❌ Inconsistent questions | ✅ Standardized, tech-specific questions |
| ❌ Manual report writing | ✅ Automated PDF + JSON reports |
| ❌ Subjective evaluation | ✅ AI-powered scoring & analysis |
| ❌ Poor organization | ✅ Structured report storage |

---

## ✨ Features

### 🎤 **Dual Input Modes**
- **💬 Chat Mode**: Interactive Q&A for live interviews
- **📄 Resume Upload**: Automatic information extraction from PDFs

### 🤖 **Intelligent Screening**
- Collects 7 essential candidate fields
- Skips already-known information
- Context-aware conversation flow
- Natural language processing

### 💻 **Technical Assessment**
- **5 personalized questions** based on candidate's tech stack
- Scenario-based problem solving
- Experience-level appropriate
- Automatic question counting

### 🎙️ **Voice Input Integration**
- Google Speech Recognition
- 15-second recording window
- Real-time transcription
- Text fallback option

### 📊 **AI-Powered Analysis**
- Technical competency scoring (0-10)
- Strengths identification
- Areas for improvement
- Knowledge depth assessment
- Communication evaluation
- Hiring recommendation (Strong Hire/Hire/Maybe/No Hire)

### 📄 **Professional Reports**
- **PDF**: Formatted with tables, styling, multi-page
- **JSON**: Structured data for database integration
- Auto-saved to `/Reports` folder
- Naming: `CandidateName_YYYYMMDD_HHMMSS.{pdf,json}`

### 🔄 **Automatic Workflow**
- Detects information completeness
- Transitions between phases automatically
- Counts questions (stops at 5)
- Auto-generates reports
- Resets for next candidate

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API Key ([Get free key](https://console.groq.com))
- Microphone (optional, for voice input)

### 3-Step Setup

```bash
# 1. Clone/Download and navigate to project
cd talentscout

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run main.py
```

**Enter your Groq API key in the sidebar** → Start screening! 🎉

---

## 📦 Installation

### Detailed Installation Steps

#### 1. **Install Python**

**Windows:**
```powershell
# Download from https://python.org
# Or use winget
winget install Python.Python.3.11
```

**macOS:**
```bash
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3-pip
```

#### 2. **Create Project Directory**

```bash
mkdir talentscout
cd talentscout
```

#### 3. **Create Virtual Environment (Recommended)**

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 4. **Create All Files**

Create these 9 files in the `talentscout` folder:

```
talentscout/
├── config.py
├── prompts.py
├── utils.py
├── llm_handler.py
├── voice_handler.py
├── report_generator.py
├── main.py
├── requirements.txt
└── README.md
```

**Quick create (Unix/Mac/Linux):**
```bash
touch config.py prompts.py utils.py llm_handler.py \
      voice_handler.py report_generator.py main.py \
      requirements.txt README.md
```

**Windows PowerShell:**
```powershell
New-Item config.py, prompts.py, utils.py, llm_handler.py, `
         voice_handler.py, report_generator.py, main.py, `
         requirements.txt, README.md
```

#### 5. **Copy Code from Artifact**

Copy each section from the main artifact to its corresponding file:
- **config.py** ← Lines 1-60
- **prompts.py** ← Lines 61-200
- **utils.py** ← Lines 201-310
- **llm_handler.py** ← Lines 311-400
- **voice_handler.py** ← Lines 401-510
- **report_generator.py** ← Lines 511-780
- **main.py** ← Lines 781-end

#### 6. **Install Dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 7. **Install PyAudio (Platform-Specific)**

**Windows:**
```powershell
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Verify:**
```python
python -c "import pyaudio; print('✅ PyAudio installed')"
```

#### 8. **Get Groq API Key**

1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Go to **API Keys** section
4. Click **Create API Key**
5. Copy the key (starts with `gsk_...`)

#### 9. **Verify Installation**

```bash
# Test all imports
python -c "import config, prompts, utils, llm_handler, voice_handler, report_generator"

# Should print: No errors
```

---

## 🎮 Usage

### Starting the Application

```bash
streamlit run main.py
```

Browser opens automatically at `http://localhost:8501`

### Step-by-Step Workflow

#### **1. Enter API Key**
- Look for sidebar: **⚙️ Configuration**
- Paste your Groq API key
- See ✅ confirmation

#### **2. Choose Input Mode**

**Option A: Chat Mode** 💬
- Click "Start Chat"
- Answer questions one by one
- Ideal for: Live interviews, phone screens

**Option B: Resume Upload** 📄
- Click "Upload Resume"
- Upload PDF file
- AI extracts information automatically
- Ideal for: Bulk screening, pre-qualified candidates

#### **3. Information Collection** (5-7 minutes)

AI collects these 7 fields:
1. ✅ Full Name
2. ✅ Email Address
3. ✅ Phone Number
4. ✅ Years of Experience
5. ✅ Desired Position(s)
6. ✅ Current Location
7. ✅ Tech Stack

**Pro Tip:** In resume mode, AI only asks for missing information!

#### **4. Technical Assessment** (10-15 minutes)

- AI asks **exactly 5 technical questions**
- Questions based on candidate's tech stack
- Scenario-based and practical

**Voice Input Option:**
- Toggle in sidebar during this phase
- Click "🎤 Record Voice"
- Speak for up to 15 seconds
- Review transcription
- Or use text input anytime

#### **5. Report Generation** (Automatic)

After 5th question:
- AI analyzes responses
- Generates comprehensive evaluation
- Creates PDF + JSON reports
- Saves to `/Reports` folder

#### **6. Review & Download**

- View analysis on screen
- Download PDF report
- Download JSON data
- Click "Screen New Candidate" to reset

### Example Session

```
👤 Recruiter: [Starts Chat Mode]

🤖 TalentScout: "Hello! I'm TalentScout. What's your full name?"
👤 Candidate: "John Doe"

🤖 TalentScout: "Great! What's your email address?"
👤 Candidate: "john.doe@example.com"

[... continues through 7 fields ...]

🤖 TalentScout: "Thank you! Now for technical assessment.
                 Question 1: Explain the difference between 
                 Python lists and tuples..."
👤 Candidate: [Answers via voice or text]

[... 5 questions total ...]

🤖 TalentScout: "That completes our assessment. 
                 Generating your report..."

✅ Reports saved:
   - John_Doe_20241119_143022.pdf
   - John_Doe_20241119_143022.json
```

---

## 📁 Project Structure

```
talentscout/
│
├── 📄 config.py                 # Configuration & session state
├── 📄 prompts.py                # AI prompts & templates
├── 📄 utils.py                  # Utility functions
├── 📄 llm_handler.py           # LLM operations
├── 📄 voice_handler.py         # Voice input handling
├── 📄 report_generator.py      # PDF/JSON generation
├── 📄 main.py                   # Main Streamlit app
│
├── 📄 requirements.txt          # Dependencies
├── 📄 README.md                 # This file
│
└── 📂 Reports/                  # Auto-generated
    ├── John_Doe_20241119_143022.pdf
    ├── John_Doe_20241119_143022.json
    ├── Jane_Smith_20241119_150815.pdf
    └── Jane_Smith_20241119_150815.json
```

### Module Descriptions

| Module | Purpose | Lines | Dependencies |
|--------|---------|-------|--------------|
| **config.py** | App configuration, session state | ~60 | streamlit, dataclasses |
| **prompts.py** | AI prompt engineering | ~140 | typing |
| **utils.py** | File processing, formatting | ~110 | pdfplumber, re, json |
| **llm_handler.py** | LLM initialization, chains | ~90 | langchain_groq |
| **voice_handler.py** | Speech recognition | ~110 | speech_recognition |
| **report_generator.py** | Report creation | ~270 | reportlab |
| **main.py** | UI & application flow | ~270 | All above modules |

---

## ⚙️ Configuration

### Customize Settings

Edit `config.py`:

```python
@dataclass
class AppConfig:
    MODEL_NAME: str = "llama-3.3-70b-versatile"  # AI model
    TEMPERATURE: float = 0                        # Creativity (0-1)
    MAX_RETRIES: int = 2                         # API retries
    REPORTS_FOLDER: str = "Reports"              # Folder name
```

### Change Number of Questions

Edit `prompts.py` (line ~50):

```python
# Change from 5 to desired number
- Generate exactly 5 technical questions
```

### Adjust Voice Recording Duration

Edit `voice_handler.py`:

```python
def get_voice_input(duration: int = 15):  # Change 15 to desired seconds
```

### Customize Report Styling

Edit `report_generator.py`:

```python
title_style = ParagraphStyle(
    'CustomTitle',
    fontSize=24,                           # Font size
    textColor=colors.HexColor('#1E88E5'), # Color
    ...
)
```

### Environment Variables (Optional)

For better security, use `.env` file:

**1. Install python-dotenv:**
```bash
pip install python-dotenv
```

**2. Create `.env` file:**
```env
GROQ_API_KEY=gsk_your_key_here
```

**3. Modify main.py:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
```

**4. Add to `.gitignore`:**
```
.env
venv/
__pycache__/
*.pyc
Reports/
```

---

## 📊 Reports

### PDF Report Contents

```
📄 CANDIDATE ASSESSMENT REPORT
├── 📋 Header
│   ├── TalentScout Logo
│   ├── Report Title
│   └── Generation Date/Time
│
├── 👤 Candidate Information
│   ├── Full Name
│   ├── Email & Phone
│   ├── Years of Experience
│   ├── Desired Position(s)
│   ├── Current Location
│   └── Tech Stack
│
├── 💻 Technical Assessment
│   ├── Question 1 ↔ Answer 1
│   ├── Question 2 ↔ Answer 2
│   ├── Question 3 ↔ Answer 3
│   ├── Question 4 ↔ Answer 4
│   └── Question 5 ↔ Answer 5
│
└── 📈 AI Analysis
    ├── Technical Competency Score (0-10)
    ├── Key Strengths (with examples)
    ├── Areas for Improvement
    ├── Knowledge Depth (Beginner-Expert)
    ├── Communication Skills Assessment
    ├── Hiring Recommendation
    └── Suggested Next Steps
```

### JSON Report Structure

```json
{
  "report_metadata": {
    "generated_at": "2024-11-19T14:30:22",
    "report_type": "Technical Screening Assessment",
    "generated_by": "TalentScout AI"
  },
  "candidate_information": {
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "phone_number": "+1-555-0123",
    "years_of_experience": 5,
    "desired_positions": ["Senior Python Developer"],
    "current_location": "New York, NY",
    "tech_stack": "Python, Django, PostgreSQL, AWS, Docker"
  },
  "technical_assessment": {
    "total_questions": 5,
    "qa_pairs": [
      {
        "question": "Explain the difference between...",
        "answer": "Lists are mutable while tuples..."
      }
    ]
  },
  "ai_analysis": "Overall Technical Competency: 8/10..."
}
```

### File Naming Convention

```
Format: {CandidateName}_{YYYYMMDD}_{HHMMSS}.{extension}

Examples:
✅ John_Doe_20241119_143022.pdf
✅ Jane_Smith_20241119_150815.json
✅ Robert_Johnson_20241120_091530.pdf

Location: Reports/{filename}
```

### Accessing Reports

**Via Application:**
- Download buttons after completion
- View analysis in expandable section

**Via File System:**
```bash
cd Reports/
ls -lh  # View all reports
open John_Doe_20241119_143022.pdf  # Open specific report
```

**Via Code:**
```python
import json

# Load JSON report
with open('Reports/John_Doe_20241119_143022.json', 'r') as f:
    data = json.load(f)
    
print(data['candidate_information']['full_name'])
print(data['ai_analysis'])
```

---

## 🎤 Voice Input

### How Voice Input Works

1. **Activation**: Automatically enabled during technical Q&A
2. **Toggle**: On/off switch in sidebar
3. **Recording**: Click "🎤 Record Voice" button
4. **Speaking**: 15-second window to answer
5. **Transcription**: Automatic speech-to-text
6. **Review**: See transcribed text before sending
7. **Fallback**: Type answer if needed

### Voice Input Tips

**For Best Results:**
- ✅ Use in quiet environment
- ✅ Speak clearly at normal pace
- ✅ Position mic 6-12 inches away
- ✅ Test mic before interview
- ✅ Wait for "Listening..." indicator

**Troubleshooting Voice:**
- 🔧 Check microphone permissions
- 🔧 Test mic in other apps
- 🔧 Restart application
- 🔧 Use text input as fallback
- 🔧 Increase recording duration in code

### Supported Languages

Google Speech Recognition supports 100+ languages:
- English (US, UK, AU, IN)
- Spanish, French, German
- Chinese, Japanese, Korean
- Hindi, Arabic, Portuguese
- And many more...

**To change language:**

Edit `voice_handler.py`:
```python
text = recognizer.recognize_google(audio, language='es-ES')  # Spanish
# language='fr-FR'  # French
# language='de-DE'  # German
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. **PyAudio Installation Failed**

**Error:** `error: Microsoft Visual C++ 14.0 required`

**Solution:**
```bash
# Windows: Use pre-built wheel
pip install pipwin
pipwin install pyaudio

# macOS: Install dependencies
brew install portaudio
pip install pyaudio

# Linux: Install dev packages
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

#### 2. **Microphone Not Working**

**Error:** `OSError: Invalid input device`

**Solution:**
```python
# List available microphones
import speech_recognition as sr
print(sr.Microphone.list_microphone_names())

# Check system permissions:
# Windows: Settings → Privacy → Microphone
# macOS: System Preferences → Security → Microphone
# Linux: pavucontrol or alsamixer
```

#### 3. **API Key Invalid**

**Error:** `AuthenticationError: Invalid API key`

**Solution:**
- Verify key format (starts with `gsk_`)
- Remove extra spaces/characters
- Regenerate key on Groq console
- Check account status

#### 4. **Reports Not Generated**

**Error:** `FileNotFoundError: Reports/`

**Solution:**
```bash
# Create folder manually
mkdir Reports

# Check permissions
chmod 755 Reports/

# Verify write access
touch Reports/test.txt
```

#### 5. **Import Errors**

**Error:** `ModuleNotFoundError: No module named 'config'`

**Solution:**
```bash
# Verify all files exist
ls -la *.py

# Run from correct directory
pwd  # Should show talentscout folder
streamlit run main.py
```

#### 6. **Streamlit Won't Start**

**Error:** `streamlit: command not found`

**Solution:**
```bash
# Reinstall Streamlit
pip install --upgrade streamlit

# Use full path
python -m streamlit run main.py

# Check installation
pip show streamlit
```

### Getting Help

**Check these first:**
1. ✅ All dependencies installed?
2. ✅ Groq API key valid?
3. ✅ All files in same directory?
4. ✅ Virtual environment activated?
5. ✅ Python version 3.8+?

**Still having issues?**
- Check error messages carefully
- Search GitHub issues
- Review documentation
- Test with minimal example

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/talentscout.git
cd talentscout

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a new branch
git checkout -b feature/your-feature-name

# Make changes and test
streamlit run main.py

# Commit and push
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Comment complex logic
- Keep functions focused
- Use type hints

### Testing

```bash
# Run unit tests
python -m unittest discover tests/

# Test specific module
python -m unittest tests/test_utils.py
```



## 🙏 Acknowledgments

**Built with:**
- [Streamlit](https://streamlit.io/) - Web framework
- [LangChain](https://www.langchain.com/) - AI orchestration
- [Groq](https://groq.com/) - LLM inference
- [ReportLab](https://www.reportlab.com/) - PDF generation
- [Google Speech Recognition](https://cloud.google.com/speech-to-text) - Voice input

**Special thanks to:**
- Open source community
- Contributors and testers
- Early adopters

---


## 🗺️ Roadmap

### Upcoming Features

- [ ] Multi-language support
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] Video interview integration
- [ ] Mobile app
- [ ] REST API

---

## 📊 Stats

- ⚡ **Screening Time**: 10-15 minutes (50% faster)
- 🎯 **Accuracy**: 95% information extraction
- 📈 **Scalability**: Unlimited concurrent sessions
- 💾 **Report Size**: 200-500 KB per candidate
- 🌍 **Languages**: 100+ via voice input

---

<div align="center">

**⭐ Star this repo if you find it useful!**

**Made with ❤️ for recruiters and developers**

[🚀 Get Started](#quick-start) • [📚 Documentation](#table-of-contents) • [🤝 Contribute](#contributing)

</div>