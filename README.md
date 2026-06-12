# The Property Game Series — Build System

Build pipeline for a WhatsApp-distributed product line of real estate decision tools
covering **India, UAE and Saudi Arabia**: deal calculators, due-diligence checklists,
an exit-decision planner, an investor self-assessment, and a 9-day WhatsApp micro-course.

The finished PDFs and Excel workbooks are **not** in this repo — they are sold through
a WhatsApp Business catalogue. This repo contains the code that generates them.

## What's here

```
00-business/        brand.py (shared PDF brand system: palette, covers, page frames)
                    LAUNCH-PACK.md (pricing, catalogue copy, launch sequencing)
01-player-scorecard/  build_scorecard.py  - free 20-question investor-type assessment
02-nri-gulf-kit/      build_boe_india.py  - India deal analyzer workbook (openpyxl)
                      build_kit_pdfs.py   - India due-diligence checklist + NRI tax annex
03-boe-analyzer/      build_boe_uae_ksa.py - UAE and KSA deal analyzer workbooks
04-dd-checklists/     build_dd_uae_ksa.py  - UAE and KSA due-diligence checklist PDFs
05-harvest-planner/   build_harvest.py     - hold/refinance/redevelop/sell decision tool
06-whatsapp-course/   9-Day-Property-Game-Course.md - daily lesson scripts + operator notes
07-rent-reality-report/ rent_report.py - made-to-order rent-band report (pincode + BHK
                        -> P10/P50/P90 from live listings + BOE verdict, one-page PDF;
                        --csv path for manual comparables)
                        samples/ - real generated reports (Bengaluru 560076,
                        Mumbai 400076 and 400011) as proof of output
```

## The core idea

Every tool applies one discipline: before any property commitment, compare what the
asset earns (return on assets) against what the financing costs (the annual financing
constant). If the spread is negative, the buyer is making a pure price-appreciation
bet — usually without knowing it. The calculators surface that verdict in one cell;
the checklists and planner cover the paperwork and the exit.

Market-specific layers include NRI tax mechanics for India (TDS, capital gains,
repatriation), service-charge stress testing for the UAE, and a Murabaha financing
block plus Zakat-intention tracking for Saudi Arabia.

## Build

Requires Python 3.10+ with `reportlab`, `openpyxl`, `pypdf`.

```bash
python 01-player-scorecard/build_scorecard.py
python 02-nri-gulf-kit/build_boe_india.py
python 02-nri-gulf-kit/build_kit_pdfs.py
python 03-boe-analyzer/build_boe_uae_ksa.py
python 04-dd-checklists/build_dd_uae_ksa.py
python 05-harvest-planner/build_harvest.py
```

All branding (colours, contact placeholders, disclaimer) lives in
`00-business/brand.py` — edit once, rebuild everything. Replace
`[YOUR-WA-NUMBER]` and `[YOUR-WA-CATALOGUE-LINK]` before distributing output.

## Notes

- Content is an independent educational adaptation inspired by decision frameworks
  popularised in W. J. Poorvu's *The Real Estate Game* (1999). No affiliation;
  no text from the book is reproduced.
- Tax figures reflect June 2026 rules and change with every budget cycle — verify
  before relying on any number.
- Nothing here is investment, legal or tax advice.

## License

All rights reserved. You may read and learn from this code; you may not resell or
redistribute the generated products.
