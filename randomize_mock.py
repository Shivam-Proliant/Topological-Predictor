import re
import random
import os

def randomize_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to match a full question block
    pattern = re.compile(
        r'(\*\*Q\d+\..*?\*\*)\n+'
        r'1\.\s(.*?)\n+'
        r'2\.\s(.*?)\n+'
        r'3\.\s(.*?)\n+'
        r'\*\*Which of the statements given above is/are correct\?\*\*\n+'
        r'\(a\)\s.*?\n+'
        r'\(b\)\s.*?\n+'
        r'\(c\)\s.*?\n+'
        r'\(d\)\s.*?\n+'
        r'\*\*Answer:\s\([a-d]\)\s(.*?)\*\*\n+'
        r'\*\*Explanation:\*\*(.*?)(?=\n---|(?:\n\*(?:Continuing))|(?:\n\n\*\*Q)|\Z)',
        re.DOTALL
    )
    
    count = 0
    
    def replacer(match):
        nonlocal count
        count += 1
        title = match.group(1).strip()
        stmt1 = match.group(2).strip()
        stmt2 = match.group(3).strip()
        stmt3 = match.group(4).strip()
        correct_ans_text = match.group(5).strip()
        explanation = match.group(6).strip()
        
        statements = [stmt1, stmt2, stmt3]
        
        # Determine which original statements were correct
        correct_original = []
        if '1' in correct_ans_text: correct_original.append(1)
        if '2' in correct_ans_text: correct_original.append(2)
        if '3' in correct_ans_text: correct_original.append(3)
        
        # Shuffle
        orig_indices = [1, 2, 3]
        shuffled_indices = orig_indices.copy()
        random.shuffle(shuffled_indices)
        
        orig_to_new = {orig: new for new, orig in enumerate(shuffled_indices, 1)}
        
        # Update explanation "Statement X" to reflect new numbers
        for orig, new in orig_to_new.items():
            explanation = re.sub(rf'Statement {orig}\b', f'Statement_TMP_{new}', explanation, flags=re.IGNORECASE)
        explanation = explanation.replace('Statement_TMP_', 'Statement ')
        
        # New correct statements
        correct_new = sorted([orig_to_new[x] for x in correct_original])
        
        def format_opts(nums):
            if not nums: return "None of the above"
            if len(nums) == 3: return "1, 2 and 3"
            if len(nums) == 1: return f"{nums[0]} only"
            return f"{nums[0]} and {nums[1]} only"
            
        correct_opt_text = format_opts(correct_new)
        
        possible_opts = [
            "1 only", "2 only", "3 only",
            "1 and 2 only", "2 and 3 only", "1 and 3 only",
            "1, 2 and 3", "None of the above"
        ]
        
        wrong_opts = [opt for opt in possible_opts if opt != correct_opt_text]
        chosen_wrong = random.sample(wrong_opts, 3)
        final_options = chosen_wrong + [correct_opt_text]
        random.shuffle(final_options)
        
        correct_letter = chr(97 + final_options.index(correct_opt_text))
        
        new_block = [
            title,
            f"1. {statements[shuffled_indices[0]-1]}",
            f"2. {statements[shuffled_indices[1]-1]}",
            f"3. {statements[shuffled_indices[2]-1]}",
            "",
            "**Which of the statements given above is/are correct?**",
            f"(a) {final_options[0]}",
            f"(b) {final_options[1]}",
            f"(c) {final_options[2]}",
            f"(d) {final_options[3]}",
            "",
            f"**Answer: ({correct_letter}) {correct_opt_text}**",
            f"**Explanation:** {explanation}"
        ]
        
        return "\n".join(new_block)
        
    new_content = pattern.sub(replacer, content)
    
    # Save the output to the same file (or a new file for safety, let's overwrite directly as requested)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Successfully randomized {count} questions in {filepath}")

if __name__ == "__main__":
    filepath = r"c:\Users\shivam\Desktop\UPSC\cleaned_adversarial_mock.md"
    randomize_questions(filepath)
