"""
HackerRank SDE Intern - AI Interview Preparation Handbook Generator
Builds a comprehensive, publication-grade A4 PDF for Lloyd Gopi.
Strictly sanitized ASCII/Latin-1 typography (zero glyph errors) and balanced pagination.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Corporate Palette (Navy, Slate, Electric Cyan, Light Gray)
NAVY_PRIMARY = HexColor("#0F2C59")     # Deep Corporate Navy
NAVY_SECONDARY = HexColor("#1E3E62")   # Medium Navy
BLUE_ACCENT = HexColor("#0284C7")      # Electric Blue / Cyan Accent
TEXT_DARK = HexColor("#1E293B")        # Slate 900 High-Contrast Body
TEXT_MUTED = HexColor("#475569")       # Slate 600 Subtext
BG_LIGHT = HexColor("#F8FAFC")         # Slate 50 Neutral Light
BG_CARD = HexColor("#FFFFFF")          # Pure White
BORDER_LIGHT = HexColor("#CBD5E1")     # Slate 300 Divider
ACCENT_GREEN = HexColor("#0D9488")     # Teal / Success
BG_HIGHLIGHT = HexColor("#F1F5F9")     # Card Header Light Gray
LINE_GRAY = HexColor("#E2E8F0")        # Inner Card Divider
AMBER_TAG = HexColor("#B45309")        # Amber Tag

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 34
CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN) # 527.28 pt

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for dynamic total page count, running headers, and running footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        if self._pageNumber > 1:
            # Running Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(NAVY_PRIMARY)
            self.drawString(MARGIN, 814, "HACKERRANK SDE INTERN")
            
            self.setFont("Helvetica", 8)
            self.setFillColor(TEXT_MUTED)
            self.drawString(MARGIN + 120, 814, "|  AI Technical & Behavioral Interview Preparation Handbook")
            self.drawRightString(PAGE_WIDTH - MARGIN, 814, "Candidate: Lloyd Gopi (JNNCE 2027)")
            
            self.setStrokeColor(BORDER_LIGHT)
            self.setLineWidth(0.6)
            self.line(MARGIN, 808, PAGE_WIDTH - MARGIN, 808)

            # Running Footer
            self.line(MARGIN, 34, PAGE_WIDTH - MARGIN, 34)
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(NAVY_PRIMARY)
            self.drawString(MARGIN, 22, "CONFIDENTIAL TECHNICAL HANDBOOK")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(TEXT_MUTED)
            self.drawString(MARGIN + 165, 22, "|  HackerRank AI Technical Interview Preparation Guide")
            
            page_str = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(PAGE_WIDTH - MARGIN, 22, page_str)
        self.restoreState()

def build_pdf(output_path="e:/ML/HackerRank_SDE_Intern_AI_Interview_Preparation.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + 12,
        bottomMargin=MARGIN + 8
    )

    styles = getSampleStyleSheet()

    # Typography Styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=0,
        textColor=NAVY_PRIMARY
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        alignment=0,
        textColor=TEXT_MUTED
    )

    style_sec_title = ParagraphStyle(
        'SecTitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13,
        textColor=HexColor('#FFFFFF')
    )

    style_sec_sub = ParagraphStyle(
        'SecSub',
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=HexColor('#E2E8F0')
    )

    style_subheading = ParagraphStyle(
        'SubHeading',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=NAVY_PRIMARY,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        alignment=4, # Justified
        textColor=TEXT_DARK,
        spaceAfter=3
    )

    style_body_bold = ParagraphStyle(
        'BodyBold',
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11.2,
        textColor=TEXT_DARK
    )

    style_bullet = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        alignment=4,
        textColor=TEXT_DARK,
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=2
    )

    style_card_q = ParagraphStyle(
        'CardQ',
        fontName='Helvetica-Bold',
        fontSize=8.6,
        leading=11.5,
        textColor=NAVY_PRIMARY
    )

    style_card_ans = ParagraphStyle(
        'CardAns',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        alignment=4,
        textColor=TEXT_DARK
    )

    style_card_why = ParagraphStyle(
        'CardWhy',
        fontName='Helvetica-Oblique',
        fontSize=7.6,
        leading=10,
        textColor=TEXT_MUTED
    )

    style_table_head = ParagraphStyle(
        'TableHead',
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.5,
        alignment=1,
        textColor=HexColor('#FFFFFF')
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.6,
        leading=10,
        textColor=TEXT_DARK
    )

    style_table_cell_center = ParagraphStyle(
        'TableCellCenter',
        fontName='Helvetica',
        fontSize=7.6,
        leading=10,
        alignment=1,
        textColor=TEXT_DARK
    )

    style_table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.6,
        leading=10,
        textColor=NAVY_PRIMARY
    )

    style_tag = ParagraphStyle(
        'Tag',
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.5,
        alignment=2,
        textColor=BLUE_ACCENT
    )

    style_practice_line = ParagraphStyle(
        'PracticeLine',
        fontName='Helvetica',
        fontSize=7.2,
        leading=10,
        textColor=HexColor('#94A3B8')
    )

    story = []

    # Helper: Section Header Banner
    def make_section_banner(title, subtitle=None):
        content = [Paragraph(f"<b>{title.upper()}</b>", style_sec_title)]
        if subtitle:
            content.append(Spacer(1, 1))
            content.append(Paragraph(subtitle, style_sec_sub))
        t = Table([[content]], colWidths=[CONTENT_WIDTH])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), NAVY_PRIMARY),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        res = [Spacer(1, 4), t, Spacer(1, 4)]
        return res

    # Helper: QA Card
    def make_qa_card(q_num, question, category, model_answer, why_it_works, framework_note=None):
        header_p1 = Paragraph(f"<b>Question {q_num}: {question}</b>", style_card_q)
        header_p2 = Paragraph(f"<b>{category.upper()}</b>", style_tag)
        
        t_head = Table([[header_p1, header_p2]], colWidths=[CONTENT_WIDTH - 85, 75])
        t_head.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))

        p_ans_label = Paragraph(f"<b><font color='{NAVY_SECONDARY}'>Model Interview Response:</font></b>", style_body_bold)
        p_ans = Paragraph(f'"{model_answer}"', style_card_ans)
        
        why_label_text = "Engineering Insight & Key Takeaway:" if not framework_note else f"Framework ({framework_note}) & Recruiter Strategy:"
        p_why_label = Paragraph(f"<b><font color='{BLUE_ACCENT}'>{why_label_text}</font></b>", style_body_bold)
        p_why = Paragraph(why_it_works, style_card_why)

        card_table = Table([[t_head], [p_ans_label], [p_ans], [p_why_label], [p_why]], colWidths=[CONTENT_WIDTH])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), BG_HIGHLIGHT),
            ('BACKGROUND', (0, 1), (-1, 2), BG_CARD),
            ('BACKGROUND', (0, 3), (-1, 4), BG_LIGHT),
            ('BOX', (0, 0), (-1, -1), 0.75, BORDER_LIGHT),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, BORDER_LIGHT),
            ('LINEBELOW', (0, 2), (-1, 2), 0.5, LINE_GRAY),
            ('LEFTPADDING', (0, 0), (-1, -1), 7),
            ('RIGHTPADDING', (0, 0), (-1, -1), 7),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ]))
        return KeepTogether([card_table, Spacer(1, 3.5)])

    # Helper: Technical Scenario Card (5-Step Breakdown)
    def make_scenario_card(q_num, title, scenario_prompt, steps):
        """
        steps is a dict with keys: 'understand', 'investigate', 'solution', 'test', 'prevent'
        """
        header_p1 = Paragraph(f"<b>Scenario {q_num}: {title}</b>", style_card_q)
        header_p2 = Paragraph(f"<b>APPLIED SCENARIO</b>", style_tag)
        
        t_head = Table([[header_p1, header_p2]], colWidths=[CONTENT_WIDTH - 110, 100])
        t_head.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))

        p_prompt = Paragraph(f"<b>Problem Situation:</b> <i>'{scenario_prompt}'</i>", style_card_ans)

        step_rows = [
            Paragraph("<b>1. Understand the Problem:</b> " + steps['understand'], style_card_ans),
            Paragraph("<b>2. Investigate & Isolate:</b> " + steps['investigate'], style_card_ans),
            Paragraph("<b>3. Implement Solution:</b> " + steps['solution'], style_card_ans),
            Paragraph("<b>4. Verify & Test:</b> " + steps['test'], style_card_ans),
            Paragraph("<b>5. Prevent Recurrence:</b> " + steps['prevent'], style_card_ans)
        ]

        card_content = [[t_head], [p_prompt]] + [[p] for p in step_rows]

        card_table = Table(card_content, colWidths=[CONTENT_WIDTH])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), BG_HIGHLIGHT),
            ('BACKGROUND', (0, 1), (-1, 1), BG_CARD),
            ('BACKGROUND', (0, 2), (-1, -1), BG_LIGHT),
            ('BOX', (0, 0), (-1, -1), 0.75, BORDER_LIGHT),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, BORDER_LIGHT),
            ('LINEBELOW', (0, 1), (-1, 1), 0.5, LINE_GRAY),
            ('LEFTPADDING', (0, 0), (-1, -1), 7),
            ('RIGHTPADDING', (0, 0), (-1, -1), 7),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        return KeepTogether([card_table, Spacer(1, 4)])

    # Helper: Callout Box
    def make_callout(title, text_paragraphs, border_color=NAVY_PRIMARY, bg_color=BG_LIGHT):
        content = [Paragraph(f"<b><font color='{border_color}'>{title}</font></b>", style_body_bold), Spacer(1, 1)]
        for p in text_paragraphs:
            if isinstance(p, str):
                content.append(Paragraph(p, style_body))
            else:
                content.append(p)
        t = Table([[content]], colWidths=[CONTENT_WIDTH])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('BOX', (0, 0), (-1, -1), 0.75, border_color),
            ('LEFTPADDING', (0, 0), (-1, -1), 7),
            ('RIGHTPADDING', (0, 0), (-1, -1), 7),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        return KeepTogether([t, Spacer(1, 3.5)])

    # ==========================================
    # 0. COVER PAGE & CANDIDATE PROFILE HEADER
    # ==========================================
    story.append(Paragraph("HACKERRANK SOFTWARE DEVELOPMENT ENGINEER INTERN", style_cover_title))
    story.append(Paragraph("<b>AI Interview Preparation Handbook</b>", ParagraphStyle('CoverTitle2', fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=NAVY_SECONDARY)))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Comprehensive Technical & Behavioral Guide for 2027 Engineering Graduates: 50+ Real-World Questions & Answers, Project Deep-Dives, Scenario Playbooks, and Core Revision", style_cover_sub))
    story.append(Spacer(1, 4))

    # Candidate Profile Header Card
    profile_data = [
        [
            Paragraph("<b>Candidate Name:</b>", style_table_cell_bold),
            Paragraph("Lloyd Gopi", style_table_cell),
            Paragraph("<b>Degree / Branch:</b>", style_table_cell_bold),
            Paragraph("B.E. Information Science & Engineering", style_table_cell)
        ],
        [
            Paragraph("<b>College / University:</b>", style_table_cell_bold),
            Paragraph("JNNCE, Shivamogga (VTU)", style_table_cell),
            Paragraph("<b>Graduation Year:</b>", style_table_cell_bold),
            Paragraph("2027 (Currently in 7th Semester)", style_table_cell)
        ],
        [
            Paragraph("<b>Primary Language:</b>", style_table_cell_bold),
            Paragraph("Python (Secondary: C++, Java, SQL, JS)", style_table_cell),
            Paragraph("<b>Target Role:</b>", style_table_cell_bold),
            Paragraph("SDE Intern (HackerRank, Bengaluru Onsite)", style_table_cell)
        ],
        [
            Paragraph("<b>Core CS Knowledge:</b>", style_table_cell_bold),
            Paragraph("Data Structures & Algorithms, OOP, DBMS, OS, Computer Networks", style_table_cell),
            Paragraph("<b>Tools & Frameworks:</b>", style_table_cell_bold),
            Paragraph("Flask, React, Node.js, Express, Git, Scapy, Npcap", style_table_cell)
        ],
        [
            Paragraph("<b>Machine Learning:</b>", style_table_cell_bold),
            Paragraph("Scikit-learn, TensorFlow, Pandas, NumPy, OpenCV, YOLO", style_table_cell),
            Paragraph("<b>Featured Projects:</b>", style_table_cell_bold),
            Paragraph("1. Zero-Trust AI NIDS | 2. AI Traffic YOLO | 3. QuickBite MERN", style_table_cell)
        ]
    ]
    t_profile = Table(profile_data, colWidths=[110, 153, 115, 149])
    t_profile.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, NAVY_PRIMARY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_profile)
    story.append(Spacer(1, 4))

    # Table of Contents
    toc_data = [
        [
            Paragraph("<b>Module</b>", style_table_head),
            Paragraph("<b>Module Title & Contents</b>", style_table_head),
            Paragraph("<b>Questions Covered</b>", style_table_head),
            Paragraph("<b>Strategic Focus & Methodology</b>", style_table_head)
        ],
        [
            Paragraph("<b>Module 1</b>", style_table_cell_center),
            Paragraph("<b>Interview Answering Frameworks</b>", style_table_cell_bold),
            Paragraph("5 Frameworks", style_table_cell_center),
            Paragraph("STAR method, 6-step technical solving, 6-stage project pitch, unknown questions, trade-offs.", style_table_cell)
        ],
        [
            Paragraph("<b>Module 2</b>", style_table_cell_center),
            Paragraph("<b>Section A: Introduction & Background</b>", style_table_cell_bold),
            Paragraph("Q1 - Q10 (10 Qs)", style_table_cell_center),
            Paragraph("Elevator pitch, technical journey, why HackerRank, strengths, weaknesses, proudest project.", style_table_cell)
        ],
        [
            Paragraph("<b>Module 3</b>", style_table_cell_center),
            Paragraph("<b>Section B: Project Deep-Dives</b>", style_table_cell_bold),
            Paragraph("Q11 - Q22 (12 Qs)", style_table_cell_center),
            Paragraph("In-depth analysis of Zero-Trust NIDS, AI Traffic YOLO, and QuickBite MERN platform.", style_table_cell)
        ],
        [
            Paragraph("<b>Module 4</b>", style_table_cell_center),
            Paragraph("<b>Section C: Applied Technical Scenarios</b>", style_table_cell_bold),
            Paragraph("Q23 - Q34 (12 Qs)", style_table_cell_center),
            Paragraph("5-step engineering playbooks: 500 errors, prod vs local, slow DB, latency, downtime, CI/CD.", style_table_cell)
        ],
        [
            Paragraph("<b>Module 5</b>", style_table_cell_center),
            Paragraph("<b>Section D: Collaboration & Behavioral</b>", style_table_cell_bold),
            Paragraph("Q35 - Q44 (10 Qs)", style_table_cell_center),
            Paragraph("STAR answers: team conflicts, code reviews, deadlines, mistakes, pressure, changing scopes.", style_table_cell)
        ],
        [
            Paragraph("<b>Module 6</b>", style_table_cell_center),
            Paragraph("<b>Section E: Motivation & Reverse Questions</b>", style_table_cell_bold),
            Paragraph("Q45 - Q50 (6 Qs)", style_table_cell_center),
            Paragraph("Intern goals, learning expectations, and high-impact questions to ask HackerRank engineers.", style_table_cell)
        ],
        [
            Paragraph("<b>Module 7</b>", style_table_cell_center),
            Paragraph("<b>Common Interview Mistakes to Avoid</b>", style_table_cell_bold),
            Paragraph("6 Anti-Patterns", style_table_cell_center),
            Paragraph("Robotic scripts, hand-waving, blaming teammates, resume inflation, lack of trade-off thinking.", style_table_cell)
        ],
        [
            Paragraph("<b>Module 8</b>", style_table_cell_center),
            Paragraph("<b>Last-Minute Technical Revision Sheets</b>", style_table_cell_bold),
            Paragraph("7 Cheat Sheets", style_table_cell_center),
            Paragraph("Python, OOP/SOLID, SQL/DBMS, Web/HTTP, Networking, DSA Complexities, Git workflows.", style_table_cell)
        ],
        [
            Paragraph("<b>Module 9</b>", style_table_cell_center),
            Paragraph("<b>Mock Interview Practice Simulation</b>", style_table_cell_bold),
            Paragraph("15 Mock Prompts", style_table_cell_center),
            Paragraph("Rigorous unanswered coding, systems, and behavioral questions for independent candidate practice.", style_table_cell)
        ],
        [
            Paragraph("<b>Module 10</b>", style_table_cell_center),
            Paragraph("<b>Final Pre-Interview Checklist</b>", style_table_cell_bold),
            Paragraph("Checklist Guide", style_table_cell_center),
            Paragraph("Actionable pre-interview, during-interview, and post-interview readiness protocols.", style_table_cell)
        ]
    ]
    t_toc = Table(toc_data, colWidths=[55, 160, 75, 237])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), BG_LIGHT]),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 4))

    # ==========================================
    # MODULE 1: INTERVIEW ANSWERING FRAMEWORKS
    # ==========================================
    story.append(PageBreak())
    story.extend(make_section_banner("Module 1: Interview Answering Frameworks", "Cognitive Blueprints for Structured, High-Impact Technical and Behavioral Delivery"))

    frameworks_info = [
        ("Framework 1: The STAR Behavioral Method (45 - 60 Seconds)",
         "Use this for any situational, behavioral, or interpersonal inquiry:<br/>"
         "- <b>Situation (10s):</b> Set the technical context concisely without unnecessary backstory.<br/>"
         "- <b>Task (10s):</b> State your exact responsibility or the challenge you had to overcome.<br/>"
         "- <b>Action (25s):</b> Detail the specific engineering actions you executed. Focus on 'I', not 'We'.<br/>"
         "- <b>Result (15s):</b> Conclude with measurable, quantifiable metrics and key learnings."),

        ("Framework 2: The 6-Step Technical Problem-Solving Protocol",
         "When given a live algorithmic, architectural, or debugging scenario:<br/>"
         "1. <b>Clarify & Bound:</b> Confirm inputs, edge cases (empty strings, negative values), and constraints.<br/>"
         "2. <b>Brute Force Baseline:</b> State the obvious naive solution and its complexity ($O(N^2)$).<br/>"
         "3. <b>Optimize with Data Structures:</b> Identify bottlenecks (e.g., using a Hash Map, Two Pointers, or Heap).<br/>"
         "4. <b>Communicate Trade-Offs:</b> Compare space vs. time complexity ($O(N)$ space for $O(N)$ time).<br/>"
         "5. <b>Write Clean, Modular Code:</b> Use descriptive variable names and handle null/empty checks.<br/>"
         "6. <b>Dry Run & Test:</b> Walk through a small test case manually, stepping through pointers."),

        ("Framework 3: The 6-Stage Project Pitch Framework",
         "When an interviewer says <i>'Tell me about your project'</i>:<br/>"
         "1. <b>Problem:</b> What real-world bottleneck or inefficiency does this address?<br/>"
         "2. <b>Architecture:</b> High-level decoupled tiers (Presentation, Gateway, Business Logic, Persistence).<br/>"
         "3. <b>Technology Stack:</b> Why specific languages, frameworks, or databases were selected.<br/>"
         "4. <b>Personal Contribution:</b> Exactly which modules, schemas, or pipelines you engineered.<br/>"
         "5. <b>Toughest Challenge:</b> A concrete technical hurdle (e.g., race conditions, packet loss).<br/>"
         "6. <b>Quantified Results:</b> Latency numbers, accuracy percentages, concurrent capacity."),

        ("Framework 4: Navigating the 'Graceful Unknown'",
         "When asked about an API, framework, or concept you have never encountered:<br/>"
         "- <b>Acknowledge Honestly:</b> <i>'I haven't deployed Redis in production yet, but I understand its role as an in-memory key-value cache.'</i><br/>"
         "- <b>Relate to First Principles:</b> Map it to concepts you know (e.g., LRU cache, RAM vs Disk latency).<br/>"
         "- <b>Explain Investigation Strategy:</b> <i>'If tasked with using it, I'd review the official docs, verify cache eviction policies (TTL/LRU), and test failure fallback behavior.'</i>"),

        ("Framework 5: Articulating Engineering Trade-Offs",
         "Great engineers never speak in absolutes; they speak in trade-offs:<br/>"
         "- <b>Time vs Space:</b> Pre-computing / caching speeds up reads but increases memory consumption.<br/>"
         "- <b>SQL vs NoSQL:</b> SQL provides ACID compliance and structured joins; NoSQL provides flexible schemas and horizontal write scaling.<br/>"
         "- <b>Microservices vs Monolith:</b> Microservices decouple fault domains but introduce network serialization and distributed tracing overhead.")
    ]

    for title, content in frameworks_info:
        story.append(make_callout(title, [content], border_color=NAVY_PRIMARY, bg_color=BG_LIGHT))

    # ==========================================
    # MODULE 2: SECTION A - INTRODUCTION & BACKGROUND (10 Qs)
    # ==========================================
    story.append(PageBreak())
    story.extend(make_section_banner("Module 2: Section A - Introduction & Background", "10 Foundational Screening and Behavioral Questions with Polished Fresher Answers"))

    sec_a_questions = [
        (
            1,
            "Tell me about yourself.",
            "Elevator Pitch",
            "I am Lloyd Gopi, currently in my 7th semester of B.E. in Information Science and Engineering at JNNCE, Shivamogga, graduating in 2027. My core technical strengths are in Python, C++, Java, and SQL, with a deep focus on backend systems, applied machine learning, and full-stack web engineering. Over the past three years, I have built three significant systems: an enterprise Zero-Trust Network Intrusion Detection System achieving sub-millisecond packet inference, an AI traffic monitoring pipeline using YOLO, and QuickBite, a full-stack food ordering platform with secure payment integration. I am eager to contribute to HackerRank as an SDE intern where I can build scalable developer tools and learn from senior engineers.",
            "Hits all core dimensions: identity, graduation year, core languages, 3 distinct projects, and role alignment in under 75 seconds."
        ),
        (
            2,
            "Walk me through your technical journey.",
            "Technical Journey",
            "My technical journey began with C and C++, where I developed a strong foundation in data structures, memory mechanics, and algorithmic problem-solving. As I advanced, I adopted Python for its versatility, using it to build RESTful APIs with Flask and implement machine learning models with Scikit-learn and TensorFlow. To broaden my engineering scope, I dove into full-stack development with React and Node.js, building interactive web platforms. In my final year, I combined these disciplines into systems engineering, working with raw Ethernet frames, Scapy, and network protocol reassembly. Each phase of my journey has been driven by moving from theoretical concepts to building end-to-end working software.",
            "Shows progressive, deliberate growth from low-level algorithms to web architecture and applied systems."
        ),
        (
            3,
            "Why did you choose software engineering as your career path?",
            "Career Motivation",
            "What draws me to software engineering is the unique blend of creative problem-solving and immediate, deterministic feedback. In college, writing an algorithm and seeing it pass edge cases after hours of debugging gave me immense satisfaction. Furthermore, software has zero physical latency to impact—code you write today can streamline operations for thousands of users tomorrow. Building projects like my intrusion detection system and seeing raw network traffic categorized in real time confirmed that I want to spend my career architecting resilient, high-impact systems.",
            "Demonstrates authentic passion grounded in the craft of debugging and real-world impact rather than generic prestige."
        ),
        (
            4,
            "Why do you specifically want to join HackerRank?",
            "Company Fit",
            "I have been an active user of HackerRank since my second year to practice algorithms and prepare for technical challenges, so contributing to the platform feels like coming full circle. Beyond personal use, I deeply respect HackerRank's mission of creating a skills-first world where developers are evaluated on their code rather than their background. From an engineering standpoint, building isolated code compilation sandboxes, managing low-latency collaborative interview environments, and scaling evaluation microservices across 40+ languages is the exact type of high-concurrency systems challenge I want to tackle.",
            "Shows real product loyalty, alignment with company values, and genuine excitement for HackerRank's engineering challenges."
        ),
        (
            5,
            "Why should we hire you over other candidates?",
            "Value Proposition",
            "You should hire me because I offer three distinct advantages: First, strong computer science fundamentals in data structures, algorithms, object-oriented design, and database systems. Second, proven execution capability—I haven't just completed toy tutorials; I've built an intrusion detection engine that processes 19,500 flows a second, a YOLO computer vision pipeline, and a full-stack MERN application with HMAC-secured payments. Third, high coachability and 100% logistical availability for an onsite 6-month internship in Bengaluru starting January 2027. I am ready to absorb feedback and ship production code.",
            "Delivers a clean three-pillar pitch: fundamental competence + demonstrated production-like projects + zero logistical friction."
        ),
        (
            6,
            "What are your strongest technical skills and programming languages?",
            "Technical Competence",
            "My strongest language is Python, which I use for backend microservices, data processing, and machine learning pipelines. For core algorithmic problem-solving and memory-conscious programming, I rely on C++. For object-oriented design and relational databases, I have solid working experience with Java and SQL. On the web side, I build responsive user interfaces using React and RESTful backends using Node.js and Flask. Across all these tools, my real strength lies in understanding how data flows across the stack—from network packets and database schemas to client state.",
            "Positions languages as tools to solve problems across different layers of the software engineering stack."
        ),
        (
            7,
            "What is your biggest technical weakness, and what are you doing to improve it?",
            "Self-Awareness",
            "Early in my engineering projects, my biggest weakness was jumping directly into writing code before thoroughly mapping out error-handling boundaries and API contracts. In my early web projects, this led to edge-case bugs during client-server integration. To address this, I adopted a strict design-first discipline: before writing any implementation code, I write out the API schema, list boundary edge cases, and define the data model. This upfront planning has dramatically reduced my debugging cycle and improved my code modularity.",
            "Presents a real, relatable engineering weakness and demonstrates a structured, disciplined habit implemented to resolve it."
        ),
        (
            8,
            "Which engineering project are you most proud of, and why?",
            "Proudest Project",
            "I am most proud of my Zero-Trust AI-Powered Network Intrusion Detection System. It challenged me across multiple domains: low-level networking, concurrent programming, and applied machine learning. I had to solve a difficult real-time bottleneck where synchronous ML inference was choking the live packet-sniffing loop. I resolved it by architecting an asynchronous flow manager using direction-agnostic 5-tuple canonical hashing and a thread-safe queue. Achieving 96.00% accuracy with 0.0512 millisecond per-flow latency on live Wi-Fi traffic made me proud of my systems engineering capability.",
            "Highlights end-to-end ownership, complex cross-disciplinary engineering (networks + ML + concurrency), and quantifiable results."
        ),
        (
            9,
            "What motivates you to learn new technologies, and how do you stay updated?",
            "Learning Agility",
            "I am motivated by solving practical engineering constraints. Rather than chasing every trending library, I learn a new technology when an existing tool cannot satisfy a requirement—such as learning Scapy when standard sockets couldn't dissect raw IP headers, or learning React Context when prop drilling made state unmanageable. I stay updated by reading engineering blogs from companies like HackerRank, Cloudflare, and Uber, exploring open-source repositories on GitHub, and solving real architectural challenges in personal projects.",
            "Demonstrates purposeful, pragmatic learning habits rather than superficial bandwagoning."
        ),
        (
            10,
            "Where do you see yourself in three years?",
            "Career Vision",
            "In three years, I see myself as a strong Software Development Engineer, taking end-to-end ownership of core backend services and developer infrastructure. I want to be the engineer who not only writes clean, high-throughput code, but also designs reliable distributed architectures, participates in critical code reviews, and mentors incoming interns. My goal is to build deep technical credibility in backend systems and distributed platforms.",
            "Strikes the ideal balance between ambition and grounded reality: focuses on engineering craftsmanship and team impact."
        )
    ]

    for q in sec_a_questions:
        story.append(make_qa_card(q[0], q[1], q[2], q[3], q[4]))

    # ==========================================
    # MODULE 3: SECTION B - PROJECT DEEP-DIVES (12 Qs)
    # ==========================================
    story.append(PageBreak())
    story.extend(make_section_banner("Module 3: Section B - Project Deep-Dives", "12 Technical Deep-Dive Inquiries Covering ZT-NIDS, QuickBite, and AI Traffic Analysis"))

    sec_b_questions = [
        (
            11,
            "Can you explain the overall architecture of your primary projects?",
            "System Architecture",
            "My primary project, the Zero-Trust NIDS, follows a decoupled four-tier microservices architecture: 1) Presentation Tier built in React 18 for live SOC operations telemetry; 2) API Gateway in Flask enforcing stateless HMAC-SHA256 JWT authentication and role-based access control; 3) Logic Tier hosting a stateful FlowManager that reassembles raw Ethernet frames into bidirectional conversations via 5-tuple hashing and dispatches them to an asynchronous LivePredictor queue; and 4) Persistence Tier managing SQLite relational schemas for audit logs and serialized model weights. Similarly, QuickBite follows a 3-tier MERN architecture with a React client, Express REST routing layer, and MongoDB document persistence.",
            "Demonstrates strong architectural vocabulary: tier decoupling, fault isolation, stateful flow management, and clear data contracts."
        ),
        (
            12,
            "What specific real-world problems do each of your three projects solve?",
            "Problem Statement",
            "First, the Zero-Trust NIDS solves the failure of legacy castle-and-moat security against internal lateral attacks, while eliminating the widespread academic flaw of train-test data leakage. Second, QuickBite addresses the high 20-30% aggregator commission fees burdening local restaurants by providing a lightweight, direct-to-consumer digital ordering channel with cryptographically verified payments. Third, the AI Traffic Analysis project solves manual, error-prone vehicle counting by deploying a YOLO-based computer vision pipeline to automate multi-class vehicle detection across traffic video streams.",
            "Clearly articulates the 'why' behind all three projects, showing business/operational awareness across security, web, and AI."
        ),
        (
            13,
            "Why did you choose your specific technology stacks for these projects?",
            "Technology Selection",
            "For ZT-NIDS, I chose Python and Flask because of Python's rich ecosystem for raw packet dissection (Scapy) and machine learning (Scikit-learn). For the model, I selected an SVM with an RBF kernel because it provides non-linear boundary separation with sub-millisecond execution (0.05ms), unlike deep recurrent nets that introduce unacceptable inference latency on live packet streams. For QuickBite, I chose the MERN stack because Node's asynchronous event loop excels at handling high-concurrency I/O (like 1,000+ simultaneous food orders), while MongoDB's flexible schema easily accommodates varying restaurant menu structures.",
            "Explains technology selection based on engineering trade-offs (I/O performance, execution latency) rather than personal familiarity."
        ),
        (
            14,
            "What was your individual contribution to these projects?",
            "Individual Contribution",
            "In the Zero-Trust NIDS team project, I served as lead developer responsible for the core systems and security layers. Specifically, I engineered the stateful FlowManager, implemented the direction-agnostic 5-tuple canonical hashing algorithm, built the Flask JWT authorization middleware, and developed the asynchronous packet queue. In QuickBite, which I built individually, I developed the complete stack: the responsive React frontend, 15+ REST endpoints, MongoDB schemas, and the server-side HMAC-SHA256 payment signature verification. In the AI Traffic project, I configured the YOLO pipeline, tuned confidence thresholds, and built the Streamlit interface.",
            "Clearly delineates exact modules, algorithms, and endpoints built personally without taking undue credit for team efforts."
        ),
        (
            15,
            "What was the most difficult technical bottleneck you encountered across your projects?",
            "Technical Roadblock",
            "In ZT-NIDS, the most difficult bottleneck was packet loss during live network sniffing. When running Scapy in promiscuous mode on high-throughput Wi-Fi, executing model feature scaling and inference synchronously inside the packet capture callback choked the CPU. Packets arrived faster than the callback could finish, causing the OS kernel buffer to overflow and drop frames. In QuickBite, a major challenge was preventing client-side payment spoofing where malicious users could tamper with the HTTP POST payload to mark unpaid orders as completed.",
            "Identifies genuine production-grade engineering bottlenecks: kernel socket buffer overflow and financial transaction tampering."
        ),
        (
            16,
            "How did you systematically debug and resolve those bottlenecks?",
            "Debugging & Resolution",
            "To solve the packet-drop bottleneck in ZT-NIDS, I decoupled capture from inference using an asynchronous producer-consumer pattern. The Scapy sniffer ran in a lightweight background thread whose only job was extracting raw packet headers and pushing them into a Python thread-safe `Queue`. A separate worker pool popped batches of flows, extracted 5-tuple features, and ran model inference independently. This eliminated kernel buffer backpressure and reduced latency to 0.0512 ms per flow. For QuickBite, I enforced server-side cryptographic verification: the payment gateway's HMAC-SHA256 signature was computed using a private webhook secret and verified against the gateway payload before any order was marked 'PAID'.",
            "Walks through systematic architectural solutions: producer-consumer queuing for I/O decoupling and HMAC verification for integrity."
        ),
        (
            17,
            "How did you test your applications for correctness, performance, and security?",
            "Testing Methodology",
            "For ZT-NIDS, I enforced a strict 70/15/15 stratified train-validation-test split strictly before fitting any StandardScaler or encoder to prevent data leakage. I benchmarked model convergence using the Frobenius weight displacement norm across 10 epochs and evaluated 3,750 unseen holdout flows from UNSW-NB15. For live testing, I replayed 1,384 recorded sessions through physical network interfaces. For QuickBite, I tested all 15+ REST API endpoints using Postman, verifying boundary validation (negative quantities, empty carts, malformed JWTs) and simulating concurrent checkouts to ensure database atomicity.",
            "Covers multiple testing layers: statistical data-leakage prevention, mathematical convergence, live replay, and API boundary testing."
        ),
        (
            18,
            "How would you scale your systems if traffic increased by 100x?",
            "System Scalability",
            "To scale ZT-NIDS by 100x, I would transition from user-space Scapy sniffing to kernel-bypass eBPF (Extended Berkeley Packet Filter) or DPDK, eliminating user-kernel context switching. I would replace the in-memory queue with Apache Kafka to ingest millions of flow events and distribute inference across a cluster of stateless Triton inference servers. For QuickBite, I would implement Redis caching for frequently read restaurant menus, introduce read-replicas for MongoDB, containerize the Node.js API with Kubernetes for horizontal auto-scaling, and place a CDN in front of static React assets.",
            "Demonstrates clear knowledge of horizontal scaling: kernel-bypass, distributed event streaming (Kafka), caching (Redis), and container orchestration."
        ),
        (
            19,
            "What would you improve or refactor if you had three more months of engineering time?",
            "Engineering Roadmap",
            "In ZT-NIDS, I would implement automated inline mitigation: currently, the system detects threats and alerts the dashboard; I would integrate with iptables or an SDN controller to dynamically inject firewall drop rules for high-risk IPs. I would also add explainable AI (SHAP or LIME) so analysts understand why a flow was flagged. In QuickBite, I would add WebSockets for real-time order tracking and GPS driver coordinates instead of HTTP polling. In the traffic project, I would integrate DeepSORT tracking algorithms to maintain unique vehicle IDs across frames rather than just detecting per-frame instances.",
            "Shows mature technical vision: closed-loop mitigation, real-time bidirectional communication, and multi-object tracking."
        ),
        (
            20,
            "How did you ensure security, authentication, and data integrity across your applications?",
            "Security Engineering",
            "I adhered strictly to the NIST SP 800-207 Zero-Trust principle of 'Never Trust, Always Verify'. In ZT-NIDS, user credentials undergo 12-round salted Bcrypt hashing, and all REST endpoints require time-bounded (1-hour) HMAC-SHA256 JWT tokens with Role-Based Access Control decorators (`@require_role(['Admin', 'Analyst'])`). Every authentication event and model dispatch is written to an immutable SQLite audit ledger with 1,316 verified cryptographic logs. In QuickBite, I sanitized user inputs against NoSQL injection, set HTTP-only secure cookie flags, and used HMAC signatures to prevent transaction tampering.",
            "Cites established security standards (NIST Zero Trust, Bcrypt, JWT RBAC, HMAC verification) and concrete implementation details."
        ),
        (
            21,
            "Can you explain a difficult technical trade-off you made during implementation?",
            "Engineering Trade-Offs",
            "In ZT-NIDS, I evaluated four candidate models: SVM with RBF kernel, Deep LSTM, Deep MLP, and Regularized Logistic Regression. Logistic Regression was the fastest (<0.01ms), but suffered an unacceptable 17.77% False Positive Rate. LSTM achieved 0% false alarms under strict confidence gating, but recurrent state unrolling took 0.385 ms per flow—too slow for line-rate traffic. I chose the SVM with RBF kernel: it achieved 96.00% accuracy, a low 2.22% FPR, and an inference latency of 0.0512 ms per flow. Trading off a fraction of deep theoretical capacity gave me a 7.5x speedup that allowed real-time processing on standard CPUs.",
            "Outstanding example of real-world trade-off analysis: latency vs. accuracy vs. false alarm rate across concrete numbers."
        ),
        (
            22,
            "What were the most important engineering lessons you learned from building these projects?",
            "Retrospective & Growth",
            "The most important lesson was that building working software is only 20% about the core algorithm and 80% about system plumbing—data ingestion boundaries, asynchronous queueing, concurrency, error handling, and state synchronization. In machine learning, I learned that a clean, leakage-free data pipeline matters more than hyperparameter tuning. In web development, I learned that security cannot be an afterthought; validating payloads and cryptographic signatures must be built into the architectural foundation. These projects transformed me from someone who writes code into someone who designs systems.",
            "Deeply reflective and mature answer that resonates strongly with senior engineering interviewers."
        )
    ]

    for q in sec_b_questions:
        story.append(make_qa_card(q[0], q[1], q[2], q[3], q[4]))

    # ==========================================
    # MODULE 4: SECTION C - APPLIED TECHNICAL SCENARIOS (12 Qs)
    # ==========================================
    story.append(PageBreak())
    story.extend(make_section_banner("Module 4: Section C - Applied Technical Scenarios", "12 Production Engineering Scenarios with 5-Step Diagnostic and Resolution Playbooks"))

    scenarios = [
        (
            23,
            "API Suddenly Returns HTTP 500 Internal Server Errors",
            "A critical public REST API endpoint that was previously stable suddenly begins responding with HTTP 500 Internal Server Error for 25% of incoming user requests.",
            {
                'understand': "HTTP 500 indicates an unhandled server-side exception. The fact that it impacts 25% of requests suggests it is tied either to specific payload attributes, a degrading dependency (like a database pool), or a specific container instance behind the load balancer.",
                'investigate': "Check centralized error logs (CloudWatch/ELK) filtered by status=500. Inspect stack traces, correlate timestamps with recent deployments or traffic spikes, and check if errors originate from a single server instance or specific input parameters (e.g., null values).",
                'solution': "If caused by an unhandled edge case (e.g., missing payload key), wrap the execution in defensive validation with HTTP 400 Bad Request. If caused by database connection exhaustion, increase pool size or restart unhealthy instances.",
                'test': "Reproduce the failing request payload in staging. Run integration tests with null and boundary payloads to verify the endpoint returns 400 instead of crashing with 500.",
                'prevent': "Implement global exception handler middleware, enforce payload schema validation (e.g., Pydantic/Joi), and set up automated alerting on 5xx error rate thresholds."
            }
        ),
        (
            24,
            "Code Works Locally in Development but Fails in Production",
            "A newly developed feature passes all local tests and executes cleanly on your development machine, but immediately crashes upon deployment to the production environment.",
            {
                'understand': "The discrepancy indicates environment drift: differences in runtime versions, environment variables, operating system dependencies, file permissions, or external network accessibility.",
                'investigate': "Compare production runtime logs against local logs. Verify all required environment variables (.env / secrets manager) are populated in production. Check database schema migrations—did the production database receive the latest table columns?",
                'solution': "Inject missing environment variables, run pending database migrations, or update runtime dependencies to match the local specification.",
                'test': "Test the exact container image in a staging environment that mirrors production data and network topologies before promoting to production.",
                'prevent': "Containerize the application using Docker to ensure environment parity ('build once, run anywhere'). Add automated CI checks to validate environment variable schemas on startup."
            }
        ),
        (
            25,
            "Application Becomes Sluggish Under Heavy Peak Traffic",
            "During a campus recruitment drive or marketing campaign, your web service's latency spikes from 150ms to 4.5 seconds, and requests begin timing out.",
            {
                'understand': "Latency spikes under load typically stem from CPU/Memory saturation, synchronous blocking I/O, database connection pool exhaustion, or unindexed database queries.",
                'investigate': "Check server resource metrics (CPU, RAM, disk I/O, network bandwidth). Inspect database slow query logs and active connection counts. Profile the application thread pool to see where execution time is spent.",
                'solution': "Implement caching with Redis for hot read queries. Scale horizontally by spinning up additional application container replicas behind the load balancer. Optimize database connection pooling.",
                'test': "Perform load testing using tools like Locust or Apache JMeter, ramping up virtual users to 2x expected peak traffic to verify response latency remains under 200ms.",
                'prevent': "Set up auto-scaling rules based on CPU and request queue depth. Enforce pagination on all list endpoints to avoid loading thousands of records into memory at once."
            }
        ),
        (
            26,
            "A Critical Database Query Takes an Unacceptable Amount of Time",
            "An essential SQL query retrieving order histories or user profiles that previously executed in 15ms now takes 3.8 seconds, degrading the entire dashboard.",
            {
                'understand': "Query slowdowns as tables grow almost always indicate a missing index, forcing a full table scan ($O(N)$), or an inefficient Cartesian join across unindexed foreign keys.",
                'investigate': "Run `EXPLAIN ANALYZE` on the slow query in a development replica. Inspect whether the database engine uses an Index Scan or a Sequential/Full Table Scan.",
                'solution': "Add a composite B-Tree index on the filtered and joined columns (e.g., `CREATE INDEX idx_user_orders ON orders(user_id, created_at DESC);`). Eliminate `SELECT *` in favor of selecting only required columns.",
                'test': "Re-run `EXPLAIN ANALYZE` to confirm the query execution plan shifts to an Index Scan and verify execution time drops back below 20ms on production-scale datasets.",
                'prevent': "Establish slow query alerts in the database engine (threshold > 100ms) and conduct query review during peer pull requests for any new database queries."
            }
        ),
        (
            27,
            "Critical Bug Discovered 15 Minutes Before Production Deployment",
            "A high-severity bug that causes cart checkout calculations to miscalculate tax on certain currency formats is discovered right before a scheduled release.",
            {
                'understand': "A financial calculation bug directly compromises business integrity and customer trust. Delivering on time is never worth shipping known financial inaccuracies.",
                'investigate': "Determine the scope of the bug. Can it be hotfixed with 100% confidence in 5 minutes, or does it require modifying core transaction logic and re-testing?",
                'solution': "Immediately halt the deployment. Inform the engineering lead and stakeholders transparently. Abort the release pipeline and revert to the stable release candidate.",
                'test': "Write failing unit tests covering the exact edge cases causing the tax miscalculation. Implement the fix, run the complete regression test suite, and verify edge cases.",
                'prevent': "Enhance automated pre-merge test suites to include comprehensive edge-case suites (currency rounding, multi-locale inputs) so bugs are caught days before release."
            }
        ),
        (
            28,
            "Two Distinct Engineering Solutions Are Proposed for the Same Problem",
            "Your team is debating two architectures: Solution A uses an in-memory Redis cache with high performance but potential data loss risk; Solution B writes directly to PostgreSQL with durability but higher latency.",
            {
                'understand': "Engineering decisions are fundamentally about trade-offs aligned with business requirements. There is no universally 'superior' tool—only the right tool for specific constraints.",
                'investigate': "Define the governing constraints: Is this data mission-critical financial data (requiring strict ACID durability) or ephemeral session telemetry (requiring sub-millisecond speed)?",
                'solution': "If durability is paramount (e.g., payment states), choose Solution B, optimizing with write-ahead logs or batching. If speed is paramount and data is recreatable (e.g., leaderboard stats), choose Solution A with periodic disk snapshots. Alternatively, combine them: write-through caching.",
                'test': "Build a lightweight proof-of-concept (POC) benchmarking latency, throughput, and memory consumption for both approaches under simulated failure scenarios.",
                'prevent': "Document the final decision and rationale in an Architectural Decision Record (ADR) in the repository so future engineers understand why the trade-off was chosen."
            }
        ),
        (
            29,
            "A Teammate Accidentally Merges a Breaking Bug into Main Branch",
            "A peer's pull request was merged into the shared `main` branch, breaking local development environments and failing the continuous integration build.",
            {
                'understand': "The immediate priority is restoring team productivity and unblocking the deployment pipeline. Assigning blame does not fix the broken build.",
                'investigate': "Inspect the CI build logs to identify the exact commit hash and breaking error. Determine whether the fix is trivial (e.g., missing import) or architectural.",
                'solution': "If the fix takes more than 5 minutes, immediately execute a clean `git revert <commit-hash>` and push it to `main` to restore a green build. Notify the team in Slack.",
                'test': "Help the teammate reproduce the issue on a separate feature branch. Guide them in writing unit tests that reproduce the failure before re-submitting the PR.",
                'prevent': "Configure GitHub branch protection rules: require status checks to pass before merging, enforce mandatory peer review approvals, and disallow direct pushes to `main`."
            }
        ),
        (
            30,
            "Application Experiences Unexpected Downtime with No Obvious Logs",
            "A production service abruptly stops responding to requests. Checking the application log file reveals it suddenly stopped writing logs with no error or exception trace.",
            {
                'understand': "When an application process vanishes without leaving an exception trace, it usually indicates an external OS-level kill (such as Linux OOM Killer) or a fatal segmentation fault.",
                'investigate': "Check OS system logs using `dmesg -T` or `/var/log/messages`. Look for `Out of memory: Kill process` (OOM-killer). Check server disk space (`df -h`)—a 100% full disk halts logging instantly.",
                'solution': "If killed by OOM, increase memory limits, restart the service, and profile the codebase for memory leaks. If caused by a full disk, rotate and compress old log archives.",
                'test': "Monitor memory consumption under steady traffic using memory profilers (e.g., `tracemalloc` in Python) to ensure memory stabilizes rather than growing monotonically.",
                'prevent': "Set up log rotation (`logrotate`), establish alerts on disk usage > 85%, and configure container memory limits with proactive warnings at 80% RAM utilization."
            }
        ),
        (
            31,
            "An API Endpoint Receives Malformed or Malicious User Input",
            "An endpoint accepting JSON order payloads receives malformed structures, unexpected types (string instead of integer for price), and SQL/script injection strings.",
            {
                'understand': "Never trust client-side data. Malformed inputs can cause unhandled crashes (500s), corrupt database state, or expose SQL/NoSQL injection and XSS vulnerabilities.",
                'investigate': "Inspect API request logs to identify attack patterns. Verify whether validation is currently handled ad-hoc inside business logic rather than at the gateway boundary.",
                'solution': "Implement strict schema validation middleware (e.g., Pydantic in Python or Joi/Zod in Node.js). Enforce type checking, field length limits, and reject unexpected keys with HTTP 422/400. Use parameterized queries for all database interactions.",
                'test': "Write fuzz testing suites passing malformed JSON, boundary values (negative prices, integer overflows), and injection payloads to verify the API safely returns 400 Bad Request.",
                'prevent': "Adopt declarative schema validation across all endpoints and enforce automated security scanners (SAST/DAST) in the continuous integration pipeline."
            }
        ),
        (
            32,
            "Automated CI/CD Deployment Fails Mid-Way During Migration",
            "During a deployment, a database migration script alters two tables successfully but fails on the third table due to a foreign key constraint violation, leaving the database in an inconsistent state.",
            {
                'understand': "A partial migration leaves the database schema out of sync with application code, preventing both the old and new code versions from functioning correctly.",
                'investigate': "Review the migration logs to identify the exact constraint failure. Check if the database engine supports transactional DDL (e.g., PostgreSQL supports transactional DDL; MySQL does not).",
                'solution': "Roll back the database schema to the previous migration checkpoint using a rollback script. If transactional DDL was active, the transaction rolled back automatically. Re-deploy the previous stable application version.",
                'test': "Replicate the migration against a staging database containing a sanitized dump of production data to uncover constraint conflicts before touching production.",
                'prevent': "Wrap migrations in transactions wherever supported. Separate schema expansions from code deployments (the Expand-and-Contract migration pattern)."
            }
        ),
        (
            33,
            "Critical Security Vulnerability (CVE) Disclosed in a Third-Party Dependency",
            "A critical Remote Code Execution (RCE) vulnerability is announced in an open-source library that your backend microservice imports for processing file uploads.",
            {
                'understand': "An unpatched RCE vulnerability provides an immediate attack vector for external attackers to compromise the host server and access private data.",
                'investigate': "Verify if your service is using the vulnerable library version and whether your application code actually invokes the vulnerable method or function.",
                'solution': "If a patched version is available, immediately bump the dependency version in `requirements.txt` or `package.json`, run integration tests, and deploy a hotfix. If no patch exists, disable the affected feature or introduce input sanitization to block the exploit payload.",
                'test': "Deploy the updated dependency to a staging environment and execute end-to-end integration tests to verify no breaking API changes occurred in the library bump.",
                'prevent': "Integrate automated software composition analysis (SCA) tools like GitHub Dependabot, Snyk, or OWASP Dependency-Check to alert on vulnerable packages before deployment."
            }
        ),
        (
            34,
            "You Must Learn and Deliver in an Unfamiliar Framework on an Urgent Deadline",
            "Your engineering pod needs an urgent internal microservice built in Go or Ruby on Rails—technologies you have never used before—with delivery required in two weeks.",
            {
                'understand': "Programming languages and frameworks are implementations of fundamental computer science concepts. Strong fundamentals make language syntax quickly transferable.",
                'investigate': "Inspect existing repositories in the company written in that framework. Identify standard architectural conventions: routing patterns, database ORM usage, and testing setup.",
                'solution': "Spend day one building a minimal 'Hello World' service with one database read/write. Replicate patterns from existing codebase templates rather than reinventing conventions. Break the two-week goal into daily milestones.",
                'test': "Write comprehensive unit tests for each module as you build it. Use linters and language formatters (`gofmt`, `rubocop`) to adhere strictly to idiomatic standards.",
                'prevent': "Engage in pair programming with a senior teammate early on for feedback, and document your learnings in internal wiki notes for future onboarders."
            }
        )
    ]

    for s in scenarios:
        story.append(make_scenario_card(s[0], s[1], s[2], s[3]))

    # ==========================================
    # MODULE 5: SECTION D - COLLABORATION & BEHAVIORAL (10 Qs)
    # ==========================================
    story.append(PageBreak())
    story.extend(make_section_banner("Module 5: Section D - Collaboration & Behavioral Questions", "10 STAR-Formatted Scenarios Demonstrating Maturity, Teamwork, and Engineering Ownership"))

    sec_d_questions = [
        (
            35,
            "Describe a challenging technical situation you navigated and how you saw it through.",
            "Technical Resilience",
            "During the development of our Zero-Trust NIDS capstone, our goal was real-time packet classification. However, during initial testing with Scapy, our callback thread dropped over 30% of incoming packets due to synchronous ML inference lag. As the lead developer, I was responsible for solving this throughput failure. I redesigned the architecture by decoupling packet sniffing from inference using a producer-consumer model with Python's thread-safe Queue and multi-threading. This decoupled the packet ingestion rate from the model scoring cycle, completely eliminating dropped packets and sustaining an inference latency of 0.0512 ms per flow. It taught me that systems engineering is fundamentally about managing concurrent I/O boundaries.",
            "STAR Breakdown: S: NIDS capstone packet drop -> T: Solve throughput bottleneck -> A: Decoupled async producer-consumer queue -> R: 0 dropped packets, 0.05ms latency.",
            "STAR"
        ),
        (
            36,
            "Tell me about a technical disagreement you had with a teammate and how you resolved it.",
            "Conflict Resolution",
            "In our QuickBite food ordering project, my teammate wanted to store all restaurant menus, active shopping carts, and order histories in MongoDB as unstructured JSON documents for maximum development speed. I disagreed, advocating for structured document schemas with strict validation rules and relational foreign keys for orders to prevent cart inconsistencies and orphaned records. To resolve the impasse objectively, I built a quick prototype demonstrating how an unvalidated cart schema could result in negative item quantities and corrupted checkout prices. Seeing the concrete proof, my teammate agreed, and we implemented schema validation using Mongoose schemas with pre-save integrity hooks. We delivered the project without any cart state bugs.",
            "STAR Breakdown: S: Disagreement on MongoDB schema validation -> T: Agree on data integrity -> A: Built concrete POC proving failure mode -> R: Team aligned on validated schema.",
            "STAR"
        ),
        (
            37,
            "How do you handle tough criticism or pushback on your code during peer review?",
            "Receptivity & Growth",
            "I view code reviews as one of the highest-leverage learning opportunities in software engineering. Early in our capstone project, I submitted a pull request with an efficient algorithm that worked, but a teammate rightly commented that my variable names were cryptic and my 80-line function lacked modular decomposition. Instead of feeling defensive, I thanked them for the feedback, refactored the function into three single-responsibility helper methods, added type annotations, and updated the PR. The refactored code was significantly easier to read and test. Since then, I actively ask peers to scrutinize my code for readability and maintainability.",
            "Demonstrates zero ego, high coachability, and deep respect for clean code and team maintainability.",
            "STAR"
        ),
        (
            38,
            "How do you manage multiple competing academic and project deadlines simultaneously?",
            "Time Management",
            "During my 6th semester, I faced a major crunch: final semester examinations overlapped with our capstone project evaluation milestone and submission of an IEEE research paper. To avoid falling behind, I applied engineering prioritization principles: I broke down project deliverables into daily two-hour milestones, prioritized tasks by urgency and dependency blockers, and communicated transparently with our project guide. I dedicated mornings to exam preparation and evenings to code commits. As a result, our team submitted the research paper ahead of deadline, delivered a successful capstone demonstration, and I maintained a strong academic GPA.",
            "STAR Breakdown: S: Exam, capstone, and paper overlap -> T: Deliver all 3 without quality drop -> A: Modular daily sprints & dependency prioritization -> R: Successful on-time delivery across all fronts.",
            "STAR"
        ),
        (
            39,
            "What would you do if a project teammate fell behind and missed an agreed deadline?",
            "Empathy & Accountability",
            "In our final-year capstone team, a teammate responsible for connecting the Flask API endpoints to our React dashboard missed their agreed sprint deadline, threatening our faculty evaluation. Rather than complaining or blaming them, I set up a call to understand what was blocking them. I discovered they were struggling with CORS configuration and handling asynchronous JWT storage in React state. I sat down with them for a two-hour pair-programming session, walked through the CORS middleware fix, and helped them implement local storage token handling. They completed the integration the following day, and our team presented a fully functioning dashboard on schedule.",
            "Demonstrates leadership, empathy, and collaborative ownership: solves the problem instead of complaining.",
            "STAR"
        ),
        (
            40,
            "Tell me about a technical mistake you made, how you resolved it, and what you learned.",
            "Learning from Failure",
            "In an early version of our NIDS preprocessing pipeline, I fitted a StandardScaler across the entire combined dataset before performing the train-test split. The model achieved a suspiciously high 99.4% accuracy. When I audited the code, I realized I had committed the classic machine learning error of data leakage—the test set variance had leaked into the training scaling parameters. I immediately discarded the results, refactored the pipeline to enforce strict 70/15/15 stratified partitioning prior to fitting any scaler or encoder, and re-trained from scratch. Accuracy dropped to an honest, defensible 96.00%. It taught me to never celebrate unrealistic metrics and reinforced the paramount importance of data integrity.",
            "Exceptional answer: acknowledges an authentic engineering mistake (data leakage), explains the fix, and highlights intellectual honesty.",
            "STAR"
        ),
        (
            41,
            "How do you respond during an interview or team discussion when you don't know the answer?",
            "Intellectual Honesty",
            "When I don't know the answer to a question, I never guess or pretend to know. I start by acknowledging honestly that I haven't encountered that specific tool or concept yet. Then, I share my thought process from first principles. For example, if asked about distributed consensus algorithms like Raft, I would say: 'I haven't implemented Raft directly, but I understand the fundamental challenge is ensuring distributed nodes agree on state even when network partitions occur. If tasked with implementing it, I would research leader election protocols and log replication mechanisms.' Interviewers appreciate honesty paired with analytical reasoning.",
            "Highlights honesty, first-principles logic, and problem-solving readiness.",
            "STAR"
        ),
        (
            42,
            "Describe a time you had to learn something complex in a very short timeframe.",
            "Rapid Learning",
            "When developing our AI Traffic Monitoring system, I had only ten days to deliver a working computer vision pipeline for our department technical symposium, having only worked with standard classification models before. I immersed myself in computer vision literature, studied the YOLO Darknet architecture, and learned how single-stage object detection divides images into grid cells with bounding box regression. I spent three days experimenting with OpenCV video frame capture and fine-tuning confidence thresholds. Within a week, I built a working Streamlit dashboard that processed video feeds and classified vehicles with ~90% accuracy. It proved to me that strong CS fundamentals enable rapid technology acquisition.",
            "Demonstrates high learning speed, self-drive, and successful project delivery under aggressive timelines.",
            "STAR"
        ),
        (
            43,
            "How do you maintain composure and high code quality when working under intense pressure?",
            "Composure Under Fire",
            "I maintain composure by breaking chaos down into structured, manageable actions. During a live demonstration of our intrusion detection system to faculty evaluators, our background packet sniffer crashed due to an unexpected Windows socket permission issue. Rather than panicking, I took a breath, explained to the evaluators calmly what occurred, inspected the command-line stack trace, and identified that Npcap required administrator privilege escalation. I relaunched the terminal with elevated permissions, and the live packet feed resumed smoothly. Keeping a calm head and methodically reading error traces allows me to resolve issues far faster than stressing.",
            "Real-world incident management: calmness, transparent communication, and methodical log inspection under scrutiny.",
            "STAR"
        ),
        (
            44,
            "How would you handle a situation where project requirements change midway through development?",
            "Adaptability",
            "In our QuickBite food platform, the initial specification was a simple single-restaurant ordering interface. Midway through development, our faculty advisor suggested transforming it into a multi-restaurant platform supporting separate vendor menus and order tracking. Because I had designed the backend using modular RESTful controllers and decoupled MongoDB document schemas, the core architecture accommodated the change gracefully. I added a `restaurant_id` foreign key reference to menu items and orders, updated the routing middleware, and expanded the frontend dropdown selector. I embrace requirement changes by building modular, loosely coupled code from day one.",
            "Shows proactive architectural foresight: modular design absorbs changing requirements without rewriting codebases.",
            "STAR"
        )
    ]

    for q in sec_d_questions:
        story.append(make_qa_card(q[0], q[1], q[2], q[3], q[4], q[5]))

    # ==========================================
    # MODULE 6: SECTION E - MOTIVATION & REVERSE QUESTIONS (6 Qs)
    # ==========================================
    story.append(PageBreak())
    story.extend(make_section_banner("Module 6: Section E - Motivation & Reverse Questions", "6 Questions on Candidate Expectations, Growth, and High-Impact Reverse Inquiries"))

    sec_e_questions = [
        (
            45,
            "Why are you specifically interested in this HackerRank SDE internship?",
            "Role Alignment",
            "I am drawn to HackerRank because you build the tools that empower the global developer ecosystem. As someone passionate about backend infrastructure, the engineering challenges here are exceptional: containerized code execution sandboxes, real-time collaborative pair-programming IDEs, and sub-second evaluation pipelines supporting millions of developers across 40+ languages. Furthermore, HackerRank's culture of giving interns production ownership from month one and pairing them with dedicated mentors is the exact environment where I want to push my limits and grow into a world-class engineer.",
            "Demonstrates specific awareness of HackerRank's unique developer platform challenges and intern ownership culture."
        ),
        (
            46,
            "What do you expect to learn and master during your six-month internship?",
            "Learning Goals",
            "During this six-month internship, I expect to bridge the gap between academic software projects and production-grade engineering at scale. Specifically, I want to master three things: 1) Writing resilient, high-throughput microservices adhering to strict code review and testing standards; 2) Understanding large-scale distributed cloud infrastructure, CI/CD pipelines, and observability on AWS; and 3) Learning how senior engineers evaluate technical trade-offs between latency, consistency, and operational simplicity in mission-critical platforms.",
            "Outlines clear, mature technical learning objectives that align directly with corporate software engineering expectations."
        ),
        (
            47,
            "What specific kind of engineering work or platform challenges interest you most?",
            "Technical Focus",
            "I am most interested in backend systems and infrastructure engineering. In particular, the mechanics of HackerRank's code execution engine fascinate me—how you securely compile and run untrusted code snippets within sandboxed Linux cgroups and Docker containers, enforcing strict CPU, memory, and execution timeouts while maintaining sub-second initialization. Working on that intersection of operating systems, container virtualization, and high-concurrency API dispatch is where I would be most excited to contribute.",
            "Shows deep, sophisticated understanding of HackerRank's core technical moat (untrusted code execution sandboxing)."
        ),
        (
            48,
            "What would success look like for you at the end of your six-month internship?",
            "Success Metrics",
            "Success at the end of six months means three concrete outcomes: First, having multiple production features designed, tested, and shipped to live users that measurably improve platform performance or developer experience. Second, earning the reputation of being a reliable, proactive, and coachable teammate who communicates clearly and unblocks peers. Third, demonstrating sufficient technical depth and cultural ownership to earn a full-time return offer (PPO) as a Software Development Engineer at HackerRank.",
            "Direct, ambitious, and metric-oriented: connects personal success with shipping production value and earning a full-time seat."
        ),
        (
            49,
            "Strategic Question for Interviewer: Architecture & Engineering Stack",
            "Reverse Interviewing",
            "<b>Question to Ask:</b> <i>'Could you share how HackerRank architectures its code execution sandbox to securely isolate untrusted candidate code while maintaining sub-second execution times across diverse runtimes? What are the biggest scaling bottlenecks the team is currently solving?'</i><br/><br/><b>What to Listen For:</b> Insights into their containerization strategy (Docker/cgroups/gVisor), queueing systems (Kafka/SQS), and latency optimization trade-offs.",
            "Signals high technical maturity: shows you understand the hardest architectural problem HackerRank solves every day."
        ),
        (
            50,
            "Strategic Question for Interviewer: Intern Expectations & PPO Milestones",
            "Reverse Interviewing",
            "<b>Question to Ask:</b> <i>'For an SDE intern joining in January, what does the ramp-up process look like in the first 30 days, and what specific qualities separate an intern who does a good job from an exceptional intern who earns a full-time PPO conversion?'</i><br/><br/><b>What to Listen For:</b> Concrete performance rubrics, mentorship availability, expectation of production deployments, and team culture dynamics.",
            "Demonstrates ambition and long-term commitment: signals that you are focused on delivering maximum value and converting to a permanent engineer."
        )
    ]

    for q in sec_e_questions:
        story.append(make_qa_card(q[0], q[1], q[2], q[3], q[4]))

    # ==========================================
    # MODULE 7: COMMON INTERVIEW MISTAKES TO AVOID
    # ==========================================
    story.append(PageBreak())
    story.extend(make_section_banner("Module 7: Common Interview Mistakes to Avoid", "6 Critical Engineering Anti-Patterns and How to Overcome Them"))

    mistakes_data = [
        ("Anti-Pattern 1: The Memorized Robotic Monologue",
         "<b>The Mistake:</b> Reciting pre-memorized paragraphs verbatim with flat vocal cadence. Interviewers immediately recognize rehearsed scripts and lose engagement.<br/>"
         "<b>The Fix:</b> Memorize structural milestones and bullet points (e.g., Problem $\\rightarrow$ Queue fix $\\rightarrow$ 0.05ms latency). Speak naturally in conversational Indian English, using natural pauses and vocal inflection."),

        ("Anti-Pattern 2: The Hand-Waving Project Explanation",
         "<b>The Mistake:</b> Giving superficial explanations: <i>'We used machine learning to detect intrusions and built a dashboard.'</i> It leaves interviewers questioning whether you actually wrote the code.<br/>"
         "<b>The Fix:</b> Quote specific architectural decisions, algorithms, and numbers: <i>'We intercepted live frames with Scapy, computed 5-tuple canonical hashes, and trained an RBF-kernel SVM achieving 96% accuracy and 0.0512 ms inference latency.'</i>"),

        ("Anti-Pattern 3: Blaming Teammates for Failures",
         "<b>The Mistake:</b> Explaining project delays by blaming peers: <i>'My teammate didn't do their part, so the backend was delayed.'</i> This signals toxic teamwork and zero accountability.<br/>"
         "<b>The Fix:</b> Demonstrate leadership and empathy: <i>'A teammate faced roadblocks with CORS and token storage; I paired with them for two hours to debug the middleware, and we shipped on time.'</i>"),

        ("Anti-Pattern 4: Resume Skill Inflation Without Depth",
         "<b>The Mistake:</b> Listing 15 frameworks on your resume after watching a 10-minute video, then freezing when asked basic internal mechanics (e.g., listing Docker but not knowing what a container image layer is).<br/>"
         "<b>The Fix:</b> Ground every listed skill in genuine experience. If you know Python, be ready for GIL, decorators, and generators. If you know SQL, understand indexes and ACID."),

        ("Anti-Pattern 5: Lack of Trade-Off Thinking",
         "<b>The Mistake:</b> Claiming a technology is universally superior: <i>'MongoDB is better than SQL,'</i> or <i>'Deep learning is always better than SVMs.'</i><br/>"
         "<b>The Fix:</b> Always frame choices as trade-offs: <i>'SVM was 7.5x faster than LSTM with minimal accuracy loss, making it optimal for real-time line-rate packet inference on CPU.'</i>"),

        ("Anti-Pattern 6: Passive Silence When Stuck",
         "<b>The Mistake:</b> Staring silently at the screen for two minutes when faced with a difficult coding or design question.<br/>"
         "<b>The Fix:</b> Think out loud! Communicate your thought process: <i>'My first thought is a brute-force approach scanning all pairs in $O(N^2)$, but we can optimize this to $O(N)$ using a hash set to store seen values.'</i>")
    ]

    for title, content in mistakes_data:
        story.append(make_callout(title, [content], border_color=NAVY_PRIMARY, bg_color=BG_LIGHT))

    # ==========================================
    # MODULE 8: LAST-MINUTE TECHNICAL REVISION SHEETS (7 CHEAT SHEETS)
    # ==========================================
    story.append(PageBreak())
    story.extend(make_section_banner("Module 8: Last-Minute Technical Revision Sheets", "7 Rapid-Review Engineering Cheat Sheets Covering Core CS and Web Architecture"))

    cheat_sheets = [
        ("Cheat Sheet 1: Python Core & Advanced Concepts",
         "• <b>GIL (Global Interpreter Lock):</b> Mutex preventing multiple native threads from executing Python bytecodes simultaneously. Makes multi-threading suitable for I/O-bound tasks, while CPU-bound tasks require multi-processing (`multiprocessing`).<br/>"
         "• <b>Memory Management:</b> Private heap managed by Python's memory manager. Uses reference counting combined with a generational garbage collector to resolve cyclic references.<br/>"
         "• <b>Generators & `yield`:</b> Functions returning an iterator that produces values lazily on-demand. Consumes $O(1)$ memory compared to $O(N)$ for full lists.<br/>"
         "• <b>Decorators:</b> Functions taking another function as an argument and extending its behavior without modifying it (e.g., `@token_required`, `@app.route`).<br/>"
         "• <b>List Comprehensions vs Generators:</b> `[x for x in data]` builds full list in memory; `(x for x in data)` yields elements generator-style.<br/>"
         "• <b>Dict Internals:</b> Implemented as a resizable hash table using open addressing with quadratic probing, achieving average $O(1)$ lookup and insert."),

        ("Cheat Sheet 2: Object-Oriented Programming (OOP) & SOLID Principles",
         "• <b>Encapsulation:</b> Bundling data and methods operating on that data within a class while restricting direct access to internal state (private attributes).<br/>"
         "• <b>Abstraction:</b> Hiding complex implementation details and exposing only essential interfaces (e.g., abstract base classes `ABC`).<br/>"
         "• <b>Inheritance:</b> Deriving new classes from existing ones to promote code reuse and establish hierarchical relationships.<br/>"
         "• <b>Polymorphism:</b> Ability of different classes to respond to the same method invocation in their own unique way (method overriding & overloading).<br/>"
         "• <b>SOLID Principles:</b><br/>"
         "  - <b>S (Single Responsibility):</b> A class should have only one reason to change.<br/>"
         "  - <b>O (Open/Closed):</b> Software entities should be open for extension, but closed for modification.<br/>"
         "  - <b>L (Liskov Substitution):</b> Subtypes must be substitutable for their base types without altering correctness.<br/>"
         "  - <b>I (Interface Segregation):</b> Clients should not be forced to depend on interfaces they do not use.<br/>"
         "  - <b>D (Dependency Inversion):</b> Depend on abstractions, not on concrete implementations."),

        ("Cheat Sheet 3: Relational DBMS & SQL Mastery",
         "• <b>ACID Properties:</b><br/>"
         "  - <b>Atomicity:</b> All operations in a transaction succeed, or all are rolled back.<br/>"
         "  - <b>Consistency:</b> Transactions transition database from one valid state to another, maintaining constraints.<br/>"
         "  - <b>Isolation:</b> Concurrent transactions execute without interfering with one another (Read Committed, Serializable).<br/>"
         "  - <b>Durability:</b> Committed transactions survive system crashes and power failures via Write-Ahead Logging (WAL).<br/>"
         "• <b>B-Tree Indexes:</b> Balanced search trees storing sorted keys with pointers to rows. Provides $O(\\log N)$ search, insert, and delete.<br/>"
         "• <b>Clustered vs Non-Clustered:</b> Clustered index determines the physical on-disk order of rows (only 1 per table); Non-clustered creates a separate sorted index structure pointing to heap rows.<br/>"
         "• <b>Normalization:</b> 1NF (atomic values, no repeating groups), 2NF (in 1NF + no partial dependency on composite key), 3NF (in 2NF + no transitive dependency)."),

        ("Cheat Sheet 4: Web Architecture, HTTP & RESTful Design",
         "• <b>HTTP Methods & Idempotency:</b><br/>"
         "  - <b>GET:</b> Safe and idempotent. Retrieves data.<br/>"
         "  - <b>POST:</b> Neither safe nor idempotent. Creates new resources.<br/>"
         "  - <b>PUT:</b> Idempotent. Completely replaces a resource.<br/>"
         "  - <b>PATCH:</b> Not strictly idempotent. Partially modifies a resource.<br/>"
         "  - <b>DELETE:</b> Idempotent. Removes a resource.<br/>"
         "• <b>HTTP Status Codes:</b> 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity, 500 Internal Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout.<br/>"
         "• <b>Stateless JWT vs Sessions:</b> JWT encodes claims and signature in Base64Url token stored on client, verified statelessly on server via secret; Sessions store session state in server memory/Redis and pass a session ID cookie."),

        ("Cheat Sheet 5: Computer Networks Fundamentals",
         "• <b>TCP vs UDP:</b> TCP is connection-oriented, reliable, guarantees in-order delivery via sequence numbers and ACKs, with flow and congestion control; UDP is connectionless, lightweight, unreliable, with zero handshake latency (ideal for DNS, video streaming).<br/>"
         "• <b>TCP 3-Way Handshake:</b> 1) Client sends SYN; 2) Server responds with SYN-ACK; 3) Client sends ACK. Connection is established.<br/>"
         "• <b>OSI 7 Layers:</b> Physical $\\rightarrow$ Data Link (Ethernet frames) $\\rightarrow$ Network (IP packets) $\\rightarrow$ Transport (TCP/UDP segments) $\\rightarrow$ Session $\\rightarrow$ Presentation $\\rightarrow$ Application (HTTP, DNS).<br/>"
         "• <b>DNS Resolution:</b> Browser cache $\\rightarrow$ OS cache $\\rightarrow$ Resolving Name Server (ISP) $\\rightarrow$ Root Name Server (`.`) $\\rightarrow$ TLD Server (`.com`) $\\rightarrow$ Authoritative Name Server (maps domain to IP)."),

        ("Cheat Sheet 6: Data Structures & Algorithms Complexity Matrix",
         "• <b>Array / Dynamic Array:</b> Access: $O(1)$, Search: $O(N)$, Insert/Delete at end: $O(1)$ amortized, Insert/Delete at beginning: $O(N)$.<br/>"
         "• <b>Singly / Doubly Linked List:</b> Access: $O(N)$, Search: $O(N)$, Insert/Delete at head/tail (with pointer): $O(1)$.<br/>"
         "• <b>Hash Table:</b> Average Search/Insert/Delete: $O(1)$, Worst case (hash collisions): $O(N)$.<br/>"
         "• <b>Binary Search Tree (Balanced / AVL / Red-Black):</b> Search/Insert/Delete: $O(\\log N)$. Unbalanced worst case: $O(N)$.<br/>"
         "• <b>Min / Max Heap (Priority Queue):</b> Find Min/Max: $O(1)$, Insert: $O(\\log N)$, Extract Min/Max: $O(\\log N)$, Heapify array: $O(N)$.<br/>"
         "• <b>Sorting Algorithms:</b><br/>"
         "  - <i>QuickSort:</i> Average: $O(N \\log N)$, Worst: $O(N^2)$, Space: $O(\\log N)$.<br/>"
         "  - <i>MergeSort:</i> Best/Avg/Worst: $O(N \\log N)$, Space: $O(N)$. Stable.<br/>"
         "  - <i>HeapSort:</i> Best/Avg/Worst: $O(N \\log N)$, Space: $O(1)$. In-place, unstable."),

        ("Cheat Sheet 7: Git & Modern Version Control Workflows",
         "• <b>Git Merge vs Rebase:</b> `git merge` creates a new merge commit combining history branches, preserving exact chronology; `git rebase` replays your commits on top of the target branch, producing a clean, linear commit history.<br/>"
         "• <b>Resolving Merge Conflicts:</b> Git marks conflict zones with `<<<<<<<`, `=======`, `>>>>>>>`. Open file, select correct code version, test, `git add <file>`, and complete merge/rebase.<br/>"
         "• <b>Git Cherry-Pick:</b> `git cherry-pick <commit-hash>` applies the changes from an isolated commit onto your current working branch.<br/>"
         "• <b>Git Stash:</b> `git stash` temporarily shelves uncommitted local modifications, enabling you to switch branches cleanly; `git stash pop` reapplies stashed changes.")
    ]

    for title, content in cheat_sheets:
        story.append(make_callout(title, [content], border_color=NAVY_PRIMARY, bg_color=BG_LIGHT))

    # ==========================================
    # MODULE 9: MOCK INTERVIEW PRACTICE (15 UNANSWERED QUESTIONS)
    # ==========================================
    story.append(PageBreak())
    story.extend(make_section_banner("Module 9: Mock Interview Practice Simulation", "15 Independent Practice Questions with Evaluation Criteria and Blank Practice Lines"))

    story.append(Paragraph(
        "Use these 15 realistic interview questions to test your real-time verbal answering capability. "
        "Practice answering aloud using the appropriate framework (STAR, 6-Step Technical, or Trade-Off) and write bullet points in the spaces provided.",
        style_body
    ))

    mock_prompts = [
        (1, "How would you detect a cycle in a singly linked list, and what are the time and space trade-offs of your approach?",
         "Algorithms / Pointers: Floyd's Tortoise and Hare ($O(N)$ time, $O(1)$ space) vs Hash Set ($O(N)$ time, $O(N)$ space)."),

        (2, "Explain the difference between a process and a thread. How does the operating system handle context switching between them?",
         "Operating Systems: Isolated address spaces vs shared memory, PCB vs TCB overhead, cache invalidation."),

        (3, "In your Zero-Trust NIDS project, how did you guarantee that testing data never leaked into the training preprocessing pipeline?",
         "Project Integrity: Stratified 70/15/15 partition strictly prior to fitting StandardScaler/LabelEncoder."),

        (4, "How does an HTTP cookie differ from local storage in terms of security, lifespan, and transmission mechanics?",
         "Web Security: HTTP-only flag preventing XSS, automatic transmission in request headers, domain scoping, CSRF vulnerabilities."),

        (5, "What happens under the hood from the millisecond you type 'https://www.hackerrank.com' into your browser and press Enter?",
         "Full-Stack Networking: DNS resolution, TCP 3-way handshake, TLS 1.3 cryptographic negotiation, HTTP GET, DOM/CSSOM rendering."),

        (6, "Describe a time when you received contradictory requirements from project stakeholders or team members. How did you proceed?",
         "STAR Behavioral: Clarification, documenting assumptions, facilitating consensus, and building flexible modular interfaces."),

        (7, "If you had to design a distributed rate-limiting algorithm to protect a public REST API from DDoS attacks, what data structure would you use?",
         "System Design: Token Bucket or Leaky Bucket algorithm using Redis sorted sets or atomic increment with TTL expiration."),

        (8, "Why did you choose an SVM model with an RBF kernel instead of a deep neural network for live packet classification in your capstone?",
         "Technical Trade-Offs: Sub-millisecond CPU latency (0.05ms) vs deep net recurrent lag (0.38ms), mathematical boundary stability."),

        (9, "What is database deadlock, and what concrete strategies can software engineers implement in their SQL transactions to prevent it?",
         "DBMS Concurrency: Circular lock dependencies, strict transaction lock ordering, keeping transactions short, timeout retries."),

        (10, "How do you test that an asynchronous queueing system handles bursty traffic spikes without running out of memory?",
         "Testing & Reliability: Bounded queue capacity, backpressure signaling, stress testing with Locust, load shedding."),

        (11, "Explain how YOLO achieves real-time vehicle detection speeds compared to older two-stage region-based algorithms like Faster R-CNN.",
         "Computer Vision: Single-stage unified regression over grid cells vs two-stage region proposal network (RPN) bottlenecks."),

        (12, "Tell me about a time you had to deliver difficult, constructive feedback to a peer about code quality or contribution.",
         "STAR Collaboration: Private conversation, focusing on code impact rather than personality, suggesting actionable improvements."),

        (13, "How does cryptographic HMAC-SHA256 signature verification work in payment gateways to prevent malicious checkout tampering?",
         "Security & Payments: Secret key hashing over order details, comparing client signature against server computation to verify authenticity."),

        (14, "What are database indexes, why shouldn't we index every single column in a table, and what is the write penalty?",
         "DBMS Performance: B-Tree maintenance overhead, insert/update write amplification, disk storage costs."),

        (15, "If you joined HackerRank as an SDE intern tomorrow, how would you approach your first 14 days to maximize your team impact?",
         "Onboarding & Ownership: Reading architecture docs, setting up local dev environment, shipping a small bugfix in week 1, pairing with mentor.")
    ]

    for q in mock_prompts:
        card_content = [
            [
                Paragraph(f"<b>Practice Prompt {q[0]}: \"{q[1]}\"</b>", style_card_q),
                Paragraph("<b>MOCK DRILL</b>", style_tag)
            ],
            [
                Paragraph(f"<b>Evaluation Focus:</b> {q[2]}", style_card_why),
                Paragraph("", style_tag)
            ],
            [
                Paragraph("<b>Your Practice Bullet Points / Delivery Structure:</b><br/>" + ("_" * 96 + "<br/>") * 2 + ("_" * 96), style_practice_line),
                Paragraph("", style_tag)
            ]
        ]
        t_card = Table(card_content, colWidths=[CONTENT_WIDTH - 85, 75])
        t_card.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), BG_HIGHLIGHT),
            ('BACKGROUND', (0, 1), (-1, -1), BG_CARD),
            ('BOX', (0, 0), (-1, -1), 0.75, BORDER_LIGHT),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, BORDER_LIGHT),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(KeepTogether([t_card, Spacer(1, 3.5)]))

    # ==========================================
    # MODULE 10: FINAL PRE-INTERVIEW READINESS CHECKLIST
    # ==========================================
    story.append(PageBreak())
    story.extend(make_section_banner("Module 10: Final Pre-Interview Readiness Checklist", "Operational, Technical, and Psychological Protocols for Interview Day"))

    checklist_data = [
        ("Phase 1: 24 Hours Prior to Interview (Environment & Setup)",
         "• <b>Hardware & Connectivity:</b> Verify laptop charger, test primary Wi-Fi and mobile hotspot backup, test external microphone and webcam.<br/>"
         "• <b>HackerRank IDE Practice:</b> Open the HackerRank platform, write a quick Python/C++ solution to verify keyboard shortcuts, indentation, and custom test input mechanics.<br/>"
         "• <b>Resume & Project Alignment:</b> Print a physical copy of your CV and the Last-Minute Revision Sheet. Ensure you can point to exact lines of code for every bullet.<br/>"
         "• <b>Environment:</b> Choose a quiet, well-lit room with a neutral background. Ensure zero background noise or door disruptions."),

        ("Phase 2: 60 Minutes Prior to Interview (Mental Warm-Up)",
         "• <b>Vocal Warm-Up:</b> Speak aloud for 5 minutes. Deliver your 60-second 'Tell me about yourself' pitch twice to establish confident vocal cadence.<br/>"
         "• <b>Browser Sanity:</b> Close all unnecessary browser tabs, mute Slack/WhatsApp notifications, and test the video meeting link (Google Meet / Zoom).<br/>"
         "• <b>Have Ready:</b> A notebook, two pens, a bottle of water, and your printed cheat sheets within arm's reach.<br/>"
         "• <b>Mental State:</b> Remember: technical interviews are collaborative engineering discussions, not interrogations. The interviewer wants you to succeed."),

        ("Phase 3: During the Interview (Live Execution Protocol)",
         "• <b>Listen Actively:</b> Do not interrupt the interviewer. Take notes as they describe coding problems or architectural scenarios.<br/>"
         "• <b>Clarify Assumptions:</b> Always ask 1-2 clarifying questions before typing code (e.g., <i>'Can the input contain duplicate values?'</i>).<br/>"
         "• <b>Think Out Loud:</b> Vocalize your thought process continuously. If you are quiet for more than 15 seconds, say: <i>'I am considering two approaches here...'</i><br/>"
         "• <b>Run Custom Test Cases:</b> Before clicking 'Run Code' or declaring your solution complete, trace through a normal case and a boundary case manually.<br/>"
         "• <b>Show Gratitude:</b> Thank the interviewer genuinely and ask your 2 prepared strategic questions about HackerRank's engineering stack."),

        ("Phase 4: Post-Interview Protocol",
         "• <b>Document Questions Immediately:</b> Within 10 minutes of finishing, write down every technical question and scenario asked while fresh in memory.<br/>"
         "• <b>Identify Knowledge Gaps:</b> If you stumbled on a concept (e.g., database isolation levels), spend 30 minutes studying it thoroughly.<br/>"
         "• <b>Send Thank-You Note:</b> If communicating via email with a recruiter or coordinator, send a brief, professional thank-you note reiterating your enthusiasm for the SDE intern role.")
    ]

    for title, content in checklist_data:
        story.append(make_callout(title, [content], border_color=NAVY_PRIMARY, bg_color=BG_LIGHT))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"HackerRank Preparation Handbook successfully generated at: {output_path}")

if __name__ == "__main__":
    build_pdf()
