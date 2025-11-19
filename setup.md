# 1. Create all files
mkdir talentscout && cd talentscout
touch config.py prompts.py utils.py llm_handler.py voice_handler.py report_generator.py main.py requirements.txt README.md

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run!
streamlit run main.py