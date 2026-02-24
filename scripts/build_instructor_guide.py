#!/usr/bin/env python3
"""Build the CMVP Capstone Instructor Guide PDF."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)

# ── Palette ──────────────────────────────────────────────────────────
CREAM      = HexColor('#f5f0e8')
DARK       = HexColor('#2d3748')
ACCENT     = HexColor('#c47a2a')
MEDIUM_GRAY = HexColor('#a0aec0')
LIGHT_GRAY = HexColor('#f7fafc')
BLUE_LINK  = HexColor('#2b6cb0')
RED_ALERT  = HexColor('#c53030')
GREEN_OK   = HexColor('#276749')

PAGE_W, PAGE_H = letter
MARGIN = 0.75 * inch

def build():
    outpath = '/mnt/user-data/outputs/CMVP_Capstone_Instructor_Guide.pdf'
    doc = SimpleDocTemplate(outpath, pagesize=letter,
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN)
    avail_w = PAGE_W - 2 * MARGIN
    story = []

    # ── Styles ───────────────────────────────────────────────────────
    s = {}
    s['Title'] = ParagraphStyle('Title', fontSize=26, textColor=DARK,
        alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold')
    s['Subtitle'] = ParagraphStyle('Subtitle', fontSize=16, textColor=ACCENT,
        alignment=TA_CENTER, spaceAfter=6, fontName='Helvetica-Bold')
    s['Sub2'] = ParagraphStyle('Sub2', fontSize=13, textColor=DARK,
        alignment=TA_CENTER, spaceAfter=4)
    s['H1'] = ParagraphStyle('H1', fontSize=16, textColor=DARK,
        fontName='Helvetica-Bold', spaceAfter=8, spaceBefore=14,
        borderWidth=0, borderColor=ACCENT, borderPadding=0)
    s['H2'] = ParagraphStyle('H2', fontSize=13, textColor=ACCENT,
        fontName='Helvetica-Bold', spaceAfter=6, spaceBefore=10)
    s['H3'] = ParagraphStyle('H3', fontSize=11, textColor=DARK,
        fontName='Helvetica-Bold', spaceAfter=4, spaceBefore=6)
    s['Body'] = ParagraphStyle('Body', fontSize=10, textColor=DARK,
        leading=14, spaceAfter=6)
    s['BodySmall'] = ParagraphStyle('BodySmall', fontSize=9, textColor=DARK,
        leading=12, spaceAfter=4)
    s['Note'] = ParagraphStyle('Note', fontSize=9, textColor=HexColor('#4a5568'),
        leading=12, spaceAfter=4, leftIndent=12, fontName='Helvetica-Oblique')
    s['Alert'] = ParagraphStyle('Alert', fontSize=10, textColor=RED_ALERT,
        leading=13, spaceAfter=6, fontName='Helvetica-Bold')
    s['Footer'] = ParagraphStyle('Footer', fontSize=8, textColor=MEDIUM_GRAY,
        alignment=TA_CENTER)
    s['Link'] = ParagraphStyle('Link', fontSize=9, textColor=BLUE_LINK,
        leading=12, spaceAfter=3)
    s['LinkBody'] = ParagraphStyle('LinkBody', fontSize=9, textColor=DARK,
        leading=12, spaceAfter=2, leftIndent=12)

    def hr():
        """Horizontal rule."""
        t = Table([['']],colWidths=[avail_w])
        t.setStyle(TableStyle([('LINEBELOW',(0,0),(0,0),0.5,MEDIUM_GRAY)]))
        story.append(t)
        story.append(Spacer(1,6))

    def section_header(text):
        story.append(Paragraph(text, s['H1']))
        hr()

    # ── Helper for link tables ──
    def link_table(rows):
        """rows = [(label, url, description), ...]"""
        data = [['Resource','Description']]
        for label, url, desc in rows:
            link = f'<a href="{url}" color="#2b6cb0">{label}</a>'
            data.append([Paragraph(link, s['BodySmall']),
                         Paragraph(desc, s['BodySmall'])])
        t = Table(data, colWidths=[2.6*inch, avail_w - 2.6*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),DARK),
            ('TEXTCOLOR',(0,0),(-1,0),white),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
            ('FONTSIZE',(0,0),(-1,0),9),
            ('GRID',(0,0),(-1,-1),0.5,MEDIUM_GRAY),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT_GRAY]),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),4),
            ('BOTTOMPADDING',(0,0),(-1,-1),4),
            ('LEFTPADDING',(0,0),(-1,-1),6),
            ('RIGHTPADDING',(0,0),(-1,-1),6),
        ]))
        story.append(t)

    # ═════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ═════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 1.2*inch))
    story.append(Paragraph('CMVP Capstone Project', s['Title']))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph('Instructor Guide', s['Subtitle']))
    story.append(Spacer(1, 0.4*inch))

    # Accent bar
    bar = Table([['']],colWidths=[2*inch])
    bar.setStyle(TableStyle([('LINEBELOW',(0,0),(0,0),3,ACCENT)]))
    bar.hAlign = 'CENTER'
    story.append(bar)
    story.append(Spacer(1, 0.35*inch))

    story.append(Paragraph('Greenfield Municipal Center', ParagraphStyle(
        'CoverBuilding', fontSize=14, textColor=DARK, alignment=TA_CENTER,
        fontName='Helvetica-Bold', spaceAfter=4)))
    story.append(Paragraph('M&amp;V Plan Development Workbook', ParagraphStyle(
        'CoverSub', fontSize=12, textColor=MEDIUM_GRAY, alignment=TA_CENTER, spaceAfter=6)))
    story.append(Spacer(1, 0.4*inch))

    # Prepared for — boxed
    prep_data = [['Prepared for Steve Kromer'],
                 ['CMVP Course Instructor  •  Association of Energy Engineers']]
    prep_t = Table(prep_data, colWidths=[4.5*inch])
    prep_t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(0,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(0,0),11),
        ('FONTSIZE',(0,1),(0,1),9),
        ('TEXTCOLOR',(0,0),(-1,-1),DARK),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('BACKGROUND',(0,0),(-1,-1),LIGHT_GRAY),
        ('BOX',(0,0),(-1,-1),0.5,MEDIUM_GRAY),
    ]))
    prep_t.hAlign = 'CENTER'
    story.append(prep_t)
    story.append(Spacer(1, 0.5*inch))

    story.append(Paragraph('<b>Contents</b>', ParagraphStyle('TOCHead',
        fontSize=12, textColor=DARK, spaceAfter=8)))
    
    toc_items = [
        ('1', '3-Day Schedule &amp; Timing', '2'),
        ('2', 'Teaching Moments in the Data', '3'),
        ('3', 'Module-by-Module Facilitation', '4–6'),
        ('4', 'Answer Scaffolding', '7'),
        ('5', 'Companion Tools &amp; Interactive Sites', '8'),
        ('A', 'Appendix — Curated Web Links', '9–11'),
    ]
    toc_data = [['§','Topic','Page']]
    for item in toc_items:
        toc_data.append(list(item))
    toc_t = Table(toc_data, colWidths=[0.5*inch, 4.5*inch, 1.2*inch])
    toc_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK),
        ('TEXTCOLOR',(0,0),(-1,0),white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),10),
        ('GRID',(0,0),(-1,-1),0.5,MEDIUM_GRAY),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT_GRAY]),
        ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    story.append(toc_t)
    story.append(Spacer(1, 0.4*inch))
    conf_data = [['CONFIDENTIAL — INSTRUCTOR USE ONLY'],
                 ['Do not distribute to students. Contains answer scaffolding and facilitation cues.']]
    conf_t = Table(conf_data, colWidths=[5*inch])
    conf_t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(0,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(0,0),11),
        ('FONTSIZE',(0,1),(0,1),9),
        ('TEXTCOLOR',(0,0),(-1,-1),RED_ALERT),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('BOX',(0,0),(-1,-1),1.5,RED_ALERT),
    ]))
    conf_t.hAlign = 'CENTER'
    story.append(conf_t)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════
    # SECTION 1: 3-DAY SCHEDULE
    # ═════════════════════════════════════════════════════════════════
    section_header('1 &nbsp; 3-Day Schedule &amp; Timing')
    
    # Day 1
    story.append(Paragraph('<b>Day 1: Context, Boundaries, and Approaches</b>', s['H2']))
    day1 = [
        ['Time','Activity','Module','Capstone Work','Tools'],
        ['8:30–9:00','Welcome, scenario intro','0','Distribute paper packets\nOpen capstone site: Overview tab','Paper packet\ncmvp-capstone.vercel.app'],
        ['9:00–10:15','Context & stakeholders','1–2','Worksheet 1A:\nStakeholder & risk matrix','Building graphic on\nOverview tab'],
        ['10:15–10:30','Break','','',''],
        ['10:30–12:00','Approaches, boundaries','3','Worksheet 1B: Boundaries\nWorksheet 1C: Approach selection','Single line diagram\n(paper packet)'],
        ['12:00–1:00','Lunch','','',''],
        ['1:00–2:30','Statistics interlude','3.1','Explore Scatter Plots tab\nIdentify patterns in data','Statistics_Exercise.xlsm\nDescriptive_Stats_Step_1.xlsx'],
        ['2:30–2:45','Break','','',''],
        ['2:45–4:00','Model concepts intro','3.1','Scatter plot observations\nGroup discussion: what model?','Least_Squares_Matrix.xlsx\nScatter Plots tab'],
        ['4:00–4:30','Day 1 wrap','','Collect Worksheets 1A–1C',''],
    ]
    t1 = Table(day1, colWidths=[0.8*inch, 1.3*inch, 0.6*inch, 2.0*inch, 1.8*inch])
    t1.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK),
        ('TEXTCOLOR',(0,0),(-1,0),white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('GRID',(0,0),(-1,-1),0.5,MEDIUM_GRAY),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT_GRAY]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    story.append(t1)
    story.append(Spacer(1,10))

    # Day 2
    story.append(Paragraph('<b>Day 2: Modeling, Baselines, and Adjustments</b>', s['H2']))
    day2 = [
        ['Time','Activity','Module','Capstone Work','Tools'],
        ['8:30–10:15','Baseline modeling','4–5','Model Fitting tab: fit 5P model\nWorksheet 2A: record observations\n⚡ Teaching Moment: change points','Model Fitting tab\ncmvp-capstone.vercel.app'],
        ['10:15–10:30','Break','','',''],
        ['10:30–12:00','Static factors, NRAs','4','Worksheet 2B: static factors\nTime Series tab: find the NRA\n⚡ Teaching Moment: NRA discovery','Time Series tab\n(toggle electric/gas)'],
        ['12:00–1:00','Lunch','','',''],
        ['1:00–2:30','Retrofit isolation','6','Worksheet 2C: lighting stipulation\nLighting Stipulation tab\n⚡ Teaching Moment: interactive effects','Lighting Stipulation tab'],
        ['2:30–2:45','Break','','',''],
        ['2:45–4:00','VFD metering design','6','Worksheet 2D: VFD metering plan\nVFD Analysis tab: fan law\n⚡ Teaching Moment: cubic relationship','VFD Analysis tab\nOEH_M_V_planning_tool.xlsx'],
        ['4:00–4:30','Day 2 wrap','','Collect Worksheets 2A–2D',''],
    ]
    t2 = Table(day2, colWidths=[0.8*inch, 1.3*inch, 0.6*inch, 2.0*inch, 1.8*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK),
        ('TEXTCOLOR',(0,0),(-1,0),white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('GRID',(0,0),(-1,-1),0.5,MEDIUM_GRAY),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT_GRAY]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    story.append(t2)
    story.append(Spacer(1,10))

    # Day 3
    story.append(Paragraph('<b>Day 3: Planning, Reporting, and Defense</b>', s['H2']))
    day3 = [
        ['Time','Activity','Module','Capstone Work','Tools'],
        ['8:30–10:15','M&V plan assembly','7–8','Worksheet 3A: plan checklist\nFinalize metering specs\nSignificant digits discussion','OEH_M_V_planning_tool.xlsx'],
        ['10:15–10:30','Break','','',''],
        ['10:30–12:00','Savings & uncertainty','8.1–9','Savings Calculator tab\nWorksheet 3B: savings table\n⚡ Teaching Moment: gas increase\n⚡ Teaching Moment: G14 fail','Savings Calculator tab\ncmvp-capstone.vercel.app'],
        ['12:00–1:00','Lunch','','',''],
        ['1:00–2:30','Report drafting','9','Worksheet 3B: valuation, CO₂\nExec summary draft\nWorksheet 3C: defense prep','Savings Calculator tab\n(valuation section)'],
        ['2:30–2:45','Break','','',''],
        ['2:45–4:00','Plan defense','9','5-minute presentations\nPeer review & discussion\nExam prep Q&A','Paper packet\n(all worksheets)'],
        ['4:00–4:30','Course wrap','','Collect final packets\nCourse evaluations',''],
    ]
    t3 = Table(day3, colWidths=[0.8*inch, 1.3*inch, 0.6*inch, 2.0*inch, 1.8*inch])
    t3.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK),
        ('TEXTCOLOR',(0,0),(-1,0),white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('GRID',(0,0),(-1,-1),0.5,MEDIUM_GRAY),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT_GRAY]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    story.append(t3)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════
    # SECTION 2: TEACHING MOMENTS
    # ═════════════════════════════════════════════════════════════════
    section_header('2 &nbsp; Teaching Moments Embedded in the Data')
    story.append(Paragraph(
        'Six deliberate teaching moments are built into the Greenfield dataset. '
        'Each surfaces a real-world M&amp;V challenge that students must discover and resolve. '
        'The prompts in the capstone app point students toward these moments without giving away the answer.',
        s['Body']))
    story.append(Spacer(1,6))

    moments = [
        ('⚡ 1. Physics vs. Statistics — Change Point Tradeoff',
         'Day 2 AM · Model Fitting tab',
         'The auto-fit algorithm finds optimal change points at 35/71°F (R² = 0.91). '
         'These are mathematically optimal but physically unrealistic — no building switches from heating '
         'to cooling at 35°F. Students use manual sliders to try 48/63°F and watch R² drop to ~0.65.',
         'This is the core professional judgment moment: do you report the model with the best statistics, '
         'or the one that makes physical sense? There is no single right answer, but students must justify '
         'their choice. Expect 15–20 minutes of group discussion.'),

        ('⚡ 2. Gas CV(RMSE) Fails Guideline 14',
         'Day 2 AM · Model Fitting tab',
         'The gas model CV(RMSE) is ~16.1%, which exceeds the ASHRAE Guideline 14 threshold of 15%. '
         'The prompt asks: "Does that mean it\'s unusable?"',
         'The answer is nuanced. The large constant baseload (DHW, kitchen) compresses the temperature signal. '
         'CV(RMSE) punishes models with high baseload-to-weather ratios. Students should discuss whether '
         'G14 is a bright line or a guideline, and what additional evidence supports the model.'),

        ('⚡ 3. NRA Discovery — The Data Center Expansion',
         'Day 2 late AM · Time Series tab',
         'Starting in month 8, reporting-period electric consumption jumps ~15,000–19,000 kWh/month above '
         'what the model predicts. Students see this as a step change in the Time Series tab.',
         'In the Savings Calculator, months 8–12 show red bars (negative savings). When students toggle '
         'the NRA adjustment on, the bars flip green. This is the visceral "aha" — without NRA, the project '
         'looks like it failed. With NRA, savings are real. Prompt: what evidence would you need?'),

        ('⚡ 4. Interactive Effects — Lighting ≠ Model',
         'Day 2 PM · Lighting Stipulation tab vs. Savings Calculator',
         'The lighting stipulation calculates ~258,000 kWh saved based on fixture counts and hours. '
         'But the whole-facility model shows different total savings.',
         'Why? Less lighting waste heat means less cooling load in summer (good) but more heating load in '
         'winter (bad). The whole-facility model captures these interactive effects; the stipulation does not. '
         'This motivates the exam topic of interactive effects and why whole-facility and retrofit isolation '
         'give different answers.'),

        ('⚡ 5. Fan Law Cubic Relationship',
         'Day 2 PM · VFD Analysis tab',
         'The Speed vs. Power scatter shows the classic cubic fan law. A 35% speed reduction yields ~73% '
         'power reduction. Students can toggle between AHUs to see consistent behavior.',
         'This motivates why VFDs are such effective ECMs and why continuous verification (not just pre/post '
         'spot measurement) is the right approach. The fan law also explains why small speed errors cause '
         'large power errors — a key uncertainty discussion.'),

        ('⚡ 6. Gas Went Up — Did the Retrofit Fail?',
         'Day 3 AM · Time Series tab (gas view) + Savings Calculator',
         'Reporting-year gas consumption is higher than baseline. Students initially think the roof insulation '
         '(ECM-3) made things worse.',
         'The model prediction (counterfactual) shows gas would have been even higher without the retrofit — '
         'the reporting year simply had colder weather. The purple prediction line sits above the green actual '
         'line, confirming positive savings. This is the entire point of counterfactual thinking.'),
    ]

    for title, timing, what, facilitation in moments:
        story.append(Paragraph(f'<b>{title}</b>', s['H3']))
        story.append(Paragraph(f'<i>{timing}</i>', s['Note']))
        story.append(Paragraph(f'<b>What happens:</b> {what}', s['BodySmall']))
        story.append(Paragraph(f'<b>Facilitation:</b> {facilitation}', s['BodySmall']))
        story.append(Spacer(1,6))

    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════
    # SECTION 3: MODULE-BY-MODULE FACILITATION
    # ═════════════════════════════════════════════════════════════════
    section_header('3 &nbsp; Module-by-Module Facilitation Notes')

    modules = [
        ('Module 0: Introduction', 'Day 1 AM',
         ['Distribute paper packets — have students write name on cover',
          'Project the capstone site Overview tab on screen',
          'Walk through the building graphic: 4 wings, HVAC assignments, ECM markers',
          'Emphasize this is an ESPC contract — savings are contractual obligations',
          'Ask: "Who are the stakeholders? What does each one care about?"']),

        ('Modules 1–2: Context &amp; Stakeholders', 'Day 1 AM',
         ['Worksheet 1A: stakeholder matrix. Students fill in interests and risks',
          'Cover all 4 risk domains: technical, commercial, legal, regulatory',
          'Discussion prompt: "What happens if M&amp;V shows zero savings?"',
          'Domain 9 (Contextual Considerations) — this is where it gets tested']),

        ('Module 3: Approaches &amp; Boundaries', 'Day 1 late AM',
         ['Worksheet 1B: measurement boundaries on single line diagram (paper packet)',
          'Worksheet 1C: approach selection for each ECM with justification',
          'Key decision: ECM-2 (chiller) — whole facility or retrofit isolation? Both are defensible',
          'ECM-1 lighting: stipulated hours or metered? Cost vs. accuracy tradeoff',
          'Domain 2 (Fundamental Approaches) — this is the primary touchpoint']),

        ('Interlude 3.1: Statistics Refresher', 'Day 1 PM',
         ['Open Statistics_Exercise.xlsm — population simulation, sampling, CV',
          'Open Descriptive_Stats_Step_1.xlsx — fixture wattage sampling exercise',
          'Then move to capstone Scatter Plots tab — "What do you see?"',
          'Optional: Least_Squares_Matrix_Formula.xlsx for advanced students',
          'Purpose: build vocabulary (R², CV(RMSE), NMBE) before Day 2 modeling']),

        ('Modules 4–5: Baseline Modeling', 'Day 2 AM',
         ['Model Fitting tab — students click Auto-Fit, record statistics in Worksheet 2A',
          'Then use manual sliders to explore alternative change points',
          '⚡ Teaching Moment 1: physics vs. statistics tradeoff',
          '⚡ Teaching Moment 2: gas CV(RMSE) fails G14',
          'Worksheet 2B: static factors inventory, NRA protocol',
          'Time Series tab: switch to gas view, then electric — find the NRA',
          '⚡ Teaching Moment 3: NRA discovery',
          'Domain 4 (Whole Facility) + Domain 8 (Modeling) + Domain 1 (Adjustments)']),

        ('Module 6: Retrofit Isolation', 'Day 2 PM',
         ['Lighting Stipulation tab — students verify 740 fixtures, edit hours, check totals vs. Worksheet 2C',
          '⚡ Teaching Moment 4: stipulation total ≠ whole-facility model savings',
          'VFD Analysis tab — select each AHU, observe fan law cubic',
          '⚡ Teaching Moment 5: fan law cubic relationship',
          'Worksheet 2D: design the VFD metering plan (what, where, how long, why)',
          'Domain 3 (Retrofit Isolation) + Domain 7 (Metering)']),

        ('Modules 7–8: M&amp;V Planning &amp; Metering', 'Day 3 AM',
         ['Worksheet 3A: M&amp;V plan assembly checklist — confirm all sections present',
          'OEH_M_V_planning_tool.xlsx: show the professional template (9 tabs)',
          'Discuss significant digits and rounding (Module 8.1)',
          'Discuss metering cost-benefit: how much M&amp;V is enough?',
          'Domain 5 (M&amp;V Planning) + Domain 7 (Metering)']),

        ('Module 9: Savings &amp; Reporting', 'Day 3 mid-AM',
         ['Savings Calculator tab — students record monthly savings in Worksheet 3B',
          '⚡ Teaching Moment 3 revisited: toggle NRA on/off, see bars flip',
          '⚡ Teaching Moment 6: gas went up — did the retrofit fail?',
          'Valuation section: apply rates ($0.105/kWh, $1.15/therm), calculate CO₂',
          'Fractional savings uncertainty at 90% confidence',
          'Domain 6 (Savings Reporting)']),

        ('Module 9 cont.: Defense', 'Day 3 PM',
         ['Worksheet 3C: prepare 5-minute presentation (4 sections)',
          'Each student presents; peers ask one challenge question',
          'Instructor challenges: "Why did you pick that change point?" '
          '"What if the data center expansion happened in month 3 instead?" '
          '"How would you explain negative gas savings to the county manager?"',
          'This is exam prep — every question maps to a domain']),
    ]

    for title, timing, bullets in modules:
        story.append(Paragraph(f'<b>{title}</b> &nbsp; <font color="#c47a2a"><i>{timing}</i></font>', s['H3']))
        for b in bullets:
            if b.startswith('⚡'):
                story.append(Paragraph(f'&bull; <font color="#c53030"><b>{b}</b></font>', s['BodySmall']))
            else:
                story.append(Paragraph(f'&bull; {b}', s['BodySmall']))
        story.append(Spacer(1,6))

    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════
    # SECTION 4: ANSWER SCAFFOLDING
    # ═════════════════════════════════════════════════════════════════
    section_header('4 &nbsp; Answer Scaffolding')
    story.append(Paragraph(
        'The capstone is designed with no single right answer — professional judgment is the point. '
        'Below are <b>defensible ranges</b> and key points to look for, not answer keys.',
        s['Body']))
    story.append(Spacer(1,6))

    scaff = [
        ['Worksheet','Key Points to Look For'],
        ['1A: Stakeholders','At least 4 stakeholders identified. Risk domains should include all 4 (T/C/L/R).\n'
         'County owner cares about budget certainty; ESCO cares about performance guarantee.'],
        ['1B: Boundaries','ECM-1 boundary at lighting circuits (Wings A & B). ECM-4 at individual AHU.\n'
         'Whole-facility boundary = utility meter. Students should note fuels: electric for all, gas for ECM-3.'],
        ['1C: Approaches','ECM-1: retrofit isolation / stipulated is standard. Some may argue for measured hours.\n'
         'ECM-2: either whole facility or retrofit isolation — both defensible with justification.\n'
         'ECM-3: whole facility (no way to isolate envelope). ECM-4: retrofit isolation / measured.'],
        ['2A: Baseline','Electric 5P model. Change points: 35–50°F (heating), 63–71°F (cooling).\n'
         'R² range: 0.65–0.91 depending on change points chosen. NMBE should be near 0.\n'
         'Gas model: 3P or 5P. CV(RMSE) around 16% — above G14 but defensible.'],
        ['2B: Static Factors','At least: occupancy, operating schedule, data center load, conditioned area.\n'
         'NRA trigger for data center: server count or IT load exceeds baseline +/- threshold.'],
        ['2C: Lighting','Total: ~258,000 kWh/yr (740 fixtures × ΔW × hours). Should match app calculation.\n'
         'Key judgment: annual hours per space. Students should cite building schedule as basis.'],
        ['2D: VFD Metering','Fan motor kW, speed (Hz or %), airflow (CFM), supply air temp.\n'
         'Pre-retrofit period: at least 2 weeks covering range of operating conditions.\n'
         'Meter types: CT-based power meter, VFD internal readout, pitot traverse or anemometer.'],
        ['3A: Plan Checklist','All 9 boxes checked. Schedule should show quarterly reporting.\n'
         'Budget for M&V should be 3–5% of project cost (industry rule of thumb).'],
        ['3B: Savings','With NRA: positive savings all 12 months. Without NRA: negative months 8–12.\n'
         'Total electric savings (with NRA): approximately 400,000–500,000 kWh/yr.\n'
         'CO₂ reduction: roughly 170–210 tonnes/yr (depends on NRA magnitude chosen).'],
        ['3C: Defense','Students should articulate: why this approach, how good the model is,\n'
         'what the NRA means, and what the final savings and uncertainty are.\n'
         'Challenge question readiness: at least 2 prepared responses.'],
    ]
    st = Table(scaff, colWidths=[1.2*inch, avail_w - 1.2*inch])
    st.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK),
        ('TEXTCOLOR',(0,0),(-1,0),white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('GRID',(0,0),(-1,-1),0.5,MEDIUM_GRAY),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT_GRAY]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('LEFTPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(st)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════
    # SECTION 5: COMPANION TOOLS & SITES
    # ═════════════════════════════════════════════════════════════════
    section_header('5 &nbsp; Companion Tools &amp; Interactive Sites')
    
    story.append(Paragraph('<b>Interactive Web Applications</b>', s['H2']))
    link_table([
        ('CMVP Capstone','https://cmvp-capstone.vercel.app',
         'This capstone — 7-tab workbench for Greenfield Municipal Center'),
        ('Counterfactual Designs','https://cfdesigns.vercel.app',
         'Full course: fundamentals, workbench, case studies, Bayesian intro'),
        ('IPMVP Translation','https://mv-course.vercel.app',
         'IPMVP-aligned M&V course with terminology crosswalk'),
        ('Learning Path','https://mv-classmap.vercel.app',
         'Progress tracker across all modules and sites'),
        ('Central Hub','https://counterfactual-designs.com',
         'Landing page linking all resources'),
    ])
    story.append(Spacer(1,10))

    story.append(Paragraph('<b>Companion Spreadsheets</b> (distribute electronically)', s['H2']))
    link_table([
        ('Statistics_Exercise.xlsm','(distribute to students)',
         'Population simulation, sampling, CV, sample size calculator. Day 1 PM.'),
        ('Descriptive_Stats_Step_1.xlsx','(distribute to students)',
         'Fixture wattage sampling → mean, variance, CV. Day 1 PM.'),
        ('Least_Squares_Matrix_Formula.xlsx','(optional — advanced students)',
         'OLS matrix algebra walkthrough (X\'X, β). Day 1 PM.'),
        ('OEH_M_V_planning_tool.xlsx','(reference — Day 3)',
         'Professional M&V plan template (9 tabs). Australian OEH format.'),
    ])
    story.append(Spacer(1,10))

    story.append(Paragraph('<b>Reference Documents</b>', s['H2']))
    link_table([
        ('CMVP Exam Scheme v1.2','(provided by AEE)',
         '9 domains, task weights, exam specifications. Open-book reference.'),
        ('CMVP Body of Knowledge v1.2.1','(provided by AEE)',
         'Study guide topics and references for all 9 domains.'),
        ('IPMVP Core Concepts (2022)','https://evo-world.org',
         'Free download from EVO. The foundational protocol.'),
        ('ASHRAE Guideline 14-2023','https://www.ashrae.org',
         'Measurement of Energy, Demand, and Water Savings. G14 criteria.'),
        ('Steve Kromer, The Role of the M&V Professional','https://elibrary.riverpublishers.com',
         'River Publishers, 2024. Course textbook.'),
    ])
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════
    # APPENDIX A: CURATED WEB LINKS
    # ═════════════════════════════════════════════════════════════════
    section_header('Appendix A &nbsp; Curated Web Links by Topic')
    story.append(Paragraph(
        'The following links are organized by topic for use as supplemental references during '
        'the course or for student self-study after the training.',
        s['Body']))
    story.append(Spacer(1,6))

    # ── Energy Efficiency & Building Performance ──
    story.append(Paragraph('<b>Energy Efficiency &amp; Building Performance</b>', s['H2']))
    link_table([
        ('Power of Existing Buildings',
         'https://www.amazon.com/Power-Existing-Buildings-Improve-Environmental/dp/164283050X',
         'Book on improving building efficiency (Amazon)'),
        ('Liftoff Energy — VPP',
         'https://edoenergy.com/blog/does-2025-pathways-to-commercial-liftoff-how-vpps-are-reshaping-utility-strategies/',
         'Virtual power plant resources and utility strategies'),
        ('Building Energy Score',
         'https://buildingenergyscore.energy.gov/buildings/5193',
         'DOE energy performance scoring tool'),
        ('ACEEE 2024 Summer Study',
         'https://www.aceee.org/2024-summer-study-energy-efficiency-buildings',
         'Energy efficiency in buildings research'),
        ('GHG Protocol',
         'https://ghgprotocol.org/',
         'Greenhouse gas accounting standards'),
        ('WattTime — Methodology',
         'https://watttime.org/data-science/methodology-validation/',
         'Energy data science methodology validation'),
        ('MRETS Tracking',
         'https://www.mrets.org/about/tracking/',
         'Renewable energy certificate tracking'),
        ('FlexValue (Recurve)',
         'https://flexvalue.recurve.com/',
         'Energy efficiency valuation platform'),
        ('DOE Life Cycle Cost',
         'https://www.energy.gov/femp/building-life-cycle-cost-programs',
         'FEMP building life cycle costing tools'),
        ('WattCarbon Blog',
         'https://blog.wattcarbon.com/',
         'Energy and carbon market insights'),
        ('RETScreen (NRCan)',
         'https://natural-resources.canada.ca/maps-tools-publications/tools-applications/retscreen',
         'Clean energy project analysis tool'),
    ])
    story.append(Spacer(1,10))

    # ── Statistics & Data Analysis ──
    story.append(Paragraph('<b>Statistics, Data Analysis &amp; Modeling</b>', s['H2']))
    link_table([
        ('Khan Academy — Statistics',
         'https://www.khanacademy.org/math/statistics-probability',
         'Free educational resource for stats fundamentals'),
        ('LINEST Function (Excel)',
         'https://support.microsoft.com/en-us/office/linest-function-84d7d0d9-6e50-4101-977a-fa7abf772b6d',
         'Excel regression function — used in multiple exercises'),
        ('TINV Function (Excel)',
         'https://support.microsoft.com/en-us/office/tinv-function-a7c85b9d-90f5-41fe-9ca5-1cd2f3e1ed7c',
         'Student-t inverse for confidence intervals'),
        ('Coefficient of Determination',
         'https://en.wikipedia.org/wiki/Coefficient_of_determination',
         'R² explanation (Wikipedia)'),
        ('Google CausalImpact',
         'https://google.github.io/CausalImpact/CausalImpact.html',
         'Bayesian causal inference tool for time series'),
        ('scikit-learn',
         'https://scikit-learn.org/stable/',
         'Python machine learning library'),
        ('Spurious Correlations',
         'https://tylervigen.com/spurious-correlations',
         'Humorous examples — great for teaching correlation ≠ causation'),
        ('Reimagine Energy — Code Tutorial',
         'https://reimagine.energy/',
         'Energy-related coding tutorials'),
        ('Chong — Calibration Models',
         'https://www.sciencedirect.com/science/article/pii/S0360132325008807',
         'Calibrating simulation models for M&V (academic paper)'),
    ])
    story.append(Spacer(1,10))

    # ── Standards & ESG ──
    story.append(Paragraph('<b>Environmental Standards &amp; ESG</b>', s['H2']))
    link_table([
        ('ISO 14064 — GHG Verification',
         'https://bit.ly/CMVP2024',
         'Greenhouse gas inventory verification standard'),
        ('ASHRAE Standards',
         'https://www.ashrae.org/technical-resources/standards-and-guidelines/read-only-versions-ofashrae-standards',
         'Read-only versions of ASHRAE standards'),
        ('GRESB Benchmark',
         'https://www.gresb.com/nl-en/benchmark-report/',
         'Real estate sustainability benchmarking'),
    ])
    story.append(Spacer(1,10))

    # ── Building Design & Engineering ──
    story.append(Paragraph('<b>Building Design &amp; Engineering Tools</b>', s['H2']))
    link_table([
        ('Carbon Craft Design',
         'https://www.carboncraftdesign.com/',
         'Sustainable design solutions'),
        ('Engineering Toolbox',
         'https://www.engineeringtoolbox.com/',
         'Engineering calculations reference'),
        ('IBPSA BEST Directory',
         'https://www.ibpsa.us/best-directory-list/',
         'Building performance simulation tools'),
        ('SkySpark for M&amp;V',
         'https://skyfoundry.com/file/337/Applying-SkySpark-for-MV-Using-the-Intl-Performance-MVProtocol.pdf',
         'Applying SkySpark for IPMVP-based M&V'),
        ('IES VE — Eaton House',
         'https://www.iesve.com/services/projects/4727/eatonhouse',
         'Digital twin / building simulation case study'),
        ('DOE Tools (ORNL)',
         'https://ornl-amo.github.io/',
         'Department of Energy modeling tools'),
    ])
    story.append(Spacer(1,10))

    # ── M&V Resources ──
    story.append(Paragraph('<b>Measurement &amp; Verification Resources</b>', s['H2']))
    link_table([
        ('BPA M&amp;V Sampling Guide',
         'https://www.bpa.gov/-/media/Aep/energy-efficiency/measurement-verification/2-bpa-mvsampling-reference-guide.pdf',
         'Bonneville Power sampling reference'),
        ('CEDMC EM&amp;V Forum',
         'https://cedmc.org/events/emv-forum/',
         'California energy measurement & verification forum'),
    ])
    story.append(Spacer(1,10))

    # ── Weather & Climate ──
    story.append(Paragraph('<b>Weather &amp; Climate Data</b>', s['H2']))
    link_table([
        ('OpenWeatherMap API',
         'https://openweathermap.org/api',
         'Weather data API for energy calculations'),
        ('DegreeDays.net',
         'https://degreedays.net/',
         'Degree day calculations for M&V'),
    ])
    story.append(Spacer(1,10))

    # ── Energy Markets ──
    story.append(Paragraph('<b>Energy Markets &amp; Grid</b>', s['H2']))
    link_table([
        ('CAISO Today\'s Outlook',
         'https://www.caiso.com/todays-outlook',
         'California ISO daily supply and demand'),
        ('CAISO Prices',
         'http://www.caiso.com/TodaysOutlook/Pages/prices.html',
         'Real-time California energy prices'),
        ('Grid Status Live',
         'https://www.gridstatus.io/live',
         'Live grid conditions across US ISOs'),
        ('AI Surge &amp; Coal Plants',
         'https://hothardware.com/news/ai-surge-causing-power-shortage-leading-coal-plants-to-stayopen',
         'AI data center energy demand impact'),
    ])
    story.append(Spacer(1,10))

    # ── Educational & Professional ──
    story.append(Paragraph('<b>Educational Resources &amp; Professional Networks</b>', s['H2']))
    link_table([
        ('Bloom\'s Taxonomy',
         'https://cft.vanderbilt.edu/wp-content/uploads/sites/59/Blooms-Taxonomy.pdf',
         'Learning framework (Vanderbilt)'),
        ('River Publishers eLibrary',
         'https://elibrary.riverpublishers.com/',
         'Academic resource library'),
        ('RMI Energy Modeling Summit',
         'https://rmi.org/wp-content/uploads/2017/05/RMI_Document_Repository_Public-Reprts_2011-21_BEMPre-read.pdf',
         'Building energy modeling pre-read'),
        ('CMVP LinkedIn Group',
         'https://www.linkedin.com/groups/7493688/',
         'Professional networking for CMVPs'),
        ('Adrien Devriendt (LinkedIn)',
         'https://www.linkedin.com/in/adriendevriendt/',
         'Energy M&V thought leader'),
    ])
    story.append(Spacer(1,10))

    # ── Research & Video ──
    story.append(Paragraph('<b>Research Methodology &amp; Video Content</b>', s['H2']))
    link_table([
        ('COS Preregistration',
         'https://www.cos.io/initiatives/prereg',
         'Research preregistration initiative'),
        ('Royal Society — Preregistration',
         'https://royalsociety.org/science-events-and-lectures/2024/03/preregistration/',
         'Preregistration in science event'),
        ('Phil Price — "Everything..."',
         'https://vimeo.com/144156352',
         'M&V video presentation (Vimeo)'),
        ('Andrej Karpathy',
         'https://www.youtube.com/@AndrejKarpathy',
         'AI/data science video channel'),
        ('Facility Condition Assessment',
         'https://en.wikipedia.org/wiki/Facility_condition_assessment',
         'Overview of facility assessment methods'),
    ])

    story.append(Spacer(1,0.5*inch))
    hr()
    story.append(Paragraph('CMVP Capstone Instructor Guide &bull; Greenfield Municipal Center &bull; Confidential',
        s['Footer']))

    # ── Build ────────────────────────────────────────────────────────
    doc.build(story)
    print(f'PDF created: {outpath}')

if __name__ == '__main__':
    build()
