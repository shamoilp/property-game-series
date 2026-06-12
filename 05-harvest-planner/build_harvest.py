"""Harvest Planner PDF - the exit decision tool (hold / refinance / sell)
with the tax overlay for India, UAE and KSA. Original content."""

import sys
sys.path.insert(0, r"C:\Users\user\real-estate-game-toolkit\00-business")
import brand
from brand import MARGIN, PAGE_W, NAVY, SAND, PAPER, LINE, SLATE, GOLD, GREEN, RED
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, NextPageTemplate, PageBreak)

S = brand.styles()
OUT = r"C:\Users\user\real-estate-game-toolkit\05-harvest-planner\Harvest-Planner.pdf"


def on_cover(canvas, doc):
    brand.draw_cover(
        canvas,
        kicker="The Property Game Series",
        title_lines=["THE HARVEST", "PLANNER"],
        subtitle=["Hold. Refinance. Sell. Redevelop.",
                  "The decision most investors never actually make -",
                  "with the tax math for India, UAE and Saudi Arabia."],
        price_tag="INR 499  |  AED 29  |  SAR 29",
        footer_note="Tax figures as of June 2026 - verify before any transaction")


def on_page(canvas, doc):
    brand.draw_page_frame(canvas, doc, "Harvest Planner")


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                      topMargin=20 * mm, bottomMargin=20 * mm)
frame = Frame(MARGIN, 18 * mm, PAGE_W - 2 * MARGIN, A4[1] - 40 * mm, id="f")
doc.addPageTemplates([
    PageTemplate(id="cover", frames=[frame], onPage=on_cover),
    PageTemplate(id="body", frames=[frame], onPage=on_page),
])

st = [NextPageTemplate("body"), PageBreak()]

# ------------------------------------------------ the one number
st.append(Paragraph("The number that decides everything", S["h1"]))
st.append(Paragraph(
    "Most owners judge a property by what it cost them. The market does not care what "
    "it cost you. The only honest question is: <b>what is my return on the equity "
    "trapped in this property TODAY?</b>", S["body"]))
st.append(Paragraph(
    "Return on Current Equity (RCE) = this year's cash flow after financing, divided by "
    "what you would walk away with if you sold today (market value, minus selling costs, "
    "minus loan payoff, minus exit taxes).", S["callout"]))
st.append(Paragraph(
    "A flat bought 12 years ago for Rs 40 lakh, now worth Rs 1.4 crore, renting at "
    "Rs 30,000/month: the owner feels brilliant - rent covers the long-paid-off EMI and "
    "the 'yield on cost' is 9%. But after-tax walk-away equity is about Rs 1.25 crore, "
    "and the net rent is maybe Rs 3 lakh. RCE = 2.4%. A fixed deposit beats it without "
    "tenants. That owner is not holding an investment; he is holding a memory.",
    S["body"]))
st.append(Paragraph(
    "Once you know your RCE, there are only four moves. The tree below picks one.",
    S["body"]))

# ------------------------------------------------ decision tree
st.append(Paragraph("The harvest decision tree", S["h2"]))
tree = [
    ["GATE", "QUESTION", "IF YES", "IF NO"],
    ["1", Paragraph("<b>Job check.</b> Is the property still doing the job you bought it for "
                    "(income, future use, family home, land bank)?", S["body"]),
     "Go to Gate 2", "SELL track - go to Gate 4"],
    ["2", Paragraph("<b>RCE check.</b> Is your Return on Current Equity above your safe "
                    "alternative (FD/sukuk/index yield) by at least 2 points?", S["body"]),
     "HOLD - review yearly", "Go to Gate 3"],
    ["3", Paragraph("<b>Release check.</b> Can a refinance / loan-against-property pull out "
                    "equity at a rate BELOW the return you can earn redeploying it - after "
                    "the property still covers the new payment from rent?", S["body"]),
     "REFINANCE - harvest without selling", "Go to Gate 4"],
    ["4", Paragraph("<b>Upgrade check.</b> Would capital spending (renovation, extra floor, "
                    "use-change, replotting) raise value by MORE than it costs, within 2 years?",
                    S["body"]),
     "REDEVELOP, then re-run Gate 2", "SELL - run the exit-tax table below"],
]
w = PAGE_W - 2 * MARGIN
t = Table(tree, colWidths=[12 * mm, w * 0.50, w * 0.19, w * 0.19], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.6),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 1), (0, -1), 12),
    ("TEXTCOLOR", (0, 1), (0, -1), GOLD),
    ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("TEXTCOLOR", (2, 1), (2, -1), GREEN),
    ("TEXTCOLOR", (3, 1), (3, -1), RED),
    ("FONTNAME", (2, 1), (3, -1), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, None]),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
st.append(t)
st.append(Paragraph(
    "Run the tree once a year, on a fixed date. The harvest is a decision, not an "
    "accident - unmade decisions quietly become 'hold', which is how 2.4% RCE assets "
    "survive in portfolios for decades.", S["small"]))

# ------------------------------------------------ exit tax overlay
st.append(Paragraph("The exit-tax overlay (what SELL actually costs)", S["h2"]))
overlay = [
    ["", "INDIA (NRI seller)", "UAE", "SAUDI ARABIA"],
    ["Tax on the gain",
     Paragraph("LTCG (held >24m): 12.5% + surcharge/cess, no indexation. STCG: slab rates. "
               "NRIs cannot use the old 20%-indexed option.", S["small"]),
     Paragraph("No capital gains tax for individuals.", S["small"]),
     Paragraph("No personal income tax on an individual's gain (unless it amounts to a "
               "business activity / entity sale).", S["small"])],
    ["Withholding at sale",
     Paragraph("Buyer deducts TDS u/s 195 - on FULL price unless you hold a s.197 "
               "certificate. Cash-flow hit of 13-15%+ until refund.", S["small"]),
     Paragraph("None.", S["small"]),
     Paragraph("None on the seller; RETT 5% filed before Najiz transfer (contractually "
               "allocated between parties).", S["small"])],
    ["Friction on the NEXT purchase",
     Paragraph("Stamp duty 5-8% + registration.", S["small"]),
     Paragraph("~6-7.5% (4% DLD + fees + agency).", S["small"]),
     Paragraph("RETT 5% + broker up to 2.5%.", S["small"])],
    ["Reliefs / planning",
     Paragraph("s.54 reinvest in Indian residential; s.54EC bonds (Rs 50L cap); time NRO "
               "repatriation across FY windows (USD 1M/yr).", S["small"]),
     Paragraph("Mortgage early-settlement fee (commonly ~1%, capped) - check before "
               "listing; golden-visa threshold if downsizing below AED 2M.", S["small"]),
     Paragraph("Zakat: trading-intent property was Zakatable while held; settle before "
               "counting proceeds. First-home RETT exemption may help your buyer - a "
               "negotiation chip.", S["small"])],
    ["The trap",
     Paragraph("Selling in April vs March changes WHICH year's USD 1M repatriation window "
               "you burn.", S["small"]),
     Paragraph("Selling mid-lease: tenant rights and 12-month notice rules transfer to "
               "your buyer and discount your price.", S["small"]),
     Paragraph("Old paper deed not yet digitised = weeks of delay exactly when your "
               "buyer's financing approval is expiring.", S["small"])],
]
t = Table(overlay, colWidths=[w * 0.16, w * 0.30, w * 0.25, w * 0.29], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 8.5),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"), ("FONTSIZE", (0, 1), (0, -1), 8.2),
    ("TEXTCOLOR", (0, 1), (0, -1), NAVY),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, None]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
st.append(t)

# ------------------------------------------------ refinance vs sell
st.append(Paragraph("Refinance: the harvest nobody tells you about", S["h2"]))
st.append(Paragraph(
    "Selling pays exit taxes and re-entry friction (see table). Refinancing pulls "
    "equity out with <b>zero tax event</b> in all three markets - borrowing is not "
    "income. The test from Gate 3, in numbers:", S["body"]))
for b in [
    "India: loan-against-property at ~9-10.5%. Worth it only if redeployment earns more AND the property's rent still covers the new EMI. Rarely clears for low-yield residential; often clears for commercial.",
    "UAE: equity release on a tenanted unit at ~4.5-5.5% against an 7-9% gross yield can fund the next deposit - the standard ladder strategy. Watch the early-settlement math if you plan to sell within 2-3 years anyway.",
    "KSA: refinancing/equity release through SAMA-licensed players against Ejar-registered income. If your original deal carries a subsidised REDF rate, think twice before touching it - you will not get that rate back.",
]:
    st.append(Paragraph(f"&bull;  {b}", S["opt"]))

# ------------------------------------------------ worksheet
st.append(Paragraph("Your harvest worksheet (one property, ten minutes)", S["h2"]))
ws_rows = [
    ["#", "LINE", "YOUR NUMBER"],
    ["1", "Realistic market value today (3 broker opinions, take the middle)", ""],
    ["2", "Selling costs (brokerage, marketing, legal)", ""],
    ["3", "Loan payoff (incl. any early-settlement fee)", ""],
    ["4", "Exit taxes from the overlay table (incl. TDS cash-flow gap if India)", ""],
    ["5", "WALK-AWAY EQUITY  =  1 - 2 - 3 - 4", ""],
    ["6", "This year's cash flow after financing (from your BOE sheet)", ""],
    ["7", "RETURN ON CURRENT EQUITY  =  6 / 5", ""],
    ["8", "Your safe alternative yield (FD / sukuk / index)", ""],
    ["9", "Verdict from the tree:  HOLD / REFINANCE / REDEVELOP / SELL", ""],
]
t = Table(ws_rows, colWidths=[10 * mm, w * 0.66, w * 0.34 - 10 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("FONTNAME", (1, 5), (1, 5), "Helvetica-Bold"),
    ("FONTNAME", (1, 7), (1, 7), "Helvetica-Bold"),
    ("FONTNAME", (1, 9), (1, 9), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, None]),
    ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
st.append(t)
st.append(Spacer(1, 8))
st.append(Paragraph(
    "Pair this with the BOE Deal Analyzer (line 6 comes straight from it) and the "
    "due-diligence pack for whichever market you redeploy into. Message KIT on WhatsApp "
    "for the full series.", S["callout"]))
st.append(Paragraph(brand.DISCLAIMER, S["small"]))
doc.build(st)
print("Built:", OUT)
