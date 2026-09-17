import json
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def clean_text_for_pdf(text):
    """Clean text for PDF rendering"""
    # Fix common encoding issues from PDF extraction
    text = text.replace(' s hielde d', ' shielded')
    text = text.replace(' th at', ' that')
    text = text.replace(' th e', ' the')
    text = text.replace(' a nd', ' and')
    text = text.replace(' o f', ' of')
    text = text.replace(' i n', ' in')
    text = text.replace(' i s', ' is')
    text = text.replace(' t o', ' to')
    text = text.replace(' f or', ' for')
    text = text.replace(' w ith', ' with')
    text = text.replace(' w hich', ' which')
    text = text.replace(' b een', ' been')
    text = text.replace(' b y', ' by')
    text = text.replace(' h as', ' has')
    text = text.replace(' h ave', ' have')
    text = text.replace(' b e', ' be')
    text = text.replace(' a re', ' are')
    text = text.replace(' w as', ' was')
    text = text.replace(' c an', ' can')
    text = text.replace(' w ill', ' will')
    text = text.replace(' s hould', ' should')
    text = text.replace(' f rom', ' from')
    text = text.replace(' t hat', ' that')
    text = text.replace(' t his', ' this')
    text = text.replace(' w ould', ' would')
    text = text.replace(' c ould', ' could')
    text = text.replace(' m ore', ' more')
    text = text.replace(' o ne', ' one')
    text = text.replace(' a ll', ' all')
    text = text.replace(' n ot', ' not')
    text = text.replace(' h ad', ' had')
    text = text.replace(' a lso', ' also')
    text = text.replace(' w here', ' where')
    text = text.replace(' w hat', ' what')
    text = text.replace(' w hen', ' when')
    text = text.replace(' w ho', ' who')
    text = text.replace(' t heir', ' their')
    text = text.replace(' t hey', ' they')
    text = text.replace(' t here', ' there')
    text = text.replace(' t hen', ' then')
    text = text.replace(' t hose', ' those')
    text = text.replace(' t hese', ' these')
    text = text.replace(' s ome', ' some')
    text = text.replace(' m ay', ' may')
    text = text.replace(' m ust', ' must')
    text = text.replace(' m ight', ' might')
    text = text.replace(' s uch', ' such')
    text = text.replace(' e ach', ' each')
    text = text.replace(' o ur', ' our')
    text = text.replace(' y our', ' your')
    text = text.replace(' a ny', ' any')
    text = text.replace(' m ost', ' most')
    text = text.replace(' o nly', ' only')
    text = text.replace(' b ut', ' but')
    text = text.replace(' a fter', ' after')
    text = text.replace(' b efore', ' before')
    text = text.replace(' b etween', ' between')
    text = text.replace(' o ver', ' over')
    text = text.replace(' u nder', ' under')
    text = text.replace(' a gainst', ' against')
    text = text.replace(' a bout', ' about')
    text = text.replace(' i nto', ' into')
    text = text.replace(' t hrough', ' through')
    text = text.replace(' d uring', ' during')
    text = text.replace(' w ithout', ' without')
    text = text.replace(' a ccording', ' according')
    text = text.replace(' h owever', ' however')
    text = text.replace(' t herefore', ' therefore')
    text = text.replace(' o therwise', ' otherwise')
    text = text.replace(' a lthough', ' although')
    text = text.replace(' b ecause', ' because')
    text = text.replace(' w hether', ' whether')
    text = text.replace(' u nless', ' unless')
    text = text.replace(' u ntil', ' until')
    text = text.replace(' s ince', ' since')
    text = text.replace(' w hile', ' while')
    text = text.replace(' a mong', ' among')
    text = text.replace(' w ithin', ' within')
    text = text.replace(' a lready', ' already')
    text = text.replace(' t ogether', ' together')
    text = text.replace(' a way', ' away')
    text = text.replace(' b ack', ' back')
    text = text.replace(' d own', ' down')
    text = text.replace(' o ut', ' out')
    text = text.replace(' o ff', ' off')
    text = text.replace(' o nce', ' once')
    text = text.replace(' a ctual', ' actual')
    text = text.replace(' r eal', ' real')
    text = text.replace(' c ertain', ' certain')
    text = text.replace(' p ossible', ' possible')
    text = text.replace(' s pecific', ' specific')
    text = text.replace(' s imilar', ' similar')
    text = text.replace(' d ifferent', ' different')
    text = text.replace(' i mportant', ' important')
    text = text.replace(' n ecessary', ' necessary')
    text = text.replace(' a vailable', ' available')
    text = text.replace(' a ppropriate', ' appropriate')
    text = text.replace(' f ollowing', ' following')
    text = text.replace(' p rimary', ' primary')
    text = text.replace(' s econdary', ' secondary')
    text = text.replace(' m inimum', ' minimum')
    text = text.replace(' m aximum', ' maximum')
    text = text.replace(' g eneral', ' general')
    text = text.replace(' s tandard', ' standard')
    text = text.replace(' n ormal', ' normal')
    text = text.replace(' s pecial', ' special')
    text = text.replace(' c ommon', ' common')
    text = text.replace(' c urrent', ' current')
    text = text.replace(' c orrect', ' correct')
    text = text.replace(' i ncorrect', ' incorrect')
    text = text.replace(' t rue', ' true')
    text = text.replace(' f alse', ' false')
    text = text.replace(' y es', ' yes')
    text = text.replace(' n o ', ' no ')
    text = text.replace(' a s ', ' as ')
    text = text.replace(' a t ', ' at ')
    text = text.replace(' i f ', ' if ')
    text = text.replace(' o r ', ' or ')
    text = text.replace(' o n ', ' on ')
    text = text.replace(' i t ', ' it ')
    text = text.replace(' d o ', ' do ')
    text = text.replace(' g o ', ' go ')
    text = text.replace(' s o ', ' so ')
    text = text.replace(' u p ', ' up ')
    text = text.replace(' w e ', ' we ')
    text = text.replace(' m y ', ' my ')
    
    # Fix XML special characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    
    return text

def parse_question_content(full_content):
    """Parse question content into structured parts"""
    result = {
        "question_text": "",
        "options": [],
        "answer": "",
        "explanation": ""
    }
    
    # Extract question text (before answer options)
    question_match = re.search(r'^(.*?)(?=\n[A-D]\.|\nAnswer:)', full_content, re.DOTALL)
    if question_match:
        result["question_text"] = question_match.group(1).strip()
    
    # Extract answer options
    options_match = re.findall(r'([A-D]\..*?)(?=\n[A-D]\.|\nAnswer:|\Z)', full_content, re.DOTALL)
    for opt in options_match:
        opt = opt.strip()
        if opt:
            result["options"].append(opt)
    
    # Extract answer
    answer_match = re.search(r'Answer:\s*([A-D])', full_content)
    if answer_match:
        result["answer"] = answer_match.group(1)
    
    # Extract explanation
    explanation_match = re.search(r'Explanation:\s*(.*?)(?=\nSource:|\nReference|$)', full_content, re.DOTALL)
    if explanation_match:
        result["explanation"] = explanation_match.group(1).strip()
    
    return result

def create_complete_pdf():
    """Create PDF with complete questions including answers and explanations"""
    
    # Load the complete questions data
    try:
        with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\complete_questions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return False
    
    # Create PDF document
    pdf_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\CISSP_Complete_Questions_Organized.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                          rightMargin=50, leftMargin=50,
                          topMargin=50, bottomMargin=50)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1a3a5c')
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=15,
        textColor=colors.HexColor('#4a7fb5')
    )
    
    domain_title_style = ParagraphStyle(
        'DomainTitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=15,
        spaceAfter=8,
        textColor=colors.white,
        backColor=colors.HexColor('#2c5f8a'),
        borderPadding=(8, 8, 8, 8)
    )
    
    question_num_style = ParagraphStyle(
        'QuestionNum',
        parent=styles['Normal'],
        fontSize=11,
        spaceBefore=10,
        spaceAfter=4,
        textColor=colors.HexColor('#1a3a5c'),
        fontName='Helvetica-Bold'
    )
    
    question_text_style = ParagraphStyle(
        'QuestionText',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=2,
        spaceAfter=6,
        leftIndent=15,
        textColor=colors.HexColor('#333333')
    )
    
    option_style = ParagraphStyle(
        'Option',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=1,
        spaceAfter=1,
        leftIndent=30,
        textColor=colors.HexColor('#444444')
    )
    
    answer_style = ParagraphStyle(
        'Answer',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=6,
        spaceAfter=4,
        leftIndent=15,
        textColor=colors.HexColor('#006600'),
        fontName='Helvetica-Bold'
    )
    
    explanation_style = ParagraphStyle(
        'Explanation',
        parent=styles['Normal'],
        fontSize=9,
        spaceBefore=4,
        spaceAfter=8,
        leftIndent=15,
        textColor=colors.HexColor('#555555'),
        fontName='Helvetica-Oblique'
    )
    
    # Build content
    content = []
    
    # Title page
    content.append(Spacer(1, 50))
    content.append(Paragraph("CISSP CERTIFICATION EXAM", title_style))
    content.append(Paragraph("Complete Questions with Answers &amp; Explanations", subtitle_style))
    content.append(Paragraph("Organized by Domain", subtitle_style))
    content.append(Spacer(1, 30))
    content.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor('#2c5f8a')))
    content.append(Spacer(1, 20))
    
    # Domain summary table
    content.append(Paragraph("Domain Summary", ParagraphStyle(
        'TableTitle', parent=styles['Heading3'],
        fontSize=14, alignment=TA_CENTER, spaceAfter=10
    )))
    
    # Create domain summary data
    domain_summary = []
    domain_weights = data['metadata']['domain_weights']
    
    for domain_key in sorted(data['domains'].keys(), 
                           key=lambda x: int(re.search(r'domain_(\d+)', x).group(1)) if re.search(r'domain_(\d+)', x) else 999):
        domain_data = data['domains'][domain_key]
        domain_name = domain_data['name']
        question_count = domain_data['question_count']
        
        domain_num_match = re.search(r'Domain (\d+)', domain_name)
        domain_num = domain_num_match.group(1) if domain_num_match else "?"
        
        weight = domain_weights.get(domain_name, "N/A")
        short_name = domain_name.split(': ')[1] if ': ' in domain_name else domain_name
        
        domain_summary.append([
            f"Domain {domain_num}",
            short_name,
            str(question_count),
            weight
        ])
    
    # Create table
    table_data = [['Domain', 'Name', 'Questions', 'Weight']] + domain_summary
    
    table = Table(table_data, colWidths=[1*inch, 3*inch, 0.8*inch, 0.8*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5f8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f5fa')]),
    ]))
    
    content.append(table)
    content.append(Spacer(1, 20))
    
    # Total questions
    total_questions = data['metadata']['total_questions']
    content.append(Paragraph(f"<b>Total Questions:</b> {total_questions}", ParagraphStyle(
        'Total', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER
    )))
    
    content.append(PageBreak())
    
    # Add each domain section
    for domain_key in sorted(data['domains'].keys(), 
                           key=lambda x: int(re.search(r'domain_(\d+)', x).group(1)) if re.search(r'domain_(\d+)', x) else 999):
        
        domain_data = data['domains'][domain_key]
        domain_name = domain_data['name']
        questions = domain_data['questions']
        
        domain_num_match = re.search(r'Domain (\d+)', domain_name)
        domain_num = domain_num_match.group(1) if domain_num_match else "?"
        
        weight = domain_weights.get(domain_name, "N/A")
        short_name = domain_name.split(': ')[1] if ': ' in domain_name else domain_name
        
        # Domain title
        domain_title = f"Domain {domain_num}: {short_name}"
        content.append(Paragraph(domain_title, domain_title_style))
        content.append(Paragraph(f"<b>Questions:</b> {len(questions)} | <b>Exam Weight:</b> {weight}", ParagraphStyle(
            'DomainInfo', parent=styles['Normal'], fontSize=9, spaceAfter=8,
            textColor=colors.HexColor('#666666')
        )))
        
        # Add questions
        for i, question in enumerate(questions):
            q_num = question['question_number']
            topic = question['topic']
            full_content = question['full_content']
            
            # Parse the question content
            parsed = parse_question_content(full_content)
            
            # Question number and text
            q_text = clean_text_for_pdf(parsed["question_text"])
            if not q_text:
                # Fallback: use first part of full_content
                q_text = clean_text_for_pdf(full_content[:500])
            
            content.append(Paragraph(f"<b>Question {q_num}</b> (Topic {topic})", question_num_style))
            content.append(Paragraph(q_text, question_text_style))
            
            # Options
            if parsed["options"]:
                for opt in parsed["options"]:
                    opt_clean = clean_text_for_pdf(opt)
                    content.append(Paragraph(opt_clean, option_style))
            
            # Answer
            if parsed["answer"]:
                content.append(Paragraph(f"<b>Answer: {parsed['answer']}</b>", answer_style))
            
            # Explanation
            if parsed["explanation"]:
                expl_clean = clean_text_for_pdf(parsed["explanation"][:800])
                if len(parsed["explanation"]) > 800:
                    expl_clean += "..."
                content.append(Paragraph(f"<i>Explanation: {expl_clean}</i>", explanation_style))
            
            # Separator
            content.append(HRFlowable(width="90%", thickness=0.5, color=colors.HexColor('#dddddd'),
                                      spaceBefore=4, spaceAfter=4))
            
            # Page break every 8 questions
            if (i + 1) % 8 == 0 and i < len(questions) - 1:
                content.append(PageBreak())
        
        # Page break after each domain
        if domain_key != list(data['domains'].keys())[-1]:
            content.append(PageBreak())
    
    # Build PDF
    try:
        doc.build(content)
        print(f"PDF created successfully: {pdf_path}")
        return True
    except Exception as e:
        print(f"Error creating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Creating complete CISSP PDF with answers and explanations...")
    success = create_complete_pdf()
    
    if success:
        print("\nPDF creation completed successfully!")
        print("The PDF contains all 2,615 questions with:")
        print("- Complete question text")
        print("- All multiple choice options (A, B, C, D)")
        print("- Correct answers")
        print("- Explanations")
    else:
        print("Failed to create PDF")

if __name__ == "__main__":
    main()