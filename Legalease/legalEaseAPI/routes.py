from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
gemini_generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):
    document_type: str = Field(..., description="Type of legal document (e.g., NDA, Employment Contract, Lease Agreement)")
    parties: str = Field(..., description="Names and roles of involved parties")
    terms: str = Field(..., description="Semicolon-separated terms and conditions")
    dates: str = Field(..., description="Effective date of the document")

@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    try:
        response = gemini_generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates
        )
        return {"document": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
