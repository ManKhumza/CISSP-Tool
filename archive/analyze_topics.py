import re
from collections import defaultdict

def read_raw_text():
    """Read the extracted raw text file"""
    try:
        with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\raw_text.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading raw text: {e}")
        return None

def extract_sample_questions_per_topic(text, samples_per_topic=3):
    """Extract sample questions from each topic to understand content"""
    if not text:
        return {}
    
    # Find all questions with their topics
    question_pattern = r'QUESTION\s+(\d+)\s*-\s*\(Topic\s+(\d+)\)'
    
    # Split text by question markers
    question_blocks = re.split(question_pattern, text)
    
    topic_samples = defaultdict(list)
    
    # Extract sample questions for each topic
    for i in range(1, len(question_blocks), 3):
        if i + 2 < len(question_blocks):
            question_num = question_blocks[i]
            topic_num = question_blocks[i + 1]
            question_content = question_blocks[i + 2]
            
            # Extract question text
            question_text_match = re.search(r'(.*?\?)', question_content, re.DOTALL)
            if question_text_match:
                question_text = question_text_match.group(1).strip()
                # Clean up
                question_text = re.sub(r'\s+', ' ', question_text)
                question_text = question_text.replace('\n', ' ').strip()
                
                if len(topic_samples[topic_num]) < samples_per_topic:
                    topic_samples[topic_num].append({
                        "question_num": question_num,
                        "text": question_text[:300] + "..." if len(question_text) > 300 else question_text
                    })
    
    return topic_samples

def main():
    print("Reading raw text...")
    text = read_raw_text()
    
    if not text:
        print("Failed to read raw text")
        return
    
    print("Extracting sample questions from each topic...")
    topic_samples = extract_sample_questions_per_topic(text)
    
    print(f"\nFound samples from {len(topic_samples)} topics:")
    
    for topic_num in sorted(topic_samples.keys(), key=lambda x: int(x)):
        samples = topic_samples[topic_num]
        print(f"\n=== Topic {topic_num} ===")
        print(f"Sample questions:")
        for sample in samples:
            print(f"  Q{sample['question_num']}: {sample['text'][:150]}...")

if __name__ == "__main__":
    main()