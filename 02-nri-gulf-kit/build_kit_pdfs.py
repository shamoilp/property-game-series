"""Build the two PDF components of the NRI Gulf Investor Kit:
1. India Due-Diligence Checklist
2. NRI Tax Annex (buy / hold / sell / repatriate)
"""

import sys
sys.path.insert(0, r"C:\Users\user\real-estate-game-toolkit\00-business")
import brand
from brand import MARGIN, PAGE_W, NAVY, SAND, PAPER, LINE, SLATE, GOLD, RED, GREEN
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, NextPageTemplate,
                                PageBreak, KeepTogether)

S = brand.styles()
DIR = r"C:\Users\user\real-estate-game-toolkit\02-nri-gulf-kit"


def make_doc(path, cover_kwargs, header_title):
    def on_cover(canvas, doc):
        brand.draw_cover(canvas, **cover_kwargs)

    def on_page(canvas, doc):
        brand.draw_page_frame(canvas, doc, header_title)

    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=20 * mm, bottomMargin=20 * mm)
    frame = Frame(MARGIN, 18 * mm, PAGE_W - 2 * MARGIN, A4[1] - 40 * mm, id="f")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=on_cover),
        PageTemplate(id="body", frames=[frame], onPage=on_page),
    ])
    return doc


def check_table(items):
    """items: list of (item, why-it-matters). Renders with a checkbox column."""
    rows = [["", "CHECK", "WHY IT MATTERS / RED FLAG"]]
    for item, why in items:
        rows.append(["[  ]", Paragraph(item, S["body"]), Paragraph(why, S["small"])])
    w_total = PAGE_W - 2 * MARGIN
    t = Table(rows, colWidths=[10 * mm, w_total * 0.42, w_total * 0.58 - 10 * mm],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (0, -1), 9),
        ("TEXTCOLOR", (0, 1), (0, -1), SLATE),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [None, PAPER]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


# =====================================================================
# PDF 1: INDIA DUE-DILIGENCE CHECKLIST
# =====================================================================
doc = make_doc(
    rf"{DIR}\India-Due-Diligence-Checklist.pdf",
    dict(kicker="NRI Gulf Investor Kit  -  Part 2 of 3",
         title_lines=["INDIA PROPERTY", "DUE DILIGENCE"],
         subtitle=["The 52-point document checklist that protects",
                   "a buyer who is 3,000 km from the property.",
                   "",
                   "Resale flats  |  Under-construction  |  Plots  |  Commercial"],
         price_tag="PART OF THE INR 1,999 KIT",
         footer_note="Current as of June 2026 - laws and rates change; verify before closing"),
    "India Due-Diligence Checklist")

st = [NextPageTemplate("body"), PageBreak()]

st.append(Paragraph("How to use this checklist", S["h1"]))
st.append(Paragraph(
    "Work through each section <b>before</b> you sign an Agreement to Sell or pay any "
    "amount beyond a refundable token. Every item is binary - you either hold the "
    "document or you do not. 'The broker said it is fine' is not a checkbox. For an NRI, "
    "insist on scanned copies over email/WhatsApp first, then originals verified by your "
    "lawyer at registration. Items marked (NRI) are traps specific to non-resident buyers.",
    S["body"]))
st.append(Paragraph(
    "Golden rule: the seller's urgency is inversely proportional to the quality of his "
    "paperwork. A clean file survives a 3-week diligence wait.", S["callout"]))

st.append(Paragraph("A. Seller and title (all purchases)", S["h2"]))
st.append(check_table([
    ("Title chain for the last 30 years (mother deed onward)",
     "Gaps in the chain = future litigation. 13 years minimum; 30 is safe for high-value."),
    ("Latest registered sale/conveyance deed in seller's name",
     "Photocopy 'pending registration' deeds are a classic fraud pattern."),
    ("Encumbrance Certificate (EC) for 30 years - Form 15/16",
     "Form 16 (nil encumbrance) is what you want. Any charge listed must be released in writing."),
    ("Mutation / khata / Patta in seller's name with up-to-date tax receipts",
     "Registered deed without mutation = municipal records still show someone else."),
    ("Seller identity: PAN + Aadhaar/passport matched against deed name",
     "Name mismatches (spellings, initials) need a notarised one-and-the-same affidavit."),
    ("If seller acts through Power of Attorney: registered POA, photo, and principal alive",
     "Unregistered/expired POA sales are voidable. Video-call the principal."),
    ("Legal heirship: if inherited property, succession certificate or registered release deeds from ALL heirs",
     "One missing sibling's signature can unwind your purchase years later."),
    ("Seller's marital status / spouse consent where state law or loan requires",
     "Avoids later claims of co-ownership interest."),
    ("Litigation search: civil court + revenue records + online case status for property and seller",
     "A pending partition or specific-performance suit follows the property, not the seller."),
    ("CERSAI search for existing mortgage/security interest",
     "Banks register charges centrally - a 5-minute search catches an undisclosed loan."),
]))

st.append(Paragraph("B. Project and regulatory (under-construction / builder purchases)", S["h2"]))
st.append(check_table([
    ("RERA registration number - verify live on the state RERA portal, not the brochure",
     "Check status is 'registered', not lapsed/revoked, and the completion date on record."),
    ("Quarterly progress reports (QPRs) filed on the RERA portal",
     "A builder current on QPRs is a builder being watched. Missing QPRs = walk away signal."),
    ("Sanctioned building plan + layout approval from the planning authority",
     "Compare tower/floor/unit count with what is being sold. Extra floors = demolition risk."),
    ("Land title in builder's name or registered JDA with landowner",
     "In a JDA, confirm your unit falls in the BUILDER's allocation, not the landowner's share."),
    ("Commencement Certificate (CC) covering the floor your unit is on",
     "CC for 10 floors does not cover your 14th-floor unit."),
    ("70% escrow account details stated in the agreement (RERA s.4(2)(l)(D))",
     "Your instalments must go to the project escrow, not the builder's group company."),
    ("Agreement for Sale follows the state RERA model form",
     "One-sided clauses (builder delay tolerated, your delay penalised) are challengeable but costly."),
    ("Construction-linked vs time-linked payment plan understood and modelled",
     "Time-linked plans transfer construction risk to you. Prefer construction-linked."),
    ("Builder delivery history: last 3 projects - promised vs actual handover dates",
     "Past slippage is the best predictor. RERA portals show this."),
]))

st.append(Paragraph("C. The property itself (resale / ready)", S["h2"]))
st.append(check_table([
    ("Occupancy Certificate (OC) for the building",
     "No OC = technically unauthorised occupation; many banks will not lend; resale value suffers."),
    ("Built structure matches sanctioned plan (no illegal balcony enclosure, extra room, terrace grab)",
     "Deviations can block society NOC and future resale to loan-funded buyers."),
    ("Carpet area measured (RERA definition) vs super built-up claimed",
     "Loading of 30-40%+ is common; you price in rupees per carpet sq ft."),
    ("Society/association NOC + no-dues certificate from the society office",
     "Unpaid maintenance transfers to you in practice. Get the ledger."),
    ("Latest property tax receipts (3 years) + water/electricity bills in seller's name",
     "Arrears attach to the property in most municipalities."),
    ("Physical inspection by someone YOU trust (not the broker): seepage, structure, parking slot allotment",
     "(NRI) Video walkthrough minimum; a paid independent inspection is INR 5-10k well spent."),
    ("Parking: allotment letter or deed mention - not 'understood'",
     "Stilt/open parking disputes are the most common society fights."),
    ("For plots: physical possession, demarcation/survey by licensed surveyor, access road ownership",
     "A plot with no legal access road is a captive asset for the neighbour."),
    ("For plots: land-use / zoning certificate (residential NA status where applicable)",
     "Agricultural land cannot be bought by NRIs at all - see tax annex (FEMA)."),
]))

st.append(Paragraph("D. Money and price (all purchases)", S["h2"]))
st.append(check_table([
    ("Circle rate / ready reckoner value vs agreement value compared",
     "Buying below circle rate triggers tax in YOUR hands on the difference (s.56(2)(x)) plus stamp duty on circle rate."),
    ("No cash component - 100% banked consideration",
     "Cash deals: s.269SS/269T penalties, plus you cannot prove cost basis at sale."),
    ("If property is mortgaged: bank's foreclosure letter + NOC, payoff routed directly to bank",
     "Pay the bank, not the seller, for the loan portion."),
    ("Token/advance paid only against a signed receipt referencing draft agreement",
     "WhatsApp transfers 'to block the deal' have no legal anchor."),
    ("Your BOE analyzer run: ROA vs loan cost, verdict accepted with open eyes",
     "If it is an appreciation bet, that is a choice - make it consciously."),
]))

st.append(Paragraph("E. NRI-specific items", S["h2"]))
st.append(check_table([
    ("(NRI) Verify what the SELLER is: resident or NRI - changes your TDS duty completely",
     "Resident seller >= INR 50L: deduct 1% u/s 194-IA. NRI seller: deduct u/s 195 on gains at higher rates and you need a TAN. Getting this wrong makes YOU liable."),
    ("(NRI) Your PAN active and linked; Form 26AS/AIS clean",
     "Registration and TDS credits fail against inoperative PANs."),
    ("(NRI) Funds routed from NRE/NRO/FCNR account in your own name",
     "Third-party funding breaks the FEMA trail and blocks future repatriation."),
    ("(NRI) Asset class permitted: residential/commercial yes; agricultural land, plantation, farmhouse - NO",
     "FEMA prohibition. No exceptions by 'converting later'."),
    ("(NRI) If buying jointly: co-owner shares stated in the deed with funding in same ratio",
     "Mismatched funding vs ownership creates benami and clubbing exposure."),
    ("(NRI) POA to a local relative for registration: specific, registered, ideally adjudicated",
     "General POAs get rejected by sub-registrars; embassy attestation needed if signed abroad."),
    ("(NRI) Buyer TDS deposited and Form 16B/16A issued before final payment",
     "Sellers vanish; the TDS default stays with you."),
]))

st.append(Paragraph("F. Closing day", S["h2"]))
st.append(check_table([
    ("Sale deed draft reviewed by your lawyer 72 hours before registration",
     "Sub-registrar queues are not where you read clause 14 for the first time."),
    ("All original documents physically handed over and listed in an annexure to the deed",
     "Originals = your future buyer's diligence file."),
    ("Possession letter + all keys + utility transfer forms signed same day",
     "Possession disputes start the day after registration, not before."),
    ("Photographs + two witnesses with ID at registration",
     "Standard, but NRIs relying on POA must ensure POA holder carries the registered original."),
    ("Post-closing: mutation application filed within 30 days; society share transfer initiated",
     "The deal is done when the records say so, not when the party happens."),
]))

st.append(Spacer(1, 8))
st.append(Paragraph(
    "Next: open the BOE Deal Analyzer workbook and run your numbers, then read the NRI "
    "Tax Annex before you wire a single dirham or riyal.", S["callout"]))
st.append(Paragraph(brand.DISCLAIMER, S["small"]))
doc.build(st)
print("Built: India-Due-Diligence-Checklist.pdf")


# =====================================================================
# PDF 2: NRI TAX ANNEX
# =====================================================================
doc = make_doc(
    rf"{DIR}\NRI-Tax-Annex.pdf",
    dict(kicker="NRI Gulf Investor Kit  -  Part 3 of 3",
         title_lines=["THE NRI", "TAX ANNEX"],
         subtitle=["Buy. Hold. Sell. Repatriate.",
                   "The Indian tax mechanics every Gulf-based NRI",
                   "must know before and after the deal.",
                   "",
                   "Written by a cross-border tax practitioner based in the Gulf"],
         price_tag="PART OF THE INR 1,999 KIT",
         footer_note="Rates as of June 2026 (FY 2026-27). Tax law changes every budget - verify before acting."),
    "NRI Tax Annex")

st = [NextPageTemplate("body"), PageBreak()]

st.append(Paragraph("Why this annex exists", S["h1"]))
st.append(Paragraph(
    "Property mistakes cost lakhs; <b>tax</b> mistakes on property cost lakhs plus "
    "interest plus penalty plus years of correspondence - handled from another country. "
    "The four moments below are where NRIs get hurt: at purchase (your TDS duty as "
    "buyer), while renting (TDS on your rent), at sale (capital gains + the buyer's TDS "
    "on you), and at repatriation (FEMA limits and certificates). Each section ends with "
    "a 'do this' line.", S["body"]))

# ---- 1. BUYING
st.append(Paragraph("1. When you BUY", S["h2"]))
st.append(Paragraph("Your TDS duty depends on who the seller is", S["h3"]))
rows = [
    ["SELLER IS...", "YOUR DUTY AS BUYER", "MECHANICS"],
    ["Resident, price >= INR 50 lakh",
     "Deduct 1% of consideration u/s 194-IA",
     "No TAN needed. File Form 26QB within 30 days of month-end; give seller Form 16B."],
    ["Resident, price < INR 50 lakh", "No TDS", "Keep PAN + bank trail anyway."],
    ["NRI (any price)",
     "Deduct u/s 195 on the taxable capital gain - in practice often on the whole consideration unless a lower-deduction certificate exists",
     "You need a TAN, must file Form 27Q, and issue Form 16A. Push the seller to obtain a s.197 lower-deduction certificate - it protects you both."],
]
t = Table(rows, colWidths=[(PAGE_W-2*MARGIN)*0.22, (PAGE_W-2*MARGIN)*0.34, (PAGE_W-2*MARGIN)*0.44])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8.3),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, None]),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
st.append(t)
st.append(Paragraph(
    "The classic trap: an NRI buys from another NRI, deducts 1% thinking 194-IA "
    "applies, and becomes an 'assessee in default' for the shortfall - with interest. "
    "Who the seller is matters more than what the property is.", S["callout"]))
st.append(Paragraph("Funding and FEMA", S["h3"]))
for b in [
    "Pay only from your own NRE / NRO / FCNR(B) account or fresh inward remittance. No third-party funding.",
    "Permitted: residential and commercial property, any number. Prohibited outright: agricultural land, plantation property, farmhouses.",
    "Joint purchase with a resident close relative is permitted; keep funding proportional to ownership share.",
    "Keep every bank advice/SWIFT copy - the repatriation file you will need in 10 years is built today.",
]:
    st.append(Paragraph(f"&bull;  {b}", S["opt"]))
st.append(Paragraph(
    "<b>Do this:</b> before the token, confirm seller residency in writing; if seller is "
    "an NRI, apply for your TAN the same week.", S["body"]))

# ---- 2. HOLDING
st.append(Paragraph("2. While you HOLD and RENT", S["h2"]))
for b in [
    "Rent from Indian property is taxable in India regardless of where you live. Standard deduction of 30% of net annual value plus full home-loan interest (s.24) apply.",
    "Your tenant must deduct TDS at 30% + surcharge + 4% cess (31.2% at base; higher with surcharge) on rent paid to an NRI u/s 195 - even an individual tenant. Most tenants do not know this; brief them at lease signing.",
    "A s.197 certificate from the AO can cut TDS to your actual expected liability - worth it when the standard deduction and interest wipe out most of the taxable rent.",
    "File the ITR even when TDS covers everything: it is how you recover excess TDS and it builds the compliance record that smooths repatriation and sale later.",
    "Gulf angle: the UAE and Saudi Arabia levy no personal income tax on this rent, so there is no foreign tax credit to claim - Indian tax is your final cost. Treaty residence questions matter only if you have Indian-source ties that risk residential status flips; track your days in India (60/120/182-day rules).",
]:
    st.append(Paragraph(f"&bull;  {b}", S["opt"]))
st.append(Paragraph(
    "<b>Do this:</b> put the TDS clause in the lease itself, with your PAN, the rate, and "
    "the tenant's duty to issue Form 16A each quarter.", S["body"]))

# ---- 3. SELLING
st.append(Paragraph("3. When you SELL", S["h2"]))
rows = [
    ["HOLDING PERIOD", "TAX", "NOTES"],
    ["> 24 months (long-term)",
     "12.5% (plus surcharge/cess) on the gain, no indexation - regime for transfers on/after 23 Jul 2024",
     "The old 20%-with-indexation option for pre-Jul-2024 acquisitions is available to resident individuals/HUFs only - NOT to NRIs. Model your gain on 12.5% flat."],
    ["<= 24 months (short-term)", "Slab rates on the gain", "Stacks on top of your other Indian income."],
]
t = Table(rows, colWidths=[(PAGE_W-2*MARGIN)*0.20, (PAGE_W-2*MARGIN)*0.36, (PAGE_W-2*MARGIN)*0.44])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8.3),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, None]),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
st.append(t)
for b in [
    "Your buyer must deduct TDS u/s 195 - typically on the full sale price unless you obtain a s.197 lower-deduction certificate. Without the certificate, ~13-15%+ of your sale value sits with the tax department until your refund processes. Apply 4-6 weeks before listing.",
    "Reinvestment reliefs available to NRIs: s.54 (new residential house in India, with timelines), s.54EC (NHAI/REC-type bonds, INR 50 lakh cap, 6-month window).",
    "Cost basis: keep purchase deed, stamp duty receipts, and capital-improvement bills. Improvements without invoices do not exist at sale time.",
]:
    st.append(Paragraph(f"&bull;  {b}", S["opt"]))
st.append(Paragraph(
    "<b>Do this:</b> the s.197 certificate is the single highest-ROI piece of paper in an "
    "NRI sale. Start it before the listing, not after the buyer is found.", S["body"]))

# ---- 4. REPATRIATION
st.append(Paragraph("4. When you REPATRIATE", S["h2"]))
for b in [
    "Sale proceeds land in your NRO account. Repatriation from NRO is capped at USD 1 million per financial year (all NRO remittances combined), with Form 15CA + a CA's Form 15CB certifying taxes paid.",
    "Property originally funded from NRE/inward remittance: sale proceeds of up to two residential properties are repatriable (principal portion); plan multi-property exits across years.",
    "Time large exits across two financial years (e.g., March + April) to use two USD 1M windows back-to-back.",
    "Keep the full file: purchase funding proof, TDS certificates, ITR acknowledgements, sale deed, 15CB. Banks ask for all of it, years later, at the worst moment.",
]:
    st.append(Paragraph(f"&bull;  {b}", S["opt"]))
st.append(Paragraph(
    "<b>Do this:</b> open the conversation with your bank's NRI desk 60 days before the "
    "sale closes - their internal checklist, not the law, sets your timeline.", S["body"]))

# ---- 5. ZAKAT NOTE
st.append(Paragraph("5. A note on Zakat (for Muslim investors)", S["h2"]))
st.append(Paragraph(
    "Tax compliance does not discharge religious obligation. Broad classical position: "
    "property held for resale/trading is Zakatable on its market value each Zakat year; "
    "property held to earn rent is not itself Zakatable, but the accumulated net rental "
    "savings are, with your other monetary assets. Intention (niyyah) at purchase - "
    "trading vs holding - drives the treatment, so record it. Positions vary across "
    "schools; take your specific case to a scholar you trust.", S["body"]))

st.append(Spacer(1, 8))
st.append(Paragraph(
    "Questions about your specific structure? This kit's maker advises Gulf-based "
    "clients on India-GCC cross-border tax. Message ADVICE on WhatsApp for a paid "
    "consultation slot.", S["callout"]))
st.append(Paragraph(brand.DISCLAIMER + " Tax positions summarised at a general level; "
                    "surcharge, cess and thresholds depend on your slab and the year of "
                    "the transaction.", S["small"]))
doc.build(st)
print("Built: NRI-Tax-Annex.pdf")
