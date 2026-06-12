"""Build the free lead-magnet PDF: 'Which Real Estate Player Are You?'"""

import sys
sys.path.insert(0, r"C:\Users\user\real-estate-game-toolkit\00-business")
import brand
from brand import (MARGIN, PAGE_W, GOLD, NAVY, SAND, PAPER, LINE, SLATE,
                   GREEN, RED, INK)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                Paragraph, Spacer, Table, TableStyle,
                                NextPageTemplate, PageBreak)

S = brand.styles()
OUT = r"C:\Users\user\real-estate-game-toolkit\01-player-scorecard\Which-Player-Are-You-Scorecard.pdf"

# ------------------------------------------------------------ content
QUESTIONS = [
    ("When you have spare capital, your instinct is to:",
     ["Park it somewhere that pays me while I sleep",
      "Hunt for something mispriced I can resell higher",
      "Buy an asset that pays rent every single month",
      "Buy raw potential - land or an ugly building I can transform"]),
    ("How many hours per week can you genuinely give to property?",
     ["Under 2 hours - I have a demanding career",
      "5-10 hours in bursts, when a deal is live",
      "A steady 5-8 hours, every week, forever",
      "20+ hours - I want this to become my business"]),
    ("A tenant calls at 11pm about a burst pipe. You feel:",
     ["Horrified - this is exactly why I never want direct ownership",
      "Indifferent - I plan to sell before tenants are my problem",
      "Fine - I have a plumber's number saved for this",
      "Curious - what does this tell me about build quality?"]),
    ("Your honest reaction to paperwork (title deeds, NOCs, approvals):",
     ["I will pay someone to never see it",
      "I read only what affects my exit price",
      "I keep a neat file and renew everything on time",
      "I enjoy it - approvals are where value gets created"]),
    ("Which return story excites you most?",
     ["9% a year, audited, with zero phone calls",
      "Buy at 70, sell at 100 within 18 months",
      "7% yield today, rising with every rent renewal",
      "Land at 40, build for 60, sell the project at 160"]),
    ("How much of your net worth would you put into ONE property deal?",
     ["Under 10% - diversification is non-negotiable",
      "10-25% if the discount is screaming",
      "25-40% in a solid rental I understand",
      "40%+ - concentration is how builders win"]),
    ("Your relationship with debt / financing:",
     ["Avoid it - I invest only what I have",
      "Use it short-term to amplify a flip",
      "A comfortable long-term loan the rent can carry",
      "Stack it - construction finance is my raw material"]),
    ("When a market crashes 20%, you:",
     ["Feel glad my exposure is small and spread out",
      "Get excited - distressed sellers are my favourite sellers",
      "Check my rents - if tenants stay, I sleep fine",
      "Buy land - it is cheapest when cranes stop moving"]),
    ("Pick the skill you actually have today:",
     ["Earning a strong salary and saving consistently",
      "Sensing what something is worth before others do",
      "Managing people, vendors and small recurring problems",
      "Coordinating many moving parts toward a deadline"]),
    ("Your investment horizon for property money:",
     ["10+ years - it is my retirement layer",
      "6 months to 2 years per deal",
      "5-15 years, collecting rent throughout",
      "2-5 years per project, then roll into the next"]),
    ("How do you feel about negotiating face to face?",
     ["I would rather a platform set the price",
      "I love it - the negotiation IS the profit",
      "I negotiate firmly but want a long relationship",
      "I negotiate daily - contractors, officials, buyers"]),
    ("What does 'risk' mean to you in property?",
     ["Losing principal - so I minimise any single bet",
      "Overpaying - so I only buy below intrinsic value",
      "Vacancy - so I buy where tenants always exist",
      "Delay - so I control approvals and contractors tightly"]),
    ("Your knowledge of your local property market is:",
     ["Honestly thin - I rely on research by others",
      "Sharp on prices - I track listings like a stock screen",
      "Deep on rents - I know what every street fetches",
      "Deep on land - I know who owns what and what is coming"]),
    ("Which headline makes you read the full article?",
     ["'New regulated fractional ownership rules announced'",
      "'Distress sales rise in premium segment'",
      "'Rental yields hit five-year high'",
      "'New expressway corridor approved'"]),
    ("If a deal needs a partner, you want one who:",
     ["Runs everything - I just want clean reporting",
      "Brings deal flow I cannot see on my own",
      "Shares the management load fifty-fifty",
      "Brings construction or approval muscle"]),
    ("Money you make should arrive:",
     ["Quietly, as distributions and appreciation",
      "In lumps, at each exit",
      "Monthly, like a second salary",
      "In large tranches as project milestones close"]),
    ("Your reaction to 'this building needs a new roof':",
     ["Deal-breaker - I want nothing that needs fixing",
      "Discount lever - I will price it in twice over",
      "Budget item - reserves exist for exactly this",
      "Opportunity - while the roof is open, add a floor"]),
    ("How do you track a property investment?",
     ["Quarterly statement is enough",
      "Price alerts and comparable sales, weekly",
      "A rent ledger I update monthly",
      "A project tracker with 40 line items"]),
    ("Which mistake scares you most?",
     ["Being locked into something illiquid",
      "Selling too early and watching it double",
      "A tenant who stops paying and will not leave",
      "A project stuck at 80% complete"]),
    ("Ten years from now, you want to say:",
     ["'My money compounded while I built my career'",
      "'I did twelve great deals and never overpaid'",
      "'My rents cover my family's entire lifestyle'",
      "'You see that building? I built that.'"]),
]

PROFILES = [
    ("A", "THE PASSIVE ALLOCATOR",
     "Capital-rich, time-poor. You win by selecting vehicles and managers, not properties. "
     "Your scoreboard metric is net distributed yield after fees and tax - nothing else.",
     ["Listed REITs and regulated fractional platforms (small-ticket commercial)",
      "Pre-leased commercial through managed platforms; audited rental funds",
      "UAE: completed, tenanted units with property management contracts",
      "KSA: REIT funds on Tadawul; avoid direct ownership unless you live there"],
     "Blind spot: fees. A 2% annual platform fee on a 8.5% yield asset takes about "
     "a quarter of your income stream. Read the fee stack before the brochure.",
     "First move: list every fee between the tenant's rent and your bank account."),
    ("B", "THE DEAL HUNTER",
     "You profit on entry price, not on holding. Your edge is valuation speed - knowing "
     "what something is worth before the market reprices it. The flip is your format.",
     ["India Tier 1: resale flats in buildings 8-15 years old, priced below new launches",
      "India Tier 2: pre-launch to possession arbitrage where RERA timelines are credible",
      "UAE: off-plan with staged payment plans - but model the full payment ladder",
      "KSA: under-priced units near giga-project announcements, before infrastructure lands"],
     "Blind spot: exit liquidity. A 30% discount means nothing in a market where the "
     "average resale takes 14 months. Time-to-sell is part of the price.",
     "First move: for your target area, find the real average days-on-market for resales."),
    ("C", "THE LANDLORD-OPERATOR",
     "You build a rent machine. Operations - tenants, maintenance, renewals - are not a "
     "chore to you, they are the business. Your metric is cash flow after EVERYTHING.",
     ["India Tier 1: small commercial (shops, clinics, offices) at 7-9% yields beats residential at 2-3%",
      "India Tier 2/3: residential near colleges, hospitals, industrial corridors",
      "UAE Northern Emirates: 8-10% gross yields - but audit service charges first",
      "KSA: residential in Riyadh/Jeddah growth districts; Ejar contracts standardise your rights"],
     "Blind spot: gross vs net. Service charges, brokerage, vacancy months and repairs "
     "routinely turn an advertised 9% into a real 5.5%. Compute net, always.",
     "First move: take any listing and build its true net yield - you will be shocked."),
    ("D", "THE BUILDER-DEVELOPER",
     "You create value that did not exist - land into plots, plots into buildings. Highest "
     "return potential, highest dependence on approvals, contractors and timing.",
     ["India Tier 2/3: plotted development along new expressway and airport corridors",
      "India: redevelopment partnerships with land-owning families (you bring execution)",
      "UAE: small-scale townhouse/villa development in newly opened freehold zones",
      "KSA: istiraha (rest-house) compounds and small residential infill in expanding districts"],
     "Blind spot: the approval clock. Every month of delay is interest paid with no "
     "revenue. Your real competitor is not other builders - it is time.",
     "First move: map every approval your next project needs, with realistic durations."),
]

# ------------------------------------------------------------ build
def on_cover(canvas, doc):
    brand.draw_cover(
        canvas,
        kicker="A 5-minute self-assessment",
        title_lines=["WHICH PLAYER", "ARE YOU?"],
        subtitle=["Find your natural position in the real estate game",
                  "before you put a single rupee, dirham or riyal at risk.",
                  "",
                  "20 questions  |  4 player types  |  India - UAE - KSA playbooks"],
        price_tag="FREE  -  SHARE THIS PDF",
        footer_note="From the maker of practical tax & investment toolkits for Gulf-based professionals",
    )

def on_page(canvas, doc):
    brand.draw_page_frame(canvas, doc, "Which Player Are You?")

doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=MARGIN, rightMargin=MARGIN,
                      topMargin=20 * mm, bottomMargin=20 * mm)
frame = Frame(MARGIN, 18 * mm, PAGE_W - 2 * MARGIN, A4[1] - 40 * mm, id="f")
doc.addPageTemplates([
    PageTemplate(id="cover", frames=[frame], onPage=on_cover),
    PageTemplate(id="body", frames=[frame], onPage=on_page),
])

story = [NextPageTemplate("body"), PageBreak()]

# --- page 2: why this matters + the four forces
story.append(Paragraph("Most people lose money in property before they buy", S["h1"]))
story.append(Paragraph(
    "They lose it at the moment they choose a deal that fits someone else's life. "
    "A salaried CFO buying a half-built flat 2,000 km away is playing a builder's game "
    "with a passive investor's calendar. A retired couple flipping off-plan units is "
    "playing a trader's game with rent-collector's nerves. The deal was never the "
    "problem - the <b>mismatch</b> was.", S["body"]))
story.append(Paragraph(
    "Harvard Business School's classic framing treats real estate as a game with four "
    "interacting forces. Before any deal, ask where you stand on each:", S["body"]))

force_rows = [
    ["FORCE", "THE QUESTION IT ASKS YOU"],
    ["The Property", "What exactly produces the income - location, product, tenant demand?"],
    ["The Players", "Who is on the other side of the table, and what do they need?"],
    ["Capital Markets", "Whose money funds this, at what cost, and when can it be pulled?"],
    ["External Environment", "What regulation, infrastructure or demographic wave moves this market?"],
]
t = Table(force_rows, colWidths=[42 * mm, PAGE_W - 2 * MARGIN - 42 * mm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("TEXTCOLOR", (0, 1), (0, -1), NAVY),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, None]),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 7),
]))
story.append(t)
story.append(Spacer(1, 6))
story.append(Paragraph(
    "This scorecard settles the fifth force - <b>you</b>. Answer the 20 questions "
    "honestly (what you would actually do, not what sounds impressive), count your "
    "letters, and read your profile. It takes five minutes and may save you five years.",
    S["body"]))
story.append(Paragraph(
    "How to score: circle one option per question. A / B / C / D each map to one player "
    "type. Your highest count is your primary type; your second-highest is your "
    "partnership style - the kind of player you should team up with, or evolve into.",
    S["callout"]))

# --- questions
story.append(Paragraph("The 20 Questions", S["h1"]))
for i, (q, opts) in enumerate(QUESTIONS, 1):
    story.append(Paragraph(f"{i}. {q}", S["q"]))
    for letter, opt in zip("ABCD", opts):
        story.append(Paragraph(f"<b>{letter}.</b>  {opt}", S["opt"]))

# --- scoring
story.append(Spacer(1, 10))
story.append(Paragraph("Your Score", S["h1"]))
score_rows = [
    ["LETTER", "COUNT", "PLAYER TYPE"],
    ["A", "", "The Passive Allocator - selects vehicles, not properties"],
    ["B", "", "The Deal Hunter - profits on entry price and exit timing"],
    ["C", "", "The Landlord-Operator - builds a monthly rent machine"],
    ["D", "", "The Builder-Developer - creates value from land and approvals"],
]
t = Table(score_rows, colWidths=[20 * mm, 20 * mm, PAGE_W - 2 * MARGIN - 40 * mm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("ALIGN", (0, 0), (1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, None]),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(t)
story.append(Spacer(1, 4))
story.append(Paragraph(
    "12+ of one letter: you are a pure type - go deep. 7-11: strong lean - read both top "
    "profiles. A flat spread across all four usually means you have not yet done a deal; "
    "start as an A or C, the forgiving formats.", S["small"]))

# --- profiles
for letter, name, desc, plays, blind, first in PROFILES:
    story.append(Spacer(1, 10))
    head = Table([[letter, name]], colWidths=[14 * mm, PAGE_W - 2 * MARGIN - 14 * mm])
    head.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), GOLD),
        ("BACKGROUND", (1, 0), (1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (0, 0), NAVY),
        ("TEXTCOLOR", (1, 0), (1, 0), SAND),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (0, 0), 14),
        ("FONTSIZE", (1, 0), (1, 0), 12),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
    ]))
    story.append(head)
    story.append(Spacer(1, 4))
    story.append(Paragraph(desc, S["body"]))
    story.append(Paragraph("Where you should play (India - UAE - KSA):", S["h3"]))
    for p in plays:
        story.append(Paragraph(f"&bull;  {p}", S["opt"]))
    story.append(Spacer(1, 3))
    story.append(Paragraph(f"<b>Your blind spot:</b> {blind}", S["body"]))
    story.append(Paragraph(f"<b>{first}</b>", S["callout"]))

# --- CTA page
story.append(PageBreak())
story.append(Paragraph("You know your type. Now run your numbers.", S["h1"]))
story.append(Paragraph(
    "Every profile above shares one discipline: before committing, run a "
    "back-of-the-envelope check - income, financing cost, and the spread between them. "
    "If the property's return on assets is below your cost of borrowing, you have "
    "<b>negative leverage</b>: the loan is eating your equity and you are betting purely "
    "on price appreciation. Most Indian residential bought on a home loan fails this "
    "test. Most buyers have never run it.", S["body"]))
story.append(Paragraph("Tools in this series", S["h2"]))
cta_rows = [
    ["NRI GULF INVESTOR KIT", "BOE deal calculator + India due-diligence checklist + NRI tax annex (TDS, capital gains, repatriation)", "INR 1,999"],
    ["BOE DEAL ANALYZER", "One-sheet calculator per market. India / UAE (service charges, payment plans) / KSA (Murabaha cost, Zakat flag)", "INR 999 each"],
    ["DUE-DILIGENCE PACKS", "The exact document checklist per market: RERA/title (India), Oqood/escrow (UAE), Najiz/REGA (KSA)", "INR 499 each"],
    ["HARVEST PLANNER", "Hold vs refinance vs sell - a decision tree with the tax math for all three markets", "INR 499"],
    ["9-DAY WHATSAPP COURSE", "The whole game, one lesson a day, each ending with an exercise on a real listing in YOUR city", "INR 799"],
]
t = Table(cta_rows, colWidths=[44 * mm, PAGE_W - 2 * MARGIN - 44 * mm - 24 * mm, 24 * mm])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
    ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
    ("TEXTCOLOR", (2, 0), (2, -1), GREEN),
    ("FONTSIZE", (0, 0), (-1, -1), 8.6),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [PAPER, None]),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("ALIGN", (2, 0), (2, -1), "CENTER"),
]))
story.append(t)
story.append(Spacer(1, 8))
story.append(Paragraph(
    "To order: message <b>KIT</b> on WhatsApp [YOUR-WA-NUMBER] or browse the catalogue "
    "[YOUR-WA-CATALOGUE-LINK]. UAE and KSA pricing available in AED/SAR.", S["callout"]))
story.append(Spacer(1, 6))
story.append(Paragraph(brand.DISCLAIMER, S["small"]))

doc.build(story)
print("Built:", OUT)
