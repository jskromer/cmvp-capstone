#!/usr/bin/env python3
"""Generate the CMVP Capstone Paper Packet — 13 pages across 3 days."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image
)
from reportlab.lib import colors
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import os

# Colors
CREAM = HexColor('#f5f0e8')
BLUE = HexColor('#2980b9')
DARK = HexColor('#2c3e50')
GREEN = HexColor('#27ae60')
ORANGE = HexColor('#e67e22')
PURPLE = HexColor('#8e44ad')
RED = HexColor('#e74c3c')
LIGHT_BLUE = HexColor('#e8f4f8')
LIGHT_GRAY = HexColor('#f5f5f5')
MEDIUM_GRAY = HexColor('#dee2e6')
HEADER_BG = HexColor('#2c3e50')

OUTPUT_DIR = '/mnt/user-data/outputs'
WORK_DIR = '/home/claude'

# Page setup
PAGE_W, PAGE_H = letter
MARGIN = 0.6 * inch

styles = getSampleStyleSheet()

# Custom styles
styles.add(ParagraphStyle('PacketTitle', parent=styles['Title'], fontSize=26,
    textColor=DARK, spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('PacketSubtitle', parent=styles['Normal'], fontSize=14,
    textColor=BLUE, spaceAfter=12, alignment=TA_CENTER))
styles.add(ParagraphStyle('DayHeader', parent=styles['Heading1'], fontSize=16,
    textColor=white, backColor=DARK, borderPadding=(6, 6, 6, 6),
    spaceAfter=10, spaceBefore=4))
styles.add(ParagraphStyle('WorksheetTitle', parent=styles['Heading2'], fontSize=14,
    textColor=BLUE, spaceBefore=2, spaceAfter=4, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('SectionHead', parent=styles['Heading3'], fontSize=11,
    textColor=DARK, spaceBefore=8, spaceAfter=4, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=9.5,
    leading=12, spaceBefore=2, spaceAfter=2))
styles.add(ParagraphStyle('BodySmall', parent=styles['Normal'], fontSize=8.5,
    leading=10.5, spaceBefore=1, spaceAfter=1))
styles.add(ParagraphStyle('Prompt', parent=styles['Normal'], fontSize=9.5,
    leading=12, textColor=BLUE, spaceBefore=6, spaceAfter=2,
    fontName='Helvetica-BoldOblique'))
styles.add(ParagraphStyle('FillLine', parent=styles['Normal'], fontSize=9.5,
    leading=18, spaceBefore=0, spaceAfter=0))
styles.add(ParagraphStyle('Footer', parent=styles['Normal'], fontSize=7.5,
    textColor=HexColor('#999999'), alignment=TA_CENTER))
styles.add(ParagraphStyle('CellBody', parent=styles['Normal'], fontSize=8.5,
    leading=10))
styles.add(ParagraphStyle('CellHeader', parent=styles['Normal'], fontSize=8.5,
    leading=10, fontName='Helvetica-Bold', textColor=white))
styles.add(ParagraphStyle('CellHeaderDark', parent=styles['Normal'], fontSize=8.5,
    leading=10, fontName='Helvetica-Bold'))

def make_table(headers, rows, col_widths=None, row_height=None):
    """Create a styled table with header row."""
    hdr = [Paragraph(h, styles['CellHeader']) for h in headers]
    data = [hdr]
    for row in rows:
        data.append([Paragraph(str(c), styles['CellBody']) if c else '' for c in row])
    
    if col_widths is None:
        col_widths = [None] * len(headers)
    
    t = Table(data, colWidths=col_widths, repeatRows=1)
    
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]
    if row_height:
        for i in range(1, len(data)):
            style_cmds.append(('ROWHEIGHT', (0, i), (-1, i), row_height))
    
    t.setStyle(TableStyle(style_cmds))
    return t

def fill_table(headers, num_rows, col_widths=None, row_height=32):
    """Table with blank rows for students to fill in."""
    rows = [[''] * len(headers) for _ in range(num_rows)]
    return make_table(headers, rows, col_widths, row_height)

def blank_lines(n=3, width='100%'):
    """Generate blank lines for written responses."""
    lines = []
    for _ in range(n):
        lines.append(Paragraph('_' * 95, styles['FillLine']))
    return lines

def phase_banner(text):
    """Create a colored day banner."""
    t = Table([[Paragraph(text, ParagraphStyle('DayBanner', fontSize=13,
        textColor=white, fontName='Helvetica-Bold', alignment=TA_CENTER))]],
        colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def build_packet():
    story = []
    avail_w = PAGE_W - 2 * MARGIN
    
    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph('Greenfield Municipal Center', styles['PacketTitle']))
    story.append(Paragraph('CMVP Capstone Project', styles['PacketSubtitle']))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph('M&V Plan Development Workbook', ParagraphStyle(
        'Sub2', fontSize=16, textColor=DARK, alignment=TA_CENTER, spaceAfter=4)))
    story.append(Spacer(1, 0.05 * inch))
    
    # Building elevation graphic
    elevation_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'greenfield-elevation.svg')
    if os.path.exists(elevation_path):
        elevation_dwg = svg2rlg(elevation_path)
        if elevation_dwg:
            scale = 0.85 * avail_w / elevation_dwg.width
            elevation_dwg.width = 0.85 * avail_w
            elevation_dwg.height = elevation_dwg.height * scale
            elevation_dwg.scale(scale, scale)
            story.append(elevation_dwg)
    story.append(Spacer(1, 0.1 * inch))
    
    # Student info
    info_data = [
        ['Student Name:', '', 'Date:', ''],
        ['Organization:', '', 'Instructor:', 'Steve Kromer'],
    ]
    info_t = Table(info_data, colWidths=[1.2*inch, 2.5*inch, 0.9*inch, 2*inch])
    info_t.setStyle(TableStyle([
        ('LINEBELOW', (1, 0), (1, 0), 0.5, black),
        ('LINEBELOW', (3, 0), (3, 0), 0.5, black),
        ('LINEBELOW', (1, 1), (1, 1), 0.5, black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(info_t)
    
    story.append(Spacer(1, 0.2 * inch))
    
    # TOC
    story.append(Paragraph('<b>Contents</b>', ParagraphStyle('TOCHead',
        fontSize=13, textColor=DARK, spaceAfter=8)))
    
    toc_items = [
        ('Scenario Brief', '2 pages', 'Reference'),
        ('Worksheet 1A', 'Stakeholder &amp; Risk Matrix', 'Phase 1'),
        ('Worksheet 1B', 'Measurement Boundaries', 'Phase 1'),
        ('Worksheet 1C', 'Approach Selection', 'Phase 1'),
        ('Worksheet 2A', 'Baseline Data Analysis', 'Phase 2'),
        ('Worksheet 2B', 'Static Factors &amp; NRA Protocol', 'Phase 2'),
        ('Worksheet 2C', 'ECM-1 Lighting Stipulation', 'Phase 2'),
        ('Worksheet 2D', 'ECM-4 VFD Metering Plan', 'Phase 2'),
        ('Worksheet 3A', 'M&amp;V Plan Assembly', 'Phase 3'),
        ('Worksheet 3B', 'Savings Calculation &amp; Reporting', 'Phase 3'),
        ('Worksheet 3C', 'Plan Defense Preparation', 'Phase 3'),
    ]
    toc_data = [['Item', 'Description', 'Phase']]
    for item in toc_items:
        toc_data.append(list(item))
    
    toc_t = Table(toc_data, colWidths=[1.3*inch, 3.2*inch, 1.8*inch])
    toc_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(toc_t)
    
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph('EnergyPlus 25.1.0 Simulation Data &bull; Mid-Atlantic Climate Zone 4A',
        styles['Footer']))
    
    story.append(PageBreak())
    
    # =========================================================================
    # SCENARIO BRIEF — PAGE 1: THE BUILDING
    # =========================================================================
    story.append(Paragraph('Scenario Brief — The Building', styles['WorksheetTitle']))
    story.append(Paragraph(
        '<b>Greenfield Municipal Center</b> is a 62,000 sq ft mixed-use government facility '
        'in the mid-Atlantic region (Climate Zone 4A). Original construction ~1995, two stories, '
        'no prior major retrofits. The County of Greenfield has entered into a 15-year Energy '
        'Savings Performance Contract (ESPC) with an ESCO to implement four energy conservation measures.',
        styles['Body']))
    story.append(Spacer(1, 4))
    
    # Wing table
    wing_headers = ['Wing', 'Use', 'Area (sq ft)', 'HVAC', 'Schedule']
    wing_rows = [
        ['A', 'Office (open-plan + private)', '35,000', 'AHU-1: Gas furnace, DX cooling\nFan: 15 HP constant volume', 'M-F 7am\u20136pm'],
        ['B', 'Public library &\ncommunity meeting', '15,000', 'AHU-2: Electric heat pump, DX cooling\nFan: 10 HP constant volume', 'M-Sat 8am\u20139pm\nSun 12\u20135pm'],
        ['C', 'Data center / IT', '2,000', 'CRAC-1: 5-ton DX, 24/7\nNo heating', '24/7'],
        ['Common', 'Lobby, corridors,\nmechanical rooms', '10,000', 'AHU-3: Gas furnace, DX cooling\nFan: 5 HP constant volume', 'M-F 6am\u201310pm'],
    ]
    story.append(make_table(wing_headers, wing_rows, 
        col_widths=[0.55*inch, 1.4*inch, 0.8*inch, 2.6*inch, 1.2*inch]))
    story.append(Spacer(1, 6))
    
    # Envelope
    story.append(Paragraph('<b>Envelope:</b> Steel stud walls R-11, built-up roof R-15, '
        'double-pane clear windows (U-0.55, SHGC 0.60), ~25% WWR.',
        styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    # Floor plan
    try:
        drawing = svg2rlg('/home/claude/greenfield-floor-plan.svg')
        if drawing:
            scale = min((avail_w) / drawing.width, 4.2*inch / drawing.height)
            drawing.width *= scale
            drawing.height *= scale
            drawing.scale(scale, scale)
            story.append(drawing)
    except Exception as e:
        story.append(Paragraph(f'[Floor plan diagram — see greenfield-floor-plan.svg]', styles['Body']))
    
    story.append(PageBreak())
    
    # =========================================================================
    # SCENARIO BRIEF — PAGE 2: THE RETROFIT & CONTEXT
    # =========================================================================
    story.append(Paragraph('Scenario Brief — The Retrofit Package', styles['WorksheetTitle']))
    
    # ECM table
    ecm_headers = ['ECM', 'Description', 'Scope', 'Combined Savings']
    ecm_rows = [
        ['ECM-1', 'LED lighting + occupancy/daylight controls', 'Wings A & B only', 'All four ECMs'],
        ['ECM-2', 'Chiller/DX replacement (higher COP)', 'All units', 'together produce'],
        ['ECM-3', 'Roof insulation upgrade (R-15 \u2192 R-30)', 'Entire building', '122,390 kWh/yr'],
        ['ECM-4', 'VFDs on AHU supply fans', 'AHU-1, 2, 3', '(10.5% of baseline)'],
    ]
    story.append(make_table(ecm_headers, ecm_rows,
        col_widths=[0.6*inch, 2.5*inch, 1.3*inch, 1.3*inch]))
    story.append(Spacer(1, 6))
    
    # Contract context
    story.append(Paragraph('<b>ESPC Contract Context</b>', styles['SectionHead']))
    story.append(Paragraph(
        '\u2022 15-year contract term with guaranteed annual savings<br/>'
        '\u2022 Annual M&amp;V reporting required to verify savings and authorize payments<br/>'
        '\u2022 Savings shortfall risk borne by ESCO; savings surplus shared 80/20 (owner/ESCO)<br/>'
        '\u2022 Owner responsible for maintaining normal building operations<br/>'
        '\u2022 Baseline conditions documented at contract signing; NRA protocol defined in M&amp;V plan',
        styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    # Stakeholders
    story.append(Paragraph('<b>Stakeholders</b>', styles['SectionHead']))
    sth_data = [
        ['Stakeholder', 'Role'],
        ['County of Greenfield', 'Building owner, contract signatory, receives savings'],
        ['ESCO (contractor)', 'Designs, installs, and maintains ECMs; guarantees savings'],
        ['Lender', 'Finances the ESPC; repaid from guaranteed savings stream'],
        ['Utility (Greenfield Electric & Gas)', 'Provides energy; may offer incentives; supplies billing data'],
        ['Building occupants', 'County employees (Wing A), library patrons (Wing B), IT staff (Wing C)'],
        ['M&V professional (you)', 'Develops M&V plan, collects data, reports savings, resolves disputes'],
    ]
    sth_t = Table(sth_data, colWidths=[1.8*inch, 4.7*inch])
    sth_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(sth_t)
    story.append(Spacer(1, 6))
    
    # Utility rates
    story.append(Paragraph('<b>Utility Rates</b>', styles['SectionHead']))
    story.append(Paragraph(
        '<b>Electric:</b> $0.085/kWh energy + $0.015/kWh fuel adj. = $0.100/kWh blended; '
        'Demand: $12.50/kW-month (15-min peak); Customer: $125/month<br/>'
        '<b>Gas:</b> $1.05/therm + $0.12/therm transport = $1.17/therm blended; Customer: $45/month<br/>'
        '<b>Emission factors:</b> Electricity 0.85 lb CO<sub>2</sub>/kWh (PJM grid); '
        'Gas 11.7 lb CO<sub>2</sub>/therm',
        styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    # Single line diagram
    try:
        drawing2 = svg2rlg('/home/claude/greenfield-single-line.svg')
        if drawing2:
            scale2 = min((avail_w) / drawing2.width, 3.0*inch / drawing2.height)
            drawing2.width *= scale2
            drawing2.height *= scale2
            drawing2.scale(scale2, scale2)
            story.append(drawing2)
    except Exception as e:
        story.append(Paragraph('[Single line diagram — see greenfield-single-line.svg]', styles['Body']))
    
    story.append(PageBreak())
    
    # =========================================================================
    # PHASE 1 WORKSHEETS
    # =========================================================================
    story.append(phase_banner('PHASE 1 — Context, Boundaries, and Approach Selection'))
    story.append(Spacer(1, 8))
    
    # --- WORKSHEET 1A ---
    story.append(Paragraph('Worksheet 1A — Stakeholder &amp; Risk Matrix', styles['WorksheetTitle']))
    story.append(Paragraph('<i>Complete after Modules 0\u20132</i>', styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    risk_headers = ['Stakeholder', 'Interest / Concern', 'Risk if M&V Fails', 'Risk Domain(s)']
    risk_rows = [
        ['County of Greenfield\n(owner)', '', '', '\u2610 Technical  \u2610 Commercial\n\u2610 Legal  \u2610 Regulatory'],
        ['ESCO\n(contractor)', '', '', '\u2610 Technical  \u2610 Commercial\n\u2610 Legal  \u2610 Regulatory'],
        ['Lender', '', '', '\u2610 Technical  \u2610 Commercial\n\u2610 Legal  \u2610 Regulatory'],
        ['Utility', '', '', '\u2610 Technical  \u2610 Commercial\n\u2610 Legal  \u2610 Regulatory'],
        ['Building\noccupants', '', '', '\u2610 Technical  \u2610 Commercial\n\u2610 Legal  \u2610 Regulatory'],
        ['M&V professional\n(you)', '', '', '\u2610 Technical  \u2610 Commercial\n\u2610 Legal  \u2610 Regulatory'],
        ['Other:\n(carbon credits,\nESG reporting, ...)', '', '', '\u2610 Technical  \u2610 Commercial\n\u2610 Legal  \u2610 Regulatory'],
    ]
    story.append(make_table(risk_headers, risk_rows,
        col_widths=[1.1*inch, 2.0*inch, 2.0*inch, 1.5*inch], row_height=42))
    story.append(Spacer(1, 6))
    story.append(Paragraph('What guiding principles would you prioritize for this project? Why?',
        styles['Prompt']))
    story.extend(blank_lines(3))
    
    story.append(PageBreak())
    
    # --- WORKSHEET 1B ---
    story.append(phase_banner('PHASE 1 — Context, Boundaries, and Approach Selection'))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Worksheet 1B — Measurement Boundaries', styles['WorksheetTitle']))
    story.append(Paragraph('<i>Complete after Module 3. Mark boundaries on the single line diagram (Scenario Brief p.2).</i>',
        styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    bnd_headers = ['ECM', 'Measurement Boundary\nDescription', "What's Inside\nthe Boundary",
                   "What's Outside", 'Fuels']
    bnd_rows = [
        ['ECM-1\nLighting', '', '', '', '\u2610 Electric\n\u2610 Gas\n\u2610 Both'],
        ['ECM-2\nChiller', '', '', '', '\u2610 Electric\n\u2610 Gas\n\u2610 Both'],
        ['ECM-3\nEnvelope', '', '', '', '\u2610 Electric\n\u2610 Gas\n\u2610 Both'],
        ['ECM-4\nVFDs', '', '', '', '\u2610 Electric\n\u2610 Gas\n\u2610 Both'],
    ]
    story.append(make_table(bnd_headers, bnd_rows,
        col_widths=[0.7*inch, 1.8*inch, 1.5*inch, 1.5*inch, 1.05*inch], row_height=52))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        'For ECM-3 (envelope), why might you need to include both fuels in the measurement boundary?',
        styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Are there any ECMs where the measurement boundary should overlap? Why?',
        styles['Prompt']))
    story.extend(blank_lines(3))
    
    story.append(PageBreak())
    
    # --- WORKSHEET 1C ---
    story.append(phase_banner('PHASE 1 — Context, Boundaries, and Approach Selection'))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Worksheet 1C — Approach Selection', styles['WorksheetTitle']))
    story.append(Paragraph('<i>Complete after Module 3. For each ECM, select the approach and method, then justify your choice.</i>',
        styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    for ecm_name in ['ECM-1: LED Lighting (Wings A & B)', 'ECM-2: Chiller/DX Replacement',
                      'ECM-3: Roof Insulation (R-15 \u2192 R-30)', 'ECM-4: VFDs on AHU Fans']:
        story.append(Paragraph(f'<b>{ecm_name}</b>', styles['SectionHead']))
        appr_data = [
            ['Approach', '\u2610 Retrofit isolation          \u2610 Whole facility'],
            ['Method', '\u2610 Key parameter measurement    \u2610 Continuous performance verification\n'
                       '\u2610 Statistical / inverse model    \u2610 Calibrated simulation / forward model'],
            ['cf. IPMVP', '\u2610 Option A    \u2610 Option B    \u2610 Option C    \u2610 Option D'],
            ['Justification', '\n\n'],
        ]
        at = Table([[Paragraph(r[0], styles['CellHeaderDark']),
                      Paragraph(r[1], styles['CellBody'])] for r in appr_data],
                   colWidths=[1.1*inch, 5.4*inch])
        at.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
            ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(at)
        story.append(Spacer(1, 4))
    
    story.append(Paragraph('Are there interactive effects between any ECMs? Which ones? How will you account for them?',
        styles['Prompt']))
    story.extend(blank_lines(2))
    
    story.append(PageBreak())
    
    # =========================================================================
    # PHASE 2 WORKSHEETS
    # =========================================================================
    story.append(phase_banner('PHASE 2 — Modeling, Baselines, and Adjustments'))
    story.append(Spacer(1, 8))
    
    # --- WORKSHEET 2A ---
    story.append(Paragraph('Worksheet 2A — Baseline Data Analysis', styles['WorksheetTitle']))
    story.append(Paragraph('<i>Complete after Modules 4\u20135. Record observations from the projected scatter plots and model fitting.</i>',
        styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph('<b>Electric Consumption vs. Outdoor Air Temperature</b>', styles['SectionHead']))
    elec_data = [
        ['What pattern do you observe?', ''],
        ['Estimated heating change point', '________ \u00b0F'],
        ['Estimated cooling change point', '________ \u00b0F'],
        ['Estimated baseload (deadband)', '________ kWh/month'],
        ['Best model type', '\u2610 2P   \u2610 3P   \u2610 4P   \u2610 5P'],
    ]
    et = Table([[Paragraph(r[0], styles['CellHeaderDark']),
                 Paragraph(r[1], styles['CellBody'])] for r in elec_data],
               colWidths=[2.2*inch, 4.3*inch])
    et.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(et)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('<b>Gas Consumption vs. Outdoor Air Temperature</b>', styles['SectionHead']))
    gas_data = [
        ['What pattern do you observe?', ''],
        ['Estimated change point', '________ \u00b0F'],
        ['Estimated baseload', '________ therms/month'],
        ['Best model type', '\u2610 2P   \u2610 3P   \u2610 4P   \u2610 5P'],
    ]
    gt = Table([[Paragraph(r[0], styles['CellHeaderDark']),
                 Paragraph(r[1], styles['CellBody'])] for r in gas_data],
               colWidths=[2.2*inch, 4.3*inch])
    gt.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(gt)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('<b>Model Validation (record from projected screen)</b>', styles['SectionHead']))
    val_headers = ['Statistic', 'Electric Model', 'ASHRAE G14 Limit', 'Pass?',
                   'Gas Model', 'ASHRAE G14 Limit', 'Pass?']
    val_rows = [
        ['NMBE', '_______%', '\u00b15% (monthly)', '\u2610', '_______%', '\u00b15%', '\u2610'],
        ['CV(RMSE)', '_______%', '15% (monthly)', '\u2610', '_______%', '15%', '\u2610'],
        ['R\u00b2', '_______', '\u22650.75', '\u2610', '_______', '\u22650.75', '\u2610'],
    ]
    story.append(make_table(val_headers, val_rows,
        col_widths=[0.7*inch, 0.85*inch, 1.0*inch, 0.45*inch, 0.85*inch, 1.0*inch, 0.45*inch]))
    story.append(Spacer(1, 6))
    story.append(Paragraph('Is this model adequate for reporting savings? What concerns do you have?',
        styles['Prompt']))
    story.extend(blank_lines(3))
    
    story.append(PageBreak())
    
    # --- WORKSHEET 2B ---
    story.append(phase_banner('PHASE 2 — Modeling, Baselines, and Adjustments'))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Worksheet 2B — Static Factors &amp; NRA Protocol', styles['WorksheetTitle']))
    story.append(Paragraph('<i>Complete after Module 4. Identify static factors and define your non-routine adjustment protocol.</i>',
        styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph('<b>Static Factors Inventory</b>', styles['SectionHead']))
    sf_headers = ['Static Factor', 'Baseline Value', 'How Monitored', 'What Triggers an NRA?']
    sf_rows = [
        ['Building occupancy', '', '', ''],
        ['Operating schedule', '', '', ''],
        ['Data center load', '', '', ''],
        ['Conditioned floor area', '', '', ''],
        ['', '', '', ''],
        ['', '', '', ''],
    ]
    story.append(make_table(sf_headers, sf_rows,
        col_widths=[1.4*inch, 1.4*inch, 1.7*inch, 2.05*inch], row_height=30))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph('<b>NRA Protocol</b>', styles['SectionHead']))
    story.append(Paragraph('Who is responsible for reporting changes to static factors?', styles['Prompt']))
    story.extend(blank_lines(1))
    story.append(Spacer(1, 4))
    story.append(Paragraph('How will the NRA be quantified? (check all that apply)', styles['Prompt']))
    story.append(Paragraph(
        '\u2610 Engineering calculation&nbsp;&nbsp;&nbsp;\u2610 Sub-metered data&nbsp;&nbsp;&nbsp;'
        '\u2610 Stipulated from manufacturer data&nbsp;&nbsp;&nbsp;\u2610 Adjusted model refit',
        styles['Body']))
    story.append(Spacer(1, 4))
    story.append(Paragraph('How will disputes about NRAs be resolved?', styles['Prompt']))
    story.extend(blank_lines(2))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'At what threshold does a change in a static factor require a non-routine adjustment '
        'rather than being absorbed as model noise?', styles['Prompt']))
    story.extend(blank_lines(2))
    
    story.append(PageBreak())
    
    # --- WORKSHEET 2C ---
    story.append(phase_banner('PHASE 2 — Modeling, Baselines, and Adjustments'))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Worksheet 2C — ECM-1 Lighting Stipulation Calculation', styles['WorksheetTitle']))
    story.append(Paragraph('<i>Complete after Module 6. Calculate stipulated savings for the LED retrofit.</i>',
        styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    ltg_headers = ['Space', 'Qty', 'Base W', 'Retro W', '\u0394W', 'Annual Hrs', 'kWh Saved']
    ltg_rows = [
        ['Wing A \u2014 Open Office (2nd fl)', '120', '128', '40', '88', '2,860', ''],
        ['Wing A \u2014 Open Office (1st fl)', '120', '128', '40', '88', '2,860', ''],
        ['Wing A \u2014 Private Offices', '80', '96', '32', '64', '2,600', ''],
        ['Wing A \u2014 Conference Rooms', '40', '128', '40', '88', '1,200', ''],
        ['Wing A \u2014 Corridors & Restrooms', '60', '64', '20', '44', '3,380', ''],
        ['Wing B \u2014 Reading Rooms', '100', '128', '40', '88', '3,900', ''],
        ['Wing B \u2014 Stacks', '150', '96', '32', '64', '2,600', ''],
        ['Wing B \u2014 Meeting Rooms', '30', '128', '40', '88', '1,500', ''],
        ['Wing B \u2014 Circulation & Entry', '40', '64', '20', '44', '4,160', ''],
        ['TOTAL (740 fixtures)', '', '', '', '', '', ''],
    ]
    story.append(make_table(ltg_headers, ltg_rows,
        col_widths=[1.35*inch, 0.5*inch, 0.65*inch, 0.65*inch, 0.55*inch, 0.85*inch, 1.0*inch]))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Formula:</b> kWh Saved = \u0394W \u00d7 Qty \u00d7 Annual Hours \u00f7 1,000',
        styles['BodySmall']))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('Basis for operating hours:', styles['Prompt']))
    story.append(Paragraph(
        '\u2610 Published schedule&nbsp;&nbsp;&nbsp;\u2610 Metered data (logger)&nbsp;&nbsp;&nbsp;'
        '\u2610 Engineering estimate&nbsp;&nbsp;&nbsp;\u2610 Other: _______________',
        styles['Body']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Does this stipulated savings total match the whole-facility model savings? If not, why not?',
        styles['Prompt']))
    story.extend(blank_lines(2))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'What are the interactive effects of reducing lighting load? How do they affect heating? Cooling?',
        styles['Prompt']))
    story.extend(blank_lines(3))
    
    story.append(PageBreak())
    
    # --- WORKSHEET 2D ---
    story.append(phase_banner('PHASE 2 — Modeling, Baselines, and Adjustments'))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Worksheet 2D — ECM-4 VFD Metering Plan', styles['WorksheetTitle']))
    story.append(Paragraph(
        '<i>Complete after Module 6. Design the continuous performance verification plan for the VFD retrofit.</i>',
        styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph('<b>Parameters to Measure Continuously</b>', styles['SectionHead']))
    mtr_headers = ['Parameter', 'Meter Type', 'Accuracy', 'Location', 'Logging Interval']
    mtr_rows = [
        ['Fan motor kW', '', '', '', ''],
        ['Fan speed (Hz or %)', '', '', '', ''],
        ['Airflow (CFM)', '', '', '', ''],
        ['Supply air temp', '', '', '', ''],
        ['', '', '', '', ''],
    ]
    story.append(make_table(mtr_headers, mtr_rows,
        col_widths=[1.2*inch, 1.2*inch, 0.9*inch, 1.5*inch, 1.0*inch], row_height=28))
    story.append(Spacer(1, 6))
    
    mtr_q = [
        ('Pre-retrofit measurement period (how long? why?):', 2),
        ('Post-retrofit measurement period (how long? why?):', 2),
        ('What happens if you lose 2 weeks of data mid-reporting period?', 2),
        ('Safety considerations for electrical metering:', 2),
        ('Estimated metering cost: $________', 0),
    ]
    for q, lines in mtr_q:
        story.append(Paragraph(q, styles['Prompt']))
        if lines:
            story.extend(blank_lines(lines))
        story.append(Spacer(1, 2))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Evidence vs. Inference for ECM-4</b>', styles['SectionHead']))
    story.append(Paragraph(
        'List what you are <b>measuring</b> (evidence) vs. what you are <b>calculating</b> (inference).',
        styles['BodySmall']))
    ei_headers = ['Evidence (measured)', 'Inference (calculated)']
    ei_rows = [['', ''], ['', ''], ['', ''], ['', '']]
    story.append(make_table(ei_headers, ei_rows,
        col_widths=[3.25*inch, 3.25*inch], row_height=24))
    
    story.append(PageBreak())
    
    # =========================================================================
    # PHASE 3 WORKSHEETS
    # =========================================================================
    story.append(phase_banner('PHASE 3 — Planning, Reporting, and Defense'))
    story.append(Spacer(1, 8))
    
    # --- WORKSHEET 3A ---
    story.append(Paragraph('Worksheet 3A — M&amp;V Plan Assembly', styles['WorksheetTitle']))
    story.append(Paragraph('<i>Complete after Modules 7\u20138. Confirm all plan sections and define the schedule.</i>',
        styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph('<b>M&amp;V Plan Sections Checklist</b>', styles['SectionHead']))
    checklist_items = [
        'Executive summary (project description, ECMs, expected savings)',
        'Baseline conditions (Worksheet 2A data, static factors from 2B)',
        'Approach and method for each ECM (from Worksheet 1C)',
        'Measurement boundary diagrams (from Worksheet 1B)',
        'Metering specifications \u2014 ECM-4 (from Worksheet 2D)',
        'Stipulation basis \u2014 ECM-1 (from Worksheet 2C)',
        'NRA protocol (from Worksheet 2B)',
        'Schedule of M&V activities and reporting (below)',
        'Risk and responsibility matrix (from Worksheet 1A)',
    ]
    for item in checklist_items:
        story.append(Paragraph(f'\u2610&nbsp;&nbsp;{item}', styles['Body']))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph('<b>Schedule of M&amp;V Activities</b>', styles['SectionHead']))
    sch_headers = ['Activity', 'Responsible Party', 'Frequency', 'Deliverable']
    sch_rows = [
        ['Utility bill collection', '', '', ''],
        ['Weather data retrieval', '', '', ''],
        ['Fan metering data download', '', '', ''],
        ['Static factor review', '', '', ''],
        ['Annual savings calculation', '', '', ''],
        ['Annual report submission', '', '', ''],
        ['Operational verification', '', '', ''],
    ]
    story.append(make_table(sch_headers, sch_rows,
        col_widths=[1.6*inch, 1.5*inch, 1.1*inch, 2.3*inch], row_height=26))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph('<b>Cost-Benefit</b>', styles['SectionHead']))
    cb_data = [
        ['Estimated annual M&V cost', '$________'],
        ['Estimated annual savings value (from Worksheet 3B)', '$________'],
        ['M&V cost as % of savings', '________%'],
    ]
    cbt = Table([[Paragraph(r[0], styles['CellHeaderDark']),
                  Paragraph(r[1], styles['CellBody'])] for r in cb_data],
                colWidths=[3.5*inch, 3.0*inch])
    cbt.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(cbt)
    story.append(Spacer(1, 4))
    story.append(Paragraph('Is this cost-effective? What is the industry rule of thumb?', styles['Prompt']))
    story.extend(blank_lines(2))
    
    story.append(PageBreak())
    
    # --- WORKSHEET 3B ---
    story.append(phase_banner('PHASE 3 — Planning, Reporting, and Defense'))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Worksheet 3B — Savings Calculation &amp; Reporting', styles['WorksheetTitle']))
    story.append(Paragraph('<i>Complete after Module 9. Record savings from the projected screen, apply NRA, and value the savings.</i>',
        styles['BodySmall']))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph('<b>Monthly Savings (record from projected screen)</b>', styles['SectionHead']))
    sav_headers = ['Month', 'Baseline Model\nPrediction (kWh)', 'Reporting\nActual (kWh)',
                   'Monthly\nSavings (kWh)', 'Notes']
    sav_rows = [[m, '', '', '', ''] for m in 
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'TOTAL']]
    story.append(make_table(sav_headers, sav_rows,
        col_widths=[0.6*inch, 1.3*inch, 1.2*inch, 1.2*inch, 2.2*inch], row_height=18))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Do you notice anything unusual in months 8\u201312? What happened? How would you adjust?',
        styles['Prompt']))
    story.extend(blank_lines(2))
    
    story.append(Paragraph('<b>After NRA Adjustment</b>', styles['SectionHead']))
    nra_data = [
        ['Gross savings (before NRA)', '________ kWh'],
        ['NRA quantity (data center expansion)', '________ kWh'],
        ['Net adjusted savings', '________ kWh'],
        ['Fractional savings uncertainty (from screen)', '________ %'],
        ['Statistically significant at 90% confidence?', '\u2610 Yes   \u2610 No   \u2610 Borderline'],
    ]
    nrat = Table([[Paragraph(r[0], styles['CellHeaderDark']),
                   Paragraph(r[1], styles['CellBody'])] for r in nra_data],
                 colWidths=[3.2*inch, 3.3*inch])
    nrat.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(nrat)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('<b>Valuation</b>', styles['SectionHead']))
    val_data = [
        ['Electric savings', '________ kWh \u00d7 $0.105/kWh = $________'],
        ['Gas change', '________ therms \u00d7 $1.15/therm = $________'],
        ['Net cost savings', '$________'],
        ['CO\u2082 reduction (electric)', '________ kWh \u00d7 0.417 kg/kWh \u00f7 1,000 = ________ metric tons'],
        ['CO\u2082 change (gas)', '________ therms \u00d7 5.302 kg/therm \u00f7 1,000 = ________ metric tons'],
        ['Net CO\u2082 reduction', '________ metric tons'],
    ]
    valt = Table([[Paragraph(r[0], styles['CellHeaderDark']),
                   Paragraph(r[1], styles['CellBody'])] for r in val_data],
                 colWidths=[1.8*inch, 4.7*inch])
    valt.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(valt)
    
    story.append(PageBreak())
    
    # --- WORKSHEET 3C ---
    story.append(phase_banner('PHASE 3 — Planning, Reporting, and Defense'))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Worksheet 3C — Plan Defense Preparation', styles['WorksheetTitle']))
    story.append(Paragraph('<i>Final phase. Prepare your 5-minute presentation and anticipate challenges.</i>',
        styles['BodySmall']))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('<b>Your 5-Minute Presentation</b>', styles['SectionHead']))
    pres_items = [
        ('1. Approach selection (1 min)', 'Which approaches did you select for each ECM and why?'),
        ('2. Baseline model (1 min)', 'What does your model tell you? How good is it?'),
        ('3. Reporting period findings (1 min)', 'What happened during the reporting period that required adjustment?'),
        ('4. Reported savings (1 min)', 'What are your final savings, uncertainty, and valuation?'),
        ('5. Lessons learned (1 min)', 'What would you do differently with more budget or time?'),
    ]
    for title, desc in pres_items:
        story.append(Paragraph(f'<b>{title}</b> \u2014 {desc}', styles['Body']))
        story.extend(blank_lines(2))
        story.append(Spacer(1, 2))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Anticipated Challenges — Prepare Your Responses</b>', styles['SectionHead']))
    
    challenges = [
        '"Why didn\'t you use continuous performance verification for the lighting ECM?"',
        '"The gas bill went up after the retrofit. How do you explain that to the building owner?"',
        '"Your savings are barely statistically significant. Should we switch to daily data?"',
        '"The ESCO says the NRA shouldn\'t count against their guaranteed savings. Do you agree?"',
    ]
    for c in challenges:
        story.append(Paragraph(f'<b>{c}</b>', styles['BodySmall']))
        story.extend(blank_lines(2))
        story.append(Spacer(1, 2))
    
    # =========================================================================
    # Build the PDF
    # =========================================================================
    output_path = os.path.join(OUTPUT_DIR, 'CMVP_Capstone_Packet.pdf')
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
    )
    
    doc.build(story)
    print(f"PDF created: {output_path}")
    return output_path

if __name__ == '__main__':
    build_packet()
