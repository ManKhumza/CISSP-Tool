"""
Create FINAL CORRECTED PDF using DOMAIN-LEVEL organization only.
This is the accurate version - sub-section classification was found to be unreliable.
"""
import json
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

def clean_for_pdf(text):
    if not text: return ""
    return (text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
               .replace('\u2019',"'").replace('\u201c','"').replace('\u201d','"'))

def create_final_corrected_pdf():
    with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\corrected_questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    total = data["metadata"]["total_questions"]
    missing = data["metadata"]["missing_explanations"]
    
    pdf_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\CISSP_Final_Corrected.pdf"
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    # Styles
    title_s = ParagraphStyle('T', parent=styles['Heading1'], fontSize=20, spaceAfter=12, alignment=TA_CENTER, textColor=colors.HexColor('#1a3a5c'))
    subtitle_s = ParagraphStyle('ST', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, spaceAfter=8, textColor=colors.HexColor('#666666'))
    domain_s = ParagraphStyle('DH', parent=styles['Heading2'], fontSize=14, spaceBefore=16, spaceAfter=4, textColor=colors.white, backColor=colors.HexColor('#1f4e79'), borderPadding=(6,6,6,6))
    info_s = ParagraphStyle('INFO', parent=styles['Normal'], fontSize=8, spaceAfter=4, textColor=colors.HexColor('#888888'))
    qnum_s = ParagraphStyle('QN', parent=styles['Normal'], fontSize=9, spaceBefore=6, spaceAfter=1, textColor=colors.HexColor('#1a3a5c'), fontName='Helvetica-Bold')
    qtext_s = ParagraphStyle('QT', parent=styles['Normal'], fontSize=8, spaceBefore=0, spaceAfter=2, leftIndent=10, textColor=colors.HexColor('#222222'))
    opt_s = ParagraphStyle('OPT', parent=styles['Normal'], fontSize=8, spaceBefore=0, spaceAfter=0, leftIndent=20, textColor=colors.HexColor('#333333'))
    ans_s = ParagraphStyle('ANS', parent=styles['Normal'], fontSize=8, spaceBefore=3, spaceAfter=1, leftIndent=10, textColor=colors.HexColor('#006600'), fontName='Helvetica-Bold')
    expl_s = ParagraphStyle('EXP', parent=styles['Normal'], fontSize=7, spaceBefore=1, spaceAfter=4, leftIndent=16, textColor=colors.HexColor('#666666'))
    noexpl_s = ParagraphStyle('NOEX', parent=styles['Normal'], fontSize=7, spaceBefore=1, spaceAfter=4, leftIndent=10, textColor=colors.HexColor('#cc6600'))
    
    content = []
    
    # Title page
    content.append(Spacer(1, 30))
    content.append(Paragraph("CISSP CERTIFICATION EXAM", title_s))
    content.append(Paragraph("Complete Question Bank — Organized by Domain", subtitle_s))
    content.append(Paragraph(f"{total} Questions | 8 Domains | {100-missing/total*100:.0f}% with explanations", 
                            ParagraphStyle('S3', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, spaceAfter=10)))
    content.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor('#1f4e79')))
    content.append(Spacer(1, 10))
    
    # IMPORTANT NOTE ABOUT SUB-SECTIONS
    content.append(Paragraph("<b>NOTE ON STRUCTURE:</b>", 
                            ParagraphStyle('NH', parent=styles['Normal'], fontSize=9, spaceAfter=4, fontName='Helvetica-Bold')))
    content.append(Paragraph(
        "This document organizes questions by the 8 official CISSP domains. "
        "A deeper sub-section level (1.1, 1.2, etc.) was attempted but found to be unreliable — "
        "keyword-based classification cannot accurately distinguish between overlapping CISSP topics "
        "(e.g., 'authentication' spans both cryptography and access control). "
        "Use the domain headings below as your primary study navigation.",
        ParagraphStyle('NB', parent=styles['Normal'], fontSize=8, spaceAfter=12, textColor=colors.HexColor('#888888'))
    ))
    
    # Domain summary table
    content.append(Paragraph("Domain Summary", ParagraphStyle('DS', parent=styles['Heading3'], fontSize=12, alignment=TA_CENTER, spaceAfter=8)))
    
    weights = {"1":"15%","2":"10%","3":"13%","4":"13%","5":"13%","6":"12%","7":"13%","8":"11%"}
    rows = [['Domain','Name','Questions','Missing Expl.','Weight']]
    
    for dk in sorted(data["domains"].keys(), key=lambda x:int(x.split("_")[1])):
        d = data["domains"][dk]
        num = dk.split("_")[1]
        name = d["name"].split(": ")[1] if ": " in d["name"] else d["name"]
        rows.append([f"D{num}", name, str(d["question_count"]), str(d["missing_explanations"]), weights.get(num,"")])
    
    rows.append(['','TOTAL',str(total),str(missing),''])
    
    tbl = Table(rows, colWidths=[0.5*inch, 2.8*inch, 0.8*inch, 0.8*inch, 0.6*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1f4e79')),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(0,0),(0,-1),'CENTER'),
        ('ALIGN',(2,0),(-1,-1),'CENTER'),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor('#f0f5fa')]),
        ('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),
        ('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#1f4e79')),
        ('TEXTCOLOR',(0,-1),(-1,-1),colors.white),
    ]))
    content.append(tbl)
    content.append(PageBreak())
    
    # Domain sections
    for dk in sorted(data["domains"].keys(), key=lambda x:int(x.split("_")[1])):
        d = data["domains"][dk]
        num = dk.split("_")[1]
        name = d["name"].split(": ")[1] if ": " in d["name"] else d["name"]
        qs = d["questions"]
        
        content.append(Paragraph(f"DOMAIN {num}: {name} ({weights.get(num,'')})", domain_s))
        content.append(Paragraph(f"{len(qs)} questions | {d['missing_explanations']} without explanation", info_s))
        content.append(Spacer(1, 6))
        
        for i, q in enumerate(qs):
            content.append(Paragraph(f"Q{q['question_number']}", qnum_s))
            qt = clean_for_pdf(q.get("question_text",""))[:600]
            content.append(Paragraph(qt, qtext_s))
            
            for opt in q.get("options",[]):
                ot = clean_for_pdf(opt["text"])[:250]
                content.append(Paragraph(f"<b>{opt['letter']}.</b> {ot}", opt_s))
            
            if q.get("answer"):
                content.append(Paragraph(f"<b>Answer: {q['answer']}</b>", ans_s))
            
            if q.get("has_explanation") and q.get("explanation"):
                expl = clean_for_pdf(q["explanation"])
                if len(expl)>800: expl = expl[:800]+"..."
                content.append(Paragraph(expl, expl_s))
            else:
                content.append(Paragraph("[No explanation in source]", noexpl_s))
            
            content.append(HRFlowable(width="95%",thickness=0.2,color=colors.HexColor('#eeeeee'),spaceBefore=2,spaceAfter=2))
            
            if (i+1)%12==0 and i<len(qs)-1:
                content.append(PageBreak())
        
        if dk != list(data["domains"].keys())[-1]:
            content.append(PageBreak())
    
    print(f"Building final corrected PDF...")
    try:
        doc.build(content)
        import os
        size_mb = os.path.getsize(pdf_path)/(1024*1024)
        print(f"\nCreated: {pdf_path}")
        print(f"Size: {size_mb:.1f} MB")
        return True
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_final_corrected_pdf()
