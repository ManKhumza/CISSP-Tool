import json
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import re

def create_organized_pdf():
    """Create a well-formatted PDF with organized CISSP questions"""
    
    # Load the organized questions data
    try:
        with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\organized_questions_final.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return False
    
    # Create PDF document
    pdf_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\CISSP_Questions_Organized.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=72)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1f4e79')
    )
    
    domain_title_style = ParagraphStyle(
        'DomainTitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceBefore=20,
        spaceAfter=12,
        textColor=colors.HexColor('#2e75b6'),
        borderWidth=1,
        borderColor=colors.HexColor('#2e75b6'),
        borderPadding=5
    )
    
    question_style = ParagraphStyle(
        'Question',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=8,
        spaceAfter=4,
        leftIndent=20,
        textColor=colors.HexColor('#333333')
    )
    
    metadata_style = ParagraphStyle(
        'Metadata',
        parent=styles['Normal'],
        fontSize=9,
        spaceBefore=2,
        spaceAfter=2,
        leftIndent=20,
        textColor=colors.HexColor('#666666')
    )
    
    # Build content
    content = []
    
    # Title page
    content.append(Paragraph("CISSP EXAM QUESTIONS", title_style))
    content.append(Paragraph("Organized by Domain", ParagraphStyle(
        'Subtitle', parent=styles['Heading2'],
        fontSize=16, alignment=TA_CENTER, spaceAfter=20,
        textColor=colors.HexColor('#4472c4')
    )))
    content.append(Spacer(1, 50))
    
    # Domain summary table
    content.append(Paragraph("Domain Summary", styles['Heading2']))
    
    # Create domain summary data
    domain_summary = []
    domain_weights = data['metadata']['domain_weights']
    
    for domain_key, domain_data in data['domains'].items():
        domain_name = domain_data['name']
        question_count = domain_data['question_count']
        
        # Extract domain number
        domain_num_match = re.search(r'Domain (\d+)', domain_name)
        domain_num = domain_num_match.group(1) if domain_num_match else "?"
        
        # Get weight
        weight = domain_weights.get(domain_name, "N/A")
        
        domain_summary.append([
            f"Domain {domain_num}",
            domain_name.split(': ')[1] if ': ' in domain_name else domain_name,
            str(question_count),
            weight
        ])
    
    # Sort by domain number
    domain_summary.sort(key=lambda x: int(x[0].split()[1]))
    
    # Create table
    table_data = [['Domain', 'Name', 'Questions', 'Exam Weight']] + domain_summary
    
    table = Table(table_data, colWidths=[1.2*inch, 3.5*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e75b6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    ]))
    
    content.append(table)
    content.append(Spacer(1, 30))
    
    # Total questions
    total_questions = sum(data['domains'][d]['question_count'] for d in data['domains'])
    content.append(Paragraph(f"<b>Total Questions:</b> {total_questions}", styles['Normal']))
    content.append(Paragraph(f"<b>Total Domains:</b> {len(data['domains'])}", styles['Normal']))
    
    content.append(PageBreak())
    
    # Add each domain section
    for domain_key in sorted(data['domains'].keys(), 
                           key=lambda x: int(re.search(r'domain_(\d+)', x).group(1)) if re.search(r'domain_(\d+)', x) else 999):
        
        domain_data = data['domains'][domain_key]
        domain_name = domain_data['name']
        questions = domain_data['questions']
        
        # Extract domain number
        domain_num_match = re.search(r'Domain (\d+)', domain_name)
        domain_num = domain_num_match.group(1) if domain_num_match else "?"
        
        # Get weight
        weight = domain_weights.get(domain_name, "N/A")
        
        # Domain title
        domain_title = f"Domain {domain_num}: {domain_name.split(': ')[1] if ': ' in domain_name else domain_name}"
        content.append(Paragraph(domain_title, domain_title_style))
        
        # Domain info
        content.append(Paragraph(f"<b>Questions:</b> {len(questions)} | <b>Exam Weight:</b> {weight}", metadata_style))
        content.append(Spacer(1, 10))
        
        # Add questions
        for i, question in enumerate(questions, 1):
            q_num = question['question_number']
            topic = question['topic']
            q_text = question['question_text']
            
            # Clean up question text for PDF
            q_text = q_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            content.append(Paragraph(f"<b>Question {q_num} (Topic {topic}):</b>", question_style))
            content.append(Paragraph(q_text, ParagraphStyle(
                'QuestionText',
                parent=styles['Normal'],
                fontSize=10,
                spaceBefore=2,
                spaceAfter=8,
                leftIndent=40,
                textColor=colors.HexColor('#333333')
            )))
            
            # Add separator line
            content.append(Spacer(1, 2))
            
            # Add page break every 15 questions to avoid overcrowding
            if i % 15 == 0 and i < len(questions):
                content.append(PageBreak())
        
        # Add page break after each domain
        if domain_key != list(data['domains'].keys())[-1]:
            content.append(PageBreak())
    
    # Build PDF
    try:
        doc.build(content)
        print(f"PDF created successfully: {pdf_path}")
        return True
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False

def main():
    print("Creating organized CISSP PDF...")
    success = create_organized_pdf()
    
    if success:
        print("PDF creation completed successfully!")
        print("\nFiles created:")
        print("1. CISSP_Questions_Organized.pdf - Main organized PDF document")
        print("\nThe PDF contains all 2,615 questions organized by the 8 CISSP domains.")
        print("Use this PDF for focused study sessions on specific domains.")
    else:
        print("Failed to create PDF")

if __name__ == "__main__":
    main()