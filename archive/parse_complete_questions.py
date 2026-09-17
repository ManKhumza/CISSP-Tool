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

def parse_complete_questions(text):
    """Parse complete questions with answers and explanations"""
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
            question_num = int(question_blocks[i])
            topic_num = int(question_blocks[i + 1])
            question_content = question_blocks[i + 2]
            
            # Clean up the content - remove extra whitespace and page headers/footers
            question_content = re.sub(r'ISC CISSP\s*\n.*?CERT EMPIRE\s*\d+', '', question_content, flags=re.DOTALL)
            question_content = re.sub(r'https://certempire\.com/\s*\d+', '', question_content)
            question_content = re.sub(r'"Best Material, Great Results"\.\s*CERT EMPIRE\s*\d+', '', question_content)
            question_content = re.sub(r'ISC CISSP\s*\n"https://certempire\.com/"\s*\d+', '', question_content)
            
            # Remove extra newlines and spaces
            question_content = re.sub(r'\n\s*\n', '\n\n', question_content)
            question_content = question_content.strip()
            
            questions.append({
                "question_number": question_num,
                "topic": topic_num,
                "full_content": question_content
            })
    
    return questions

def map_topics_to_domains():
    """Map topic numbers to CISSP domains based on content analysis"""
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
    domain_questions = defaultdict(list)
    
    for q in questions:
        topic = q["topic"]
        domain = topic_to_domain.get(topic, f"Topic {topic} (Unclassified)")
        domain_questions[domain].append(q)
    
    return domain_questions

def main():
    print("Reading raw text...")
    text = read_raw_text()
    
    if not text:
        print("Failed to read raw text")
        return
    
    print("Parsing complete questions with answers and explanations...")
    questions = parse_complete_questions(text)
    
    print(f"Found {len(questions)} complete questions")
    
    # Show sample of first question to verify completeness
    if questions:
        print("\n" + "="*80)
        print("SAMPLE QUESTION (Question 1):")
        print("="*80)
        print(questions[0]["full_content"][:1000])
        print("...")
    
    print("\nOrganizing questions by domain...")
    domain_questions = organize_questions_by_domain(questions)
    
    print(f"\nOrganized into {len(domain_questions)} domains:")
    for domain, qs in domain_questions.items():
        domain_num_match = re.search(r'Domain (\d+)', domain)
        if domain_num_match:
            print(f"  Domain {domain_num_match.group(1)}: {len(qs)} questions")
        else:
            print(f"  {domain}: {len(qs)} questions")
    
    # Save complete organized data
    output_data = {
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
    
    for domain, qs in domain_questions.items():
        domain_num_match = re.search(r'Domain (\d+)', domain)
        domain_key = f"domain_{domain_num_match.group(1)}" if domain_num_match else domain
        
        output_data["domains"][domain_key] = {
            "name": domain,
            "question_count": len(qs),
            "questions": [
                {
                    "question_number": q["question_number"],
                    "topic": q["topic"],
                    "full_content": q["full_content"]
                }
                for q in qs
            ]
        }
    
    json_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\complete_questions.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nComplete questions data saved to: {json_path}")
    print(f"File size: {len(json.dumps(output_data, ensure_ascii=False))} characters")

if __name__ == "__main__":
    main()