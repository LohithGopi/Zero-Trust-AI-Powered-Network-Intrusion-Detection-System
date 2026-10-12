import os
import re
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas

REPORT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(REPORT_DIR, "Chapter_4_Results_and_Analysis.md")
FIG_DIR = os.path.join(REPORT_DIR, "figures")
OUTPUT_PDF = os.path.join(REPORT_DIR, "Chapter_4_Results_and_Analysis.pdf")


class Chapter4NumberedCanvas(canvas.Canvas):
    """Two-pass canvas that renders academic headers, footers, and total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"Total PDF Pages Generated: {num_pages}")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_decorations(self, page_count):
        self.saveState()
        width, height = A4

        # Header
        self.setFont("Times-Italic", 9.5)
        self.setFillColor(colors.HexColor("#334155"))
        self.drawString(48, height - 36, "Zero Trust AI-Powered Network Intrusion Detection System")
        self.drawRightString(width - 48, height - 36, "Chapter 4: Results and Analysis")
        self.setStrokeColor(colors.HexColor("#94A3B8"))
        self.setLineWidth(0.6)
        self.line(48, height - 42, width - 48, height - 42)

        # Footer
        self.line(48, 44, width - 48, 44)
        self.setFont("Times-Roman", 9.5)
        self.drawString(48, 30, "Dept. of Information Science & Engineering, JNNCE Shivamogga")
        self.drawRightString(width - 48, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_styles():
    base = getSampleStyleSheet()
    NAVY = colors.HexColor("#0F172A")
    BLUE = colors.HexColor("#1D4ED8")
    SLATE = colors.HexColor("#1E293B")

    styles = {
        "ChapterHeader": ParagraphStyle(
            "ChapterHeader", parent=base["Normal"], fontName="Times-Bold",
            fontSize=14, leading=18, alignment=TA_CENTER, textColor=BLUE, spaceAfter=3
        ),
        "ChapterTitle": ParagraphStyle(
            "ChapterTitle", parent=base["Normal"], fontName="Times-Bold",
            fontSize=18.5, leading=23, alignment=TA_CENTER, textColor=NAVY, spaceAfter=7
        ),
        "MetaLine": ParagraphStyle(
            "MetaLine", parent=base["Normal"], fontName="Times-Roman",
            fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=SLATE, spaceAfter=2.5
        ),
        "H1": ParagraphStyle(
            "H1", parent=base["Normal"], fontName="Times-Bold",
            fontSize=13.5, leading=17.5, textColor=NAVY, spaceBefore=10, spaceAfter=4, keepWithNext=True
        ),
        "H2": ParagraphStyle(
            "H2", parent=base["Normal"], fontName="Times-Bold",
            fontSize=11.5, leading=15.0, textColor=BLUE, spaceBefore=8, spaceAfter=3.5, keepWithNext=True
        ),
        "Body": ParagraphStyle(
            "Body", parent=base["Normal"], fontName="Times-Roman",
            fontSize=10.5, leading=15.0, alignment=TA_JUSTIFY, textColor=SLATE, spaceAfter=4.5
        ),
        "Bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"], fontName="Times-Roman",
            fontSize=10.3, leading=14.5, alignment=TA_JUSTIFY, leftIndent=16, firstLineIndent=-10,
            textColor=SLATE, spaceAfter=3.4
        ),
        "SubBullet": ParagraphStyle(
            "SubBullet", parent=base["Normal"], fontName="Times-Roman",
            fontSize=10.1, leading=14.0, alignment=TA_JUSTIFY, leftIndent=26, firstLineIndent=-10,
            textColor=SLATE, spaceAfter=2.8
        ),
        "Caption": ParagraphStyle(
            "Caption", parent=base["Normal"], fontName="Times-BoldItalic",
            fontSize=9.2, leading=12.4, alignment=TA_CENTER, textColor=NAVY, spaceBefore=3.0, spaceAfter=6.0
        ),
        "TableTitle": ParagraphStyle(
            "TableTitle", parent=base["Normal"], fontName="Times-Bold",
            fontSize=10.0, leading=13.0, alignment=TA_LEFT, textColor=NAVY, spaceBefore=7, spaceAfter=3.5, keepWithNext=True
        ),
        "TblHeader": ParagraphStyle(
            "TblHeader", parent=base["Normal"], fontName="Times-Bold",
            fontSize=7.5, leading=9.4, textColor=colors.white
        ),
        "TblCell": ParagraphStyle(
            "TblCell", parent=base["Normal"], fontName="Times-Roman",
            fontSize=7.4, leading=9.2, textColor=SLATE
        ),
        "Equation": ParagraphStyle(
            "Equation", parent=base["Normal"], fontName="Times-BoldItalic",
            fontSize=10.0, leading=13.5, alignment=TA_CENTER, textColor=NAVY
        ),
        "PlaceholderTitle": ParagraphStyle(
            "PlaceholderTitle", parent=base["Normal"], fontName="Times-Bold",
            fontSize=9.5, leading=12.0, textColor=colors.HexColor("#1E3A8A"), spaceAfter=2
        ),
        "PlaceholderBody": ParagraphStyle(
            "PlaceholderBody", parent=base["Normal"], fontName="Times-Roman",
            fontSize=9.0, leading=11.8, textColor=SLATE, leftIndent=8, firstLineIndent=-5, spaceAfter=1.5
        )
    }
    return styles


def clean_latex_and_md_to_rl_html(text: str) -> str:
    """Convert inline LaTeX math and Markdown bold/italic/code into ReportLab XML."""
    s = text.strip()

    # Specific LaTeX math expressions used in Chapter 4
    replacements = [
        (r"$\|\Delta W^{(e)}\|_F = \sum_l \|W^{(l,e)} - W^{(l,e-1)}\|_F$", "||ΔW^(e)||_F = Σ_l ||W^(l,e) - W^(l,e-1)||_F"),
        (r"$\|\Delta W^{(e)}\|_F$", "||ΔW^(e)||_F"),
        (r"$\|\Delta W^{(1)}\|_F$", "||ΔW^(1)||_F"),
        (r"$\|\Delta W\|_F$", "||ΔW||_F"),
        (r"$\Delta W^{(e)}$", "ΔW^(e)"),
        (r"$\Delta W$", "ΔW"),
        (r"$\Delta t = 0$", "Δt = 0"),
        (r"$N \times 1 \times 122$", "N × 1 × 122"),
        (r"$(38 + 3 + 70 + 11 = 122)$", "(38 + 3 + 70 + 11 = 122)"),
        (r"$X_{train}, y_{train}$", "X_train, y_train"),
        (r"$X_{val}, y_{val}$", "X_val, y_val"),
        (r"$X_{test}, y_{test}$", "X_test, y_test"),
        (r"$X_{train\_raw}$", "X_train_raw"),
        (r"$X_{val\_raw}$", "X_val_raw"),
        (r"$X_{test\_raw}$", "X_test_raw"),
        (r"$X_{train}, X_{val}, X_{test}$", "X_train, X_val, X_test"),
        (r"$\mu_{train}, \sigma_{train}$", "μ_train, σ_train"),
        (r"$\mu \approx 0, \sigma \approx 1$", "μ ≈ 0, σ ≈ 1"),
        (r"$W^{(1)} \in \mathbb{R}^{d \times 64}$", "W^(1) in R^(d×64)"),
        (r"$W^{(2)} \in \mathbb{R}^{64 \times 32}$", "W^(2) in R^(64×32)"),
        (r"$W^{(3)} \in \mathbb{R}^{32 \times C}$", "W^(3) in R^(32×C)"),
        (r"$d \in \{15, 19, 22\}$", "d in {15, 19, 22}"),
        (r"$X_{raw} \in \mathbb{R}^{1 \times d}$", "X_raw in R^(1×d)"),
        (r"$Z = (X_{raw} - \mu_{train}) / \sigma_{train}$", "Z = (X_raw - μ_train) / σ_train"),
        (r"$\hat{p} \in [0, 1]^C$", "p_hat in [0, 1]^C"),
        (r"$\hat{y} = \arg\max_c \hat{p}_c$", "y_hat = argmax_c p_hat_c"),
        (r"$\hat{L}$", "L_hat"),
        (r"$\text{Conf} < 0.60$", "Conf < 0.60"),
        (r"$0.60 \le \text{Conf} < 0.85$", "0.60 <= Conf < 0.85"),
        (r"$\text{Conf} \ge 0.85$", "Conf >= 0.85"),
        (r"$ROC\text{-}AUC$", "ROC-AUC"),
        (r"$F_1\text{-Score}$", "F1-Score"),
        (r"$F_1$", "F1"),
        (r"$FPR < 2.5\%$", "FPR < 2.5%"),
        (r"$FPR$", "FPR"),
        (r"$FNR$", "FNR"),
        (r"$TPR$", "TPR"),
        (r"$TP + FP = 0$", "TP + FP = 0"),
        (r"$FN = 930, TP = 0$", "FN = 930, TP = 0"),
        (r"$TP$", "TP"),
        (r"$TN$", "TN"),
        (r"$FP$", "FP"),
        (r"$FN$", "FN"),
        (r"$N_{test} = 3,750$", "N_test = 3,750"),
        (r"$N_{test}$", "N_test"),
        (r"$(N)$", "(N)"),
        (r"$10^0$", "10^0"),
        (r"$10^8$", "10^8"),
        (r"$[0.60, 0.85)$", "[0.60, 0.85)"),
        (r"$\ge 60\%$", ">= 60%"),
        (r"$\ge 85\%$", ">= 85%"),
        (r"$\ge$", ">="),
        (r"$\le$", "<="),
        (r"$\rightarrow$", "->"),
        (r"$\times$", "×"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)

    # Strip remaining inline $...$
    s = re.sub(r"\$([^$]+)\$", r"\1", s)

    # Escape XML entities (&, <, >)
    s = escape(s)

    # Convert Markdown **bold**, *italic*, `code`
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)
    s = re.sub(r"`(.+?)`", r"<font name='Courier' size='8.4'>\1</font>", s)
    return s


def add_figure(story, styles, rel_path, caption, max_height=165):
    path = os.path.join(REPORT_DIR, rel_path.replace("/", os.sep))
    if not os.path.exists(path):
        return
    img = Image(path)
    avail_w = 499.0
    ratio = img.imageHeight / float(img.imageWidth)
    w = avail_w
    h = w * ratio
    if h > max_height:
        h = max_height
        w = h / ratio
    img.drawWidth = w
    img.drawHeight = h
    img.hAlign = "CENTER"
    story.append(Spacer(1, 3))
    story.append(KeepTogether([
        img,
        Paragraph(clean_latex_and_md_to_rl_html(caption), styles["Caption"])
    ]))
    story.append(Spacer(1, 3))


def add_markdown_table(story, styles, table_lines):
    clean_rows = []
    for r in table_lines:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if all(set(c) <= set(":- ") for c in cells):
            continue
        clean_rows.append(cells)
    if not clean_rows:
        return

    num_cols = max(len(r) for r in clean_rows)
    avail_w = 505.0

    # Calculate proportional column widths based on max text length per column
    col_weights = []
    for c_idx in range(num_cols):
        max_len = max(
            (len(re.sub(r"[*`$]", "", row[c_idx])) if c_idx < len(row) else 8)
            for row in clean_rows
        )
        col_weights.append(max(8.0, min(float(max_len), 48.0)))

    total_weight = sum(col_weights)
    col_widths = [(w / total_weight) * avail_w for w in col_weights]

    data = []
    for r_idx, row in enumerate(clean_rows):
        row_cells = []
        for c_idx in range(num_cols):
            val = row[c_idx] if c_idx < len(row) else ""
            html_val = clean_latex_and_md_to_rl_html(val)
            style = styles["TblHeader"] if r_idx == 0 else styles["TblCell"]
            row_cells.append(Paragraph(html_val, style))
        data.append(row_cells)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#94A3B8")),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3.0),
    ]))
    story.append(t)
    story.append(Spacer(1, 4))


def add_placeholder_box(story, styles, quote_lines):
    flowables = []
    for idx, qline in enumerate(quote_lines):
        cleaned = qline.lstrip(">").strip()
        if not cleaned:
            continue
        html = clean_latex_and_md_to_rl_html(cleaned)
        if idx == 0:
            flowables.append(Paragraph(html, styles["PlaceholderTitle"]))
        else:
            if html.startswith("- "):
                html = "• " + html[2:]
            flowables.append(Paragraph(html, styles["PlaceholderBody"]))

    if not flowables:
        return

    tbl = Table([[flowables]], colWidths=[503.0])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ("BOX", (0, 0), (-1, -1), 0.85, colors.HexColor("#1D4ED8")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(Spacer(1, 2))
    story.append(KeepTogether([tbl]))
    story.append(Spacer(1, 2.5))


def add_display_equation(story, styles, eq_line):
    raw = eq_line.strip().strip("$").strip()
    if "Accuracy" in raw:
        formatted = (
            "Accuracy = (TP + TN) / (TP + TN + FP + FN)    |    "
            "Precision = TP / (TP + FP)    |    "
            "Recall (ADR) = TP / (TP + FN)"
        )
    elif "F_1" in raw:
        formatted = (
            "F1-Score = (2 × Precision × Recall) / (Precision + Recall)    |    "
            "False-Positive Rate (FPR) = FP / (FP + TN)"
        )
    else:
        formatted = clean_latex_and_md_to_rl_html(raw)

    tbl = Table([[Paragraph(escape(formatted), styles["Equation"])]], colWidths=[495.0])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(Spacer(1, 2))
    story.append(tbl)
    story.append(Spacer(1, 4))


def generate_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF, pagesize=A4,
        leftMargin=48, rightMargin=48, topMargin=52, bottomMargin=52
    )
    styles = build_styles()
    story = []

    with open(MD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    table_buffer = []
    quote_buffer = []

    def flush_buffers():
        nonlocal table_buffer, quote_buffer
        if table_buffer:
            add_markdown_table(story, styles, table_buffer)
            table_buffer = []
        if quote_buffer:
            add_placeholder_box(story, styles, quote_buffer)
            quote_buffer = []

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        # Table rows
        if stripped.startswith("|") and stripped.endswith("|"):
            if quote_buffer:
                add_placeholder_box(story, styles, quote_buffer)
                quote_buffer = []
            table_buffer.append(stripped)
            continue
        elif table_buffer:
            add_markdown_table(story, styles, table_buffer)
            table_buffer = []

        # Blockquote rows (Screenshot Placeholders)
        if stripped.startswith(">"):
            quote_buffer.append(stripped)
            continue
        elif quote_buffer:
            add_placeholder_box(story, styles, quote_buffer)
            quote_buffer = []

        if not stripped or stripped == "---":
            continue

        # Display equation $$ ... $$
        if stripped.startswith("$$") and stripped.endswith("$$"):
            add_display_equation(story, styles, stripped)
            continue

        # Image ![caption](path)
        img_match = re.match(r"^!\[(.*?)\]\((.*?)\)$", stripped)
        if img_match:
            caption_txt = img_match.group(1)
            rel_path = img_match.group(2)
            add_figure(story, styles, rel_path, caption_txt, max_height=165)
            continue

        # Chapter Title (# CHAPTER 4: ...)
        if stripped.startswith("# "):
            story.append(Paragraph("CHAPTER 4", styles["ChapterHeader"]))
            story.append(Paragraph("RESULTS AND ANALYSIS", styles["ChapterTitle"]))
            story.append(HRFlowable(
                width="100%", thickness=1.8, color=colors.HexColor("#1D4ED8"),
                spaceBefore=0, spaceAfter=6
            ))
            continue

        # Project Title / Department metadata lines at top
        if stripped.startswith("**Project Title:**") or stripped.startswith("**Department:**"):
            story.append(Paragraph(clean_latex_and_md_to_rl_html(stripped), styles["MetaLine"]))
            continue

        # Section H1 (## 4.x ...)
        if stripped.startswith("## "):
            story.append(Paragraph(clean_latex_and_md_to_rl_html(stripped[3:]), styles["H1"]))
            story.append(HRFlowable(
                width="100%", thickness=0.8, color=colors.HexColor("#CBD5E1"),
                spaceBefore=0, spaceAfter=5
            ))
            continue

        # Subsection H2 (### 4.x.y ...)
        if stripped.startswith("### "):
            story.append(Paragraph(clean_latex_and_md_to_rl_html(stripped[4:]), styles["H2"]))
            continue

        # Table Titles (**Table 4.x: ...**)
        if stripped.startswith("**Table 4."):
            story.append(Paragraph(clean_latex_and_md_to_rl_html(stripped), styles["TableTitle"]))
            continue

        # Indented sub-bullets (   - ...)
        if line.startswith("   - "):
            html = "• " + clean_latex_and_md_to_rl_html(stripped[2:])
            story.append(Paragraph(html, styles["SubBullet"]))
            continue

        # Top-level bullets (- ...) or numbered items (1. ...)
        if stripped.startswith("- "):
            html = "• " + clean_latex_and_md_to_rl_html(stripped[2:])
            story.append(Paragraph(html, styles["Bullet"]))
            continue

        num_match = re.match(r"^(\d+\.)\s+(.*)$", stripped)
        if num_match:
            prefix = num_match.group(1)
            rest = clean_latex_and_md_to_rl_html(num_match.group(2))
            story.append(Paragraph(f"<b>{prefix}</b> {rest}", styles["Bullet"]))
            continue

        # Standard paragraph
        story.append(Paragraph(clean_latex_and_md_to_rl_html(stripped), styles["Body"]))

    flush_buffers()
    doc.build(story, canvasmaker=Chapter4NumberedCanvas)
    print(f"Successfully generated PDF: {OUTPUT_PDF}")


if __name__ == "__main__":
    generate_pdf()
