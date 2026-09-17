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
    
    # Pattern to match questions: "QUESTION X - (Topic Y)" or similar patterns
    # Looking at the structure, it seems like: "QUESTION X - (Topic Y)"
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
            # Look for the question text ending with "?" or before answer options
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
                "question_text": question_text,
                "full_content": question_content
            })
    
    return questions

def map_topics_to_domains():
    """Map topic numbers to CISSP domains based on common patterns"""
    # Based on typical CISSP exam structure and the content we saw
    # Topic 1 appears to be Security and Risk Management (Domain 1)
    # We need to analyze more content to map other topics
    
    # For now, let's create a mapping based on common CISSP patterns
    # This will need refinement based on actual content analysis
    topic_to_domain = {
        1: "Domain 1: Security and Risk Management",
        2: "Domain 2: Asset Security", 
        3: "Domain 3: Security Architecture and Engineering",
        4: "Domain 4: Communication and Network Security",
        5: "Domain 5: Identity and Access Management (IAM)",
        6: "Domain 6: Security Assessment and Testing",
        7: "Domain 7: Security Operations",
        8: "Domain 8: Software Development Security"
    }
    
    return topic_to_domain

def analyze_question_content(question_text):
    """Analyze question content to determine domain if topic mapping is unclear"""
    question_lower = question_text.lower()
    
    # Domain keyword analysis
    domain_keywords = {
        "Domain 1": ["risk", "governance", "compliance", "legal", "policy", "procedure", "ethics", "business continuity", "disaster recovery", "personnel", "security management"],
        "Domain 2": ["asset", "data", "information", "classification", "ownership", "privacy", "retention", "handling", "labeling"],
        "Domain 3": ["architecture", "engineering", "cryptograph", "encryption", "decryption", "key", "security model", "vulnerability", "security control", "physical security", "facility"],
        "Domain 4": ["network", "communication", "protocol", "firewall", "IDS", "IPS", "VPN", "wireless", "network attack", "router", "switch"],
        "Domain 5": ["identity", "access", "authentication", "authorization", "accounting", "AAA", "IAM", "single sign-on", "federation", "directory", "biometric"],
        "Domain 6": ["assessment", "testing", "audit", "vulnerability", "penetration", "monitoring", "logging", "metric", "security assessment"],
        "Domain 7": ["operation", "incident", "forensic", "disaster", "business continuity", "patch", "change", "problem", "service", "availability"],
        "Domain 8": ["software", "development", "application", "SDLC", "database", "web", "API", "code review", "testing", "software security"]
    }
    
    domain_scores = {}
    for domain, keywords in domain_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in question_lower:
                score += 1
        domain_scores[domain] = score
    
    if domain_scores:
        best_domain = max(domain_scores.items(), key=lambda x: x[1])
        if best_domain[1] > 0:
            return best_domain[0]
    
    return None

def organize_questions_by_domain(questions):
    """Organize questions by domain"""
    topic_to_domain = map_topics_to_domains()
    
    # Group questions by domain
    domain_questions = defaultdict(list)
    
    for q in questions:
        topic = q["topic"]
        if topic in topic_to_domain:
            domain = topic_to_domain[topic]
        else:
            # Try to determine domain from content
            domain = analyze_question_content(q["question_text"])
            if not domain:
                domain = f"Topic {topic} (Unclassified)"
        
        domain_questions[domain].append(q)
    
    return domain_questions

def create_organized_document(domain_questions):
    """Create an organized document with questions by domain"""
    output = []
    
    # Sort domains by domain number
    sorted_domains = sorted(domain_questions.keys(), key=lambda x: int(re.search(r'Domain (\d+)', x).group(1)) if re.search(r'Domain (\d+)', x) else 999)
    
    for domain in sorted_domains:
        questions = domain_questions[domain]
        output.append(f"\n{'='*80}")
        output.append(f"DOMAIN: {domain}")
        output.append(f"Number of Questions: {len(questions)}")
        output.append(f"{'='*80}\n")
        
        # Sort questions by question number
        questions.sort(key=lambda x: x["question_number"])
        
        for q in questions:
            output.append(f"Question {q['question_number']} (Topic {q['topic']}):")
            output.append(f"{q['question_text']}")
            output.append("-" * 40)
    
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
    
    # Show some statistics
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
        print(f"  {domain}: {len(questions)} questions")
    
    # Create organized document
    print("\nCreating organized document...")
    organized_doc = create_organized_document(domain_questions)
    
    # Save organized document
    output_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\organized_cissp_questions.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(organized_doc)
    
    print(f"\nOrganized document saved to: {output_path}")
    
    # Also save as JSON for easier processing
    json_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\organized_questions.json"
    
    # Convert to JSON-serializable format
    json_data = {}
    for domain, questions in domain_questions.items():
        json_data[domain] = [
            {
                "question_number": q["question_number"],
                "topic": q["topic"],
                "question_text": q["question_text"]
            }
            for q in questions
        ]
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    
    print(f"JSON data saved to: {json_path}")

if __name__ == "__main__":
    main()