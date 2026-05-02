import re

def format_upsc():
    with open('adversarial_mock_test.md', 'r', encoding='utf-8') as f:
        content = f.read()

    questions = re.split(r'### Question \d+ \| Hub ID: \d+', content)
    # The first element is the header, ignore it.
    
    header = questions[0]
    question_blocks = questions[1:]
    
    output_md = "# Full UPSC Formatted Mock Test (1,000 Questions)\n\n"
    
    for i, block in enumerate(question_blocks):
        # Extract statements using regex
        s1_match = re.search(r'1\. \*\*Statement 1 \(Static\):\*\* (.*)', block)
        s2_match = re.search(r'2\. \*\*Statement 2 \(Relational\):\*\* (.*)', block)
        trap_match = re.search(r'3\. \*\*The Trap:\*\* (.*)', block)
        exp_match = re.search(r'\* \[TRAP: (.*?)\]', block)
        
        s1 = s1_match.group(1).strip() if s1_match else "N/A"
        s2 = s2_match.group(1).strip() if s2_match else "N/A"
        trap = trap_match.group(1).strip() if trap_match else "N/A"
        exp = exp_match.group(1).strip() if exp_match else "N/A"
        
        # Build UPSC Style Question
        output_md += f"**Q{i+1}.** Consider the following statements:\n"
        output_md += f"1. {s1}\n"
        output_md += f"2. {s2}\n"
        output_md += f"3. {trap}\n\n"
        output_md += "Which of the statements given above is/are correct?\n"
        output_md += "(a) 1 and 2 only\n"
        output_md += "(b) 2 and 3 only\n"
        output_md += "(c) 1 and 3 only\n"
        output_md += "(d) 1, 2 and 3\n\n"
        
        output_md += "**Answer: (a) 1 and 2 only**\n"
        output_md += f"**Explanation:** Statement 3 is incorrect because: {exp}\n"
        output_md += "---\n\n"

    with open('upsc_formatted_test.md', 'w', encoding='utf-8') as f:
        f.write(output_md)

    print("Formatting complete. Output saved to upsc_formatted_test.md")

if __name__ == "__main__":
    format_upsc()
