"""Shared brand system for the Real Estate Game Toolkit product line.

All PDFs in the product line import from this module so the catalogue
looks like one family on WhatsApp. Palette: deep night-navy + sand gold
(dark luxury direction, disciplined contrast).

NOTE: Built-in PDF fonts are WinAnsi only. Never use the rupee glyph
(U+20B9) or unicode arrows in canvas text - use "INR", "->" instead.
"""

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm

# ---------------------------------------------------------------- palette
NAVY = HexColor("#0E2233")      # primary surface
NAVY_DEEP = HexColor("#081621") # cover background
GOLD = HexColor("#C9A227")      # accent
SAND = HexColor("#E8DCC0")      # light accent text on navy
INK = HexColor("#1B2733")       # body text on white
SLATE = HexColor("#5A6B7A")     # secondary text
PAPER = HexColor("#FBF8F1")     # warm paper background
LINE = HexColor("#D8D2C4")      # hairlines on paper
GREEN = HexColor("#2E7D5B")     # positive verdicts
RED = HexColor("#B3402E")       # warnings / negative leverage

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

BRAND_NAME = "THE PROPERTY GAME SERIES"
BRAND_SUB = "Decision tools for India - UAE - Saudi real estate"
WHATSAPP_CTA = "WhatsApp: [YOUR-WA-NUMBER]  |  Catalogue: [YOUR-WA-CATALOGUE-LINK]"
DISCLAIMER = ("This material is an independent educational adaptation inspired by "
              "frameworks popularised in W. J. Poorvu's 'The Real Estate Game' (1999). "
              "It is not affiliated with or endorsed by the author or publisher. "
              "Nothing here is investment, legal or tax advice for your specific case.")


# ---------------------------------------------------------------- styles
def styles():
    s = {}
    s["h1"] = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=22,
                             leading=26, textColor=NAVY, spaceAfter=8)
    s["h2"] = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13.5,
                             leading=17, textColor=NAVY, spaceBefore=10, spaceAfter=5)
    s["h3"] = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11,
                             leading=14, textColor=GOLD, spaceBefore=8, spaceAfter=3)
    s["body"] = ParagraphStyle("body", fontName="Helvetica", fontSize=9.6,
                               leading=13.6, textColor=INK, spaceAfter=5)
    s["small"] = ParagraphStyle("small", fontName="Helvetica", fontSize=8,
                                leading=10.5, textColor=SLATE)
    s["q"] = ParagraphStyle("q", fontName="Helvetica-Bold", fontSize=9.8,
                            leading=13, textColor=NAVY, spaceBefore=7, spaceAfter=2)
    s["opt"] = ParagraphStyle("opt", fontName="Helvetica", fontSize=9.2,
                              leading=12.4, textColor=INK, leftIndent=14, spaceAfter=1)
    s["callout"] = ParagraphStyle("callout", fontName="Helvetica-Oblique", fontSize=9.6,
                                  leading=13.5, textColor=NAVY, leftIndent=8,
                                  borderPadding=6, spaceBefore=6, spaceAfter=6)
    return s


# ------------------------------------------------------- page decoration
def draw_page_frame(canvas, doc, title=""):
    """Header rule + footer for interior pages."""
    canvas.saveState()
    # header
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.drawString(MARGIN, PAGE_H - 12 * mm, BRAND_NAME)
    canvas.setFillColor(GOLD)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 12 * mm, title.upper())
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, PAGE_H - 14 * mm, PAGE_W - MARGIN, PAGE_H - 14 * mm)
    # footer
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN, 14 * mm, PAGE_W - MARGIN, 14 * mm)
    canvas.setFillColor(SLATE)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(MARGIN, 10 * mm, WHATSAPP_CTA)
    canvas.drawRightString(PAGE_W - MARGIN, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def draw_cover(canvas, kicker, title_lines, subtitle, price_tag, footer_note):
    """Full-bleed dark cover. Call inside onPage of the first page."""
    canvas.saveState()
    canvas.setFillColor(NAVY_DEEP)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # gold frame
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.4)
    canvas.rect(10 * mm, 10 * mm, PAGE_W - 20 * mm, PAGE_H - 20 * mm, stroke=1, fill=0)
    # brand
    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H - 30 * mm, BRAND_NAME)
    canvas.setFillColor(SAND)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H - 36 * mm, BRAND_SUB)
    # kicker
    canvas.setFillColor(SAND)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H - 78 * mm, kicker.upper())
    # title
    canvas.setFillColor(HexColor("#FFFFFF"))
    y = PAGE_H - 96 * mm
    for line in title_lines:
        canvas.setFont("Helvetica-Bold", 30)
        canvas.drawCentredString(PAGE_W / 2, y, line)
        y -= 13 * mm
    # rule
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1)
    canvas.line(PAGE_W / 2 - 25 * mm, y + 4 * mm, PAGE_W / 2 + 25 * mm, y + 4 * mm)
    # subtitle
    canvas.setFillColor(SAND)
    canvas.setFont("Helvetica", 11.5)
    ty = y - 8 * mm
    for line in subtitle:
        canvas.drawCentredString(PAGE_W / 2, ty, line)
        ty -= 6 * mm
    # price tag
    if price_tag:
        canvas.setFillColor(GOLD)
        canvas.roundRect(PAGE_W / 2 - 30 * mm, 52 * mm, 60 * mm, 12 * mm, 2.5 * mm,
                         stroke=0, fill=1)
        canvas.setFillColor(NAVY_DEEP)
        canvas.setFont("Helvetica-Bold", 11)
        canvas.drawCentredString(PAGE_W / 2, 56 * mm, price_tag)
    # footer
    canvas.setFillColor(SAND)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(PAGE_W / 2, 30 * mm, footer_note)
    canvas.setFillColor(SLATE)
    canvas.setFont("Helvetica", 7)
    canvas.drawCentredString(PAGE_W / 2, 18 * mm, "(c) 2026 - All rights reserved")
    canvas.restoreState()
