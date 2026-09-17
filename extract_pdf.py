import PyPDF2
import re
import json

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                print("PDF is encrypted. Attempting to decrypt...")
                # Try with empty password
                pdf_reader.decrypt("")
            
            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
                    
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    
    return text

def analyze_questions(text):
    """Analyze the text to identify CISSP domains and questions"""
    if not text:
        return None
    
    # CISSP 2024 domains
    domains = {
        "Domain 1": "Security and Risk Management",
        "Domain 2": "Asset Security", 
        "Domain 3": "Security Architecture and Engineering",
        "Domain 4": "Communication and Network Security",
        "Domain 5": "Identity and Access Management (IAM)",
        "Domain 6": "Security Assessment and Testing",
        "Domain 7": "Security Operations",
        "Domain 8": "Software Development Security"
    }
    
    # Common CISSP keywords by domain
    domain_keywords = {
        "Domain 1": ["risk management", "security governance", "compliance", "legal", "regulations", "policies", "procedures", "business continuity", "disaster recovery", "personnel security", "professional ethics"],
        "Domain 2": ["asset", "data", "information", "classification", "ownership", "privacy", "retention", "protection", "handling"],
        "Domain 3": ["architecture", "engineering", "cryptograph", "encryption", "decryption", "key management", "security models", "vulnerabilities", "security controls", "physical security"],
        "Domain 4": ["network", "communication", "protocols", "network security", "firewall", "IDS", "IPS", "VPN", "wireless", "network attacks"],
        "Domain 5": ["identity", "access", "authentication", "authorization", "accounting", "AAA", "IAM", "single sign-on", "federation", "directory services"],
        "Domain 6": ["assessment", "testing", "audit", "vulnerability", "penetration testing", "security monitoring", "logging", "metrics"],
        "Domain 7": ["operations", "incident response", "forensics", "disaster recovery", "business continuity", "patch management", "change management", "problem management"],
        "Domain 8": ["software", "development", "application security", "SDLC", "database", "web security", "API security", "code review", "testing"]
    }
    
    # Split text into potential questions (looking for patterns like "Q:", "Question", numbered items)
    questions = []
    
    # Try different question patterns
    patterns = [
        r'(?:Q\d+[:.]\s*|Question\s*\d+[:.]\s*|\d+[.)]\s*)(.*?)(?=(?:Q\d+[:.]\s*|Question\s*\d+[:.]\s*|\d+[.)]\s*|$))',
        r'(?:^|\n)(.*?\?(?:\s|$))',
        r'(?:^|\n)(\d+\.\s*.*?(?:\?|\.))'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
        if matches:
            questions.extend(matches)
            break
    
    # If no questions found with patterns, try splitting by paragraphs
    if not questions:
        paragraphs = text.split('\n\n')
        questions = [p.strip() for p in paragraphs if p.strip() and len(p.strip()) > 20]
    
    # Analyze each question to determine domain
    question_analysis = []
    for i, question in enumerate(questions[:50]):  # Limit to first 50 for analysis
        question_lower = question.lower()
        domain_scores = {}
        
        # Score each domain based on keywords
        for domain, keywords in domain_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in question_lower:
                    score += 1
            domain_scores[domain] = score
        
        # Find the domain with highest score
        if domain_scores:
            best_domain = max(domain_scores.items(), key=lambda x: x[1])
            if best_domain[1] > 0:
                question_analysis.append({
                    "question_number": i + 1,
                    "question_text": question[:200] + "..." if len(question) > 200 else question,
                    "domain": best_domain[0],
                    "domain_name": domains[best_domain[0]],
                    "confidence": best_domain[1]
                })
    
    return question_analysis

def main():
    pdf_path = r"C:\Users\Khumza\.dsh\attachments\v1\files\33\331d4b0169214504da60bb320fd223ab90b139026e4901c550433ab96e7230c5\Cissp-8sn2bm.pdf"
    
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("Failed to extract text from PDF")
        return
    
    print(f"Extracted {len(text)} characters of text")
    
    # Save raw text for inspection
    with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\raw_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    print("Analyzing questions...")
    analysis = analyze_questions(text)
    
    if analysis:
        print(f"Found {len(analysis)} questions with domain analysis")
        
        # Group by domain
        domain_groups = {}
        for item in analysis:
            domain = item["domain"]
            if domain not in domain_groups:
                domain_groups[domain] = []
            domain_groups[domain].append(item)
        
        # Print summary
        print("\n=== Domain Analysis Summary ===")
        for domain, questions in domain_groups.items():
            print(f"\n{domain}: {item['domain_name']}")
            print(f"  Questions: {len(questions)}")
            for q in questions[:3]:  # Show first 3 examples
                print(f"    Q{q['question_number']}: {q['question_text'][:100]}...")
        
        # Save detailed analysis
        with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\question_analysis.json", "w") as f:
            json.dump(analysis, f, indent=2)
        
        print(f"\nDetailed analysis saved to question_analysis.json")
    else:
        print("No questions found for analysis")

if __name__ == "__main__":
    main()