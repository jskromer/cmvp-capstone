#!/usr/bin/env python3
"""
Generate the SLO Large Office CMVP Capstone Paper Packet — 14 worksheets across 3 phases.

Requires: pip install reportlab svglib
Usage: python scripts/build_slo_packet.py
Output: CMVP_Capstone_SLO_Packet.pdf
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether,
)
import os
import json

# Colors (matching app theme)
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
AMBER_BG = HexColor('#fff3cd')

PAGE_W, PAGE_H = letter
MARGIN = 0.6 * inch

styles = getSampleStyleSheet()

# Custom styles
styles.add(ParagraphStyle('PacketTitle', parent=styles['Title'], fontSize=26,
    textColor=DARK, spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('PacketSubtitle', parent=styles['Normal'], fontSize=14,
    textColor=BLUE, spaceAfter=12, alignment=TA_CENTER))
styles.add(ParagraphStyle('PhaseHeader', parent=styles['Heading1'], fontSize=16,
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
styles.add(ParagraphStyle('CellBody', parent=styles['Normal'], fontSize=8.5, leading=10))
styles.add(ParagraphStyle('CellHeader', parent=styles['Normal'], fontSize=8.5,
    leading=10, fontName='Helvetica-Bold', textColor=white))

AVAIL_W = PAGE_W - 2 * MARGIN


def make_table(headers, rows, col_widths=None, row_height=None):
    """Create a styled table with header row."""
    hdr = [Paragraph(h, styles['CellHeader']) for h in headers]
    data = [hdr]
    for row in rows:
        data.append([Paragraph(str(c), styles['CellBody']) if c else '' for c in row])

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
    rows = [[''] * len(headers) for _ in range(num_rows)]
    return make_table(headers, rows, col_widths, row_height)


def blank_lines(n=3):
    return [Paragraph('_' * 95, styles['FillLine']) for _ in range(n)]


def phase_banner(text):
    t = Table([[Paragraph(text, ParagraphStyle('PhaseBanner', fontSize=13,
        textColor=white, fontName='Helvetica-Bold', alignment=TA_CENTER))]],
        colWidths=[AVAIL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def build_packet():
    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 0.8 * inch))
    story.append(Paragraph('SLO Large Office', styles['PacketTitle']))
    story.append(Paragraph('CMVP Capstone — Forward Model Case Study', styles['PacketSubtitle']))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('M&V Plan Development Workbook', ParagraphStyle(
        'Sub2', fontSize=16, textColor=DARK, alignment=TA_CENTER, spaceAfter=4)))
    story.append(Spacer(1, 0.3 * inch))

    # Building summary box
    story.append(Paragraph(
        '90,000 sq ft · 5 stories · 1980s construction · VAV with reheat<br/>'
        'San Luis Obispo, California — Climate Zone 3C<br/>'
        'Calibrated EnergyPlus forward model · 3 ECMs',
        ParagraphStyle('CoverInfo', fontSize=12, leading=16, alignment=TA_CENTER,
                       textColor=DARK, spaceBefore=8, spaceAfter=12)
    ))
    story.append(Spacer(1, 0.3 * inch))

    # Student info
    info_data = [
        ['Student Name:', '', 'Date:', ''],
        ['Organization:', '', 'Instructor:', 'Steve Kromer'],
    ]
    t = Table(info_data, colWidths=[1.2*inch, 2.5*inch, 1.0*inch, 2.0*inch])
    t.setStyle(TableStyle([
        ('LINEBELOW', (1, 0), (1, 0), 0.5, black),
        ('LINEBELOW', (3, 0), (3, 0), 0.5, black),
        ('LINEBELOW', (1, 1), (1, 1), 0.5, black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(PageBreak())

    # =========================================================================
    # SCENARIO BRIEF (2 pages)
    # =========================================================================
    story.append(Paragraph('Scenario Brief', styles['WorksheetTitle']))
    story.append(Paragraph(
        'The SLO Large Office is a 90,000 sq ft, 5-story commercial office building in '
        'San Luis Obispo, California (Climate Zone 3C — mild marine climate). The building '
        'was constructed in the 1980s and uses a Variable Air Volume (VAV) system with hot '
        'water reheat coils. The HVAC system includes a centrifugal chiller (COP 3.2, 15 years old), '
        'a gas-fired boiler for reheat, and 15 thermal zones across 5 floors.',
        styles['Body']))
    story.append(Spacer(1, 0.1 * inch))

    # Utility data table
    story.append(Paragraph('Annual Utility Data (2023)', styles['SectionHead']))
    story.append(make_table(
        ['Month', 'Days', 'kWh', 'kW Demand', 'Therms', 'Elec Cost ($)', 'Gas Cost ($)'],
        [
            ['Jan', '31', '86,400', '245', '1,920', '14,688', '2,304'],
            ['Feb', '28', '77,600', '228', '2,090', '13,192', '2,508'],
            ['Mar', '31', '82,000', '240', '1,650', '13,940', '1,980'],
            ['Apr', '30', '89,300', '264', '1,110', '15,181', '1,332'],
            ['May', '31', '99,800', '312', '640', '16,966', '768'],
            ['Jun', '30', '112,700', '372', '300', '19,159', '360'],
            ['Jul', '31', '124,200', '408', '235', '21,114', '282'],
            ['Aug', '31', '120,000', '390', '255', '20,400', '306'],
            ['Sep', '30', '109,100', '348', '280', '18,547', '336'],
            ['Oct', '31', '96,500', '288', '570', '16,405', '684'],
            ['Nov', '30', '85,200', '246', '1,310', '14,484', '1,572'],
            ['Dec', '31', '83,600', '240', '1,785', '14,212', '2,142'],
            ['<b>TOTAL</b>', '<b>365</b>', '<b>1,166,400</b>', '<b>408</b>', '<b>13,145</b>',
             '<b>$197,988</b>', '<b>$14,574</b>'],
        ],
        col_widths=[0.6*inch, 0.5*inch, 0.8*inch, 0.7*inch, 0.7*inch, 0.9*inch, 0.9*inch],
    ))

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('Proposed ECMs', styles['SectionHead']))
    story.append(make_table(
        ['ECM', 'Description', 'Approach', 'Method', 'cf. IPMVP'],
        [
            ['ECM-1', 'LED Lighting Retrofit (LPD 10.8 → 7.0 W/m²)', 'Retrofit isolation', 'Key parameter measurement', 'Option A'],
            ['ECM-2', 'Chiller Replacement (COP 3.2 → 4.0)', 'Whole facility', 'Calibrated simulation / forward model', 'Option D'],
            ['ECM-3', 'VAV Box Optimization', 'Whole facility', 'Calibrated simulation / forward model', 'Option D'],
        ],
        col_widths=[0.6*inch, 1.8*inch, 1.0*inch, 1.8*inch, 0.8*inch],
    ))

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('Utility Rates', styles['SectionHead']))
    story.append(Paragraph(
        '<b>Electric:</b> $0.170/kWh (PG&amp;E commercial), Demand: $18.00/kW-month<br/>'
        '<b>Gas:</b> $1.20/therm<br/>'
        '<b>Emissions:</b> Electric 0.53 lb CO₂/kWh (CAMX grid); Gas 11.7 lb CO₂/therm',
        styles['Body']))

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('<b>Key Distinction:</b> This case study uses a calibrated simulation '
        '(forward model), not an inverse/statistical model. The direction of inference is reversed: '
        'physical parameters → predicted energy.', styles['Body']))
    story.append(Paragraph('<font color="#856404"><b>Gas Limitation:</b></font> The EnergyPlus '
        'prototype uses electric reheat internally. Gas calibration was not performed. Gas savings '
        'cannot be reliably estimated from this model.', styles['Body']))
    story.append(PageBreak())

    # =========================================================================
    # PHASE 1: CONTEXT & BOUNDARIES
    # =========================================================================
    story.append(phase_banner('PHASE 1 — Context, Boundaries, and Approach Selection'))
    story.append(Spacer(1, 0.15 * inch))

    # 1A: Stakeholder & Risk Matrix
    story.append(Paragraph('Worksheet 1A: Stakeholder & Risk Matrix', styles['WorksheetTitle']))
    story.append(Paragraph(
        'Identify the key stakeholders for this California commercial building retrofit project. '
        'Consider building owner, tenants, utility (PG&E), ESCO, M&V professional, '
        'and regulatory bodies (CEC/CPUC).', styles['Body']))
    story.append(fill_table(
        ['Stakeholder', 'Interest / Concern', 'Risk They Bear', 'What They Need from M&V'],
        6, col_widths=[1.2*inch, 2.0*inch, 1.8*inch, 1.8*inch], row_height=36,
    ))
    story.append(Paragraph('What is the primary contractual structure for this project?', styles['Prompt']))
    story.extend(blank_lines(2))
    story.append(PageBreak())

    # 1B: Measurement Boundaries
    story.append(Paragraph('Worksheet 1B: Measurement Boundaries', styles['WorksheetTitle']))
    story.append(Paragraph(
        'Define the measurement boundary for each ECM. For a forward model approach, '
        'the boundary is typically whole-facility (the simulation encompasses the entire building).', styles['Body']))
    story.append(fill_table(
        ['ECM', 'Boundary Type', 'What Is Inside', 'What Is Outside', 'Metering Points'],
        3, col_widths=[0.6*inch, 1.0*inch, 1.6*inch, 1.6*inch, 1.3*inch], row_height=40,
    ))
    story.append(Paragraph('Why does a forward model approach typically use a whole-facility boundary?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(PageBreak())

    # 1C: Approach Selection
    story.append(Paragraph('Worksheet 1C: Approach Selection Justification', styles['WorksheetTitle']))
    story.append(Paragraph(
        'For each ECM, justify the selected M&V approach. ECM-1 uses retrofit isolation '
        'while ECMs 2-3 use the calibrated simulation. Why the different approaches?', styles['Body']))
    story.append(fill_table(
        ['ECM', 'Approach', 'Method', 'Justification', 'cf. IPMVP'],
        3, col_widths=[0.6*inch, 1.0*inch, 1.4*inch, 2.4*inch, 0.7*inch], row_height=40,
    ))
    story.append(Paragraph(
        'Could all 3 ECMs be verified with the forward model alone? Why or why not?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(PageBreak())

    # =========================================================================
    # PHASE 2: MODELING, CALIBRATION, SENSITIVITY
    # =========================================================================
    story.append(phase_banner('PHASE 2 — Calibration, Sensitivity, and Baseline'))
    story.append(Spacer(1, 0.15 * inch))

    # 2A: Calibration Assessment
    story.append(Paragraph('Worksheet 2A: Calibration Assessment', styles['WorksheetTitle']))
    story.append(Paragraph(
        'Record the calibration results from the web app\'s Calibration Assessment tab.', styles['Body']))
    story.append(make_table(
        ['Metric', 'Value', 'ASHRAE G14 Limit', 'Pass/Fail'],
        [
            ['NMBE (%)', '', '≤ 5%', ''],
            ['CV(RMSE) (%)', '', '≤ 15%', ''],
            ['Annual Simulated (kWh)', '', '—', '—'],
            ['Annual Metered (kWh)', '', '—', '—'],
            ['Annual Difference (%)', '', '—', '—'],
        ],
        col_widths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch],
    ))
    story.append(Paragraph(
        'Does passing ASHRAE G14 mean the model is "correct"? What does calibration actually prove?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(Paragraph(
        'The model over-predicts winter and under-predicts summer. Why might this happen with a prototype-based model?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(PageBreak())

    # 2B: Parameter Provenance
    story.append(Paragraph('Worksheet 2B: Parameter Provenance', styles['WorksheetTitle']))
    story.append(Paragraph(
        'For each of the 8 sensitivity parameters, document the evidence source category.', styles['Body']))
    story.append(fill_table(
        ['Parameter', 'Sensitivity Rank', 'Source Category', 'Evidence Description', 'Confidence'],
        8, col_widths=[1.2*inch, 0.8*inch, 1.0*inch, 2.2*inch, 0.9*inch], row_height=30,
    ))
    story.append(Paragraph('Source categories: audit, nameplate, design docs, assumption, calculation, manufacturer data', styles['BodySmall']))
    story.append(Paragraph(
        'Which parameters have the weakest evidence? How does that affect your confidence in the savings estimate?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(PageBreak())

    # 2C: Sensitivity Ranking
    story.append(Paragraph('Worksheet 2C: Sensitivity Ranking', styles['WorksheetTitle']))
    story.append(Paragraph(
        'Record the sensitivity analysis results from the web app. Rank parameters by '
        'their impact on annual electricity prediction (±15% perturbation).', styles['Body']))
    story.append(fill_table(
        ['Rank', 'Parameter', '±15% Impact (kWh)', '±15% Impact (%)', 'Direction', 'Measure Priority?'],
        8, col_widths=[0.5*inch, 1.3*inch, 1.2*inch, 1.0*inch, 0.8*inch, 1.3*inch], row_height=28,
    ))
    story.append(Paragraph(
        'Which 3 parameters would you prioritize for additional measurement or verification? Why?', styles['Prompt']))
    story.extend(blank_lines(4))
    story.append(Paragraph(
        'Two parameters show zero sensitivity. What does this tell you about the model?', styles['Prompt']))
    story.extend(blank_lines(2))
    story.append(PageBreak())

    # 2D: Lighting Stipulation
    story.append(Paragraph('Worksheet 2D: ECM-1 Lighting Stipulation', styles['WorksheetTitle']))
    story.append(Paragraph(
        'Calculate stipulated savings for the LED retrofit across all 5 floors. '
        'Wattage is measured; hours are stipulated.', styles['Body']))
    story.append(fill_table(
        ['Space', 'Qty', 'Baseline W', 'Retrofit W', 'ΔW', 'Annual Hours', 'kWh Saved'],
        9, col_widths=[1.6*inch, 0.5*inch, 0.7*inch, 0.7*inch, 0.5*inch, 0.8*inch, 0.9*inch], row_height=24,
    ))
    story.append(Spacer(1, 0.05 * inch))
    story.append(make_table(
        ['Total Fixtures', 'Baseline kW', 'Retrofit kW', 'Δ kW', 'Annual kWh Saved'],
        [['', '', '', '', '']],
        col_widths=[1.2*inch, 1.2*inch, 1.2*inch, 1.0*inch, 1.5*inch],
    ))
    story.append(Paragraph(
        'How does the stipulated lighting savings compare to the sensitivity analysis prediction for LPD?', styles['Prompt']))
    story.extend(blank_lines(2))
    story.append(PageBreak())

    # =========================================================================
    # PHASE 3: SAVINGS, COUNTERFACTUAL, ASSESSMENT
    # =========================================================================
    story.append(phase_banner('PHASE 3 — Savings, Counterfactual, and Assessment'))
    story.append(Spacer(1, 0.15 * inch))

    # 3A: Competent Counterfactual
    story.append(Paragraph('Worksheet 3A: Competent Counterfactual', styles['WorksheetTitle']))
    story.append(Paragraph(
        'Evaluate whether the calibrated simulation meets the standard for a competent counterfactual. '
        'For each criterion, check Yes / Partial / No and explain.', styles['Body']))
    criteria = [
        ['Parameter Provenance', 'Can you trace every model input to a documented source?'],
        ['Physical Plausibility', 'Are all parameter values within physically reasonable bounds?'],
        ['Sensitivity Awareness', 'Do you know which parameters drive the most uncertainty?'],
        ['Honest Calibration', 'Does the calibration accurately represent model capability?'],
        ['Limitations Disclosed', 'Are all known limitations explicitly stated?'],
    ]
    story.append(fill_table(
        ['Criterion', 'Question', 'Y / P / N', 'Explanation'],
        5, col_widths=[1.2*inch, 2.0*inch, 0.6*inch, 2.3*inch], row_height=40,
    ))
    # Pre-fill the criteria column text
    story.append(Paragraph(
        'Based on your assessment, is this model a competent counterfactual? What is your confidence level?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(PageBreak())

    # 3B: Forward Model Savings
    story.append(Paragraph('Worksheet 3B: Forward Model Savings', styles['WorksheetTitle']))
    story.append(Paragraph(
        'Record the projected savings for each ECM from the web app\'s ECM Savings tab.', styles['Body']))
    story.append(fill_table(
        ['ECM', 'Savings (kWh/yr)', 'Savings (%)', 'Uncertainty (±%)', 'Cost Savings ($/yr)', 'Notes'],
        3, col_widths=[0.6*inch, 1.1*inch, 0.8*inch, 0.9*inch, 1.0*inch, 1.7*inch], row_height=36,
    ))
    story.append(make_table(
        ['Total Package', 'Savings kWh', 'Savings %', 'Cost Savings'],
        [['All ECMs', '', '', '']],
        col_widths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch],
    ))
    story.append(Paragraph(
        'Why do the uncertainty bands differ across ECMs? How does parameter confidence propagate into savings uncertainty?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(Paragraph(
        'How would you communicate these savings and their uncertainty to a building owner?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(PageBreak())

    # 3C: MnVScore Self-Assessment
    story.append(Paragraph('Worksheet 3C: MnVScore Self-Assessment', styles['WorksheetTitle']))
    story.append(Paragraph(
        'For each ECM, evaluate your M&V methodology across 8 dimensions. '
        'Rate as S (Sufficient), L (Limited), or N (Not Addressed).', styles['Body']))

    dimensions = [
        'Measurement Method', 'Boundary & Scope', 'Duration & Cadence', 'Use Case Fit',
        'Savings Isolation', 'Interactive Effects', 'Baseline Robustness', 'Uncertainty Quantification',
    ]

    for ecm_num, ecm_name in [(1, 'LED Lighting'), (2, 'Chiller Replacement'), (3, 'VAV Optimization')]:
        story.append(Paragraph(f'ECM-{ecm_num}: {ecm_name}', styles['SectionHead']))
        story.append(fill_table(
            ['Dimension', 'S / L / N', 'Justification'],
            8, col_widths=[1.5*inch, 0.7*inch, 4.0*inch], row_height=26,
        ))
        story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph(
        'Compare the profiles across 3 ECMs. Which has the strongest methodology? Where are the gaps?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(PageBreak())

    # 3D: Gas Model Disclosure
    story.append(Paragraph('Worksheet 3D: Gas Model Disclosure', styles['WorksheetTitle']))
    story.append(Paragraph(
        'The calibrated EnergyPlus model cannot reliably predict gas consumption because the '
        'DOE prototype uses electric reheat internally while the actual building has gas-fired reheat. '
        'Draft a disclosure statement for the client.', styles['Body']))

    story.append(Paragraph('1. What is the specific limitation?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(Paragraph('2. What impact does this have on savings claims?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(Paragraph('3. What would you recommend to address this gap?', styles['Prompt']))
    story.extend(blank_lines(3))
    story.append(Paragraph('4. Draft a 2-3 sentence disclosure for the M&V report:', styles['Prompt']))
    story.extend(blank_lines(5))

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        'CMVP Capstone — SLO Large Office · Calibrated EnergyPlus Forward Model · California CZ 3C',
        styles['Footer']))
    story.append(Paragraph(
        'Counterfactual Designs · counterfactual-designs.com',
        styles['Footer']))

    # Build PDF
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, '..', 'CMVP_Capstone_SLO_Packet.pdf')
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )
    doc.build(story)
    print(f"Generated: {os.path.abspath(output_path)}")


if __name__ == '__main__':
    build_packet()
