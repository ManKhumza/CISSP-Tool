import re
import json
from collections import defaultdict

def read_raw_text():
    """Read the extracted raw text file"""
    try:
        with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\raw_text.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading raw text: {e}")
        return None

def parse_questions(text):
    """Parse questions from the raw text"""
    if not text:
        return []
    
    questions = []
    
    # Pattern to match questions: "QUESTION X - (Topic Y)"
    question_pattern = r'QUESTION\s+(\d+)\s*-\s*\(Topic\s+(\d+)\)'
    
    # Split text by question markers
    question_blocks = re.split(question_pattern, text)
    
    # The first element is text before first question, then alternating question numbers and content
    for i in range(1, len(question_blocks), 3):
        if i + 2 < len(question_blocks):
            question_num = question_blocks[i]
            topic_num = question_blocks[i + 1]
            question_content = question_blocks[i + 2]
            
            # Extract the actual question text (before the answer options)
            question_text_match = re.search(r'(.*?\?)', question_content, re.DOTALL)
            if question_text_match:
                question_text = question_text_match.group(1).strip()
            else:
                # If no question mark, take text before first answer option
                answer_pattern = r'\n[A-D]\.'
                answer_match = re.search(answer_pattern, question_content)
                if answer_match:
                    question_text = question_content[:answer_match.start()].strip()
                else:
                    question_text = question_content[:200].strip()
            
            # Clean up the question text
            question_text = re.sub(r'\s+', ' ', question_text)
            question_text = question_text.replace('\n', ' ').strip()
            
            questions.append({
                "question_number": int(question_num),
                "topic": int(topic_num),
                "question_text": question_text
            })
    
    return questions

def map_topics_to_domains():
    """Map topic numbers to CISSP domains based on content analysis"""
    # Based on the sample questions analyzed
    topic_to_domain = {
        1: "Domain 1: Security and Risk Management",
        2: "Domain 4: Communication and Network Security",
        3: "Domain 1: Security and Risk Management", 
        4: "Domain 8: Software Development Security",
        5: "Domain 7: Security Operations",
        6: "Domain 3: Security Architecture and Engineering",
        7: "Domain 3: Security Architecture and Engineering",
        8: "Domain 3: Security Architecture and Engineering",
        9: "Domain 6: Security Assessment and Testing",
        10: "Domain 4: Communication and Network Security",
        11: "Domain 5: Identity and Access Management (IAM)",
        12: "Domain 7: Security Operations",
        13: "Domain 2: Asset Security",
        14: "Domain 2: Asset Security",
        15: "Domain 6: Security Assessment and Testing"
    }
    
    return topic_to_domain

def organize_questions_by_domain(questions):
    """Organize questions by domain"""
    topic_to_domain = map_topics_to_domains()
    
    # Group questions by domain
    domain_questions = defaultdict(list)
    
    for q in questions:
        topic = q["topic"]
        domain = topic_to_domain.get(topic, f"Topic {topic} (Unclassified)")
        domain_questions[domain].append(q)
    
    return domain_questions

def create_final_organized_document(domain_questions):
    """Create the final organized document"""
    output = []
    
    # CISSP Domain information
    domain_info = {
        "Domain 1: Security and Risk Management": {
            "description": "Security and Risk Management covers security governance, compliance, legal and regulatory issues, professional ethics, security documentation, risk management concepts, threat modeling, supply chain risk management, and business continuity requirements.",
            "weight": "15%"
        },
        "Domain 2: Asset Security": {
            "description": "Asset Security covers information and asset classification, data ownership, data privacy, data retention, protecting data, and handling requirements.",
            "weight": "10%"
        },
        "Domain 3: Security Architecture and Engineering": {
            "description": "Security Architecture and Engineering covers secure design principles, security models, security evaluation models, security capabilities of information systems, vulnerabilities in web-based systems, mobile systems, and embedded systems, cryptography, and site design.",
            "weight": "13%"
        },
        "Domain 4: Communication and Network Security": {
            "description": "Communication and Network Security covers secure network architecture design, secure network components, secure communication channels, and network attacks.",
            "weight": "13%"
        },
        "Domain 5: Identity and Access Management (IAM)": {
            "description": "Identity and Access Management covers physical and logical access control, identification and authentication of people and devices, identity as a service, and authorization mechanisms.",
            "weight": "13%"
        },
        "Domain 6: Security Assessment and Testing": {
            "description": "Security Assessment and Testing covers security control testing, collecting security process data, test outputs, security audits, and vulnerability assessments.",
            "weight": "12%"
        },
        "Domain 7: Security Operations": {
            "description": "Security Operations covers investigations, incident management, disaster recovery, business continuity, physical security, personnel safety, and problem management.",
            "weight": "13%"
        },
        "Domain 8: Software Development Security": {
            "description": "Software Development Security covers software development lifecycle security, application security, database security, and software-based vulnerabilities.",
            "weight": "11%"
        }
    }
    
    # Sort domains by domain number
    def domain_sort_key(domain):
        match = re.search(r'Domain (\d+)', domain)
        if match:
            return int(match.group(1))
        return 999
    
    sorted_domains = sorted(domain_questions.keys(), key=domain_sort_key)
    
    # Create document header
    output.append("=" * 100)
    output.append("CISSP EXAM QUESTIONS - ORGANIZED BY DOMAIN")
    output.append("=" * 100)
    output.append("")
    output.append("This document contains 2,615 CISSP exam questions organized by the 8 CISSP domains.")
    output.append("Questions are grouped by domain to facilitate focused study on each topic area.")
    output.append("")
    output.append("CISSP Domain Weights:")
    output.append("-" * 50)
    for domain, info in domain_info.items():
        output.append(f"{domain}: {info['weight']}")
    output.append("")
    output.append("=" * 100)
    
    # Add each domain section
    for domain in sorted_domains:
        questions = domain_questions[domain]
        
        # Get domain info
        domain_num_match = re.search(r'Domain (\d+)', domain)
        if domain_num_match:
            domain_num = int(domain_num_match.group(1))
            info = domain_info.get(domain, {})
            description = info.get("description", "Domain description not available")
            weight = info.get("weight", "Weight not specified")
        else:
            description = "Unclassified domain"
            weight = "N/A"
        
        output.append("")
        output.append("=" * 100)
        output.append(f"DOMAIN {domain_num}: {domain.split(': ')[1] if ': ' in domain else domain}")
        output.append("=" * 100)
        output.append(f"Domain Weight in CISSP Exam: {weight}")
        output.append(f"Number of Questions: {len(questions)}")
        output.append("")
        output.append(f"Description: {description}")
        output.append("")
        output.append("-" * 100)
        output.append("QUESTIONS:")
        output.append("-" * 100)
        
        # Sort questions by question number
        questions.sort(key=lambda x: x["question_number"])
        
        for q in questions:
            output.append(f"\nQuestion {q['question_number']} (Topic {q['topic']}):")
            output.append(f"{q['question_text']}")
            output.append("-" * 40)
        
        output.append("")
        output.append("=" * 100)
    
    return "\n".join(output)

def main():
    print("Reading raw text...")
    text = read_raw_text()
    
    if not text:
        print("Failed to read raw text")
        return
    
    print("Parsing questions...")
    questions = parse_questions(text)
    
    print(f"Found {len(questions)} questions")
    
    # Show topic distribution
    topics = defaultdict(int)
    for q in questions:
        topics[q["topic"]] += 1
    
    print("\nQuestions by topic:")
    for topic, count in sorted(topics.items()):
        print(f"  Topic {topic}: {count} questions")
    
    print("\nOrganizing questions by domain...")
    domain_questions = organize_questions_by_domain(questions)
    
    print(f"\nOrganized into {len(domain_questions)} domains:")
    for domain, questions in domain_questions.items():
        domain_num_match = re.search(r'Domain (\d+)', domain)
        if domain_num_match:
            print(f"  Domain {domain_num_match.group(1)}: {len(questions)} questions")
        else:
            print(f"  {domain}: {len(questions)} questions")
    
    # Create final organized document
    print("\nCreating final organized document...")
    organized_doc = create_final_organized_document(domain_questions)
    
    # Save organized document
    output_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\CISSP_Questions_Organized_by_Domain.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(organized_doc)
    
    print(f"\nFinal organized document saved to: {output_path}")
    
    # Also save as JSON for easier processing
    json_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\organized_questions_final.json"
    
    # Convert to JSON-serializable format
    json_data = {
        "metadata": {
            "total_questions": len(questions),
            "domains": len(domain_questions),
            "domain_weights": {
                "Domain 1: Security and Risk Management": "15%",
                "Domain 2: Asset Security": "10%",
                "Domain 3: Security Architecture and Engineering": "13%",
                "Domain 4: Communication and Network Security": "13%",
                "Domain 5: Identity and Access Management (IAM)": "13%",
                "Domain 6: Security Assessment and Testing": "12%",
                "Domain 7: Security Operations": "13%",
                "Domain 8: Software Development Security": "11%"
            }
        },
        "domains": {}
    }
    
    for domain, questions in domain_questions.items():
        domain_num_match = re.search(r'Domain (\d+)', domain)
        domain_key = f"domain_{domain_num_match.group(1)}" if domain_num_match else domain
        
        json_data["domains"][domain_key] = {
            "name": domain,
            "question_count": len(questions),
            "questions": [
                {
                    "question_number": q["question_number"],
                    "topic": q["topic"],
                    "question_text": q["question_text"]
                }
                for q in questions
            ]
        }
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    
    print(f"JSON data saved to: {json_path}")
    
    # Create a summary statistics file
    summary_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\CISSP_Study_Summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("CISSP EXAM STUDY SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Questions: {len(questions)}\n")
        f.write(f"Total Domains: {len(domain_questions)}\n\n")
        
        f.write("Questions by Domain:\n")
        f.write("-" * 30 + "\n")
        
        for domain in sorted(domain_questions.keys(), key=domain_sort_key):
            domain_num_match = re.search(r'Domain (\d+)', domain)
            if domain_num_match:
                f.write(f"Domain {domain_num_match.group(1)}: {len(domain_questions[domain])} questions\n")
        
        f.write("\nStudy Recommendations:\n")
        f.write("-" * 30 + "\n")
        f.write("1. Focus on domains with higher exam weights\n")
        f.write("2. Practice questions from all domains regularly\n")
        f.write("3. Review explanations for incorrect answers\n")
        f.write("4. Take practice exams simulating real test conditions\n")
        f.write("5. Use this organized document for focused domain study\n")
    
    print(f"Study summary saved to: {summary_path}")

def domain_sort_key(domain):
    match = re.search(r'Domain (\d+)', domain)
    if match:
        return int(match.group(1))
    return 999

if __name__ == "__main__":
    main()