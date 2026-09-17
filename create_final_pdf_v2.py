"""
Create the final corrected PDF with complete questions, options, answers, and explanations.
Uses the corrected_questions.json data.
"""
import json
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, 
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def clean_for_pdf(text):
    """Escape XML and clean text for PDF rendering"""
    if not text:
        return ""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('\u2019', "'")
    text = text.replace('\u2018', "'")
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    text = text.replace('\u2013', '-')
    text = text.replace('\u2014', '--')
    return text

def create_final_pdf():
    print("Loading corrected questions data...")
    with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\corrected_questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    total = data["metadata"]["total_questions"]
    missing = data["metadata"]["missing_explanations"]
    
    print(f"Total questions: {total}")
    print(f"Missing explanations: {missing} ({missing/total*100:.1f}%)")
    
    pdf_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\CISSP_Complete_Questions_Organized.pdf"
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                          rightMargin=45, leftMargin=45,
                          topMargin=45, bottomMargin=45)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_s = ParagraphStyle('Title2', parent=styles['Heading1'],
                            fontSize=20, spaceAfter=15, alignment=TA_CENTER,
                            textColor=colors.HexColor('#1a3a5c'))
    
    domain_s = ParagraphStyle('DomainH', parent=styles['Heading2'],
                             fontSize=14, spaceBefore=12, spaceAfter=6,
                             textColor=colors.white, backColor=colors.HexColor('#2c5f8a'),
                             borderPadding=(6, 6, 6, 6))
    
    qnum_s = ParagraphStyle('QNum', parent=styles['Normal'],
                           fontSize=10, spaceBefore=8, spaceAfter=2,
                           textColor=colors.HexColor('#1a3a5c'), fontName='Helvetica-Bold')
    
    qtext_s = ParagraphStyle('QText', parent=styles['Normal'],
                            fontSize=9, spaceBefore=1, spaceAfter=3,
                            leftIndent=12, textColor=colors.HexColor('#222222'))
    
    opt_s = ParagraphStyle('Option', parent=styles['Normal'],
                          fontSize=9, spaceBefore=0, spaceAfter=0,
                          leftIndent=24, textColor=colors.HexColor('#333333'))
    
    ans_s = ParagraphStyle('Answer', parent=styles['Normal'],
                          fontSize=9, spaceBefore=4, spaceAfter=2,
                          leftIndent=12, textColor=colors.HexColor('#006600'),
                          fontName='Helvetica-Bold')
    
    expl_s = ParagraphStyle('Expl', parent=styles['Normal'],
                           fontSize=8, spaceBefore=2, spaceAfter=6,
                           leftIndent=18, textColor=colors.HexColor('#555555'))
    
    info_s = ParagraphStyle('Info', parent=styles['Normal'],
                           fontSize=8, spaceAfter=4, textColor=colors.HexColor('#888888'))
    
    noexpl_s = ParagraphStyle('NoExpl', parent=styles['Normal'],
                             fontSize=8, spaceBefore=2, spaceAfter=6,
                             leftIndent=12, textColor=colors.HexColor('#cc6600'),
                             fontName='Helvetica-Oblique')
    
    content = []
    
    # --- TITLE PAGE ---
    content.append(Spacer(1, 40))
    content.append(Paragraph("CISSP CERTIFICATION EXAM", title_s))
    content.append(Paragraph("Complete Questions with Answers &amp; Explanations", 
                            ParagraphStyle('Sub', parent=styles['Heading2'],
                                          fontSize=13, alignment=TA_CENTER, spaceAfter=8,
                                          textColor=colors.HexColor('#4a7fb5'))))
    content.append(Paragraph(f"Organized by Domain | {total} Questions",
                            ParagraphStyle('Sub2', parent=styles['Normal'],
                                          fontSize=10, alignment=TA_CENTER, spaceAfter=15)))
    
    content.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor('#2c5f8a')))
    content.append(Spacer(1, 15))
    
    # Accuracy note
    content.append(Paragraph(
        f"<b>Quality Note:</b> {total-missing} of {total} questions ({100-missing/total*100:.1f}%) include "
        f"complete explanations. {missing} questions ({missing/total*100:.1f}%) lack explanations in the "
        f"original source material and are marked accordingly.",
        ParagraphStyle('Note', parent=styles['Normal'], fontSize=9, spaceAfter=10,
                      textColor=colors.HexColor('#666666'))
    ))
    
    # Domain summary table
    content.append(Paragraph("Domain Distribution", ParagraphStyle(
        'TblTitle', parent=styles['Heading3'], fontSize=12, alignment=TA_CENTER, spaceAfter=8)))
    
    table_rows = [['Domain', 'Name', 'Questions', 'Missing Expl.']]
    domain_weights = {
        "Domain 1: Security and Risk Management": "15%",
        "Domain 2: Asset Security": "10%",
        "Domain 3: Security Architecture and Engineering": "13%",
        "Domain 4: Communication and Network Security": "13%",
        "Domain 5: Identity and Access Management (IAM)": "13%",
        "Domain 6: Security Assessment and Testing": "12%",
        "Domain 7: Security Operations": "13%",
        "Domain 8: Software Development Security": "11%"
    }
    
    for dk in sorted(data["domains"].keys(), key=lambda x: int(x.split("_")[1])):
        d = data["domains"][dk]
        name = d["name"]
        short = name.split(": ")[1] if ": " in name else name
        dom_num = dk.split("_")[1]
        qc = d["question_count"]
        me = d["missing_explanations"]
        weight = domain_weights.get(name, "")
        table_rows.append([f"Domain {dom_num}", f"{short} ({weight})", str(qc), str(me)])
    
    # Total row
    table_rows.append(['', 'TOTAL', str(total), str(missing)])
    
    col_widths = [0.9*inch, 3.2*inch, 0.8*inch, 0.8*inch]
    table = Table(table_rows, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5f8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f0f5fa')]),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8edf2')),
    ]))
    
    content.append(table)
    content.append(PageBreak())
    
    # --- DOMAIN SECTIONS ---
    for dk in sorted(data["domains"].keys(), key=lambda x: int(x.split("_")[1])):
        d = data["domains"][dk]
        name = d["name"]
        dom_num = dk.split("_")[1]
        short = name.split(": ")[1] if ": " in name else name
        questions = d["questions"]
        weight = domain_weights.get(name, "")
        
        # Domain header
        content.append(Paragraph(f"Domain {dom_num}: {short}", domain_s))
        content.append(Paragraph(f"Questions: {len(questions)} | Exam Weight: {weight} | Missing Explanations: {d['missing_explanations']}", info_s))
        content.append(Spacer(1, 6))
        
        for i, q in enumerate(questions):
            qnum = q["question_number"]
            topic = q["original_topic"]
            
            # Question number
            content.append(Paragraph(f"Q{qnum} (Topic {topic})", qnum_s))
            
            # Question text
            qt = clean_for_pdf(q["question_text"]) if q["question_text"] else "[Question text not extractable]"
            content.append(Paragraph(qt[:600], qtext_s))
            
            # Options
            for opt in q.get("options", []):
                opt_text = clean_for_pdf(opt["text"])[:300]
                content.append(Paragraph(f"<b>{opt['letter']}.</b> {opt_text}", opt_s))
            
            # Answer
            if q.get("answer"):
                content.append(Paragraph(f"<b>Answer: {q['answer']}</b>", ans_s))
            
            # Explanation
            if q.get("has_explanation") and q.get("explanation"):
                expl = clean_for_pdf(q["explanation"])
                # Truncate very long explanations
                if len(expl) > 1000:
                    expl = expl[:1000] + "..."
                content.append(Paragraph(f"{expl}", expl_s))
            else:
                content.append(Paragraph("[No explanation available in source document]", noexpl_s))
            
            # Divider
            content.append(HRFlowable(width="95%", thickness=0.3, color=colors.HexColor('#dddddd'),
                                      spaceBefore=3, spaceAfter=3))
            
            # Page break every 10 questions
            if (i + 1) % 10 == 0 and i < len(questions) - 1:
                content.append(PageBreak())
        
        # Domain separator
        if dk != list(data["domains"].keys())[-1]:
            content.append(PageBreak())
    
    # Build
    print(f"Building PDF (this may take a while with {total} questions)...")
    try:
        doc.build(content)
        print(f"\nPDF created: {pdf_path}")
        
        import os
        size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        print(f"File size: {size_mb:.1f} MB")
        return True
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_final_pdf()