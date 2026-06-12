"""Rent Reality Report - evidence-based rent bands for one pincode + BHK,
delivered as a branded one-page PDF with an optional BOE verdict.

Usage:
  python rent_report.py --pincode 560076 --bhk 2
  python rent_report.py --pincode 560076 --bhk 2 --price 9000000
  python rent_report.py --csv listings.csv --bhk 2 --label "Hulimavu, Bengaluru"

Data source: NoBroker public search API (rent listings near the pincode's
coordinates). The --csv path accepts a manual file with columns
rent,area,locality so the product still works if the API changes or for
localities better covered by broker quotes.

Run politely: a few pages, seconds apart, per customer report. This is a
low-volume research tool, not a crawler.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import date

import requests

sys.path.insert(0, r"C:\Users\user\real-estate-game-toolkit\00-business")
import brand  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import (BaseDocTemplate, Frame, NextPageTemplate,  # noqa: E402
                                PageBreak, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle)
from brand import MARGIN, PAGE_W, NAVY, SAND, PAPER, LINE, GREEN, RED  # noqa: E402

UA_BROWSER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
UA_GEO = {"User-Agent": "rent-reality-report/1.0"}
NOBROKER_API = "https://www.nobroker.in/api/v3/multi/property/RENT/filter"


@dataclass(frozen=True)
class Listing:
    rent: int
    area: int | None
    locality: str


# ------------------------------------------------------------------ fetch
def geocode_pincode(pincode: str, city_hint: str = "India") -> tuple[float, float, str]:
    r = requests.get("https://nominatim.openstreetmap.org/search",
                     params={"q": f"{pincode}, {city_hint}", "format": "json", "limit": 1},
                     headers=UA_GEO, timeout=20)
    r.raise_for_status()
    res = r.json()
    if not res:
        raise SystemExit(f"Could not geocode pincode {pincode}. "
                         f"Try --city to disambiguate, or use --csv.")
    return float(res[0]["lat"]), float(res[0]["lon"]), res[0].get("display_name", "")


def fetch_nobroker(lat: float, lon: float, bhk: int, pages: int,
                   radius_km: float) -> list[Listing]:
    search_param = base64.b64encode(
        json.dumps([{"lat": lat, "lon": lon}]).encode()).decode()
    seen: set[str] = set()
    out: list[Listing] = []
    for page in range(1, pages + 1):
        r = requests.get(NOBROKER_API,
                         params={"pageNo": page, "searchParam": search_param,
                                 "radius": radius_km, "type": f"BHK{bhk}"},
                         headers=UA_BROWSER, timeout=25)
        if r.status_code != 200:
            print(f"  page {page}: HTTP {r.status_code}, stopping")
            break
        items = (r.json().get("data") or [])
        if not items:
            break
        for it in items:
            p = it.get("property", it)
            pid = str(p.get("id") or p.get("propertyId") or id(it))
            rent = p.get("rent")
            if pid in seen or not isinstance(rent, (int, float)) or rent <= 0:
                continue
            seen.add(pid)
            area = p.get("builtUpArea") or p.get("propertySize")
            out.append(Listing(rent=int(rent),
                               area=int(area) if isinstance(area, (int, float)) and area > 0 else None,
                               locality=str(p.get("locality") or "")))
        print(f"  page {page}: {len(items)} rows, {len(out)} unique so far")
        if page < pages:
            time.sleep(2.0)
    return out


def load_csv(path: str) -> list[Listing]:
    out: list[Listing] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            try:
                rent = int(float(row["rent"]))
            except (KeyError, ValueError):
                continue
            area_raw = row.get("area", "")
            try:
                area = int(float(area_raw)) if area_raw else None
            except ValueError:
                area = None
            out.append(Listing(rent=rent, area=area,
                               locality=row.get("locality", "").strip()))
    return out


# ------------------------------------------------------------------ stats
def pct(sorted_vals: list[int], p: float) -> int:
    if not sorted_vals:
        return 0
    k = (len(sorted_vals) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(sorted_vals) - 1)
    return int(sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo))


def summarise(listings: list[Listing]) -> dict:
    rents = sorted(l.rent for l in listings)
    psf = [l.rent / l.area for l in listings if l.area]
    locs: dict[str, list[int]] = {}
    for l in listings:
        if l.locality:
            locs.setdefault(l.locality, []).append(l.rent)
    top_locs = sorted(locs.items(), key=lambda kv: -len(kv[1]))[:6]
    return {
        "n": len(rents),
        "p10": pct(rents, 0.10), "p25": pct(rents, 0.25), "p50": pct(rents, 0.50),
        "p75": pct(rents, 0.75), "p90": pct(rents, 0.90),
        "psf_median": statistics.median(psf) if psf else None,
        "top_locs": [(name, len(v), int(statistics.median(v))) for name, v in top_locs],
    }


# ------------------------------------------------------------------ BOE
def boe_verdict(price: int, monthly_rent: int) -> dict:
    """India cost-stack defaults, mirroring the BOE Deal Analyzer assumptions."""
    total = price * 1.07 + 200000          # stamp/registration ~7% + brokerage/fit-out
    gross = monthly_rent * 11              # one vacant month
    noi = gross - 0.30 * gross             # society + tax + insurance + reserve, rolled at 30%
    loan = price * 0.75
    i, n = 0.0875 / 12, 20 * 12
    annual_ds = loan * i / (1 - (1 + i) ** -n) * 12
    roa = noi / total
    fc = annual_ds / loan
    cfaf = noi - annual_ds
    return {"roa": roa, "fc": fc, "cfaf": cfaf,
            "equity": total - loan,
            "positive": roa >= fc}


# ------------------------------------------------------------------ PDF
def build_pdf(out_path: str, label: str, bhk: int, stats: dict,
              verdict_p50: dict | None, verdict_p10: dict | None,
              price: int | None, source_note: str) -> None:
    S = brand.styles()

    def on_page(canvas, doc):
        brand.draw_page_frame(canvas, doc, "Rent Reality Report")

    doc = BaseDocTemplate(out_path, pagesize=A4, leftMargin=MARGIN,
                          rightMargin=MARGIN, topMargin=22 * mm, bottomMargin=20 * mm)
    frame = Frame(MARGIN, 18 * mm, PAGE_W - 2 * MARGIN, A4[1] - 42 * mm, id="f")
    doc.addPageTemplates([PageTemplate(id="body", frames=[frame], onPage=on_page)])
    st = []
    w = PAGE_W - 2 * MARGIN

    st.append(Paragraph(f"Rent Reality Report - {bhk} BHK", S["h1"]))
    st.append(Paragraph(f"<b>{label}</b>  |  prepared {date.today():%d %b %Y}  |  "
                        f"{stats['n']} live listings analysed  |  {source_note}", S["small"]))
    st.append(Spacer(1, 6))

    st.append(Paragraph("The rent band (monthly, INR)", S["h2"]))
    band = [
        ["P10 (soft floor)", "P25", "P50 (THE NUMBER)", "P75", "P90 (broker's story)"],
        [f"{stats['p10']:,}", f"{stats['p25']:,}", f"{stats['p50']:,}",
         f"{stats['p75']:,}", f"{stats['p90']:,}"],
    ]
    t = Table(band, colWidths=[w / 5] * 5)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, 0), 7.6),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"), ("FONTSIZE", (0, 1), (-1, 1), 12),
        ("BACKGROUND", (2, 1), (2, 1), PAPER),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    st.append(t)
    st.append(Paragraph(
        "Read it like a professional: underwrite your deal at <b>P50</b>, stress-test it "
        "at <b>P10</b>, and treat anything quoted above P75 as a marketing number until "
        "a tenant actually signs. Half of all comparable listings are asking less than "
        "the P50.", S["body"]))
    if stats["psf_median"]:
        st.append(Paragraph(
            f"Median asking rent per built-up sq ft: <b>Rs {stats['psf_median']:.1f}/sqft/month</b> "
            f"- use this to sanity-check units of a different size.", S["body"]))

    if stats["top_locs"]:
        st.append(Paragraph("Where the supply sits", S["h2"]))
        rows = [["LOCALITY", "LISTINGS", "MEDIAN ASK (Rs/month)"]]
        for name, n, med in stats["top_locs"]:
            rows.append([name, str(n), f"{med:,}"])
        t = Table(rows, colWidths=[w * 0.5, w * 0.2, w * 0.3], repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8.8),
            ("GRID", (0, 0), (-1, -1), 0.5, LINE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, None]),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        st.append(t)

    if price and verdict_p50 and verdict_p10:
        st.append(Paragraph(f"Your deal at Rs {price:,} - the BOE verdict", S["h2"]))
        rows = [["", "AT P50 RENT", "AT P10 STRESS RENT"],
                ["Return on assets (ROA)",
                 f"{verdict_p50['roa']:.2%}", f"{verdict_p10['roa']:.2%}"],
                ["Financing constant (75% loan, 8.75%, 20y)",
                 f"{verdict_p50['fc']:.2%}", f"{verdict_p10['fc']:.2%}"],
                ["Cash flow after financing (Rs/yr)",
                 f"{verdict_p50['cfaf']:,.0f}", f"{verdict_p10['cfaf']:,.0f}"],
                ["Verdict",
                 "POSITIVE" if verdict_p50["positive"] else "NEGATIVE - appreciation bet",
                 "POSITIVE" if verdict_p10["positive"] else "NEGATIVE - appreciation bet"]]
        t = Table(rows, colWidths=[w * 0.44, w * 0.28, w * 0.28], repeatRows=1)
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), SAND),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8.8),
            ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, LINE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, None]),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("FONTNAME", (1, 4), (-1, 4), "Helvetica-Bold"),
            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
        for col, v in ((1, verdict_p50), (2, verdict_p10)):
            style.append(("TEXTCOLOR", (col, 4), (col, 4), GREEN if v["positive"] else RED))
        t.setStyle(TableStyle(style))
        st.append(t)
        st.append(Paragraph(
            "Assumptions mirror the BOE Deal Analyzer India defaults (7% acquisition "
            "costs, one vacant month, 30% operating cost load, 75% loan at 8.75% for "
            "20 years). For your exact cost stack, run the full analyzer workbook.",
            S["small"]))

    st.append(Spacer(1, 6))
    st.append(Paragraph(
        "Asking rents are a ceiling, not a promise: signed rents typically close 3-8% "
        "below ask in balanced markets. Sample reflects listings live on the report "
        "date within ~2 km of the pincode centroid.", S["small"]))
    st.append(Paragraph(brand.DISCLAIMER, S["small"]))
    doc.build(st)


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser(description="Generate a Rent Reality Report PDF")
    ap.add_argument("--pincode")
    ap.add_argument("--bhk", type=int, default=2, choices=[1, 2, 3, 4])
    ap.add_argument("--city", default="India", help="geocode disambiguation hint")
    ap.add_argument("--pages", type=int, default=3)
    ap.add_argument("--radius", type=float, default=2.0, help="km around pincode centroid")
    ap.add_argument("--csv", help="manual listings file (columns: rent,area,locality)")
    ap.add_argument("--label", help="report label override (used with --csv)")
    ap.add_argument("--price", type=int, help="optional deal price for the BOE verdict")
    ap.add_argument("--out", help="output PDF path")
    a = ap.parse_args()

    if a.csv:
        listings = load_csv(a.csv)
        label = a.label or a.csv
        source_note = "source: client-provided comparables"
    elif a.pincode:
        lat, lon, place = geocode_pincode(a.pincode, a.city)
        print(f"Geocoded {a.pincode} -> {lat:.4f},{lon:.4f} ({place[:60]})")
        listings = fetch_nobroker(lat, lon, a.bhk, a.pages, a.radius)
        label = a.label or f"Pincode {a.pincode} ({place.split(',')[1].strip() if ',' in place else place})"
        source_note = "source: live portal listings"
    else:
        ap.error("provide --pincode or --csv")
        return

    if len(listings) < 8:
        raise SystemExit(f"Only {len(listings)} usable listings - too thin for honest "
                         f"percentiles. Widen --radius/--pages or supply --csv comparables.")

    stats = summarise(listings)
    v50 = boe_verdict(a.price, stats["p50"]) if a.price else None
    v10 = boe_verdict(a.price, stats["p10"]) if a.price else None
    out = a.out or rf"C:\Users\user\real-estate-game-toolkit\07-rent-reality-report\Rent-Reality-{a.pincode or 'csv'}-{a.bhk}BHK.pdf"
    build_pdf(out, label, a.bhk, stats, v50, v10, a.price, source_note)
    print(f"n={stats['n']}  P10={stats['p10']:,}  P50={stats['p50']:,}  P90={stats['p90']:,}")
    print("Built:", out)


if __name__ == "__main__":
    main()
