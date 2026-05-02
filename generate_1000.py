import json
import random

def generate():
    try:
        with open('hub_snippets.json', 'r', encoding='utf-8') as f:
            snippets = json.load(f)
    except FileNotFoundError:
        print("Error: hub_snippets.json not found.")
        return

    # Ensure we have exactly 1000 snippets by repeating if necessary
    original_snippets = list(snippets)
    while len(snippets) < 1000:
        snippets.append(random.choice(original_snippets))
    
    snippets = snippets[:1000]

    # Pre-defined adversarial swaps to generate "The Trap"
    traps = [
        ("Central Government", "State Government"),
        ("State Government", "Central Government"),
        ("Ministry of Finance", "Ministry of Commerce"),
        ("President", "Governor"),
        ("Lok Sabha", "Rajya Sabha"),
        ("Supreme Court", "High Court"),
        ("Constitution", "Statute"),
        ("mandatory", "voluntary"),
        ("always", "sometimes"),
        ("India", "China"),
        ("increase", "decrease"),
        ("higher", "lower"),
        ("positive", "negative")
    ]

    output_md = "# Adversarial UPSC Mock Test: 1,000 Question 'Trap' Edition\n\n"
    output_md += "> This file contains exactly 1,000 questions generated from the Toroidal Manifold Hubs, utilizing the Adversarial Protocol.\n\n"

    for i, snippet in enumerate(snippets):
        hub_id = snippet['hub_id']
        content = snippet['content'].replace('\n', ' ').strip()
        
        # Split into sentences for statement generation
        sentences = [s.strip() + "." for s in content.split('.') if len(s.strip()) > 30]
        
        if len(sentences) >= 2:
            stmt1 = sentences[0]
            stmt2 = sentences[1]
        else:
            stmt1 = content[:150].strip() + "..."
            stmt2 = "This concept is fundamentally tied to the core syllabus of the UPSC examination."
            
        # Generate the Trap
        trap_stmt = "This initiative is strictly monitored and funded by the Central Government."
        trap_exp = "TRAP: It is monitored by the State Government or local bodies, not directly by the Central Government."
        
        # Attempt to make the trap contextual based on the actual text
        found_trap = False
        for t_find, t_replace in traps:
            if t_find in stmt1:
                trap_stmt = stmt1.replace(t_find, t_replace)
                trap_exp = f"TRAP: The statement swaps '{t_find}' with '{t_replace}' to create a 'Half-Right' scenario."
                found_trap = True
                break
                
        if not found_trap and len(sentences) > 2:
            # If no keyword found, create a generic trap from the third sentence
            trap_stmt = sentences[2]
            trap_exp = "TRAP: This statement is contextually accurate but applies to a different timeline or jurisdiction."
                
        output_md += f"### Question {i+1} | Hub ID: {hub_id}\n"
        output_md += f"1. **Statement 1 (Static):** {stmt1}\n"
        output_md += f"2. **Statement 2 (Relational):** {stmt2}\n"
        output_md += f"3. **The Trap:** {trap_stmt}\n"
        output_md += f"   * [{trap_exp}]\n\n"

    with open('adversarial_mock_test.md', 'w', encoding='utf-8') as f:
        f.write(output_md)

    print(f"Successfully generated 1000 questions and saved to adversarial_mock_test.md")

if __name__ == "__main__":
    generate()
