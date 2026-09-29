import os
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME

class GeminiDocumentGenerator:
    """
    Generates professional legal documents using Google Gemini Generative AI models.
    """
    def __init__(self, model_name: str = None, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)
        self.model_name = model_name or os.getenv("GEMINI_MODEL_NAME", GEMINI_MODEL_NAME)
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        """
        Generate legal document text based on document_type, parties, terms, and dates.
        """
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions: {terms}\n"
            f"Ensure formal legal structure with multiple sections and legal clauses.\n"
            f"Include standard sections such as Preamble / Recitals (WITNESSETH), Definitions, "
            f"Obligations and Services, Compensation / Consideration, Confidentiality, Term & Termination, "
            f"Intellectual Property, Governing Law, Severability, Entire Agreement, and Signature Blocks."
        )

        # If API key is available, call Gemini API
        if self.api_key:
            try:
                if self.model is None:
                    genai.configure(api_key=self.api_key)
                    self.model = genai.GenerativeModel(self.model_name)
                
                response = self.model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                # Log and fallback to template generation if offline or API error
                print(f"[Gemini Document Generator Warning] API call failed: {e}. Generating high-quality standard document template.")
                return self._generate_fallback_document(document_type, parties, terms, dates)
        
        # Fallback generator if API Key is not configured yet
        return self._generate_fallback_document(document_type, parties, terms, dates)

    def _generate_fallback_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        """
        Generates a robust, professionally formatted legal document fallback when Gemini API key is not supplied.
        """
        term_items = [t.strip() for t in terms.split(";") if t.strip()]
        if not term_items:
            term_items = ["Standard terms and conditions as agreed upon by all participating parties."]

        party_lines = [p.strip() for p in parties.split(",") if p.strip()]
        if len(party_lines) >= 2:
            party_a = party_lines[0]
            party_b = party_lines[1]
        elif len(party_lines) == 1:
            party_a = party_lines[0]
            party_b = "Counterparty"
        else:
            party_a = "First Party"
            party_b = "Second Party"

        formatted_terms = ""
        for i, term in enumerate(term_items, start=1):
            formatted_terms += f"{i}. **Term & Condition {i}**: {term}\n"

        doc = f"""## {document_type}

This {document_type} (the "Agreement") is entered into and made effective as of {dates} (the "Effective Date").

### BETWEEN:

**{party_a}** (hereinafter referred to as the "First Party"),

### AND:

**{party_b}** (hereinafter referred to as the "Second Party").

---

### RECITALS (WITNESSETH):

WHEREAS, the First Party and the Second Party desire to establish a formal agreement governing their professional relationship and obligations; and

WHEREAS, both parties possess the requisite authority and capacity to enter into this legally binding agreement.

NOW, THEREFORE, in consideration of the mutual covenants, conditions, and promises contained herein, the parties agree as follows:

---

### 1. Purpose and Scope
The purpose of this Agreement is to establish the specific understandings, roles, and obligations regarding {document_type} between the involved stakeholders.

### 2. Terms and Specific Conditions
{formatted_terms}
### 3. Confidentiality and Proprietary Information
Each party agrees to maintain the confidentiality of any proprietary or non-public information disclosed during the course of this Agreement and not to disclose such information to any third party without prior written consent.

### 4. Term and Termination
This Agreement shall commence on the Effective Date ({dates}) and shall remain in effect until fulfilled or terminated in accordance with the provisions specified herein or upon 15 days written notice by either party.

### 5. Governing Law and Jurisdiction
This Agreement shall be construed, interpreted, and governed in accordance with the applicable laws of the governing jurisdiction, without giving effect to any principles of conflicts of law.

### 6. Severability
If any provision of this Agreement is held to be invalid or unenforceable, such provision shall be severed and the remaining provisions shall continue in full force and effect.

### 7. Entire Agreement
This Agreement constitutes the entire understanding between the parties concerning the subject matter hereof and supersedes all prior discussions, negotiations, and agreements.

---

### IN WITNESS WHEREOF:

The parties hereto have executed this {document_type} as of the Effective Date written above.

___________________________________                    ___________________________________
**{party_a}**                                          **{party_b}**
Date: {dates}                                          Date: {dates}
"""
        return doc
