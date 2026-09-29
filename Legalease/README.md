# LegalEase: AI-Powered Legal Document Generator

**LegalEase** leverages Generative AI (Google Gemini 1.5 Pro) and modern web architectures to simplify the creation of legal documents by providing customizable, accurate, and editable templates for contracts, NDAs, lease agreements, and employment agreements.

---

## 🏛️ Project Architecture

- **Frontend**: [Streamlit](file:///c:/Legalease/frontend/app.py) - Clean user interface for user inputs, dynamic styling, inline document editing, and multi-format export (.TXT, .DOCX, .PDF).
- **Backend API**: [FastAPI](file:///c:/Legalease/legalEaseAPI/main.py) - Robust REST API handling `/generate` requests with Pydantic schemas.
- **AI Core**: [GeminiDocumentGenerator](file:///c:/Legalease/ai_core/gemini_generator.py) - Seamless integration with Google Gemini 1.5 Pro via `google-generativeai`.
- **Document Formatting Engine**: [ai_core/generator.py](file:///c:/Legalease/ai_core/generator.py) - Custom document converters supporting PDF styling with headers, footers, logos, Times New Roman typography, and auto-structured legal sections.

---

## 📁 Project Directory Structure

```
LEGALEASE/
├── ai_core/
│   ├── __init__.py
│   ├── gemini_generator.py       # Gemini AI prompt orchestration & model integration
│   └── generator.py              # Export formatters (.pdf, .docx, .txt, HTML preview)
├── docs/
│   └── README.md
├── frontend/
│   └── app.py                    # Streamlit web user interface
├── Image/
│   ├── Logo.png                  # LegalEase scale logo
│   └── inverseLogo.png           # Inverse dark-mode logo
├── legalEaseAPI/
│   ├── __init__.py
│   ├── main.py                   # FastAPI server entrypoint
│   └── routes.py                 # REST endpoints & Pydantic models
├── .env                          # Environment variables & API keys
├── .env.example                  # Template environment file
├── config.py                     # Configuration constants & path references
├── requirements.txt              # Project dependencies
├── run.bat                       # Windows 1-click startup script
└── run.sh                        # Unix/Linux/macOS startup script
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and set your Google Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL_NAME=gemini-1.5-pro
API_HOST=0.0.0.0
API_PORT=8000
API_URL=http://localhost:8000
```

### 3. Run the Application

#### Option A: 1-Click Launch (Windows)
Double-click `run.bat` or run:
```cmd
run.bat
```

#### Option B: Manual Launch
**Terminal 1 - FastAPI Backend:**
```bash
python -m uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Streamlit Frontend:**
```bash
streamlit run frontend/app.py
```

Open your browser at `http://localhost:8501`.

---

## 🧪 Scenarios & Features
1. **Employment Contract**: Generate customized employment terms, roles, and compensation agreements.
2. **Non-Disclosure Agreement (NDA)**: Define confidentiality scope, disclosures, and non-compete periods.
3. **Residential Lease Agreement**: Specify property details, tenant requirements, security deposits, and rules.
4. **Editable Previews**: Inline editing of generated text prior to export.
5. **Multi-Format Export**:
   - `.TXT` (Plain Text)
   - `.DOCX` (Times New Roman, embedded branding logo, structured clauses, footers)
   - `.PDF` (Branded header with logo, dynamic page numbers, footer)
