"""Due-Diligence Checklist PDFs - UAE and KSA editions.
All content original; structured for buyers transacting in 2026."""

import sys
sys.path.insert(0, r"C:\Users\user\real-estate-game-toolkit\00-business")
import brand
from brand import MARGIN, PAGE_W, NAVY, SAND, PAPER, LINE, SLATE
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, NextPageTemplate, PageBreak)

S = brand.styles()
DIR = r"C:\Users\user\real-estate-game-toolkit\04-dd-checklists"


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
    rows = [["", "CHECK", "WHY IT MATTERS / RED FLAG"]]
    for item, why in items:
        rows.append(["[  ]", Paragraph(item, S["body"]), Paragraph(why, S["small"])])
    w = PAGE_W - 2 * MARGIN
    t = Table(rows, colWidths=[10 * mm, w * 0.42, w * 0.58 - 10 * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 1), (0, -1), SLATE),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [None, PAPER]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


# =====================================================================
# UAE EDITION
# =====================================================================
doc = make_doc(
    rf"{DIR}\UAE-Due-Diligence-Checklist.pdf",
    dict(kicker="The Property Game Series",
         title_lines=["UAE PROPERTY", "DUE DILIGENCE"],
         subtitle=["Ready units  |  Off-plan  |  Secondary market",
                   "The document checklist for Dubai and the other",
                   "emirates - built for expat and overseas buyers."],
         price_tag="AED 29  |  INR 499",
         footer_note="Current as of June 2026 - fees and rules change; verify before transfer"),
    "UAE Due-Diligence Checklist")

st = [NextPageTemplate("body"), PageBreak()]
st.append(Paragraph("How to use this checklist", S["h1"]))
st.append(Paragraph(
    "The UAE transfers property in days, not months - which means your diligence window "
    "is short and front-loaded. Everything below happens <b>before</b> you sign the MOU "
    "(Form F in Dubai) and hand over a deposit cheque. Dubai-specific portal names are "
    "given; Abu Dhabi, Sharjah and the northern emirates have equivalents - the "
    "principle transfers even where the portal name does not.", S["body"]))
st.append(Paragraph(
    "Golden rule: in a market this fast, the pressure tactic is speed. Anyone who "
    "cannot give you 48 hours to verify a title deed is telling you something.",
    S["callout"]))

st.append(Paragraph("A. The seller and the title", S["h2"]))
st.append(check_table([
    ("Title deed verified against the DLD record (Dubai REST app 'Deed Verification')",
     "Takes 2 minutes. Confirms the deed is genuine, the owner's name, and the plot/unit details."),
    ("Seller's passport/Emirates ID matches the deed name exactly",
     "Name transliteration mismatches must be resolved before, not at, the trustee office."),
    ("Mortgage status: if mortgaged, bank liability letter with payoff figure and validity date",
     "The liability letter expires; the blocking process at the trustee depends on it."),
    ("If seller uses a POA: notarised (UAE notary) or attested if executed abroad; check scope covers SALE",
     "POAs limited to 'management' cannot sell. Verify with the issuing notary where possible."),
    ("Company seller: trade licence, MOA, board/shareholder resolution authorising sale",
     "Free-zone and offshore (JAFZA offshore for Dubai property) sellers have extra NOC steps."),
    ("Inheritance situation? Court succession order naming heirs before any MOU",
     "UAE applies forum rules to estates - an unprobated deed cannot transfer."),
]))

st.append(Paragraph("B. Off-plan purchases", S["h2"]))
st.append(check_table([
    ("Project registered with RERA and the escrow account number stated in your SPA",
     "Pay ONLY into the project escrow account - never the developer's operating account."),
    ("Developer registered and project status live on the DLD project portal",
     "Check completion percentage vs what the sales office claims."),
    ("Your purchase registered as Oqood (pre-completion registration) in your name",
     "Unregistered off-plan = you are an unsecured creditor of the developer."),
    ("Payment plan mapped against construction milestones, not calendar dates",
     "Calendar-linked plans pay the developer even when the crane stops."),
    ("Developer's delivered-project history: promised vs actual handover, quality forums",
     "The brand on the hoarding is not always the entity on the SPA - check the actual LLC."),
    ("SPA clauses: delay compensation, area variation tolerance (and refund per sqft), DLP terms",
     "1-year defects liability + 10-year structural liability are the standard you should see."),
    ("Post-handover payment plan modelled as a loan in your BOE analyzer",
     "It IS financing - usually priced into the unit at 10-20% above cash price."),
]))

st.append(Paragraph("C. The unit itself (ready/secondary)", S["h2"]))
st.append(check_table([
    ("Service charge record pulled from Mollak (not the broker's WhatsApp message)",
     "Also check OA budget approval and any announced increases."),
    ("Owners Association no-objection + service charge clearance to transfer date",
     "Arrears block the NOC; negotiate who clears them in the MOU."),
    ("Developer NOC requirement, fee and timeline confirmed",
     "AED 500-5,000 and up to 2 weeks in some master communities - affects your transfer date."),
    ("Ejari/rental history: is a tenant in place? Eviction notice status and notice periods",
     "A sitting tenant with 9 months left changes your plans - 12-month notice rules apply for sale/own-use."),
    ("Chiller/district cooling provider, deposits, and any unpaid capacity charges",
     "Capacity charges can run even for vacant units - confirm the account is clean and transferable."),
    ("Professional snagging inspection (even for resale)",
     "AED 1,000-2,500. MEP and waterproofing faults cost 50x that after transfer."),
    ("Parking bay(s) and storage on the title deed or allocation letter",
     "'Comes with two parkings' must appear in writing somewhere enforceable."),
]))

st.append(Paragraph("D. Money and closing", S["h2"]))
st.append(check_table([
    ("MOU (Form F) through a RERA-licensed broker; broker's BRN verified on REST",
     "Unlicensed 'consultants' cannot lodge Form F - your deposit has no procedural home."),
    ("Deposit cheque held by the licensed broker as stakeholder, stated in the MOU",
     "Never transfer a cash deposit to the seller's personal account."),
    ("Mortgage pre-approval validity covers the expected transfer date",
     "Pre-approvals lapse in 60-90 days; an expired one at the trustee = penalty under the MOU."),
    ("All transfer costs tabulated: 4% DLD + trustee fee + NOC fee + broker 2% + mortgage registration 0.25%",
     "Budget ~6-7.5% on top of price; your BOE sheet has the rows."),
    ("Transfer at the registration trustee: manager's cheques prepared exactly as instructed",
     "Wrong payee spelling = rescheduled transfer."),
    ("Overseas buyer: funds remitted under your own name with a clean bank trail",
     "AML checks at transfer are real; third-party cash is the classic failure."),
]))

st.append(Paragraph("E. After transfer - the two documents expats skip", S["h2"]))
st.append(check_table([
    ("Register a will covering UAE assets (DIFC Wills Service or Dubai Courts; ADJD in Abu Dhabi)",
     "Without one, default inheritance rules apply to your estate and accounts freeze during probate. "
     "This is the single most skipped item by expat owners."),
    ("Update Ejari, DEWA/utility accounts, and OA records to your name within the month",
     "Your ownership file should be self-proving while you live abroad."),
]))
st.append(Spacer(1, 8))
st.append(Paragraph(brand.DISCLAIMER, S["small"]))
doc.build(st)
print("Built: UAE-Due-Diligence-Checklist.pdf")


# =====================================================================
# KSA EDITION
# =====================================================================
doc = make_doc(
    rf"{DIR}\KSA-Due-Diligence-Checklist.pdf",
    dict(kicker="The Property Game Series",
         title_lines=["SAUDI PROPERTY", "DUE DILIGENCE"],
         subtitle=["Riyadh  |  Jeddah  |  Dammam  |  Growth cities",
                   "The document checklist for the Kingdom's",
                   "digital-first property system (Najiz, Ejar, Balady)."],
         price_tag="SAR 29  |  INR 499",
         footer_note="Current as of June 2026 - the foreign-ownership regime is new; verify zone rules"),
    "KSA Due-Diligence Checklist")

st = [NextPageTemplate("body"), PageBreak()]
st.append(Paragraph("How to use this checklist", S["h1"]))
st.append(Paragraph(
    "Saudi property runs on government platforms: title via <b>Najiz</b>, leases via "
    "<b>Ejar</b>, municipal status via <b>Balady</b>, brokers licensed by <b>REGA</b> "
    "(FAL licence), and transfer tax via the <b>ZATCA RETT portal</b>. This is good "
    "news: most diligence is a portal query, not a courthouse archive. The discipline "
    "is doing the queries yourself rather than trusting screenshots.", S["body"]))
st.append(Paragraph(
    "If you are a non-Saudi buying under the new foreign-ownership framework (in force "
    "January 2026): your FIRST check is whether the property sits inside a designated "
    "permitted zone and what conditions attach. Everything else comes second.",
    S["callout"]))

st.append(Paragraph("A. Title and the seller", S["h2"]))
st.append(check_table([
    ("Electronic title deed (sakk) verified on Najiz 'deed inquiry' - number, owner, area, boundaries",
     "Paper deeds should have been digitised; an owner who cannot show an e-deed has homework to do first."),
    ("Seller identity via national ID/Iqama matched to the deed; for companies, CR + authorised signatory",
     "Verify the signatory's authority on the Ministry of Commerce record."),
    ("Mortgage/encumbrance status on the deed record; payoff letter from the financing bank",
     "Saudi financings are registered against the deed - the record shows them."),
    ("Inherited property: probate deed (hasr al-irth) + ALL heirs' consent or court order",
     "Partial-heir sales unwind. Female heirs' shares missing from old paperwork is a known pattern."),
    ("POA sales: POA issued/verified through the Najiz attorney service and still in force",
     "Najiz POAs are queryable - revoked POAs keep circulating as PDFs."),
    ("Seller's RETT and Zakat position on the property understood (who files, who pays)",
     "RETT is filed on the ZATCA portal BEFORE Najiz transfer - the appointment fails without it."),
]))

st.append(Paragraph("B. The property and municipality", S["h2"]))
st.append(check_table([
    ("Building permit + completion/occupancy certificate against the actual structure",
     "Unpermitted floors and majlis extensions surface during your future sale, at the worst price."),
    ("Balady check: violations, demolition orders, road-widening plans on the parcel",
     "Municipal expropriation lines (tanzeem) can take metres off a plot - check the approved plan."),
    ("Plot boundaries by licensed surveyor against the deed coordinates",
     "Older deeds describe boundaries by neighbour names; coordinate conversion errors are common."),
    ("Saudi Building Code compliance for newer builds; structural condition report for older ones",
     "SAR 1,500-4,000 for an inspection; AC, waterproofing and plumbing are the money pits."),
    ("Utilities: SEC meter, water connection, and no accumulated bills",
     "Meters in old owners' names with arrears delay your Ejar registration later."),
    ("For land: white land levy status of the parcel and the district's development obligations",
     "The expanded levy regime makes 'buy and sit' expensive in covered zones - know before you bank land."),
]))

st.append(Paragraph("C. Regulatory and transaction", S["h2"]))
st.append(check_table([
    ("Broker holds a valid REGA FAL licence (verify the number, not the business card)",
     "Commission disputes and fake listings concentrate in the unlicensed tail."),
    ("Off-plan project: Wafi licence for off-plan sales + escrow account stated in the contract",
     "Wafi licensing is what separates a project from a PowerPoint."),
    ("Foreign buyer: property inside a permitted zone; ownership conditions and any caps confirmed",
     "Rules differ by city/zone (and Makkah/Madinah have special regimes). Get the zone status in writing."),
    ("Premium Residency or eligibility route documented if your ownership relies on it",
     "Your residency status and the ownership right are linked - renewals matter."),
    ("RETT 5% computed on the higher of price or fair value; exemption claims (first home support) verified",
     "Under-declared values resurface as ZATCA assessments with penalties."),
    ("Financing through a SAMA-licensed bank/finance company; REDF/Sakani subsidy eligibility checked",
     "The subsidised profit rate changes the BOE verdict completely - model both ways."),
    ("Independent valuation by a Taqeem-accredited valuer for any financed or high-value purchase",
     "Banks require it; cash buyers should want it for the same reason."),
]))

st.append(Paragraph("D. Income property specifics", S["h2"]))
st.append(check_table([
    ("Existing leases registered on Ejar; terms, expiry and rent payment history exported",
     "Unregistered side agreements do not bind you - but sitting tenants are still real people in your unit."),
    ("District rent comparables from the Ejar index, not listing-app asking prices",
     "Asking rents in hot Riyadh districts run well above signed rents."),
    ("Service/facility contracts (guard, cleaning, elevator) - cost, term, transferability",
     "For buildings: these contracts are your future NOI line items."),
    ("Your intention recorded at purchase: trading or holding (Zakat treatment differs)",
     "Write it in your file the day you sign - see the Zakat note in the BOE analyzer."),
]))

st.append(Paragraph("E. Closing via Najiz", S["h2"]))
st.append(check_table([
    ("RETT filed and payment reference generated before the transfer appointment",
     "Sequence matters: ZATCA first, Najiz second."),
    ("Funds by bank transfer/certified cheque - no cash component, full trail",
     "AML screening applies; clean trails also protect your future resale and repatriation."),
    ("E-conveyancing completed and the NEW deed verified in YOUR Najiz account before releasing final funds",
     "The deed update is near-instant - there is no excuse for paying before you see it."),
    ("Utilities, Ejar (if renting out) and insurance moved to your name within 30 days",
     "An absentee owner's best protection is records that are current without explanation."),
]))
st.append(Spacer(1, 8))
st.append(Paragraph(brand.DISCLAIMER, S["small"]))
doc.build(st)
print("Built: KSA-Due-Diligence-Checklist.pdf")
