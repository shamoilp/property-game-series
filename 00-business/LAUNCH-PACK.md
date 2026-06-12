# Property Game Series — Launch Pack
*Prepared 12 June 2026.*

---

## 1. Product line and pricing

| # | Product | Files | INR | AED | SAR | Role |
|---|---------|-------|-----|-----|-----|------|
| 0 | Which Player Are You? Scorecard | 1 PDF (7 pp) | FREE | FREE | FREE | Lead magnet — share everywhere |
| 1 | **NRI Gulf Investor Kit** | 1 XLSX + 2 PDFs | **1,999** | 89 | 89 | Flagship; hero product |
| 2 | BOE Deal Analyzer — India | 1 XLSX | 999 | 45 | 45 | Standalone (included in #1) |
| 3 | BOE Deal Analyzer — UAE | 1 XLSX | 999 | 45 | 45 | Standalone |
| 4 | BOE Deal Analyzer — KSA | 1 XLSX | 999 | 45 | 45 | Standalone; Murabaha + Zakat block |
| 5 | UAE Due-Diligence Checklist | 1 PDF (4 pp) | 499 | 29 | 29 | Standalone |
| 6 | KSA Due-Diligence Checklist | 1 PDF (4 pp) | 499 | 29 | 29 | Standalone |
| 7 | Harvest Planner | 1 PDF (3 pp) | 499 | 29 | 29 | Cross-sell to every owner |
| 8 | 9-Day Property Game (WhatsApp course) | 9 daily messages | 799 | 49 | 49 | Engagement engine → kit upsell |
| 9 | Rent Reality Report (per pincode+BHK) | 1 PDF, made to order | 399 | 25 | 25 | Productized service; data moat |
| 10 | **Everything Bundle** | All static products (1–8) | **3,499** | 159 | 159 | Anchor; makes #1 look cheap |

Pricing psychology: the bundle exists to anchor; the flagship kit is the intended purchase. Course buyers are the warmest upsell pool (they reply with their own deal numbers).

**Lesson from the toolkit launch:** keep ONE price per product everywhere — catalogue, PDF covers, conference banner. (The ₹800 vs ₹4,999 inconsistency on the freight toolkit cost trust; do not repeat.)

---

## 2. WhatsApp catalogue copy (paste-ready)

**Item: NRI Gulf Investor Kit — ₹1,999**
> Buying Indian property from the Gulf? This kit is the 3 documents that protect you: (1) a deal calculator that tells you in ONE cell whether the rent carries the loan or you're feeding the flat from salary, (2) the 52-point India due-diligence checklist built for buyers 3,000 km away, (3) the NRI Tax Annex — TDS on your rent, the 195 trap when buying from another NRI, capital gains at sale, and repatriating the money home. Written by a Gulf-based cross-border tax practitioner. Instant delivery on WhatsApp.

**Item: BOE Deal Analyzer (India / UAE / KSA) — ₹999 each**
> The 5-minute check professionals run before any property commitment. Enter price, rent and loan — get ROA, true financing cost, ROE and a green/red leverage verdict. India edition: full cost stack incl. NRI TDS rows. UAE edition: service-charge stress test (the number that kills Dubai yields). KSA edition: Murabaha APR financing block + Zakat intention tracker. Compare 3 deals side by side.

**Item: Due-Diligence Checklist (UAE / KSA) — ₹499 each**
> Every document to demand BEFORE the MOU/token, and why. UAE: REST deed verification, Mollak service-charge records, Oqood for off-plan, the expat will nobody registers. KSA: Najiz deed inquiry, REGA broker licence check, RETT-before-Najiz sequencing, white land levy exposure, foreign-ownership zone rules (new since Jan 2026).

**Item: Harvest Planner — ₹499**
> Own property already? One number — Return on Current Equity — tells you whether to hold, refinance, redevelop or sell. Includes the exit-tax table for India (12.5% LTCG + NRI TDS), UAE and KSA, and the 10-minute worksheet. Most owners are holding a 2.4% asset and calling it 9%.

**Item: 9-Day Property Game — ₹799**
> One WhatsApp lesson a day for 9 days. Forces → numbers → paperwork → REITs → development → operations → exit. Every lesson ends with an exercise on a real listing in YOUR city. Finish all 9 exercises and unhappy? Full refund.

**Item: Rent Reality Report — ₹399 (made to order, delivered within 24h)**
> Stop underwriting your deal on the broker's rent quote. Send a pincode + BHK and get a one-page report from LIVE listings: the real rent band (P10/P50/P90), rent per sq ft, where the supply sits by locality — and if you share your deal price, the BOE verdict computed at the realistic rent AND the stress rent. India's first rent report that tells you whether the loan survives the truth.

**Item: Which Player Are You? — FREE**
> 20 questions. 4 investor types. Find your natural position in the property game — and the plays per market for your type — before risking a rupee, dirham or riyal. Forward freely.

---

## 3. Pre-launch checklist

- [ ] Replace `[YOUR-WA-NUMBER]` and `[YOUR-WA-CATALOGUE-LINK]` placeholders in `brand.py`, rebuild all PDFs (one command per folder).
- [ ] Create Razorpay payment links: 1,999 / 999 / 799 / 499 / 3,499 (test each on live mode — lesson from IdeaLens: test the live link, not just test mode).
- [ ] AED/SAR collection: Razorpay handles INR; for Gulf buyers either (a) quote INR and let cards convert, or (b) Stripe/Tap payment links in AED/SAR. Start with (a) — zero setup.
- [ ] Add all 9 products to the WhatsApp Business catalogue with the copy above + cover images.
- [ ] Cover images: export page 1 of each PDF as PNG (consistent navy/gold family look) — `pdftoppm` alternative: `python -c` with pypdfium2, or screenshot at 200%.
- [ ] Set up WhatsApp quick replies: `KIT` → catalogue + payment links; `PLAYER` → free scorecard PDF; `ADVICE` → consultation booking message.
- [ ] Dry-run delivery: buy each product yourself, time the click-to-delivery flow.

## 4. Launch channels and positioning

**Positioning:** you are the *tax practitioner who built investor tools*, not a course seller. Lead with the trap stories, not the products:
1. "An NRI buying from another NRI must deduct TDS under s.195, not 1% — get it wrong and the liability is YOURS." (buying trap)
2. "Most Indian flats bought on Gulf salaries run 1.5% return against a 10.6% loan cost — the sheet shows it in one cell." (negative leverage)
3. "The 197 certificate is the highest-ROI paper in an NRI sale — start it before listing." (selling trap)

**Channels, in order of warmth:**
- **WhatsApp Status** — one trap story per day for a week, each ending "reply PLAYER for the free scorecard". Your existing contact base is the warmest NRI audience you have.
- **Existing clients and the EXIM WhatsApp group** — the free scorecard is the authority play (same free-hook pattern as trade-chokepoint); never pitch the paid kit cold.
- **Jeddah/Gulf NRI community groups** (Indian associations, professional circles) — share the scorecard, not the catalogue; let the PDF's own CTA page do the selling.
- **LinkedIn** — the negative-leverage worked example as a carousel/post; tax practitioners sharing real math travel well there.

**Funnel mechanics:**
- Keyword "PLAYER" → free scorecard lands instantly → catalogue follows 24h later (drip, not dump).
- Launch offer: flagship kit at ₹1,499 for the first 2 weeks (code LAUNCH) — urgency without devaluing list price.
- Collect name + city of property interest in the chat; this segments India vs UAE vs KSA follow-ups.

## 5. Sequencing

1. Week 1: placeholders, payment links, catalogue, dry-run purchase.
2. Week 2: Status story sequence + scorecard distribution; LAUNCH code live.
3. Week 3: first 9-Day course cohort (Monday start) for scorecard takers who didn't buy the kit.
4. Week 4+: UAE/KSA analyzer push to segmented lists; Harvest Planner to anyone who mentioned owning property.
5. Ongoing: every consultation client gets the bundle free — the products are also business-development collateral for the advisory practice.

## 6. Rebuild commands (after any edit)

```
python 01-player-scorecard/build_scorecard.py
python 02-nri-gulf-kit/build_boe_india.py
python 02-nri-gulf-kit/build_kit_pdfs.py
python 03-boe-analyzer/build_boe_uae_ksa.py
python 04-dd-checklists/build_dd_uae_ksa.py
python 05-harvest-planner/build_harvest.py
```

**Rent Reality Report (per order):**
```
python 07-rent-reality-report/rent_report.py --pincode 560076 --city "Bengaluru, India" --bhk 2 --price 9000000
```
Use `--csv listings.csv --label "Locality, City"` (columns: rent,area,locality) when the
portal API changes or the customer's micro-market is thin. Fewer than 8 usable listings
aborts rather than producing dishonest percentiles. Run politely: a few pages per order,
seconds apart — this is per-customer research, not crawling.
All brand styling (colours, WhatsApp number, disclaimer) lives in `00-business/brand.py` — edit once, rebuild all.
