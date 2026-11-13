"""Builds static/kristian-sagi-resume.pdf.

Edit the content below, then run (needs reportlab):
    python resume/build_resume.py
Keep facts in sync with content/work/_index.md and content/now/_index.md.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

OUT = Path(__file__).resolve().parent.parent / "static" / "kristian-sagi-resume.pdf"

INK = colors.HexColor("#111111")
MUTED = colors.HexColor("#555555")
RULE = colors.HexColor("#D9D9D9")
FILL = colors.HexColor("#F4F4F2")

S = {
    "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=INK),
    "tag": ParagraphStyle("tag", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=INK, spaceBefore=2),
    "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=8.8, leading=12, textColor=MUTED, spaceBefore=3),
    "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=INK, spaceBefore=11, spaceAfter=4),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.2, leading=13.2, textColor=INK, alignment=TA_LEFT),
    "org": ParagraphStyle("org", fontName="Helvetica-Bold", fontSize=9.4, leading=13, textColor=INK, spaceBefore=6),
    "role": ParagraphStyle("role", fontName="Helvetica", fontSize=9.2, leading=13, textColor=INK, spaceBefore=1, spaceAfter=1),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.0, leading=12.6, textColor=INK),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.6, leading=11, textColor=INK),
    "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=8.6, leading=11, textColor=INK),
}

LINK = '<link href="{0}" color="#111111"><u>{1}</u></link>'


def h(text):
    return Paragraph(text.upper(), S["h"])


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(t, S["bullet"]), leftIndent=11, value="•") for t in items],
        bulletType="bullet", start="•", bulletFontSize=7, leftIndent=11, bulletOffsetY=-1,
        spaceBefore=1, spaceAfter=2,
    )


def job(org, roles):
    """roles: list of (title, period, [bullets])"""
    flow = [Paragraph(org, S["org"])]
    for title, period, items in roles:
        block = [Paragraph(f"<b>{title}</b>  <font color='#555555'>|  {period}</font>", S["role"])]
        if items:
            block.append(bullets(items))
        flow.append(KeepTogether(block))
    return flow


story = [
    Paragraph("KRISTIAN SÄGI", S["name"]),
    Paragraph("Technology Leader &amp; CEO  |  Building resilient companies, teams and systems", S["tag"]),
    Paragraph(
        "Tallinn, Estonia (open to relocation)  ·  "
        + LINK.format("mailto:kristian@kristiansagi.com", "kristian@kristiansagi.com") + "  ·  "
        + LINK.format("https://kristiansagi.com", "kristiansagi.com") + "  ·  "
        + LINK.format("https://www.linkedin.com/in/kristiansagi/", "linkedin.com/in/kristiansagi"),
        S["contact"],
    ),

    h("Professional Summary"),
    Paragraph(
        "Technology and engineering leader with over two decades of experience founding companies, building "
        "high-performing teams and scaling global software organizations. Currently CEO of Entringo. Co-founded "
        "Playtech Mobile and scaled it from inception to $120M in annual revenue, co-founded the globally used "
        "mobile CI/CD platform Codemagic, and built Dynatrace’s Tallinn engineering hub.",
        S["body"]),
    Spacer(1, 4),
    Paragraph(
        "Combines a founder’s mindset with executive discipline — translating complex technology challenges into "
        "scalable systems, empowered teams and measurable outcomes. Experienced in product strategy, P&amp;L "
        "leadership and organizational transformation across multinational, distributed teams.",
        S["body"]),

    h("Professional Experience"),
    *job("Entringo — Tallinn, Estonia", [
        ("Chief Executive Officer", "2026 – Present", [
            "Leading a provider of integrated vehicle flow systems — ticketless ANPR parking, yard and traffic "
            "management — combining in-house software with purpose-built hardware.",
        ]),
    ]),
    *job("Dynatrace Inc — Tallinn, Estonia", [
        ("Director of Engineering / Site Lead", "2022 – 2025", [
            "Scaled Dynatrace’s Tallinn engineering hub, tripling headcount and establishing culture, processes "
            "and a new office from the ground up.",
            "Directed delivery of high-performance monitoring products, aligning releases with global strategy.",
            "Led cross-functional engineering, product and operations teams across multiple countries.",
            "Partnered with global leadership on portfolio strategy and long-term scaling plans.",
        ]),
    ]),
    *job("Nevercode Ltd / Codemagic — London &amp; Tallinn", [
        ("Co-Founder &amp; Head of Product Strategy", "2017 – 2019", [
            "Co-founded and scaled Codemagic, a CI/CD platform for mobile developers now used globally.",
            "Defined and executed product strategy, achieving recognition in the Google Flutter ecosystem.",
            "Led engineering and product teams through early-stage growth and funding.",
        ]),
        ("Advisory Board Member", "2019 – 2022", [
            "Advised leadership on scaling, product strategy, market positioning and investor relations.",
        ]),
    ]),
    *job("Playtech Mobile (Playtech plc) — Estonia", [
        ("Co-Founder &amp; CTO, Mobile Division", "2005 – 2015", [
            "Built and scaled Playtech Mobile from inception to $120M in annual revenue across multiple "
            "regulated international markets.",
            "Built and led an organization of 100+ engineers and product managers across distributed teams.",
            "Delivered product strategy, architecture and execution for 100+ clients globally.",
            "Introduced an agile delivery model, moving release cycles from quarterly to monthly.",
        ]),
        ("Product Manager, Bingo Network", "2004 – 2005", [
            "Managed 24/7 global operations across multiple regulated markets; directed product enhancements "
            "and customer integrations.",
        ]),
    ]),
    Paragraph("Earlier roles (selected)", S["org"]),
    Paragraph(
        "GreenhouseCI — Head of Business Development (2016 – 2017)  ·  Simplify OÜ — Design Thinking Coach (2016)  ·  "
        "Fujitsu — Product Manager (1999 – 2003)  ·  Assert AS — Software Engineer (1996 – 1999)",
        S["body"]),

    h("Board, Advisory &amp; Mentorship"),
    bullets([
        "<b>Advisor</b> to technology companies on scaling engineering organizations, product strategy and leadership (Present)",
        "<b>Key Mentor</b> — Ajujaht Startup Accelerator (2022 – Present)",
        "<b>Coach</b> — ESA Business Incubation Centre Estonia (2018 – Present)",
        "Member — Estonian Business Angels Network, EstBAN (2015 – 2018); Estonian Startup Leaders Club (2017 – 2018)",
    ]),

    h("Talks &amp; Media"),
    bullets([
        "Keynote: <i>To Build Fast, You Need to Be Slow</i> — sTARTUp Day 2022",
        "Featured in <i>The Story of Codemagic</i> — documentary on the Google Flutter partnership",
        "Podcasts and interviews: The Pursuit of Scrappiness (2023), TalentHub (2022), Äripäev, Postimees — "
        + LINK.format("https://kristiansagi.com/media/", "kristiansagi.com/media"),
    ]),

    h("Education"),
    Paragraph("<b>University of Tartu</b> — B.Sc., Engineering Physics (Applied Physics)", S["body"]),
]

skills = [
    ["Leadership &amp; Strategy", "Technology &amp; Delivery", "Growth &amp; Partnerships"],
    ["Executive Leadership (CEO)", "Software Architecture", "Business Development"],
    ["P&amp;L Leadership", "DevTools &amp; CI/CD", "Partner Ecosystems"],
    ["Product Management", "Cloud Platforms &amp; SDK Integration", "Ecosystem Development"],
    ["Cross-Functional Leadership", "Agile Delivery at Scale", "Mentoring &amp; Coaching"],
]
table = Table(
    [[Paragraph(c, S["cellh" if r == 0 else "cell"]) for c in row] for r, row in enumerate(skills)],
    colWidths=[58 * mm, 62 * mm, 54 * mm],
)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), FILL),
    ("GRID", (0, 0), (-1, -1), 0.5, RULE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
]))
story += [
    KeepTogether([h("Skills"), table]),
    h("Languages"),
    Paragraph("Estonian (Native)  |  English (Full Professional)  |  Russian (Limited Working)  |  German (Elementary)", S["body"]),
]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Kristian Sägi — Résumé  ·  {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4,
    leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
    title="Kristian Sägi — Résumé", author="Kristian Sägi",
    subject="Technology Leader & CEO", creator="kristiansagi.com",
    keywords="Kristian Sägi, CEO, Technology Leadership, Engineering Leadership",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"Wrote {OUT}")
