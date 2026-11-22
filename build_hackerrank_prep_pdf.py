"""
HackerRank SDE Intern - Recruiter Screening Interview Preparation Guide Generator
Generates a comprehensive, publication-grade A4 PDF for Lloyd Gopi.
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

# Palette Constants (Corporate Navy, Slate & Subtle Gray)
NAVY_PRIMARY = HexColor("#0F2C59")     # Deep Corporate Navy
NAVY_SECONDARY = HexColor("#1E3E62")   # Medium Navy
BLUE_ACCENT = HexColor("#0284C7")      # Bright Accent Cyan/Blue
TEXT_DARK = HexColor("#1E293B")        # Slate 900 Body Text
TEXT_MUTED = HexColor("#475569")       # Slate 600 Subtle Text
BG_LIGHT = HexColor("#F8FAFC")         # Slate 50 Neutral Light
BG_CARD = HexColor("#FFFFFF")          # Pure White
BORDER_LIGHT = HexColor("#CBD5E1")     # Slate 300 Divider
ACCENT_GREEN = HexColor("#0D9488")     # Success / Checkmark Teal
BG_HIGHLIGHT = HexColor("#F1F5F9")     # Callout Light Gray
AMBER_WARNING = HexColor("#B45309")    # Amber for Confirmation Needed
LINE_GRAY = HexColor("#E2E8F0")

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 34 # ~0.47 inch margins for optimal vertical budgeting
CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN) # 527.28 pt

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw exact total page counts and running headers/footers."""
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
            self.drawString(MARGIN + 120, 814, "|  Recruiter Screening Interview Preparation Guide")
            self.drawRightString(PAGE_WIDTH - MARGIN, 814, "Candidate: Lloyd Gopi (JNNCE 2027)")
            
            self.setStrokeColor(BORDER_LIGHT)
            self.setLineWidth(0.6)
            self.line(MARGIN, 808, PAGE_WIDTH - MARGIN, 808)

            # Running Footer
            self.line(MARGIN, 34, PAGE_WIDTH - MARGIN, 34)
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(NAVY_PRIMARY)
            self.drawString(MARGIN, 22, "STRICTLY CONFIDENTIAL")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(TEXT_MUTED)
            self.drawString(MARGIN + 105, 22, "|  Prepared for 6-Month Recruiter Screening (Jan 2027 Start)")
            
            page_str = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(PAGE_WIDTH - MARGIN, 22, page_str)
        self.restoreState()

def create_guide_pdf(output_path="e:/ML/HackerRank_SDE_Intern_Screening_Preparation_Guide.pdf"):
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
        fontSize=19,
        leading=23,
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

    # Helper: QA Card (Tuned for precise vertical packing)
    def make_qa_card(q_num, question, category, model_answer, why_it_works, word_count=None):
        wc_str = f" ({word_count} words)" if word_count else ""
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

        p_ans_label = Paragraph(f"<b><font color='{NAVY_SECONDARY}'>Conversational Model Answer{wc_str}:</font></b>", style_body_bold)
        p_ans = Paragraph(f'"{model_answer}"', style_card_ans)
        
        p_why_label = Paragraph(f"<b><font color='{BLUE_ACCENT}'>Recruiter Psychology & Strategy:</font></b>", style_body_bold)
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
            ('TOPPADDING', (0, 0), (-1, -1), 3.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ]))
        return KeepTogether([t, Spacer(1, 4)])

    # ==========================================
    # 0. COVER PAGE & CANDIDATE PROFILE SNAPSHOT
    # ==========================================
    story.append(Paragraph("HACKERRANK SOFTWARE DEVELOPMENT ENGINEER INTERN", style_cover_title))
    story.append(Paragraph("<b>Recruiter Screening Interview Preparation Guide</b>", ParagraphStyle('CoverTitle2', fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=NAVY_SECONDARY)))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Comprehensive Interview Strategy, 25 Screening Questions & Model Answers, Project Elevator Pitches, Tricky HR Scenarios, Mock Simulation & Last-Minute Cheat Sheet", style_cover_sub))
    story.append(Spacer(1, 5))

    # Candidate Profile Header Card
    profile_data = [
        [
            Paragraph("<b>Candidate Name:</b>", style_table_cell_bold),
            Paragraph("Lloyd Gopi", style_table_cell),
            Paragraph("<b>Current Degree:</b>", style_table_cell_bold),
            Paragraph("B.E. Information Science & Engineering", style_table_cell)
        ],
        [
            Paragraph("<b>Institution / College:</b>", style_table_cell_bold),
            Paragraph("JNNCE, Shivamogga, Karnataka", style_table_cell),
            Paragraph("<b>Academic Standing:</b>", style_table_cell_bold),
            Paragraph("7th Semester (Graduating Batch 2027)", style_table_cell)
        ],
        [
            Paragraph("<b>Internship Duration:</b>", style_table_cell_bold),
            Paragraph("6 Months Full-Time (Jan 2027 - June 2027)", style_table_cell),
            Paragraph("<b>Earliest Joining:</b>", style_table_cell_bold),
            Paragraph("Early January 2027", style_table_cell)
        ],
        [
            Paragraph("<b>Target Location:</b>", style_table_cell_bold),
            Paragraph("Bengaluru (100% Onsite Ready)", style_table_cell),
            Paragraph("<b>College Approval (NOC):</b>", style_table_cell_bold),
            Paragraph("Yes, 8th Sem Dedicated Internship Policy", style_table_cell)
        ],
        [
            Paragraph("<b>Primary Technical Skills:</b>", style_table_cell_bold),
            Paragraph("Python, C++, Java, SQL, Machine Learning, Web Development (React, Flask, Node.js)", style_table_cell),
            Paragraph("<b>Core Projects:</b>", style_table_cell_bold),
            Paragraph("1. Zero-Trust AI-Powered NIDS<br/>2. Full-Stack Food Ordering Platform", style_table_cell)
        ]
    ]
    t_profile = Table(profile_data, colWidths=[110, 153, 115, 149])
    t_profile.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, NAVY_PRIMARY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_profile)
    story.append(Spacer(1, 5))

    # Table of Contents Grid (Updated with precise page targets)
    toc_data = [
        [
            Paragraph("<b>Section</b>", style_table_head),
            Paragraph("<b>Module Title & Coverage</b>", style_table_head),
            Paragraph("<b>Target Page</b>", style_table_head),
            Paragraph("<b>Core Focus & Strategic Value</b>", style_table_head)
        ],
        [
            Paragraph("<b>Section 1</b>", style_table_cell_center),
            Paragraph("<b>Company & Role Overview</b>", style_table_cell_bold),
            Paragraph("Page 1 - 2", style_table_cell_center),
            Paragraph("HackerRank business model, developer ecosystem, SDE intern scope & recruiter evaluation checklist.", style_table_cell)
        ],
        [
            Paragraph("<b>Section 2</b>", style_table_cell_center),
            Paragraph("<b>Top 25 Recruiter Screening Q&As</b>", style_table_cell_bold),
            Paragraph("Page 3 - 7", style_table_cell_center),
            Paragraph("Detailed conversational answers (40-90 words) tailored to Lloyd Gopi with recruiter psychology breakdown.", style_table_cell)
        ],
        [
            Paragraph("<b>Section 3</b>", style_table_cell_center),
            Paragraph("<b>Project Explanation Preparation</b>", style_table_cell_bold),
            Paragraph("Page 8 - 9", style_table_cell_center),
            Paragraph("60-second elevator pitches and deep-dives for Zero-Trust AI NIDS and Full-Stack Food Ordering Platform.", style_table_cell)
        ],
        [
            Paragraph("<b>Section 4</b>", style_table_cell_center),
            Paragraph("<b>HR & Recruiter Tricky Scenarios</b>", style_table_cell_bold),
            Paragraph("Page 10 - 11", style_table_cell_center),
            Paragraph("Diplomatic, authentic handling of relocation, stipend expectations, competing offers, NOC delays, and tech gaps.", style_table_cell)
        ],
        [
            Paragraph("<b>Section 5</b>", style_table_cell_center),
            Paragraph("<b>Questions to Ask the Recruiter</b>", style_table_cell_bold),
            Paragraph("Page 12", style_table_cell_center),
            Paragraph("High-impact reverse-interviewing questions covering team placement, mentorship, stipend, and PPO milestones.", style_table_cell)
        ],
        [
            Paragraph("<b>Section 6</b>", style_table_cell_center),
            Paragraph("<b>Communication & Interview Mastery</b>", style_table_cell_bold),
            Paragraph("Page 13", style_table_cell_center),
            Paragraph("The STAR method, 45-60s sweet spot, voice modulation, avoiding robotic answers, and handling the unknown.", style_table_cell)
        ],
        [
            Paragraph("<b>Section 7</b>", style_table_cell_center),
            Paragraph("<b>Mock Interview Practice Simulation</b>", style_table_cell_bold),
            Paragraph("Page 14 - 16", style_table_cell_center),
            Paragraph("Realistic 10-12 minute 14-question screening simulation in natural sequence with blank candidate response spaces.", style_table_cell)
        ],
        [
            Paragraph("<b>Section 8</b>", style_table_cell_center),
            Paragraph("<b>Last-Minute Revision Sheet</b>", style_table_cell_bold),
            Paragraph("Page 17", style_table_cell_center),
            Paragraph("Concise one-page executive cheat sheet for 5-minute pre-call review: key facts, pitch, metrics, and questions.", style_table_cell)
        ]
    ]
    t_toc = Table(toc_data, colWidths=[55, 160, 60, 252])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), BG_LIGHT]),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 6))

    # ==========================================
    # 1. COMPANY & ROLE OVERVIEW
    # ==========================================
    story.extend(make_section_banner("1. Company and Role Overview", "HackerRank Architecture, Business Model, Engineering Culture, and Recruiter Evaluation Criteria"))
    
    story.append(Paragraph("1.1 What HackerRank Does", style_subheading))
    story.append(Paragraph(
        "HackerRank is the global market leader in technical assessment, remote interview platforms, and developer skills benchmarking. "
        "Founded in 2012 by Vivek Ravisankar and Hari Karunanidhi (alumni of NIT Trichy), HackerRank was the first Indian startup incubated "
        "by Y Combinator (Summer 2011). The company's core mission is to accelerate the world's innovation by matching developer skills with opportunity, "
        "replacing traditional pedigree-driven resume filtering with objective, hands-on code evaluations.",
        style_body
    ))
    story.append(Paragraph(
        "Today, HackerRank operates at massive global scale across two symbiotic ecosystems: a vibrant <b>Developer Community of over 23 million developers</b> "
        "who practice algorithms, learn new languages, and earn certifications; and an <b>Enterprise Talent Platform used by over 3,000 corporate clients</b> "
        "(including Goldman Sachs, Amazon, Cisco, Vanguard, Atlassian, and Morgan Stanley) to screen, interview, and rank software engineering candidates.",
        style_body
    ))

    story.append(PageBreak()) # Clean transition to Page 2

    story.append(Paragraph("1.2 High-Level Products and Business Model", style_subheading))
    story.append(Paragraph(
        "HackerRank monetizes through an enterprise B2B SaaS model featuring multi-tiered annual subscriptions, customized assessment libraries, "
        "and applicant tracking system (ATS) integrations with platforms like Workday, Greenhouse, and Lever. Its primary product pillars include:",
        style_body
    ))
    story.append(Paragraph("- <b>HackerRank Skills / Assessment:</b> Automated coding assessments featuring a secure, containerized cloud code execution engine. It supports 40+ programming languages, compiles and executes code against custom test suites within memory/time limits, and scores candidate solutions automatically.", style_bullet))
    story.append(Paragraph("- <b>HackerRank Interview (formerly CodePair):</b> A low-latency collaborative browser IDE for live technical interviews, featuring interactive multi-file coding, shared terminal execution, audio/video conferencing, and digital whiteboard diagramming.", style_bullet))
    story.append(Paragraph("- <b>HackerRank AI Insights & Plagiarism Telemetry:</b> Advanced proctoring algorithms analyzing keystroke cadence, paste frequency, code similarity, and automated test telemetry to ensure assessment integrity.", style_bullet))
    story.append(Paragraph("- <b>HackerRank Benchmarks:</b> Standardized competency rubrics that allow enterprise engineering leaders to compare their applicant pool against global developer skill distributions.", style_bullet))

    story.append(Paragraph("1.3 What an SDE Intern Might Work On", style_subheading))
    story.append(Paragraph(
        "As an SDE Intern at HackerRank's Bengaluru engineering center, you will typically be embedded within an agile product pod. Depending on team placement, typical intern projects involve:",
        style_body
    ))
    story.append(Paragraph("- <b>Code Execution & Sandbox Infrastructure:</b> Enhancing isolated Linux container sandboxes (Docker, cgroups) to securely compile and execute millions of user-submitted code snippets per month with sub-second initialization times.", style_bullet))
    story.append(Paragraph("- <b>Backend Microservices:</b> Building and scaling RESTful and GraphQL APIs in Go, Java, Python, or Ruby on Rails that power candidate session state, assessment grading, and test dispatch queues.", style_bullet))
    story.append(Paragraph("- <b>Candidate & Recruiter Frontend Experiences:</b> Developing responsive, accessible, high-performance UI components in React, TypeScript, and modern CSS for the coding IDE and recruiter analytics dashboards.", style_bullet))
    story.append(Paragraph("- <b>Data & Telemetry Pipelines:</b> Instrumenting telemetry pipelines to track latency, system reliability, and candidate test analytics hosted on AWS cloud infrastructure.", style_bullet))

    story.append(Paragraph("1.4 What Recruiters Evaluate During the Initial Screening Call", style_subheading))
    story.append(Paragraph(
        "The recruiter screening is a <b>10 to 15-minute qualification filter</b>. The recruiter is typically not an engineer; their objective is to determine whether you meet basic logistical and behavioral bars before dedicating expensive senior engineer hours to technical rounds. Recruiters evaluate:",
        style_body
    ))
    story.append(Paragraph("1. <b>Eligibility & Timeline Fit:</b> Confirmation of 2027 graduation, 7th semester status, and an uninterrupted 6-month commitment starting January 2027.", style_bullet))
    story.append(Paragraph("2. <b>Institutional Clearances (NOC):</b> Clear proof that JNNCE permits full-time 8th-semester industry internships without conflicting on-campus classes.", style_bullet))
    story.append(Paragraph("3. <b>Location & Onsite Readiness:</b> Sincere, immediate willingness to relocate to Bengaluru and work onsite without hesitation or housing complications.", style_bullet))
    story.append(Paragraph("4. <b>Spoken English & Articulation:</b> Clear, structured communication. Can you explain your background and projects concisely in 45-60 seconds without babbling or sounding like a pre-recorded tape?", style_bullet))
    story.append(Paragraph("5. <b>Foundational Technical Depth:</b> Genuine passion for software engineering, comfort discussing core languages (Python, C++, Java, SQL), and logical debugging instinct.", style_bullet))
    story.append(Paragraph("6. <b>Culture & Coachability:</b> Humility, positive energy, excitement about developer tooling, and clear motivation to earn a full-time return offer (PPO).", style_bullet))

    story.append(Paragraph("1.5 Verified HackerRank Facts vs. General Industry Expectations", style_subheading))
    facts_data = [
        [
            Paragraph("<b>Category</b>", style_table_head),
            Paragraph("<b>Verified HackerRank Specific Information</b>", style_table_head),
            Paragraph("<b>General Industry / Variable Expectations</b>", style_table_head)
        ],
        [
            Paragraph("<b>Internship Duration</b>", style_table_cell_bold),
            Paragraph("Strict 6-month full-time internship model (Jan-June) for final-year Indian engineering students.", style_table_cell),
            Paragraph("Some companies offer 2-month summer or flexible 3-month stints; HackerRank focuses on 6-month deep immersion.", style_table_cell)
        ],
        [
            Paragraph("<b>Work Mode & Office</b>", style_table_cell_bold),
            Paragraph("India Technology Center located in Bengaluru; engineering interns are expected onsite for pairing & mentoring.", style_table_cell),
            Paragraph("Post-COVID policies vary widely; recruiter will confirm exact weekly in-office cadence during the call.", style_table_cell)
        ],
        [
            Paragraph("<b>Technical Stack</b>", style_table_cell_bold),
            Paragraph("Core platforms built in Ruby on Rails, Go, Python, Java, React, TypeScript, and AWS.", style_table_cell),
            Paragraph("Interns are not expected to know all languages upfront; recruiters evaluate core CS fundamentals and adaptability.", style_table_cell)
        ],
        [
            Paragraph("<b>PPO Potential</b>", style_table_cell_bold),
            Paragraph("Strong track record of converting high-performing 6-month interns into full-time Software Engineers.", style_table_cell),
            Paragraph("PPO conversion is always subject to individual performance ratings, mentor feedback, and business headcount.", style_table_cell)
        ]
    ]
    t_facts = Table(facts_data, colWidths=[95, 216, 216])
    t_facts.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), BG_LIGHT]),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_facts)

    # ==========================================
    # 2. TOP 25 RECRUITER SCREENING QUESTIONS
    # ==========================================
    # Organized strictly into 5 pages (5 questions per page: Q1-Q5, Q6-Q10, Q11-Q15, Q16-Q20, Q21-Q25)
    
    qa_list = [
        # --- Page 3: Q1 - Q5 ---
        (
            1,
            "Tell me about yourself.",
            "Elevator Pitch",
            "I'm Lloyd Gopi, currently pursuing my 7th semester of B.E. in Information Science and Engineering at JNNCE, Shivamogga, graduating in 2027. I have a strong foundation in Python, C++, Java, and SQL, with a primary focus on backend engineering and systems. Recently, I built an enterprise-grade Zero-Trust Network Intrusion Detection System that performs sub-millisecond threat classification on live network packets, as well as a full-stack food ordering platform with secure payment integration. I am now looking for a six-month onsite SDE internship starting in January 2027 where I can apply my problem-solving skills to high-scale developer platforms.",
            "Why it works: Hits all key recruiter filters in under 60 seconds (Name, 7th sem, JNNCE, 2027 batch, core languages, two strong projects, 6-month commitment, Jan 2027 start, and onsite Bengaluru readiness) without rambling.",
            86
        ),
        (
            2,
            "Why do you want to join HackerRank?",
            "Motivation & Fit",
            "I have been an active user of HackerRank since my second year of engineering to practice data structures and algorithms, so joining as an engineering intern feels like a natural extension of my journey. Beyond the product, I admire HackerRank's mission of creating a skills-first world where developers are evaluated on what they can build rather than their pedigree. Technically, building low-latency code execution engines and collaborative interview environments that handle millions of submissions across 40+ languages is the exact high-scale systems challenge I want to learn from.",
            "Why it works: Establishes organic product loyalty as a real user, connects with the company's core mission, and highlights technical awareness of HackerRank's backend engineering challenges.",
            84
        ),
        (
            3,
            "What do you know about HackerRank?",
            "Company Knowledge",
            "HackerRank is the market leader in technical hiring and developer skills assessments. Founded in 2012 by Vivek Ravisankar and Hari Karunanidhi, it was the first Indian startup to graduate from Y Combinator. It operates a developer community of over 23 million programmers while serving more than 3,000 enterprise customers, including Amazon and Goldman Sachs. Its flagship products include HackerRank Skills for automated coding assessments and HackerRank Interview for real-time collaborative pair-programming evaluations.",
            "Why it works: Delivers crisp, accurate corporate facts (founders, YC pedigree, community size, enterprise scale, key products) proving you did authentic homework.",
            71
        ),
        (
            4,
            "Why are you interested in this SDE internship?",
            "Career Ambition",
            "At this stage in my 7th semester, I have built complete software projects academically and independently. However, I want to bridge the gap between academic code and production-grade engineering. This internship offers the ideal platform to write clean, tested code that operates at scale, participate in peer code reviews, understand cloud infrastructure, and learn directly from senior engineers. I want to spend these six months contributing meaningfully and earning a full-time role.",
            "Why it works: Strikes the perfect balance between self-awareness and ambition. Recruiters respect interns who want to learn production standards and aim for a full-time return offer.",
            77
        ),
        (
            5,
            "Are you currently based in Bengaluru?",
            "Location Logistics",
            "I am currently based in Shivamogga completing my 7th semester coursework at JNNCE. However, Bengaluru is my top preferred location for my internship. I have family and local accommodation arrangements already in place in Bengaluru, which means I can relocate seamlessly by late December without any logistical delays before the January start date.",
            "Why it works: Honest about current physical location, but instantly eliminates recruiter anxiety regarding accommodation friction or delayed relocation.",
            53
        ),

        # --- Page 4: Q6 - Q10 ---
        (
            6,
            "Are you comfortable relocating to Bengaluru?",
            "Relocation Commitment",
            "Yes, 100%. Relocating to Bengaluru has been an integral part of my career plan for my final year. Bengaluru is the center of the technology ecosystem in India, and my family is entirely supportive of my relocation. I am prepared to move immediately upon completion of my 7th-semester examinations in December.",
            "Why it works: Proactive, enthusiastic, and decisive. Shows family alignment and guarantees zero relocation hesitation.",
            50
        ),
        (
            7,
            "Are you comfortable working onsite from our office?",
            "Work Mode Preference",
            "Yes, absolutely. In fact, I actively prefer an onsite internship. For an engineering intern, being in the office accelerates the learning curve tremendously - it allows me to sit with mentors, participate in whiteboard architectural discussions, pair-program, and absorb the engineering culture directly. I am eager to work onsite five days a week.",
            "Why it works: Recruiters strongly favor onsite interns because in-person onboarding, mentorship, and accountability yield significantly higher success rates.",
            55
        ),
        (
            8,
            "Can you commit to the entire six-month internship duration?",
            "Availability",
            "Yes, I can commit fully to the entire six months from January 2027 through June 2027. Under our university curriculum, our 8th semester is specifically dedicated to a full-time industry internship. I have no competing coursework on campus during this period, so my time and attention will be 100% dedicated to HackerRank.",
            "Why it works: Assures the recruiter of uninterrupted availability and provides the academic justification (8th semester dedicated to industry internship).",
            52
        ),
        (
            9,
            "When can you join us?",
            "Start Date",
            "My earliest joining date is early January 2027. Our 7th-semester university examinations are scheduled to conclude in late December 2026. As soon as the exams wrap up, I will be relocated and ready to join on the exact date HackerRank begins its January onboarding cohort.",
            "Why it works: Gives a realistic, concrete timeframe that matches corporate winter/spring internship onboarding cycles.",
            46
        ),
        (
            10,
            "What semester are you currently pursuing?",
            "Academic Standing",
            "I am currently in my 7th semester of B.E. in Information Science and Engineering at JNNCE, Shivamogga. I am on track to complete all 7th-semester academic requirements and examinations by December 2026, after which my final 8th semester commences in January 2027.",
            "Why it works: Clear, direct confirmation of degree, branch, semester, and timeline.",
            43
        ),

        # --- Page 5: Q11 - Q15 ---
        (
            11,
            "When does your next semester begin?",
            "Academic Calendar",
            "Our 8th and final semester officially begins in January 2027 and runs through June 2027. The university curriculum is specifically designed so that final-semester students can undertake full-time industry internships off-campus for project credits.",
            "Why it works: Reassures the recruiter that the semester timeline matches the 6-month internship window perfectly.",
            35
        ),
        (
            12,
            "Do you have examinations or academic commitments during the internship?",
            "Academic Commitments",
            "There are no written classroom examinations or regular weekday lectures during our 8th semester. The only academic requirement is submitting a periodic internship project report and presenting a final viva to our college committee in late May or June. Our department arranges these reviews on weekends or accommodates virtual presentations, so it will not interfere with my workday.",
            "Why it works: Completely neutralizes the recruiter's fear of the intern taking frequent study leaves or missing sprint deliverables.",
            58
        ),
        (
            13,
            "Does your college permit full-time internships?",
            "Institutional Policy",
            "Yes, absolutely. Visvesvaraya Technological University (VTU) and our institution, JNNCE, have an established institutional policy that permits and strongly encourages students to undertake full-time external internships during their 8th semester. Course credits are formally allocated to this industry training.",
            "Why it works: Cites both university (VTU) and college regulations, establishing authoritative academic legitimacy.",
            41
        ),
        (
            14,
            "Can you obtain a No Objection Certificate (NOC) from your college?",
            "NOC Clearance",
            "Yes, obtaining an NOC is a standard, streamlined process at JNNCE. Once I receive the formal internship offer letter detailing the role, duration, and Bengaluru location, our Training and Placement Cell issues the signed NOC from our Principal and Head of Department within three to five working days.",
            "Why it works: Shows clear knowledge of administrative steps and quotes a specific, fast turnaround window (3-5 working days).",
            49
        ),
        (
            15,
            "Are you currently interviewing with other companies?",
            "Pipeline Status",
            "Yes, I am participating in our ongoing campus placement drives and currently in preliminary evaluation rounds with a couple of other tech companies. However, HackerRank is my top priority because of my genuine interest in developer platforms and backend systems. If offered this internship, I would accept without hesitation.",
            "Why it works: Demonstrates that you are an attractive candidate in demand, while giving the recruiter confidence that they are your #1 first choice.",
            53
        ),

        # --- Page 6: Q16 - Q20 ---
        (
            16,
            "Do you currently have any internship offers in hand?",
            "Offer Status",
            "Currently, I do not have a finalized offer in hand; I am in active interview pipelines with two other technology firms for early 2027 internships. This gives me complete flexibility to commit wholeheartedly to HackerRank's January-to-June timeline without any competing contractual obligations.",
            "Why it works: Completely honest. It frames having no active signed offer as a distinct advantage for HackerRank: zero lock-in and 100% availability.",
            46
        ),
        (
            17,
            "What are your strongest technical skills?",
            "Technical Competence",
            "My strongest skills are core programming in Python and C++, object-oriented design in Java, and relational database modeling using SQL. On the systems and web engineering side, I build RESTful services using Flask and responsive interfaces using React. Through my intrusion detection project, I also developed practical experience with asynchronous packet processing, network protocols, and applied machine learning pipelines.",
            "Why it works: Prioritizes foundational programming languages over superficial frameworks, grounding every skill in real project applications.",
            60
        ),
        (
            18,
            "What are your personal strengths?",
            "Behavioral Strengths",
            "My primary strength is a structured, analytical approach to problem-solving. When faced with complex bugs or new technologies, I break problems down systematically rather than relying on guesswork. Secondly, I have strong coachability - I actively seek constructive feedback and iterate quickly. Finally, I communicate reliably and take complete ownership of deliverables assigned to me.",
            "Why it works: Avoids clichés like 'I am a perfectionist' and highlights traits engineering managers value most: systematic thinking, coachability, and accountability.",
            55
        ),
        (
            19,
            "Tell me about your most important project.",
            "Project Highlight",
            "My most significant project is a Zero-Trust AI-Powered Network Intrusion Detection System. I designed a decoupled four-tier architecture that intercepts live network packets using Scapy and Windows kernel drivers, reconstructs bidirectional conversations using direction-agnostic 5-tuple canonical hashing, and scores threats in real time using a Support Vector Machine model. The system achieved 96% detection accuracy with an inference latency of just 0.05 milliseconds per flow on the benchmark UNSW-NB15 dataset, while enforcing strict Zero-Trust JWT authentication.",
            "Why it works: Follows the Problem-Architecture-Result framework. Features impressive technical metrics (96% accuracy, 0.05 ms latency, 5-tuple hashing) that immediately signal engineering depth.",
            76
        ),
        (
            20,
            "What challenges did you face while developing your project?",
            "Technical Problem-Solving",
            "The most critical challenge was handling high-throughput live network traffic without dropping packets. Initially, running synchronous ML inference inside the packet capture callback created a major processing bottleneck. I resolved this by decoupling packet interception into an asynchronous background thread that pushed reconstructed flows into a thread-safe queue, allowing the ML engine to perform batched inference independently. This eliminated packet loss and reduced per-flow latency to 0.05 milliseconds.",
            "Why it works: Describes a genuine systems challenge (blocking I/O during packet sniffing), an architectural solution (asynchronous worker thread + thread-safe queue), and a quantifiable performance gain.",
            68
        ),

        # --- Page 7: Q21 - Q25 ---
        (
            21,
            "How do you approach debugging and problem-solving?",
            "Engineering Methodology",
            "I use a disciplined four-step method: First, I reproduce the bug consistently with the smallest possible test case. Second, I isolate the root cause using structured logging, breakpoints, and stack-trace analysis, validating assumptions step-by-step rather than making random code changes. Third, once the root cause is confirmed, I write the fix and test edge cases. Finally, I write regression tests to ensure the issue cannot reoccur.",
            "Why it works: Proves you have professional engineering hygiene rather than chaotic trial-and-error habits.",
            66
        ),
        (
            22,
            "Are you comfortable working in a team environment?",
            "Collaboration",
            "Yes, I thrive in collaborative teams. In our four-member final-year capstone project, I led the core backend architecture and ML inference pipeline. We managed our codebase on GitHub using feature branches, pull requests, and peer code reviews. When teammates faced roadblocks with API integrations, I helped debug and align our data schemas. I believe clear communication and shared ownership are vital for delivering solid software.",
            "Why it works: Backs up the claim with concrete evidence: 4-person team, GitHub PR workflow, schema alignment, and peer debugging.",
            68
        ),
        (
            23,
            "What are your short-term and long-term career goals?",
            "Career Vision",
            "In the short term, my goal is to spend this six-month internship mastering production engineering practices, writing clean, tested, high-throughput code, and earning a full-time SDE return offer at HackerRank. Long-term, over the next three to five years, I aspire to grow into a senior backend systems engineer, taking ownership of distributed architecture and scaling mission-critical developer tools.",
            "Why it works: Realistic, focused, and highlights immediate loyalty: you want to do great work, learn, and convert into a full-time engineer.",
            62
        ),
        (
            24,
            "Why should HackerRank select you over other candidates?",
            "Value Proposition",
            "You should consider me because I bring three key qualities: First, strong computer science fundamentals in data structures, algorithms, and systems. Second, a proven track record of building complex, high-performance projects like my real-time intrusion detection engine and full-stack web application. Third, 100% logistical readiness: complete six-month availability from January 2027, college NOC approval, and immediate relocation to Bengaluru. I am eager to contribute from day one.",
            "Why it works: Delivers a clean 3-pillar closing pitch: technical competence + demonstrated project execution + zero logistical friction.",
            69
        ),
        (
            25,
            "Do you have any questions for me?",
            "Reverse Interviewing",
            "Yes, thank you! I would love to learn: for an SDE intern joining the Bengaluru engineering center in January, which product pod or infrastructure team would they typically be paired with? Also, could you share what qualities separate a good intern from an exceptional intern who earns a full-time PPO conversion at HackerRank?",
            "Why it works: High-value question that demonstrates focus on team impact and eagerness to earn a full-time return offer.",
            53
        )
    ]

    # Render Section 2: Exactly 5 questions per page
    for idx, q in enumerate(qa_list):
        if idx % 5 == 0:
            story.append(PageBreak())
            if idx == 0:
                story.extend(make_section_banner("2. Top 25 Recruiter Screening Questions with Model Answers", "Conversational, Impactful Answers Tailored to Lloyd Gopi with Recruiter Psychology Analysis"))
        story.append(make_qa_card(q[0], q[1], q[2], q[3], q[4], q[5]))

    # ==========================================
    # 3. PROJECT EXPLANATION PREPARATION
    # ==========================================
    # Page 8: Project 1 (Zero-Trust AI NIDS)
    story.append(PageBreak())
    story.extend(make_section_banner("3. Project Explanation Preparation", "60-Second Spoken Elevator Pitches and Technical Deep-Dives for Both Candidate Projects"))

    story.append(Paragraph("Project 1: Zero-Trust AI-Powered Network Intrusion Detection System", style_subheading))
    
    pitch_nids = (
        "\"My primary project is an enterprise-grade Zero-Trust Network Intrusion Detection System designed to eliminate implicit trust "
        "in modern distributed networks. Traditional firewalls only protect the perimeter, leaving internal networks vulnerable to lateral movement. "
        "I engineered a decoupled four-tier architecture that intercepts raw Ethernet frames out-of-band using Scapy and kernel hooks, reassembles "
        "bidirectional conversations via direction-agnostic 5-tuple canonical hashing, and predicts intrusion probabilities in 0.05 milliseconds per flow. "
        "On the UNSW-NB15 benchmark, our active Support Vector Machine classifier achieved 96.00% accuracy and an ROC-AUC of 0.9853 with just 2.22% false alarms, "
        "strictly protected by JWT role-based access control.\""
    )
    story.append(make_callout(
        "60-Second Spoken Elevator Pitch (Script for Recruiter & Phone Screenings)",
        [pitch_nids],
        border_color=NAVY_PRIMARY,
        bg_color=BG_HIGHLIGHT
    ))

    nids_breakdown_data = [
        [
            Paragraph("<b>Technical Dimension</b>", style_table_head),
            Paragraph("<b>Implementation Details & Architecture Invariants</b>", style_table_head)
        ],
        [
            Paragraph("<b>Problem Statement</b>", style_table_cell_bold),
            Paragraph("Traditional perimeter 'castle-and-moat' defenses fail against lateral movement once an attacker penetrates the network. Furthermore, academic ML models often suffer from catastrophic data leakage and high inference latency that causes dropped packets during live network sniffing.", style_table_cell)
        ],
        [
            Paragraph("<b>Proposed Solution</b>", style_table_cell_bold),
            Paragraph("An enterprise Zero-Trust NIDS (NIST SP 800-207) featuring decoupled multi-tier microservices, continuous cryptographic authentication, leakage-free preprocessing, and real-time bidirectional flow inference.", style_table_cell)
        ],
        [
            Paragraph("<b>Technologies Used</b>", style_table_cell_bold),
            Paragraph("<b>Backend & Sniffing:</b> Python, Flask REST API, Scapy, Windows Npcap kernel hooks.<br/><b>Machine Learning:</b> Scikit-learn, PyTorch/TensorFlow, Joblib.<br/><b>Frontend & Telemetry:</b> React 18, Vite, Tailwind CSS, Server-Sent Events (SSE).<br/><b>Database & Auth:</b> SQLite, SQLAlchemy, Bcrypt, HMAC-SHA256 JWT.", style_table_cell)
        ],
        [
            Paragraph("<b>System Architecture</b>", style_table_cell_bold),
            Paragraph("<b>4 Decoupled Tiers:</b><br/>1. <i>Presentation Tier:</i> React SOC operations dashboard & real-time telemetry.<br/>2. <i>API Gateway:</i> Flask microservices enforcing JWT auth & role-based access control.<br/>3. <i>Service & Logic Tier:</i> Stateful FlowManager & asynchronous LivePredictor queue.<br/>4. <i>Persistence Tier:</i> Relational audit ledger, detection history, and serialized models.", style_table_cell)
        ],
        [
            Paragraph("<b>Machine Learning Models</b>", style_table_cell_bold),
            Paragraph("Primary model: Support Vector Machine (SVM) with Gaussian Radial Basis Function (RBF) kernel (96.00% accuracy, 96.01% precision, 0.9853 ROC-AUC). Benchmarked against Long Short-Term Memory (LSTM) recurrent networks, Deep Multilayer Perceptrons (MLP), and Regularized Logistic Regression. Optimization convergence tracked via Frobenius weight displacement norm.", style_table_cell)
        ],
        [
            Paragraph("<b>Anti-Leakage Data Pipeline</b>", style_table_cell_bold),
            Paragraph("Enforced strict 70/15/15 stratified train/val/test split <i>before</i> fitting any StandardScaler or LabelEncoder. Incorporated epsilon damping (eps = 10^-8) to prevent zero-variance divisions and inverse frequency class weighting to combat class imbalance on UNSW-NB15.", style_table_cell)
        ],
        [
            Paragraph("<b>Live Network Sniffing</b>", style_table_cell_bold),
            Paragraph("Promiscuous packet interception reassembled via <b>direction-agnostic 5-tuple canonical hashing</b>: SHA256(min(IP_src:P_src, IP_dst:P_dst) || max(IP_src:P_src, IP_dst:P_dst) || Proto). Sustained sub-millisecond inference latency (0.0512 ms/flow, ~19,531 flows/sec) across 1,384+ recorded live flows.", style_table_cell)
        ],
        [
            Paragraph("<b>Key Challenges & Solutions</b>", style_table_cell_bold),
            Paragraph("<i>Challenge:</i> Packet drops during synchronous inference.<br/><i>Solution:</i> Decoupled packet sniffing into an asynchronous thread feeding a thread-safe queue, enabling batched ML scoring without blocking network capture.", style_table_cell)
        ],
        [
            Paragraph("<b>Lloyd's Personal Contribution</b>", style_table_cell_bold),
            Paragraph("Architected the stateful FlowManager, implemented canonical 5-tuple hashing, engineered the JWT authentication and RBAC decorators, integrated Scapy packet capture hooks, and optimized the inference latency pipeline.", style_table_cell)
        ]
    ]
    t_nids = Table(nids_breakdown_data, colWidths=[120, 407])
    t_nids.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), BG_LIGHT]),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_nids)

    # Page 9: Project 2 (Food Ordering Platform)
    story.append(PageBreak())
    story.append(Paragraph("Project 2: Full-Stack Food Ordering Platform with Payment Gateway", style_subheading))
    
    pitch_food = (
        "\"My second project is a production-style Full-Stack Food Ordering Web Platform developed to provide a responsive, commission-free "
        "ordering experience for local restaurants. I built the application with a modular React frontend and a RESTful backend service, integrating "
        "a secure payment gateway sandbox. The system features dynamic menu filtering, persistent cart state management, and an end-to-end checkout "
        "workflow where payment integrity is verified server-side using cryptographic HMAC-SHA256 signature validation before order fulfillment. "
        "The platform also includes JWT-based user authentication and an administrative dashboard for real-time order tracking.\""
    )
    story.append(make_callout(
        "60-Second Spoken Elevator Pitch (Script for Recruiter & Phone Screenings)",
        [pitch_food],
        border_color=NAVY_SECONDARY,
        bg_color=BG_HIGHLIGHT
    ))

    food_breakdown_data = [
        [
            Paragraph("<b>Technical Dimension</b>", style_table_head),
            Paragraph("<b>Implementation Details & Architecture Invariants</b>", style_table_head)
        ],
        [
            Paragraph("<b>Problem Statement</b>", style_table_cell_bold),
            Paragraph("Local restaurants face exorbitant 20-30% commission fees on third-party aggregators and lack direct customer relationships. They require an agile, lightweight, and secure direct-to-consumer digital ordering channel.", style_table_cell)
        ],
        [
            Paragraph("<b>Frontend Technologies</b>", style_table_cell_bold),
            Paragraph("React SPA, Vite, Tailwind CSS / Modern CSS, Context API / Redux for global cart state, Axios for asynchronous API communication.", style_table_cell)
        ],
        [
            Paragraph("<b>Backend Technologies</b>", style_table_cell_bold),
            Paragraph("RESTful API services built with Node.js/Express <i>[Confirmation Needed: verify if Node.js or Python/Flask backend was used]</i>, modular routing, input validation middleware, and CORS configuration.", style_table_cell)
        ],
        [
            Paragraph("<b>Database Schema</b>", style_table_cell_bold),
            Paragraph("Relational database schema (PostgreSQL / MySQL) <i>[Confirmation Needed: verify exact DB]</i> modeling entities: Users, Restaurants, Menu Categories, Items, Orders, Order Items, and Payment Transactions with foreign key referential integrity.", style_table_cell)
        ],
        [
            Paragraph("<b>Payment Gateway Integration</b>", style_table_cell_bold),
            Paragraph("Integrated Razorpay / Stripe sandbox <i>[Confirmation Needed: verify gateway]</i>. Implemented secure 3-step checkout: 1) Client requests order initiation; 2) Backend generates gateway Order ID; 3) Client completes checkout modal and passes payment signature to backend, where <b>HMAC-SHA256 cryptographic verification</b> confirms payment authenticity before updating status to 'PAID'.", style_table_cell)
        ],
        [
            Paragraph("<b>Authentication & Security</b>", style_table_cell_bold),
            Paragraph("Stateless JSON Web Tokens (JWT) stored securely, password hashing with 10-12 salt rounds of Bcrypt, role-based authorization separating Customers from Restaurant Admin managers.", style_table_cell)
        ],
        [
            Paragraph("<b>Lloyd's Personal Contribution</b>", style_table_cell_bold),
            Paragraph("Architected the checkout state machine, integrated the payment gateway API and server-side signature validation, designed the cart persistence logic, and built the administrative order dispatch interface.", style_table_cell)
        ]
    ]
    t_food = Table(food_breakdown_data, colWidths=[120, 407])
    t_food.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), BG_LIGHT]),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_food)

    # ==========================================
    # 4. HR AND RECRUITER TRICKY QUESTIONS
    # ==========================================
    # Page 10 (Q1-Q5) and Page 11 (Q6-Q10)
    tricky_qa = [
        # --- Page 10: Q1 - Q5 ---
        (
            1,
            "What are your stipend expectations for this internship?",
            "My primary priority for this six-month internship is the opportunity to work on HackerRank's high-scale developer platform and learn production engineering standards under senior mentors. I am confident that HackerRank provides a fair, competitive monthly stipend in line with industry benchmarks for SDE interns in Bengaluru, and I am entirely comfortable adhering to the company's standardized intern compensation band.",
            "Why it works: Avoids prematurely quoting a fixed number that might price you out or under-sell yourself; demonstrates professional maturity by anchoring to HackerRank's standard intern tier."
        ),
        (
            2,
            "Does HackerRank cover relocation expenses or provide accommodation assistance?",
            "I understand that companies have established corporate policies regarding relocation support and initial guesthouse accommodation for interns, and I will gladly accept whatever assistance HackerRank provides. However, I want to reassure you that relocation is not a blocker for me - I have family and local housing arrangements in Bengaluru, so I am ready to relocate independently well before the January start date.",
            "Why it works: Inquires respectfully about company benefits while eliminating any fear that you will decline the offer if relocation assistance is not provided."
        ),
        (
            3,
            "Can you extend your internship beyond six months, or join earlier in December?",
            "Regarding joining earlier, our 7th-semester university examinations wrap up in late December 2026, so early January is my earliest possible full-time start date. Regarding extending beyond June, my graduation completes in June/July 2027. My ultimate goal is to convert this internship into a full-time SDE role, so I would be thrilled to continue as a full-time engineer post-internship.",
            "Why it works: Sets clear, honest boundaries regarding university exam schedules while enthusiastically pitching your desire for full-time conversion."
        ),
        (
            4,
            "What if your college calls you back during the internship for mandatory attendance?",
            "Fortunately, that situation will not arise. At JNNCE and under VTU guidelines, our entire 8th semester is officially designated as an external industry internship semester. Course credits are awarded directly based on company project evaluations. The college requires zero on-campus attendance during regular working hours throughout this period.",
            "Why it works: Cites official academic guidelines to provide 100% legal and operational certainty to the recruiter."
        ),
        (
            5,
            "What happens if there is an administrative delay in receiving your college NOC?",
            "Our college Training and Placement Cell maintains a very proactive, structured process for issuing NOCs. However, if any unexpected administrative delay occurs, our department routinely provides an interim provisional authorization letter signed by our Head of Department on day one. I will maintain direct communication with both our placement officer and HackerRank to ensure total transparency.",
            "Why it works: Shows proactive problem-solving and offers a concrete backup solution (provisional departmental letter) to prevent onboarding delays."
        ),

        # --- Page 11: Q6 - Q10 ---
        (
            6,
            "If you receive an offer from another company while interviewing with us, how will you decide?",
            "While I am participating in other evaluation processes, HackerRank is my unequivocal first choice. I have spent years using HackerRank's platform, and the opportunity to work directly on code execution engines and developer infrastructure is unmatched. If I receive an offer from HackerRank, I will accept it immediately and withdraw from all other hiring pipelines.",
            "Why it works: Gives the recruiter highest hiring confidence. Recruiters hate extending offers to candidates who renege; this guarantees commitment."
        ),
        (
            7,
            "Can you work under intense deadline pressure and sprint crunches?",
            "Yes. During the development of our Zero-Trust NIDS capstone, we faced strict project evaluation milestones alongside our academic exams. I managed the pressure by establishing clear daily goals, prioritizing critical architectural blockers early, and communicating transparently with teammates. I remain calm and analytical when deadlines are tight.",
            "Why it works: Anchors the answer in a real academic/project scenario rather than making generic, unsupported claims."
        ),
        (
            8,
            "How do you handle technical disagreements with teammates or senior engineers?",
            "I approach disagreements with data, humility, and an open mind. If a teammate and I disagree on an architecture or design choice, I benchmark both approaches or build a minimal proof-of-concept to evaluate performance, readability, and maintainability objectively. When working with senior engineers, I share my rationale respectfully, listen to their architectural perspective, and align fully with the team's consensus.",
            "Why it works: Demonstrates high emotional intelligence, respect for senior engineering mentorship, and objective, data-driven decision-making."
        ),
        (
            9,
            "HackerRank uses technologies you might not know well, like Ruby on Rails or Go. Can you adapt?",
            "Yes, absolutely. My core foundation is built on computer science fundamentals - data structures, algorithms, object-oriented principles, and systems design. Programming languages are tools to implement these concepts. Having worked with Python, C++, Java, and SQL, I am confident in my ability to pick up Go, Ruby, or any internal framework within a couple of weeks through active documentation reading and code exploration.",
            "Why it works: Demonstrates the growth mindset that top tech firms prize: strong fundamentals enable rapid language acquisition."
        ),
        (
            10,
            "What would you do if you were assigned a task and got completely stuck for half a day?",
            "First, I would spend up to 45 minutes investigating systematically: reading error logs, checking internal documentation, reviewing codebase examples, and formulating a hypothesis. If I remain blocked, I would summarize what I tried, what the expected versus actual behavior is, and reach out to my mentor or a teammate. This respects their time while ensuring project momentum isn't stalled.",
            "Why it works: Shows balanced autonomy and collaboration: tries to solve it first, then asks smart, well-documented questions without suffering in silence."
        )
    ]

    for idx, q in enumerate(tricky_qa):
        if idx % 5 == 0:
            story.append(PageBreak())
            if idx == 0:
                story.extend(make_section_banner("4. HR and Recruiter Tricky Questions", "Diplomatic, Honest, and Strategic Responses to High-Stakes Screening Inquiries"))
        story.append(make_qa_card(q[0], q[1], "Tricky Recruiter Question", q[2], q[3]))

    # ==========================================
    # 5. QUESTIONS TO ASK THE RECRUITER
    # ==========================================
    # Page 12: Dedicated Page
    story.append(PageBreak())
    story.extend(make_section_banner("5. Strategic Questions to Ask the Recruiter", "High-Impact Reverse-Interviewing Questions to Display Maturity, Engagement, and Long-Term Value"))

    story.append(Paragraph(
        "At the end of the screening, the recruiter will ask: <i>'Do you have any questions for me?'</i> "
        "Never say 'No'. Asking thoughtful questions signals high motivation, intellectual curiosity, and that you are seriously evaluating HackerRank as your future employer.",
        style_body
    ))

    ask_recruiter_data = [
        [
            Paragraph("<b>Category</b>", style_table_head),
            Paragraph("<b>Professional Phrasing & Question Script</b>", style_table_head),
            Paragraph("<b>Strategic Recruiter Intent</b>", style_table_head)
        ],
        [
            Paragraph("<b>Team Placement & Scope</b>", style_table_cell_bold),
            Paragraph("<i>'For an SDE intern joining in January 2027, which engineering pod or product area would they typically be assigned to - such as Core Assessments, Live Interview, or Infrastructure?'</i>", style_table_cell),
            Paragraph("Shows that you understand HackerRank's product architecture and are curious about where your contributions will land.", style_table_cell)
        ],
        [
            Paragraph("<b>Mentorship & Onboarding</b>", style_table_cell_bold),
            Paragraph("<i>'Could you share how mentorship and onboarding are structured for engineering interns at HackerRank? Will interns be paired with a dedicated mentor or buddy?'</i>", style_table_cell),
            Paragraph("Signals that you value engineering guidance, want to integrate smoothly, and respect established development workflows.", style_table_cell)
        ],
        [
            Paragraph("<b>PPO & Conversion Benchmarks</b>", style_table_cell_bold),
            Paragraph("<i>'What specific milestones and performance qualities distinguish an intern who successfully converts into a full-time SDE role at the end of the six months?'</i>", style_table_cell),
            Paragraph("Demonstrates ambitious, long-term intent: you are not just looking for a temporary resume bullet, but want to earn a permanent engineering seat.", style_table_cell)
        ],
        [
            Paragraph("<b>Logistics & Joining Timeline</b>", style_table_cell_bold),
            Paragraph("<i>'What is the expected onboarding date for the January 2027 internship cohort, and are there any paperwork or background verification steps I should prepare in advance?'</i>", style_table_cell),
            Paragraph("Shows organizational foresight and enthusiasm for completing documentation without operational friction.", style_table_cell)
        ],
        [
            Paragraph("<b>Internship Compensation</b>", style_table_cell_bold),
            Paragraph("<i>'Could you please share the monthly stipend and compensation structure associated with this six-month Bengaluru onsite internship?'</i>", style_table_cell),
            Paragraph("Standard, professional inquiry that brings clarity to compensation without appearing pushy or aggressive.", style_table_cell)
        ],
        [
            Paragraph("<b>Next Steps in the Hiring Process</b>", style_table_cell_bold),
            Paragraph("<i>'What are the subsequent rounds in the evaluation process following this screening, and what is the typical timeline for feedback?'</i>", style_table_cell),
            Paragraph("Essential closing question that gives you clear visibility into the interview roadmap and next technical milestones.", style_table_cell)
        ]
    ]
    t_ask = Table(ask_recruiter_data, colWidths=[105, 238, 184])
    t_ask.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), BG_LIGHT]),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_ask)

    # ==========================================
    # 6. COMMUNICATION AND INTERVIEW TIPS
    # ==========================================
    # Page 13: Dedicated Page
    story.append(PageBreak())
    story.extend(make_section_banner("6. Communication and Interview Tips", "Frameworks, Vocal Delivery, Answering Cadence, and Psychological Readiness"))

    story.append(Paragraph("6.1 The STAR Method Adapted for Technical Screening", style_subheading))
    story.append(Paragraph(
        "Recruiters evaluate how you communicate as much as what you say. When answering behavioral or challenge-oriented questions, "
        "use the <b>STAR Framework (Situation, Task, Action, Result)</b> in an abbreviated, 45-second format:",
        style_body
    ))
    story.append(Paragraph("- <b>Situation (10s):</b> Set the technical context briefly. <i>'In our final-year Zero-Trust NIDS capstone, we were capturing live network packets...'</i>", style_bullet))
    story.append(Paragraph("- <b>Task (10s):</b> State the exact challenge. <i>'Running synchronous ML inference inside the packet-sniffing loop caused severe bottlenecks and packet drops.'</i>", style_bullet))
    story.append(Paragraph("- <b>Action (20s):</b> Detail your specific contribution. <i>'I decoupled packet capture into an asynchronous worker thread that pushed reconstructed flows into a thread-safe queue for batched inference.'</i>", style_bullet))
    story.append(Paragraph("- <b>Result (10s):</b> Conclude with measurable metrics. <i>'This eliminated packet drops and reduced per-flow latency to 0.05 milliseconds across 1,384 live flows.'</i>", style_bullet))

    story.append(Paragraph("6.2 The 45-60 Second Rule: Brevity Without Omission", style_subheading))
    story.append(Paragraph(
        "A screening call is rapid-fire. If your answer is shorter than 25 seconds, you sound unenthusiastic or unprepared. "
        "If it drags beyond 90 seconds, the recruiter loses focus and cannot complete their checklist. "
        "Aim for the <b>45 to 60-second sweet spot (80-110 words)</b>. If the recruiter wants more technical depth, let them ask follow-up questions.",
        style_body
    ))

    story.append(Paragraph("6.3 Avoiding Memorized or Robotic Delivery", style_subheading))
    story.append(Paragraph(
        "Recruiters instantly detect candidates who recite memorized essays verbatim. "
        "Instead of memorizing sentences, <b>memorize bullet points and structural milestones</b>. "
        "Speak naturally in professional Indian English, use conversational transitions ('That's a great question,' 'Specifically in my case...'), "
        "and maintain an energetic, engaging vocal tone.",
        style_body
    ))

    story.append(Paragraph("6.4 Handling Questions When You Don't Know the Exact Answer", style_subheading))
    story.append(Paragraph(
        "Never guess, fabricate facts, or freeze in silence. Use the <b>'Honest Acknowledgement + Logical Thought Process'</b> technique:<br/>"
        "<i>'I haven't worked with that specific tool directly in my academic projects, but based on my understanding of backend microservices, "
        "it operates similarly to X. If tasked with implementing it, I would review the official documentation, inspect existing codebase patterns, "
        "and build a minimal proof-of-concept.'</i> This demonstrates humility, honesty, and analytical maturity.",
        style_body
    ))

    story.append(Paragraph("6.5 Maintaining Absolute Consistency Across Your Answers", style_subheading))
    story.append(Paragraph(
        "Recruiters note timestamps, graduation years, and college policies. Ensure you never contradict yourself across different answers:",
        style_body
    ))
    story.append(Paragraph("- Always state: <b>Graduation year 2027</b>, currently in <b>7th semester</b>, <b>8th semester begins January 2027</b>.", style_bullet))
    story.append(Paragraph("- Always confirm: <b>Full 6-month duration</b> from <b>January to June 2027</b>, <b>100% onsite in Bengaluru</b>.", style_bullet))
    story.append(Paragraph("- Always confirm: <b>NOC is guaranteed</b> through JNNCE's dedicated 8th-semester industry internship curriculum.", style_bullet))

    # ==========================================
    # 7. MOCK INTERVIEW PRACTICE SIMULATION
    # ==========================================
    # Pages 14-16 (14 questions with practice lines)
    mock_questions = [
        # --- Page 14: Q1 - Q5 ---
        (1, "Hi Lloyd, thanks for taking the time to speak today! To get us started, could you walk me through your background and tell me a bit about yourself?",
         "Icebreaker: Assesses self-introduction, clarity of articulation, and core profile alignment.",
         ["Name, 7th sem ISE at JNNCE, 2027 batch", "Core stack: Python, C++, Java, SQL, web & ML", "2 projects: Zero-Trust NIDS & Food Ordering App", "Seeking 6-month onsite SDE internship starting Jan 2027"]),
        
        (2, "That sounds interesting! What specifically motivated you to apply for an SDE internship at HackerRank?",
         "Motivation: Assesses company knowledge, organic interest, and cultural resonance.",
         ["Active user since 2nd year practicing DSA", "Belief in skills-first developer evaluation over resume pedigree", "Excited by scale: code execution sandboxes across 40+ languages"]),
        
        (3, "I see you're currently studying in Shivamogga. Are you comfortable relocating to Bengaluru and working fully onsite from our office?",
         "Logistics Check: Eliminates relocation and remote-work friction.",
         ["100% comfortable; prefer onsite for in-person mentoring & pairing", "Family in Bengaluru; accommodation pre-arranged", "Ready to move in late December 2026"]),
        
        (4, "Can you commit to our required six-month internship duration from January 2027 through June 2027 without interruptions?",
         "Timeline Verification: Confirms no semester disruptions.",
         ["Yes, full 6 months committed (Jan-June 2027)", "8th semester dedicated exclusively to industry internship", "No competing on-campus coursework"]),
        
        (5, "Does your college officially permit you to work full-time off-campus, and can you obtain an NOC?",
         "College Policy Check: Confirms university clearance.",
         ["VTU and JNNCE mandate 8th-semester industry internships", "Placement cell issues NOC in 3-5 working days upon offer letter receipt"]),

        # --- Page 15: Q6 - Q10 ---
        (6, "Do you have any examinations, laboratory vivas, or academic reviews scheduled between January and June?",
         "Disruption Risk: Assesses potential sprint absenteeism.",
         ["No classroom exams during 8th semester", "Periodic internship report & final project viva scheduled on weekends / virtual", "Zero weekday office disruption"]),
        
        (7, "Looking at your technical profile, what would you say are your top two or three programming languages?",
         "Core Competence: Evaluates language depth over buzzwords.",
         ["Python (backend APIs, data manipulation, ML pipelines)", "C++ (DSA, algorithms, memory management)", "Java & SQL (OOP design, relational schemas)"]),
        
        (8, "Could you give me a brief, one-minute overview of your Zero-Trust AI Network Intrusion Detection project?",
         "Technical Articulation: Tests structured project explanation under a 60-second limit.",
         ["Problem: perimeter security fails against lateral attacks", "Decoupled 4-tier architecture, Scapy kernel packet interception", "5-tuple canonical hashing, SVM model with 96% accuracy, 0.05ms latency"]),
        
        (9, "What was the most challenging technical roadblock you encountered while building this intrusion detection system?",
         "Problem-Solving Depth: Assesses engineering resilience and debugging capability.",
         ["Packet drops during synchronous live frame sniffing", "Decoupled packet sniffer into async thread feeding a thread-safe queue", "Batched ML scoring eliminated packet drops"]),
        
        (10, "Tell me about your second project - the Food Ordering Platform. How did you handle the payment gateway integration?",
         "Full-Stack Integration: Verifies security awareness and API integration skills.",
         ["React frontend, RESTful backend, PostgreSQL/Node", "3-step checkout with Razorpay/Stripe sandbox", "Cryptographic HMAC-SHA256 signature verification server-side before order commit"]),

        # --- Page 16: Q11 - Q14 ---
        (11, "Our engineering stack uses technologies like Go and Ruby on Rails. How comfortable are you picking up languages you haven't used extensively?",
         "Adaptability: Assesses growth mindset and learning agility.",
         ["Solid grounding in CS fundamentals, OOP, and systems design", "Languages are tools; confident in picking up Go/Ruby in 2-3 weeks", "Proven track record picking up React and Flask quickly"]),
        
        (12, "Are you currently in the interview process with any other companies, or holding any active offers?",
         "Candidate Pipeline: Assesses timeline urgency and candidate availability.",
         ["Participating in college campus drives; in active early rounds with 2 firms", "No signed offer in hand; 100% available for HackerRank", "HackerRank is top priority; will accept immediately if selected"]),
        
        (13, "Why should we select you as an SDE intern over candidates from other engineering colleges?",
         "Closing Pitch: Evaluates confidence, self-worth, and value proposition.",
         ["Pillar 1: Strong CS fundamentals in algorithms, OOP, and databases", "Pillar 2: Proven complex project execution (real-time NIDS, full-stack platform)", "Pillar 3: 100% availability, NOC ready, Bengaluru onsite from Jan 2027"]),
        
        (14, "We have a couple of minutes left. Do you have any questions you'd like to ask me about HackerRank or the internship?",
         "Reverse Interviewing: Evaluates intellectual curiosity and role seriousness.",
         ["Which engineering pod/product would an intern join in January?", "What qualities distinguish an intern who earns a full-time PPO conversion?"])
    ]

    for idx, q in enumerate(mock_questions):
        if idx in [0, 5, 10]:
            story.append(PageBreak())
            if idx == 0:
                story.extend(make_section_banner("7. Mock Interview Practice Simulation", "Realistic 10-12 Minute Screening Simulation with 14 Sequenced Questions and Blank Practice Lines"))
        
        q_card_data = [
            [
                Paragraph(f"<b>Prompt {q[0]}: \"{q[1]}\"</b>", style_card_q),
                Paragraph(f"<b>SIMULATION</b>", style_tag)
            ],
            [
                Paragraph(f"<b>Recruiter Intent:</b> {q[2]}", style_card_why),
                Paragraph("", style_tag)
            ],
            [
                Paragraph("<b>Recommended Talking Points:</b> " + " - ".join(q[3]), style_body),
                Paragraph("", style_tag)
            ],
            [
                Paragraph("<b>Your Notes / Practice Points:</b><br/>" + ("_" * 95 + "<br/>") * 2 + ("_" * 95), style_practice_line),
                Paragraph("", style_tag)
            ]
        ]
        t_mock = Table(q_card_data, colWidths=[CONTENT_WIDTH - 85, 75])
        t_mock.setStyle(TableStyle([
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
        story.append(KeepTogether([t_mock, Spacer(1, 4)]))

    # ==========================================
    # 8. LAST-MINUTE REVISION SHEET
    # ==========================================
    # Page 17: Dedicated Executive Cheat Sheet
    story.append(PageBreak())
    story.extend(make_section_banner("8. Last-Minute Revision Sheet (Cheat Sheet)", "One-Page Pre-Call Executive Briefing: Review 5 Minutes Before Your Recruiter Phone Call"))

    story.append(Paragraph(
        "Keep this cheat sheet in front of you during your screening call. It synthesizes all critical numbers, dates, pitch lines, and questions onto a single high-visibility reference page.",
        style_body
    ))

    cheat_data = [
        [
            Paragraph("<b>Core Candidate Facts</b>", style_table_head),
            Paragraph("<b>Logistical Affirmations</b>", style_table_head),
            Paragraph("<b>Top Technical Keywords</b>", style_table_head)
        ],
        [
            Paragraph(
                "- <b>Name:</b> Lloyd Gopi<br/>"
                "- <b>Degree:</b> B.E. Information Science (ISE)<br/>"
                "- <b>College:</b> JNNCE, Shivamogga<br/>"
                "- <b>Semester:</b> 7th Semester<br/>"
                "- <b>Graduation:</b> Batch 2027",
                style_table_cell
            ),
            Paragraph(
                "- <b>Duration:</b> 6 Months (Jan-June 2027)<br/>"
                "- <b>Joining Date:</b> Early January 2027<br/>"
                "- <b>Work Mode:</b> 100% Onsite Bengaluru<br/>"
                "- <b>NOC Status:</b> Approved (VTU 8th Sem)<br/>"
                "- <b>Housing:</b> Arranged in Bengaluru",
                style_table_cell
            ),
            Paragraph(
                "- <b>Languages:</b> Python, C++, Java, SQL<br/>"
                "- <b>Systems:</b> Scapy, Npcap, Linux cgroups<br/>"
                "- <b>Web & Auth:</b> React, Flask, JWT, Bcrypt<br/>"
                "- <b>ML:</b> SVM, RBF Kernel, Scikit-learn<br/>"
                "- <b>Security:</b> Zero-Trust, HMAC-SHA256",
                style_table_cell
            )
        ]
    ]
    t_cheat = Table(cheat_data, colWidths=[175, 175, 177])
    t_cheat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('BACKGROUND', (0, 1), (-1, 1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_cheat)
    story.append(Spacer(1, 4))

    cheat_sections = [
        ("30-Second Elevator Pitch (Word-for-Word Memorization)",
         "\"I'm Lloyd Gopi, 7th semester Information Science student at JNNCE graduating in 2027. I specialize in backend systems and applied ML using Python, C++, Java, and SQL. I recently built a real-time Zero-Trust Network Intrusion Detection System achieving 96% accuracy and 0.05ms inference latency, as well as a full-stack food ordering platform with HMAC-secured payments. I'm completely ready for a 6-month onsite internship in Bengaluru starting January 2027 with full college NOC clearance.\""),
        
        ("Five Non-Negotiable Screening Affirmations (Say YES Confidently)",
         "1. <b>Six-Month Duration:</b> YES, available full-time from January 2027 through June 2027 without academic disruptions.<br/>"
         "2. <b>Onsite Bengaluru:</b> YES, 100% committed to working onsite in the Bengaluru office 5 days a week.<br/>"
         "3. <b>College NOC Approval:</b> YES, VTU & JNNCE formally authorize 8th-semester industry internships; NOC turnaround is 3-5 days.<br/>"
         "4. <b>Joining Date:</b> YES, available to join in early January 2027 immediately following 7th-semester examinations.<br/>"
         "5. <b>HackerRank Priority:</b> YES, HackerRank is my absolute #1 top-choice company; if selected, I will accept immediately."),
        
        ("Project 1 Metrics Snapshot: Zero-Trust AI NIDS",
         "- <b>Problem:</b> Ineffective perimeter firewalls against lateral intrusion; training-test data leakage in ML.<br/>"
         "- <b>Architecture:</b> 4 decoupled tiers (React UI, Flask REST API with JWT, stateful FlowManager, SQLite persistence).<br/>"
         "- <b>Performance:</b> SVM with RBF kernel: <b>96.00% accuracy, 96.01% precision, 0.9853 ROC-AUC, 2.22% FPR</b>.<br/>"
         "- <b>Speed & Throughput:</b> <b>0.0512 ms/flow inference</b> (~19,531 flows/sec) across 1,384+ live packets captured via Scapy.<br/>"
         "- <b>Key Technique:</b> Direction-agnostic 5-tuple canonical hashing + async worker queue preventing packet loss."),
        
        ("Project 2 Metrics Snapshot: Full-Stack Food Ordering Platform",
         "- <b>Stack:</b> React 18, Vite, Tailwind CSS, Node.js/Express REST backend, PostgreSQL/MongoDB database.<br/>"
         "- <b>Security & Payments:</b> Razorpay/Stripe sandbox with server-side <b>HMAC-SHA256 payment signature verification</b>.<br/>"
         "- <b>State Management:</b> Dynamic shopping cart persistence, multi-step order state machine, role-based JWT auth."),
        
        ("Why HackerRank? (The Perfect 3-Sentence Justification)",
         "\"I've used HackerRank since my 2nd year of college to practice DSA, so joining as an engineer feels like coming full circle. I love the mission of matching developer skills with opportunity rather than pedigree. Building high-scale execution sandboxes and live interview tools handling millions of code submissions across 40+ languages is the exact systems challenge I want to work on.\""),
        
        ("Three Go-To Questions to Ask the Recruiter",
         "1. <i>'For an SDE intern joining the Bengaluru center in January, which engineering pod or product area would they be placed in?'</i><br/>"
         "2. <i>'Could you describe how mentorship is structured for interns and what qualities separate an intern who earns a PPO conversion?'</i><br/>"
         "3. <i>'What are the next technical rounds in the evaluation process, and what is the expected timeline for feedback?'</i>")
    ]

    for title, content in cheat_sections:
        story.append(make_callout(title, [content], border_color=NAVY_PRIMARY, bg_color=BG_LIGHT))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"HackerRank Preparation Guide successfully compiled to: {output_path}")

if __name__ == "__main__":
    create_guide_pdf()
