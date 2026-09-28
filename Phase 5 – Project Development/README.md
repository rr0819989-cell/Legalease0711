# LegalEase - AI-Powered Legal Document Generator

This implementation follows the LegalEase project document:
- Streamlit frontend
- FastAPI backend
- Gemini integration
- Editable document preview
- TXT / DOCX / PDF downloads
- Local VS Code deployment

## 1. Open the project

Open this folder in VS Code.

## 2. Create a virtual environment

### Windows PowerShell
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 3. Install packages

```powershell
pip install -r requirements.txt
```

## 4. Configure Gemini

Copy `.env.example` to `.env` and add your Gemini API key:

```text
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-1.5-pro
```

If the selected model is unavailable for your API account, set `GEMINI_MODEL` to an available Gemini model.

## 5. Start FastAPI

Open Terminal 1:

```powershell
python main.py
```

The API will run at:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs

## 6. Start Streamlit

Open Terminal 2:

```powershell
.\venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

Streamlit will show a local browser URL, normally:

http://localhost:8501

## 7. Demo input

Document Type:
Freelance Work Contract

Parties:
Jane Doe (Service Provider), TechNova Inc. (Client)

Terms:
Payment within 30 days; Confidentiality must be maintained; Provider shall deliver work by the agreed deadline; Either party may terminate with 15 days notice

Effective Date:
25/09/2026

Click Generate Document.

The generated draft can then be edited and downloaded as:
- TXT
- DOCX
- PDF

## If you do not have a Gemini API key

The application still runs using the built-in local template fallback. Add a Gemini key later to enable AI generation.

## Project structure

LegalEase/
├── main.py
├── legalaseAPI/
│   ├── __init__.py
│   └── routes.py
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── frontend/
│   └── app.py
├── utils/
│   ├── __init__.py
│   └── formatters.py
├── assets/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
