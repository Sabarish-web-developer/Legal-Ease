import os
import io
import re
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from fpdf import FPDF
from config import LOGO_PATH

def sanitize_text(text: str) -> str:
    """
    Removes special unicode characters, typographic quotes, and non-standard dashes
    to ensure clean formatting across all export mediums (PDF, DOCX, TXT).
    """
    if not text:
        return ""
    
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "--",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "*",
        "\t": "    ",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    
    # Remove any unprintable control characters except standard newlines
    text = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\u00A0-\u00FF]', '', text)
    return text.strip()

class LegalPDF(FPDF):
    """
    Custom PDF generator class for LegalEase documents with Header & Footer.
    """
    def __init__(self, doc_type: str = "Legal Document"):
        super().__init__()
        self.doc_type = doc_type
        self.set_margins(left=20, top=25, right=20)
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        # Embed Logo if exists
        if os.path.exists(LOGO_PATH):
            try:
                self.image(str(LOGO_PATH), x=75, y=10, w=60)
                self.ln(12)
            except Exception:
                pass
        
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 41, 59)
        self.cell(0, 10, self.doc_type, border=0, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(203, 213, 225)
        self.set_line_width(0.4)
        self.line(20, self.get_y() + 2, 190, self.get_y() + 2)
        self.ln(8)

    def footer(self):
        self.set_y(-20)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(2)
        
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139)
        footer_text = f"LegalEase Inc. | contact@legalease.com | All Rights Reserved.   |   Page {self.page_no()}/{{nb}}"
        self.cell(0, 8, footer_text, border=0, align="C")

def format_pdf(text: str, doc_type: str = "Legal Document") -> bytes:
    """
    Generates a professionally styled PDF byte stream using FPDF.
    """
    clean_text = sanitize_text(text)
    pdf = LegalPDF(doc_type=doc_type)
    pdf.alias_nb_pages()
    pdf.add_page()
    
    lines = clean_text.split("\n")
    for line in lines:
        line_str = line.strip()
        if not line_str:
            pdf.ln(3)
            continue
        
        # Heading 1 / 2 (Markdown ##)
        if line_str.startswith("#"):
            heading_text = line_str.lstrip("#").strip()
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(15, 23, 42)
            pdf.ln(3)
            pdf.multi_cell(0, 6, heading_text, align="L", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif line_str.startswith("*") or line_str.startswith("-"):
            # Bullet items
            bullet_text = line_str.lstrip("*- ").strip()
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 5, f"  *  {bullet_text}", align="L", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif line_str.startswith("---") or line_str.startswith("___"):
            # Horizontal rule
            pdf.ln(2)
            pdf.set_draw_color(226, 232, 240)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(4)
        else:
            # Regular paragraph
            # Check if line contains bold cues like **Title:**
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(51, 65, 85)
            # Remove bold markdown tags for PDF rendering
            plain_line = line_str.replace("**", "")
            pdf.multi_cell(0, 5.5, plain_line, align="J", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            
    # Output to bytes
    pdf_output = pdf.output()
    if isinstance(pdf_output, str):
        return pdf_output.encode("latin-1", errors="replace")
    return bytes(pdf_output)

def format_docx(text: str, doc_type: str = "Legal Document") -> bytes:
    """
    Generates a professionally formatted DOCX file with Logo, Times New Roman font,
    structured headings, term tables, and footer.
    """
    clean_text = sanitize_text(text)
    doc = Document()
    
    # Page setup - Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Add footer to docx
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run("LegalEase Inc. | contact@legalease.com | All Rights Reserved.")
        f_run.font.name = "Times New Roman"
        f_run.font.size = Pt(9)
        f_run.font.italic = True
        f_run.font.color.rgb = RGBColor(100, 116, 139)

    # Add Logo at top if exists
    if os.path.exists(LOGO_PATH):
        try:
            logo_p = doc.add_paragraph()
            logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            logo_p.paragraph_format.space_after = Pt(12)
            logo_run = logo_p.add_run()
            logo_run.add_picture(str(LOGO_PATH), width=Inches(2.5))
        except Exception:
            pass

    # Document Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_after = Pt(18)
    title_run = title_p.add_run(doc_type.upper())
    title_run.bold = True
    title_run.font.name = "Times New Roman"
    title_run.font.size = Pt(18)
    title_run.font.color.rgb = RGBColor(15, 23, 42)

    # Parse lines
    lines = clean_text.split("\n")
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        
        if line_str.startswith("#"):
            h_level = 1 if line_str.startswith("# ") else 2
            h_text = line_str.lstrip("#").strip()
            hp = doc.add_paragraph()
            hp.paragraph_format.space_before = Pt(12)
            hp.paragraph_format.space_after = Pt(6)
            hrun = hp.add_run(h_text)
            hrun.bold = True
            hrun.font.name = "Times New Roman"
            hrun.font.size = Pt(13 if h_level == 1 else 11.5)
            hrun.font.color.rgb = RGBColor(15, 23, 42)
        elif line_str.startswith("*") or line_str.startswith("-"):
            bp = doc.add_paragraph(style='List Bullet')
            bp.paragraph_format.space_after = Pt(4)
            b_text = line_str.lstrip("*- ").strip()
            _add_formatted_runs(bp, b_text)
        elif line_str.startswith("---") or line_str.startswith("___"):
            sep_p = doc.add_paragraph()
            sep_p.paragraph_format.space_before = Pt(6)
            sep_p.paragraph_format.space_after = Pt(6)
            sep_run = sep_p.add_run("___________________________________________________________________")
            sep_run.font.color.rgb = RGBColor(203, 213, 225)
            sep_run.font.size = Pt(8)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            _add_formatted_runs(p, line_str)

    # Save to BytesIO stream
    target_stream = io.BytesIO()
    doc.save(target_stream)
    target_stream.seek(0)
    return target_stream.getvalue()

def _add_formatted_runs(paragraph, text: str):
    """Helper to handle bold **text** markdown syntax inside docx paragraphs"""
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            bold_text = part[2:-2]
            run = paragraph.add_run(bold_text)
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(30, 41, 59)
        else:
            run = paragraph.add_run(part)
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(51, 65, 85)

def format_html_preview(text: str) -> str:
    """
    Converts markdown text to a styled HTML document card for Streamlit preview.
    """
    clean_text = sanitize_text(text)
    
    # Simple markdown to HTML conversion with elegant styling
    html_lines = []
    lines = clean_text.split("\n")
    in_list = False

    for line in lines:
        line_str = line.strip()
        if not line_str:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        # Format bold tags
        line_str = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #f8fafc; font-weight: 600;">\1</strong>', line_str)

        if line_str.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = line_str[3:]
            html_lines.append(f'<h3 style="color: #38bdf8; font-size: 1.25rem; margin-top: 1.5rem; margin-bottom: 0.5rem; border-bottom: 1px solid #334155; padding-bottom: 0.25rem;">{title}</h3>')
        elif line_str.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = line_str[4:]
            html_lines.append(f'<h4 style="color: #94a3b8; font-size: 1.05rem; margin-top: 1rem; margin-bottom: 0.35rem; font-weight: 600;">{title}</h4>')
        elif line_str.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = line_str[2:]
            html_lines.append(f'<h2 style="color: #60a5fa; font-size: 1.45rem; text-align: center; margin-bottom: 1rem;">{title}</h2>')
        elif line_str.startswith("* ") or line_str.startswith("- "):
            if not in_list:
                html_lines.append('<ul style="margin: 0.5rem 0; padding-left: 1.5rem; color: #cbd5e1;">')
                in_list = True
            item_text = line_str[2:]
            html_lines.append(f'<li style="margin-bottom: 0.3rem;">{item_text}</li>')
        elif line_str.startswith("---") or line_str.startswith("___"):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append('<hr style="border: 0; border-top: 1px solid #334155; margin: 1rem 0;" />')
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6; margin-bottom: 0.75rem;">{line_str}</p>')

    if in_list:
        html_lines.append("</ul>")

    inner_content = "\n".join(html_lines)
    
    styled_container = f"""
    <div style="
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 24px;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
        max-height: 520px;
        overflow-y: auto;
    ">
        {inner_content}
    </div>
    """
    return styled_container
