# 🩺 Patient Interpreter

**Patient Interpreter** is an AI-powered assistant designed to help users prepare for doctor visits, rewrite symptoms in medically clear language, and track personal health notes.

## ✨ Features

- 📝 Rewrite user-described symptoms into structured, clinical summaries
- 💬 Generate helpful follow-up questions to ask your doctor
- 💾 Save visit notes and organize them by date and doctor
- 🔍 Explore potential causes of symptoms using a built-in chat assistant
- 👤 Supports multiple users with login and personalized note history

## 🚀 Built With

- [Streamlit](https://streamlit.io/) – Frontend framework for interactive Python apps
- [OpenAI API](https://openai.com/api/) – GPT-3.5 for natural language understanding
- [Pandas](https://pandas.pydata.org/) – Note and visit data management
- [streamlit-authenticator](https://github.com/mkhorasani/streamlit-authenticator) – Simple login system

## 📂 Folder Structure

```
patient-interpreter/
│
├── app.py                     # Main Streamlit app
├── gpt_utils.py              # GPT functions for rewriting and Q&A
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment entry point (for Render/Heroku)
├── .streamlit/secrets.toml  # OpenAI API key (local only)
├── .config/credentials.yaml  # Login credentials (dev use)
├── visit_logs/               # Saved notes per user
├── visit_summary/            # Final logged visit summaries
```

## 🧪 Getting Started

1. Clone the repo:
```bash
git clone https://github.com/rnaltami/patient-interpreter.git
cd patient-interpreter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run locally:
```bash
streamlit run app.py
```

## 📌 Note

This is a prototype intended for development and demonstration only. Not for use as a medical diagnostic tool.

---

Created with ❤️ by [@rnaltami](https://github.com/rnaltami)
