"""
Create the final PDF organized by CISSP Domain -> Sub-Section
with complete questions, options, answers, and explanations.
"""
import json
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def clean_for_pdf(text):
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

def natural_sort_key(s):
    """Sort section IDs: 1.1, 1.2, ..., 1.12, 2.1, ..., 8.5, unclassified"""
    if s == "unclassified":
        return (999, 0)
    parts = s.split(".")
    return (int(parts[0]), int(parts[1]))

def create_subsection_pdf():
    print("Loading sub-section organized data...")
    with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\subsection_organized_questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    total = data["metadata"]["total_questions"]
    missing = data["metadata"]["missing_explanations"]
    unmatched = data["metadata"]["unmatched_questions"]
    
    print(f"Total: {total} | Missing expl: {missing} | Unmatched: {unmatched}")
    
    pdf_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\CISSP_Questions_by_Subsection.pdf"
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                          rightMargin=40, leftMargin=40,
                          topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    
    # === STYLES ===
    title_s = ParagraphStyle('MTitle', parent=styles['Heading1'],
                            fontSize=20, spaceAfter=12, alignment=TA_CENTER,
                            textColor=colors.HexColor('#1a3a5c'))
    
    subtitle_s = ParagraphStyle('MSub', parent=styles['Normal'],
                               fontSize=10, alignment=TA_CENTER, spaceAfter=8,
                               textColor=colors.HexColor('#666666'))
    
    domain_s = ParagraphStyle('DomainH', parent=styles['Heading2'],
                             fontSize=14, spaceBefore=16, spaceAfter=4,
                             textColor=colors.white, backColor=colors.HexColor('#1f4e79'),
                             borderPadding=(6, 6, 6, 6))
    
    section_s = ParagraphStyle('SectionH', parent=styles['Heading3'],
                              fontSize=12, spaceBefore=10, spaceAfter=3,
                              textColor=colors.HexColor('#2e75b6'),
                              leftIndent=8, fontName='Helvetica-Bold')
    
    section_desc_s = ParagraphStyle('SectionDesc', parent=styles['Normal'],
                                   fontSize=8, spaceBefore=1, spaceAfter=4,
                                   leftIndent=20, textColor=colors.HexColor('#888888'))
    
    qnum_s = ParagraphStyle('QNum', parent=styles['Normal'],
                           fontSize=9, spaceBefore=6, spaceAfter=1,
                           textColor=colors.HexColor('#1a3a5c'), fontName='Helvetica-Bold')
    
    qtext_s = ParagraphStyle('QText', parent=styles['Normal'],
                            fontSize=8, spaceBefore=0, spaceAfter=2,
                            leftIndent=10, textColor=colors.HexColor('#222222'))
    
    opt_s = ParagraphStyle('Option', parent=styles['Normal'],
                          fontSize=8, spaceBefore=0, spaceAfter=0,
                          leftIndent=20, textColor=colors.HexColor('#333333'))
    
    ans_s = ParagraphStyle('Answer', parent=styles['Normal'],
                          fontSize=8, spaceBefore=3, spaceAfter=1,
                          leftIndent=10, textColor=colors.HexColor('#006600'),
                          fontName='Helvetica-Bold')
    
    expl_s = ParagraphStyle('Expl', parent=styles['Normal'],
                           fontSize=7, spaceBefore=1, spaceAfter=4,
                           leftIndent=16, textColor=colors.HexColor('#666666'))
    
    noexpl_s = ParagraphStyle('NoExpl', parent=styles['Normal'],
                             fontSize=7, spaceBefore=1, spaceAfter=4,
                             leftIndent=10, textColor=colors.HexColor('#cc6600'))
    
    tbl_hdr_s = ParagraphStyle('TblHdr', parent=styles['Normal'],
                               fontSize=9, textColor=colors.white,
                               fontName='Helvetica-Bold', alignment=TA_CENTER)
    
    tbl_cell_s = ParagraphStyle('TblCell', parent=styles['Normal'],
                               fontSize=8, textColor=colors.HexColor('#333333'))
    
    content = []
    
    # === TITLE PAGE ===
    content.append(Spacer(1, 35))
    content.append(Paragraph("CISSP CERTIFICATION EXAM", title_s))
    content.append(Paragraph("Complete Question Bank with Answers &amp; Explanations", subtitle_s))
    content.append(Paragraph(f"Organized by Domain &amp; Sub-Section<br/>"
                            f"Official ISC2 CISSP Exam Outline (April 15, 2024)",
                            ParagraphStyle('S2', parent=styles['Normal'],
                                          fontSize=10, alignment=TA_CENTER, spaceAfter=6)))
    content.append(Paragraph(f"{total} Questions | 8 Domains | {len(data['sections'])} Sub-Sections",
                            ParagraphStyle('S3', parent=styles['Normal'],
                                          fontSize=9, alignment=TA_CENTER, spaceAfter=10)))
    
    content.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor('#1f4e79')))
    content.append(Spacer(1, 10))
    
    # Quality note
    pct_matched = 100 - unmatched/total*100
    content.append(Paragraph(
        f"<b>Classification Quality:</b> {pct_matched:.1f}% of questions matched to sub-sections. "
        f"{unmatched} questions are listed as 'Unclassified' at the end. "
        f"{missing} questions ({missing/total*100:.1f}%) lack explanations in the source material.",
        ParagraphStyle('Note', parent=styles['Normal'], fontSize=8, spaceAfter=12,
                      textColor=colors.HexColor('#888888'))
    ))
    
    # Table of contents
    content.append(Paragraph("TABLE OF CONTENTS", ParagraphStyle(
        'TOC', parent=styles['Heading2'], fontSize=12, spaceAfter=8, alignment=TA_CENTER)))
    
    toc_rows = [['Domain / Section', 'Topic', 'Questions']]
    
    outline = data["outline"]
    sections = data["sections"]
    
    for dom_num in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        dom_info = outline[dom_num]
        dom_name = dom_info["name"]
        dom_weight = dom_info["weight"]
        
        # Count domain total
        dom_total = sum(
            len(sections.get(sid, {}).get("questions", []))
            for sid in sections
            if sid.startswith(dom_num + ".")
        )
        
        toc_rows.append([f"DOMAIN {dom_num}: {dom_name} ({dom_weight})", "", str(dom_total)])
        
        for sec_id, sec_name in dom_info["sections"].items():
            sec_count = len(sections.get(sec_id, {}).get("questions", []))
            toc_rows.append([f"  {sec_id}", sec_name, str(sec_count)])
    
    # Unclassified row
    uc_count = len(sections.get("unclassified", {}).get("questions", []))
    if uc_count > 0:
        toc_rows.append(["  Unclassified", "Questions with no keyword match", str(uc_count)])
    
    toc_rows.append(["TOTAL", "", str(total)])
    
    toc_table = Table(toc_rows, colWidths=[1.5*inch, 3.2*inch, 0.8*inch])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#cccccc')),
        # Bold domain rows
        ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
        # Highlight domain rows
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e8edf2')),
        ('BACKGROUND', (0, 14), (-1, 14), colors.HexColor('#e8edf2')),
        ('BACKGROUND', (0, 24), (-1, 24), colors.HexColor('#e8edf2')),
        ('BACKGROUND', (0, 28), (-1, 28), colors.HexColor('#e8edf2')),
        ('BACKGROUND', (0, 35), (-1, 35), colors.HexColor('#e8edf2')),
        ('BACKGROUND', (0, 40), (-1, 40), colors.HexColor('#e8edf2')),
        ('BACKGROUND', (0, 56), (-1, 56), colors.HexColor('#e8edf2')),
        # Total row
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#1f4e79')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
    ]))
    
    content.append(toc_table)
    content.append(PageBreak())
    
    # === DOMAIN SECTIONS ===
    for dom_num in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        dom_info = outline[dom_num]
        dom_name = dom_info["name"]
        dom_weight = dom_info["weight"]
        
        content.append(Paragraph(f"DOMAIN {dom_num}: {dom_name} ({dom_weight})", domain_s))
        content.append(Spacer(1, 4))
        
        # Process each sub-section
        for sec_id, sec_name in dom_info["sections"].items():
            if sec_id not in sections:
                content.append(Paragraph(f"{sec_id} {sec_name}", section_s))
                content.append(Paragraph("No questions classified to this sub-section.", section_desc_s))
                continue
            
            sec_data = sections[sec_id]
            sec_qs = sec_data.get("questions", [])
            
            content.append(Paragraph(f"{sec_id} {sec_name}", section_s))
            content.append(Paragraph(f"{len(sec_qs)} questions", section_desc_s))
            
            for i, q in enumerate(sec_qs):
                qnum = q["question_number"]
                topic = q["original_topic"]
                
                content.append(Paragraph(f"Q{qnum} (Topic {topic})", qnum_s))
                
                qt = clean_for_pdf(q.get("question_text", ""))[:600]
                content.append(Paragraph(qt, qtext_s))
                
                for opt in q.get("options", []):
                    ot = clean_for_pdf(opt["text"])[:250]
                    content.append(Paragraph(f"<b>{opt['letter']}.</b> {ot}", opt_s))
                
                if q.get("answer"):
                    content.append(Paragraph(f"<b>Answer: {q['answer']}</b>", ans_s))
                
                if q.get("has_explanation") and q.get("explanation"):
                    expl = clean_for_pdf(q["explanation"])
                    if len(expl) > 800:
                        expl = expl[:800] + "..."
                    content.append(Paragraph(expl, expl_s))
                else:
                    content.append(Paragraph("[No explanation in source]", noexpl_s))
                
                content.append(HRFlowable(width="95%", thickness=0.2, color=colors.HexColor('#eeeeee'),
                                          spaceBefore=2, spaceAfter=2))
                
                # Page break every 12 questions
                if (i + 1) % 12 == 0 and i < len(sec_qs) - 1:
                    content.append(PageBreak())
            
            content.append(Spacer(1, 4))
        
        content.append(PageBreak())
    
    # === UNCLASSIFIED SECTION ===
    if "unclassified" in sections and sections["unclassified"].get("questions"):
        uc_data = sections["unclassified"]
        uc_qs = uc_data["questions"]
        
        content.append(Paragraph("UNCLASSIFIED QUESTIONS", domain_s))
        content.append(Paragraph(f"These {len(uc_qs)} questions could not be automatically matched to a specific sub-section. "
                                f"They are listed here for manual review.", section_desc_s))
        content.append(Spacer(1, 6))
        
        for i, q in enumerate(uc_qs):
            qnum = q["question_number"]
            ot = q.get('original_topic', '?')
            content.append(Paragraph(f"Q{qnum} (Topic {ot})", qnum_s))
            
            qt = clean_for_pdf(q.get("question_text", ""))[:500]
            content.append(Paragraph(qt, qtext_s))
            
            for opt in q.get("options", []):
                content.append(Paragraph(f"<b>{opt['letter']}.</b> {clean_for_pdf(opt['text'])[:200]}", opt_s))
            
            if q.get("answer"):
                content.append(Paragraph(f"<b>Answer: {q['answer']}</b>", ans_s))
            
            if q.get("has_explanation") and q.get("explanation"):
                content.append(Paragraph(clean_for_pdf(q["explanation"])[:600], expl_s))
            
            content.append(HRFlowable(width="95%", thickness=0.2, color=colors.HexColor('#eeeeee'),
                                      spaceBefore=2, spaceAfter=2))
    
    # Build
    print(f"Building PDF with {total} questions across {len(data['sections'])} sub-sections...")
    try:
        doc.build(content)
        import os
        size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        print(f"\nPDF created: {pdf_path}")
        print(f"File size: {size_mb:.1f} MB")
        return True
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_subsection_pdf()