import os
import sys
from pathlib import Path
import streamlit as st
import requests

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from config import API_URL, LOGO_PATH, INVERSE_LOGO_PATH
from ai_core.generator import sanitize_text, format_docx, format_pdf, format_html_preview
from ai_core.gemini_generator import GeminiDocumentGenerator

# Page configuration
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark-themed sleek UI matching screenshots
st.markdown("""
<style>
    .main-header {
        text-align: center;
        margin-top: -20px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .download-section {
        margin-top: 20px;
        padding: 15px;
        background-color: #1e293b;
        border-radius: 8px;
        border: 1px solid #334155;
    }
    .stTextArea textarea {
        font-family: inherit;
    }
</style>
""", unsafe_allow_html=True)

# Logo Display
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    logo_file = INVERSE_LOGO_PATH if os.path.exists(INVERSE_LOGO_PATH) else LOGO_PATH
    if os.path.exists(logo_file):
        st.image(str(logo_file), use_container_width=True)

# Title
st.markdown("<h2 style='text-align: center; margin-top: -10px;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 25px;'>Draft, customize, and export professional legal documents in seconds.</p>", unsafe_allow_html=True)

# Initialize Session States
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "doc_type" not in st.session_state:
    st.session_state.doc_type = ""
if "show_edit" not in st.session_state:
    st.session_state.show_edit = False

# Input Form
with st.container():
    doc_type_input = st.text_input(
        "Document Type (Ex: Agreement, Contract, NDA)",
        value=st.session_state.doc_type or "Freelance Work Contract",
        placeholder="Freelance Work Contract"
    )

    parties_input = st.text_area(
        "Parties Involved",
        value="Jane Doe (Service Provider), TechNova Inc. (Client)",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        help="Names and roles of the individuals or entities involved in the document."
    )

    terms_input = st.text_area(
        "Terms & Conditions (Use semicolons for bullet points)",
        value="Work must be delivered by May 15, 2025;\nPayment will be made within 7 days of invoice;\nThe client retains intellectual property rights;\nEither party may terminate with 15 days notice",
        placeholder="Payment to be made within 30 days of invoice;\nThe provider agrees to deliver work by the agreed deadline;",
        height=120,
        help="Specific clauses or rules that define the agreement. Separate clauses with semicolons (;)."
    )

    dates_input = st.text_input(
        "Effective Date",
        value="April 15, 2025",
        placeholder="April 15, 2025"
    )

    generate_clicked = st.button("Generate Document", type="primary", use_container_width=True)

# Document Generation Logic
if generate_clicked:
    if not doc_type_input or not parties_input or not terms_input:
        st.error("Please fill in the Document Type, Parties Involved, and Terms & Conditions.")
    else:
        with st.spinner("Generating legal document with AI..."):
            payload = {
                "document_type": doc_type_input,
                "parties": parties_input,
                "terms": terms_input,
                "dates": dates_input
            }
            
            raw_text = None
            # Attempt to call FastAPI backend
            try:
                backend_url = f"{API_URL}/generate"
                response = requests.post(backend_url, json=payload, timeout=30)
                if response.status_code == 200:
                    raw_text = response.json().get("document", "")
                else:
                    st.warning(f"Backend API returned status {response.status_code}. Using fallback generator.")
            except Exception:
                # Direct in-process generation fallback if API server is not running
                generator = GeminiDocumentGenerator()
                raw_text = generator.generate_document(
                    doc_type_input,
                    parties_input,
                    terms_input,
                    dates_input
                )

            if raw_text:
                st.session_state.generated_text = sanitize_text(raw_text)
                st.session_state.doc_type = doc_type_input
                st.success("Document Generated Successfully!")

# Display Generated Document & Export Options
if st.session_state.generated_text:
    st.markdown("---")
    
    # Styled HTML Preview
    st.markdown("### Document Preview")
    styled_html = format_html_preview(st.session_state.generated_text)
    st.markdown(styled_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Edit Document Section
    edit_col1, edit_col2 = st.columns([1, 1])
    with edit_col1:
        if st.button("📝 Click to Edit Document", use_container_width=True):
            st.session_state.show_edit = not st.session_state.show_edit

    if st.session_state.show_edit:
        edited_text = st.text_area(
            "Edit Document Below:",
            value=st.session_state.generated_text,
            height=320
        )
        st.session_state.generated_text = sanitize_text(edited_text)
        st.caption("ℹ️ Any changes made here are instantly applied to download exports.")

    st.markdown("---")
    st.markdown("### Download Document")
    
    # Generate export files
    file_base = st.session_state.doc_type.lower().replace(" ", "_").replace("/", "_")
    txt_data = st.session_state.generated_text.encode("utf-8")
    
    try:
        docx_data = format_docx(st.session_state.generated_text, st.session_state.doc_type)
    except Exception as e:
        docx_data = None
        st.error(f"Error preparing DOCX: {e}")

    try:
        pdf_data = format_pdf(st.session_state.generated_text, st.session_state.doc_type)
    except Exception as e:
        pdf_data = None
        st.error(f"Error preparing PDF: {e}")

    # Download Buttons Layout
    d_col1, d_col2, d_col3 = st.columns(3)
    
    with d_col1:
        st.download_button(
            label="📄 Download as .TXT",
            data=txt_data,
            file_name=f"{file_base}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with d_col2:
        if docx_data:
            st.download_button(
                label="📝 Download as .DOCX",
                data=docx_data,
                file_name=f"{file_base}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

    with d_col3:
        if pdf_data:
            st.download_button(
                label="📕 Download as .PDF",
                data=pdf_data,
                file_name=f"{file_base}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
