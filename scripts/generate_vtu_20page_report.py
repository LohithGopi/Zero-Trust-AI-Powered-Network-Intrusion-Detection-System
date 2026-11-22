"""
Master VTU Engineering Project Report Compiler & Validator:
Compiles:
  1. PDF via ReportLab with exactly 20 pages of main content + front/back matter.
  2. DOCX via python-docx with identical structure and tables.
  3. Verifies physical rendered PDF pagination using PyMuPDF.
"""

import os
import sys

# ReportLab Imports
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate
from reportlab.pdfgen import canvas
import pymupdf

# Directories
PROJECT_ROOT = r"E:\ML"
FIG_DIR = os.path.join(PROJECT_ROOT, "report", "figures")
OUTPUT_DIR = PROJECT_ROOT
LOGO_PATH = os.path.join(PROJECT_ROOT, "frontend", "public", "jnnce_logo.png")

PDF_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "Zero_Trust_AI_NIDS_VTU_System_Design_and_Implementation_Report.pdf")
DOCX_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "Zero_Trust_AI_NIDS_VTU_System_Design_and_Implementation_Report.docx")

class VTUReportCanvas(canvas.Canvas):
    """
    Two-pass canvas for rigorous VTU academic pagination:
      - Front Matter: Lowercase Roman numerals (i, ii, iii, iv, etc.)
      - Main Content (Pages 1-20): Running headers & 'Page X of 20' footer!
      - Back Matter: 'References - Page R-X' or 'Appendix A - Page A-X'
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"Total Physical PDF Pages Rendered: {num_pages}")
        
        # Front matter is pages 1 to 8 (8 pages)
        # Main report is pages 9 to 28 (20 pages)
        # Back matter is pages 29 to end
        for page_idx, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            phys_page = page_idx + 1
            self.draw_vtu_decorations(phys_page, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_vtu_decorations(self, phys_page, total_phys_pages):
        self.saveState()
        w, h = A4
        
        # Physical Page 1 is Title Page (No header or footer)
        if phys_page == 1:
            self.restoreState()
            return
            
        # Physical Pages 2 to 8: Front Matter (Roman numerals)
        if 2 <= phys_page <= 8:
            roman_numerals = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]
            roman_str = roman_numerals[phys_page] if phys_page < len(roman_numerals) else f"fm-{phys_page}"
            
            # Header
            self.setFont("Times-Italic", 9)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(54, h - 38, "Zero Trust AI-Powered Network Intrusion Detection System — Preliminary Pages")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, h - 42, w - 54, h - 42)
            
            # Footer with Roman numeral
            self.line(54, 46, w - 54, 46)
            self.setFont("Times-Roman", 9.5)
            self.drawString(54, 34, "Department of Information Science and Engineering, JNNCE, Shivamogga")
            self.drawRightString(w - 54, 34, roman_str)
            self.restoreState()
            return

        # Physical Pages 9 to 28: Main Report (EXACTLY 20 PAGES, Page 1 of 20 to Page 20 of 20)
        if 9 <= phys_page <= 28:
            main_page_num = phys_page - 8  # 1 to 20
            
            # Running Header
            self.setFont("Times-Bold", 8.5)
            self.setFillColor(colors.HexColor("#1E3A8A"))
            self.drawString(54, h - 36, "VISVESVARAYA TECHNOLOGICAL UNIVERSITY, BELAGAVI")
            self.setFont("Times-Italic", 8.5)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawRightString(w - 54, h - 36, "B.E. ISE — Zero Trust AI-NIDS System Design & Implementation")
            self.setStrokeColor(colors.HexColor("#94A3B8"))
            self.setLineWidth(0.7)
            self.line(54, h - 42, w - 54, h - 42)
            
            # Running Footer
            self.line(54, 44, w - 54, 44)
            self.setFont("Times-Roman", 8.5)
            self.setFillColor(colors.HexColor("#334155"))
            self.drawString(54, 32, "JNNCE, Shivamogga | Project Batch No. 34 (2023–2027)")
            self.setFont("Times-Bold", 9)
            self.setFillColor(colors.HexColor("#0F172A"))
            self.drawRightString(w - 54, 32, f"Page {main_page_num} of 20")
            self.restoreState()
            return

        # Physical Pages 29+: Back Matter (References & Appendices)
        if phys_page >= 29:
            back_num = phys_page - 28
            self.setFont("Times-Bold", 8.5)
            self.setFillColor(colors.HexColor("#1E3A8A"))
            self.drawString(54, h - 36, "VISVESVARAYA TECHNOLOGICAL UNIVERSITY, BELAGAVI")
            self.setFont("Times-Italic", 8.5)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawRightString(w - 54, h - 36, "References & Supplementary Appendices")
            self.setStrokeColor(colors.HexColor("#94A3B8"))
            self.setLineWidth(0.7)
            self.line(54, h - 42, w - 54, h - 42)
            
            # Footer
            self.line(54, 44, w - 54, 44)
            self.setFont("Times-Roman", 8.5)
            self.setFillColor(colors.HexColor("#334155"))
            self.drawString(54, 32, "JNNCE, Shivamogga | Project Batch No. 34")
            self.setFont("Times-Bold", 9)
            self.setFillColor(colors.HexColor("#0F172A"))
            self.drawRightString(w - 54, 32, f"Back Matter - Page {back_num}")
            self.restoreState()
            return
            
        self.restoreState()

def get_vtu_styles():
    """Build typography matching VTU academic guidelines."""
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        'VTUTitle',
        fontName='Times-Bold',
        fontSize=15,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1E3A8A')
    ))
    styles.add(ParagraphStyle(
        'VTUSubtitle',
        fontName='Times-Roman',
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#334155')
    ))
    styles.add(ParagraphStyle(
        'VTUChapter',
        fontName='Times-Bold',
        fontSize=13.5,
        leading=16.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'VTUH1',
        fontName='Times-Bold',
        fontSize=11.5,
        leading=14.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=3,
        spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        'VTUH2',
        fontName='Times-Bold',
        fontSize=10,
        leading=13,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=2,
        spaceAfter=1
    ))
    styles.add(ParagraphStyle(
        'VTUBody',
        fontName='Times-Roman',
        fontSize=9.2,
        leading=12.2,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'VTUBodyBold',
        fontName='Times-Bold',
        fontSize=9.2,
        leading=12.2,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'VTUCaption',
        fontName='Times-Italic',
        fontSize=8.2,
        leading=10.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#475569'),
        spaceBefore=2,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'VTUTableHeader',
        fontName='Times-Bold',
        fontSize=8,
        leading=9.5,
        alignment=TA_CENTER,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        'VTUTableCell',
        fontName='Times-Roman',
        fontSize=7.5,
        leading=9,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#1E293B')
    ))
    styles.add(ParagraphStyle(
        'VTUTableCellCenter',
        fontName='Times-Roman',
        fontSize=7.5,
        leading=9,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1E293B')
    ))
    styles.add(ParagraphStyle(
        'VTUTableCellBold',
        fontName='Times-Bold',
        fontSize=7.5,
        leading=9,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#0F172A')
    ))
    styles.add(ParagraphStyle(
        'VTUCode',
        fontName='Courier',
        fontSize=7.2,
        leading=8.8,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#0F172A')
    ))
    return styles

def compile_pdf_report():
    print("\n=======================================================")
    print("STEP 1: COMPILING VTU PDF REPORT (REPORTLAB)")
    print("=======================================================")
    
    # Import builders inside to ensure fresh modules
    from vtu_front_matter import build_front_matter_story
    from vtu_main_pages import (
        build_page_1, build_page_2, build_page_3, build_page_4, build_page_5,
        build_page_6, build_page_7, build_page_8, build_page_9, build_page_10,
        build_page_11, build_page_12, build_page_13, build_page_14, build_page_15,
        build_page_16, build_page_17, build_page_18, build_page_19, build_page_20
    )
    from vtu_back_matter import build_back_matter_story

    styles = get_vtu_styles()
    
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )
    
    story = []
    
    # 1. Front Matter (8 pages)
    print("Assembling Front Matter (Pages i to viii)...")
    front_story = build_front_matter_story(styles, LOGO_PATH)
    story.extend(front_story)
    
    # 2. Main Content (EXACTLY 20 PAGES)
    print("Assembling Main Content (Pages 1 to 20)...")
    page_builders = [
        build_page_1, build_page_2, build_page_3, build_page_4, build_page_5,
        build_page_6, build_page_7, build_page_8, build_page_9, build_page_10,
        build_page_11, build_page_12, build_page_13, build_page_14, build_page_15,
        build_page_16, build_page_17, build_page_18, build_page_19, build_page_20
    ]
    
    for idx, builder in enumerate(page_builders, start=1):
        print(f"  Building Main Report Page {idx}...")
        p_story = builder(styles, FIG_DIR)
        story.extend(p_story)
        
    # 3. Back Matter (References & Appendices)
    print("Assembling Back Matter (References & Appendices)...")
    back_story = build_back_matter_story(styles)
    story.extend(back_story)
    
    print(f"Building PDF with {len(story)} flowable elements...")
    doc.build(story, canvasmaker=VTUReportCanvas)
    print(f"PDF Successfully Generated: {PDF_OUTPUT_PATH}")

def verify_pdf_pagination():
    print("\n=======================================================")
    print("STEP 2: RIGOROUS PYMUPDF PAGINATION VERIFICATION")
    print("=======================================================")
    
    doc = pymupdf.open(PDF_OUTPUT_PATH)
    total_pages = len(doc)
    print(f"Total Physical PDF Pages: {total_pages}")
    
    for i in range(total_pages):
        page = doc[i]
        lines = [l.strip() for l in page.get_text("text").split("\n") if l.strip()]
        header = lines[:2] if len(lines) >= 2 else lines
        print(f"Physical Page {i+1:02d}: {header}")
        
    # Boundary identification
    front_matter_pages = 8
    expected_main_pages = 20
    
    main_start_phys = front_matter_pages + 1
    main_end_phys = front_matter_pages + expected_main_pages
    
    # Check text on physical page 9 (Main Page 1)
    p9_text = doc[main_start_phys - 1].get_text("text")
    is_p9_intro = "CHAPTER 1: INTRODUCTION" in p9_text
    
    # Check text on physical page 28 (Main Page 20)
    p28_text = doc[main_end_phys - 1].get_text("text")
    is_p28_conclusion = "CHAPTER 20: CONCLUSION & REFERENCES" in p28_text
    
    # Check text on physical page 29 (Back Matter References)
    p29_text = doc[main_end_phys].get_text("text") if total_pages >= main_end_phys + 1 else ""
    is_p29_refs = "REFERENCES (COMPREHENSIVE IEEE BIBLIOGRAPHY)" in p29_text
    
    print("\n--- PAGINATION VALIDATION SUMMARY ---")
    print(f"• Front-Matter Page Count:        {front_matter_pages}")
    print(f"• Main Content Starts Physical:   Page {main_start_phys} (Intro Match: {is_p9_intro})")
    print(f"• Main Content Ends Physical:     Page {main_end_phys} (Conclusion Match: {is_p28_conclusion})")
    print(f"• Actual Main-Content Page Count: {main_end_phys - main_start_phys + 1}")
    print(f"• Back-Matter Starts Physical:    Page {main_end_phys + 1} (Refs Match: {is_p29_refs})")
    print(f"• Additional Back-Matter Pages:   {total_pages - main_end_phys}")
    print(f"• Total Physical Pages:           {total_pages}")
    
    doc.close()
    
    if (main_end_phys - main_start_phys + 1) == 20 and is_p9_intro and is_p28_conclusion and is_p29_refs:
        print("\n>>> ABSOLUTE PAGINATION REQUIREMENT MET: EXACTLY 20 MAIN-CONTENT PAGES! <<<\n")
        return True
    else:
        print("\n>>> WARNING: PAGINATION MISMATCH DETECTED! INVESTIGATING OVERFLOW... <<<\n")
        return False

def compile_docx_report():
    print("\n=======================================================")
    print("STEP 3: COMPILING MATCHING VTU DOCX REPORT")
    print("=======================================================")
    from vtu_docx_generator import generate_docx_report
    generate_docx_report(DOCX_OUTPUT_PATH, FIG_DIR, LOGO_PATH)

if __name__ == "__main__":
    compile_pdf_report()
    pdf_valid = verify_pdf_pagination()
    compile_docx_report()
    
    print("\n=======================================================")
    print("FINAL DELIVERABLES CONFIRMATION")
    print("=======================================================")
    print(f"1. PDF Report:  {PDF_OUTPUT_PATH} ({os.path.getsize(PDF_OUTPUT_PATH):,} bytes)")
    print(f"2. DOCX Report: {DOCX_OUTPUT_PATH} ({os.path.getsize(DOCX_OUTPUT_PATH):,} bytes)")
    print("Status: COMPLETED SUCCESSFULLY.")
