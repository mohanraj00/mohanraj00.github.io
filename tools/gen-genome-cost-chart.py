#!/usr/bin/env python3
"""Render responsive charts using every observation in NHGRI's cost table."""
import csv
import math
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/synapse"
with (OUT / "genome-sequencing-cost-nhgri.csv").open(newline="") as f:
    ROWS = [(date.fromisoformat(r["date"]), float(r["cost_per_genome_usd"])) for r in csv.DictReader(f)]
assert len(ROWS) == 78 and round(ROWS[-1][1]) == 525
INK, MUTED, BLUE, WARM = "#12203a", "#526178", "#2f6f9f", "#c2603f"
FONT = "Inter,ui-sans-serif,system-ui,sans-serif"

def year(d):
    return d.year + (d.timetuple().tm_yday - 1) / 365.25

def render(mobile):
    w, h = (390, 676) if mobile else (960, 638)
    l, r, t, b = (62, 350, 164, 478) if mobile else (105, 906, 142, 464)
    x = lambda d: l + (year(d)-year(ROWS[0][0]))/(year(ROWS[-1][0])-year(ROWS[0][0]))*(r-l)
    y = lambda v: b - (math.log10(v)-2)/6*(b-t)
    sw = x(date(2008,1,1))
    pts = " ".join(f"{x(d):.2f},{y(v):.2f}" for d,v in ROWS)
    a = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">The machine changed. The curve followed.</title>
<desc id="desc">All 78 NHGRI production-cost observations from September 2001 to May 2022 on a logarithmic scale. The cost falls from 95.3 million dollars to 525 dollars. January 2008 marks the sequencing platform transition. No observations after May 2022 are shown.</desc>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="#fff" stroke="#dce5ee" stroke-width="2"/>
<text x="{30 if mobile else 42}" y="{39 if mobile else 47}" fill="{INK}" font-family="{FONT}" font-size="{20 if mobile else 28}" font-weight="750">The machine changed.</text>''']
    if mobile:
        a.append(f'<text x="30" y="65" fill="{INK}" font-family="{FONT}" font-size="20" font-weight="750">The curve followed.</text>')
    else:
        a[0] = a[0].replace("The machine changed.</text>", "The machine changed. The curve followed.</text>")
    a.append(f'<text x="{30 if mobile else 42}" y="{92 if mobile else 77}" fill="{MUTED}" font-family="{FONT}" font-size="{12 if mobile else 15}">Cost per human-sized genome · USD · logarithmic scale</text>')
    a.append(f'<rect x="{sw:.1f}" y="{t}" width="{r-sw:.1f}" height="{b-t}" fill="#edf4f8"/>')
    labels = {8:"$100m",7:"$10m",6:"$1m",5:"$100k",4:"$10k",3:"$1k",2:"$100"}
    for power in ([8,6,4,2] if mobile else range(8,1,-1)):
        yy = y(10**power)
        a += [f'<line x1="{l}" y1="{yy:.1f}" x2="{r}" y2="{yy:.1f}" stroke="#d9e3ec"/>',
              f'<text x="{l-12}" y="{yy+4:.1f}" text-anchor="end" fill="{MUTED}" font-family="{FONT}" font-size="{11 if mobile else 13}">{labels[power]}</text>']
    for yr in ([2002,2008,2014,2022] if mobile else [2002,2005,2008,2011,2014,2017,2020,2022]):
        a.append(f'<text x="{x(date(yr,1,1)):.1f}" y="{b+25}" text-anchor="middle" fill="{MUTED}" font-family="{FONT}" font-size="{11 if mobile else 13}">{yr}</text>')
    a += [f'<line x1="{sw:.1f}" y1="{t}" x2="{sw:.1f}" y2="{b}" stroke="{WARM}" stroke-width="2" stroke-dasharray="5 5"/>',
          f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="{2.8 if mobile else 3.3}" stroke-linecap="round" stroke-linejoin="round"/>']
    for d,v in [ROWS[0], min(ROWS,key=lambda row: abs((row[0]-date(2008,1,1)).days)), ROWS[-1]]:
        a.append(f'<circle cx="{x(d):.1f}" cy="{y(v):.1f}" r="6" fill="#fff" stroke="{BLUE}" stroke-width="3"/>')
    if mobile:
        a += [f'<rect x="{sw-47:.1f}" y="112" width="190" height="35" rx="9" fill="#fff7f2" stroke="#e6bcaa"/>',
              f'<text x="{sw-36:.1f}" y="135" fill="{WARM}" font-family="{FONT}" font-size="12" font-weight="700">JAN 2008 · PLATFORM SHIFT</text>']
        cards = [(30,"SEP 2001","$95.3m"),(202,"MAY 2022","$525")]
        for cx,lab,val in cards:
            a += [f'<rect x="{cx}" y="528" width="158" height="82" rx="12" fill="#f3f6fa"/>',
                  f'<text x="{cx+14}" y="552" fill="{MUTED}" font-family="{FONT}" font-size="11" font-weight="700">{lab}</text>',
                  f'<text x="{cx+14}" y="586" fill="{INK}" font-family="{FONT}" font-size="27" font-weight="750">{val}</text>']
        a += [f'<text x="30" y="641" fill="{MUTED}" font-family="{FONT}" font-size="11">NHGRI · May 2022 table · production cost only</text>',
              f'<text x="30" y="657" fill="{MUTED}" font-family="{FONT}" font-size="11">All 78 observations · data end in 2022</text>']
    else:
        a += [f'<rect x="{sw-63:.1f}" y="101" width="242" height="30" rx="8" fill="#fff7f2" stroke="#e6bcaa"/>',
              f'<text x="{sw-49:.1f}" y="121" fill="{WARM}" font-family="{FONT}" font-size="13" font-weight="700">JAN 2008 · PLATFORM SHIFT</text>']
        for cx,lab,val in [(42,"SEP 2001","$95.3m"),(354,"JAN 2008","$3.06m"),(666,"MAY 2022","$525")]:
            a += [f'<rect x="{cx}" y="510" width="252" height="74" rx="12" fill="#f3f6fa"/>',
                  f'<text x="{cx+18}" y="536" fill="{MUTED}" font-family="{FONT}" font-size="12" font-weight="700">{lab}</text>',
                  f'<text x="{cx+18}" y="568" fill="{INK}" font-family="{FONT}" font-size="26" font-weight="750">{val}</text>']
        a.append(f'<text x="42" y="610" fill="{MUTED}" font-family="{FONT}" font-size="12">NHGRI, May 2022 table · all 78 observations · production cost only; excludes downstream analysis</text>')
    return "\n".join(a+["</svg>"])

for name,mobile in [("genome-sequencing-cost-curve.svg",False),("genome-sequencing-cost-curve-mobile.svg",True)]:
    path = OUT/name
    path.write_text(render(mobile))
    print(path)
