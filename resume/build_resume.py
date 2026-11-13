"""Builds static/kristian-sagi-resume.pdf.

Edit the content below, then run (needs reportlab):
    python resume/build_resume.py
Keep facts in sync with content/work/_index.md and content/now/_index.md.

Look: Apple-style — Inter (the site's font, static TTFs in resume/fonts/, SIL OFL),
Apple greys, blue links without underlines, sentence-case headings, hairline rules,
dates right-aligned.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (HRFlowable, KeepTogether, ListFlowable, ListItem, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "static" / "kristian-sagi-resume.pdf"

# ---- Fonts: Inter (same family as the website) ------------------------------
FONTS = ROOT / "fonts"
for name, file in [
    ("Inter", "Inter-Regular.ttf"),
    ("Inter-Medium", "Inter-Medium.ttf"),
    ("Inter-SemiBold", "Inter-SemiBold.ttf"),
    ("Inter-Italic", "Inter-Italic.ttf"),
    ("InterDisplay-SemiBold", "InterDisplay-SemiBold.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / file)))
# <b> → SemiBold, <i> → Italic inside paragraphs
pdfmetrics.registerFontFamily("Inter", normal="Inter", bold="Inter-SemiBold",
                              italic="Inter-Italic", boldItalic="Inter-SemiBold")

# ---- Apple palette ------------------------------------------------------------
INK = colors.HexColor("#1D1D1F")
MUTED = colors.HexColor("#6E6E73")
RULE = colors.HexColor("#D2D2D7")
FILL = colors.HexColor("#F5F5F7")
BLUE = "#0066CC"

PAGE_W = A4[0] - 2 * 20 * mm - 12   # usable width (page margins + 6pt frame padding each side)

S = {
    "name": ParagraphStyle("name", fontName="InterDisplay-SemiBold", fontSize=30, leading=34, textColor=INK),
    "tag": ParagraphStyle("tag", fontName="Inter", fontSize=12.5, leading=17, textColor=INK, spaceBefore=4),
    "contact": ParagraphStyle("contact", fontName="Inter", fontSize=8.8, leading=12, textColor=MUTED, spaceBefore=6),
    "h": ParagraphStyle("h", fontName="InterDisplay-SemiBold", fontSize=14, leading=18, textColor=INK,
                        spaceBefore=16, spaceAfter=6),
    "body": ParagraphStyle("body", fontName="Inter", fontSize=9.2, leading=13.8, textColor=INK, alignment=TA_LEFT),
    "org": ParagraphStyle("org", fontName="Inter-SemiBold", fontSize=10.2, leading=14, textColor=INK, spaceBefore=9),
    "role": ParagraphStyle("role", fontName="Inter-Medium", fontSize=9.2, leading=13, textColor=INK),
    "period": ParagraphStyle("period", fontName="Inter", fontSize=8.6, leading=13, textColor=MUTED, alignment=2),
    "bullet": ParagraphStyle("bullet", fontName="Inter", fontSize=9.0, leading=13.2, textColor=INK),
    "cell": ParagraphStyle("cell", fontName="Inter", fontSize=8.8, leading=13, textColor=INK),
    "cellh": ParagraphStyle("cellh", fontName="Inter-SemiBold", fontSize=8.4, leading=12, textColor=MUTED),
}

LINK = '<link href="{0}" color="' + BLUE + '">{1}</link>'


def h(text):
    return Paragraph(text, S["h"])


def rule(space_before=10, space_after=0):
    return HRFlowable(width="100%", thickness=0.5, color=RULE, spaceBefore=space_before, spaceAfter=space_after)


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(t, S["bullet"]), leftIndent=11, value="•", bulletFontName="Inter",
                  bulletColor=MUTED, bulletFontSize=6.5) for t in items],
        bulletType="bullet", start="•", bulletFontName="Inter", bulletFontSize=6.5,
        bulletColor=MUTED, leftIndent=11, bulletOffsetY=-1.2, spaceBefore=2, spaceAfter=2,
    )


def role_line(title, period):
    """Role on the left, dates right-aligned in grey."""
    t = Table([[Paragraph(title, S["role"]), Paragraph(period, S["period"])]],
              colWidths=[PAGE_W - 38 * mm, 38 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def job(org, roles):
    """roles: list of (title, period, [bullets])"""
    flow = [Paragraph(org, S["org"])]
    for title, period, items in roles:
        block = [role_line(title, period)]
        if items:
            block.append(bullets(items))
        flow.append(KeepTogether(block))
    return flow


story = [
    Paragraph("Kristian Sägi", S["name"]),
    Paragraph("Technology Leader &amp; CEO. Building resilient companies, teams and systems.", S["tag"]),
    Paragraph(
        "Tallinn, Estonia  ·  "
        + LINK.format("mailto:kristian@kristiansagi.com", "kristian@kristiansagi.com") + "  ·  "
        + LINK.format("https://kristiansagi.com", "kristiansagi.com") + "  ·  "
        + LINK.format("https://www.linkedin.com/in/kristiansagi/", "linkedin.com/in/kristiansagi"),
        S["contact"],
    ),
    rule(12, 0),

    h("Professional summary"),
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

    rule(14, 0),
    h("Professional experience"),
    *job("Entringo — Tallinn, Estonia", [
        ("Chief Executive Officer", "2026 – Present", [
            "Leading a provider of integrated vehicle flow systems — ticketless ANPR parking, yard and traffic "
            "management — combining in-house software with purpose-built hardware.",
            "Moving Tallinn Airport to fully ticketless, number-plate-based parking, unifying every parking product "
            "(taxi lanes, rideshare, short and long term, VIP, tenant access) on one platform, delivered with Hansab Eesti.",
            "Serving customers across the Baltics, including frictionless paid parking for Business Garden Vilnius.",
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
    *job("Assert AS / Fujitsu Estonia — Tallinn, Estonia", [
        ("Software Engineer → Product Manager, Persona", "1996 – 2003", [
            "Part of the original team that built the first version of Persona, the HR and payroll software still in "
            "daily use three decades later; later led the team responsible for Persona V2.",
        ]),
    ]),
    Paragraph("Other roles", S["org"]),
    Paragraph(
        "GreenhouseCI — Head of Business Development (2016 – 2017)  ·  Simplify OÜ — Design Thinking Coach (2016)",
        S["body"]),

    rule(14, 0),
    h("Board, advisory &amp; mentorship"),
    bullets([
        "<b>Advisor</b> to technology companies on scaling engineering organizations, product strategy and leadership (Present)",
        "<b>Key Mentor</b> — Ajujaht Startup Accelerator (2022 – Present)",
        "<b>Coach</b> — ESA Business Incubation Centre Estonia (2018 – Present)",
        "Member — Estonian Business Angels Network, EstBAN (2015 – 2018); Estonian Startup Leaders Club (2017 – 2018)",
    ]),

    rule(14, 0),
    h("Talks &amp; media"),
    bullets([
        "Keynote: <i>To Build Fast, You Need to Be Slow</i> — sTARTUp Day 2022",
        "Featured in " + LINK.format("https://www.youtube.com/watch?v=vI9hbJPjkdA", "<i>The Story of Codemagic</i>") + " — documentary on the Google Flutter partnership",
        "Podcasts and interviews: The Pursuit of Scrappiness (2023), TalentHub (2022), Äripäev, Postimees — "
        + LINK.format("https://kristiansagi.com/media/", "kristiansagi.com/media"),
    ]),

    rule(14, 0),
    h("Education"),
    Paragraph("<b>University of Tartu</b>  <font color='#6E6E73'>B.Sc., Engineering Physics (Applied Physics)</font>", S["body"]),
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
    colWidths=[PAGE_W / 3] * 3,
    hAlign="LEFT",
    cornerRadii=[8, 8, 8, 8],
)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), FILL),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 1.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ("TOPPADDING", (0, 0), (-1, 0), 9),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
    ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
]))
story += [
    KeepTogether([rule(14, 0), h("Skills"), table]),
    rule(14, 0),
    h("Languages"),
    Paragraph("Estonian <font color='#6E6E73'>Native</font>   ·   English <font color='#6E6E73'>Full professional</font>"
              "   ·   Russian <font color='#6E6E73'>Limited working</font>   ·   German <font color='#6E6E73'>Elementary</font>",
              S["body"]),
]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Inter", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(A4[0] / 2, 10 * mm, f"Kristian Sägi  ·  Résumé  ·  {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4,
    leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
    title="Kristian Sägi — Résumé", author="Kristian Sägi",
    subject="Technology Leader & CEO", creator="kristiansagi.com",
    keywords="Kristian Sägi, CEO, Technology Leadership, Engineering Leadership",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"Wrote {OUT}")
