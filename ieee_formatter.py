import re

# 1. Clean each LLM output (remove tags and extra labels)
def clean_text(text):
    if isinstance(text, dict):
        text = text.get("content", "")
    # Remove anything in <...> tags like <think>, <thoughts>, etc.
    text = re.sub(r'<[^>]+>', '', text)
    # Remove label prefixes like "Summary:", "Recommendations:"
    text = re.sub(r'^\s*(Summary|Quality Review|Recommendations):\s*', '', text, flags=re.IGNORECASE).strip()
    return text

# 2. Guess section type based on keywords
def detect_section(text):
    text_lower = text.lower()
    if "hypothetical case" in text_lower or "methodology" in text_lower:
        return "Methodology"
    elif "experiment" in text_lower or "result" in text_lower:
        return "Experiments and Results"
    elif "future work" in text_lower or "further research" in text_lower:
        return "Future Work"
    elif "literature" in text_lower or "survey" in text_lower:
        return "Literature Survey"
    elif "research topics" in text_lower or "recommendations" in text_lower or "related work" in text_lower:
        return "Related Research"
    elif "introduction" in text_lower or "this paper" in text_lower:
        return "Introduction"
    elif "framework" in text_lower or "contribution" in text_lower or "competencies" in text_lower:
        return "Abstract"
    else:
        return "Uncategorized"

# 3. Organize IEEE sections
ieee_sections = [
    "Abstract",
    "Introduction",
    "Related Research",
    "Literature Survey",
    "Methodology",
    "Experiments and Results",
    "Future Work",
    "Uncategorized"
]

# 4. Format outputs into IEEE paper layout
def generate_ieee_output(raw_outputs):
    section_map = {section: [] for section in ieee_sections}

    for entry in raw_outputs:
        cleaned = clean_text(entry)
        section = detect_section(cleaned)
        section_map[section].append(cleaned)

    # Print final formatted output
    print("\nIEEE-Formatted Output\n" + "="*30)
    for section in ieee_sections:
        if section_map[section]:
            print(f"\n{section}\n{'-'*len(section)}")
            for paragraph in section_map[section]:
                print(paragraph.strip() + "\n")

# 5. Example input from your LLM agent
raw_outputs = [
    {"content": "Summary: <think>Agent thought</think> This paper explores the transformative impact of artificial intelligence (AI)..."},
    {"content": "Quality Review: <> The framework uses a hypothetical case to demonstrate methodology..."},
    {"content": "Recommendations: <> Suggested research topics include interdisciplinary AI and case studies..."}
]

# 6. Run it
generate_ieee_output(raw_outputs)
