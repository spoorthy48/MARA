import re

def clean_output(response):
    """
    Cleans agent response by removing THINK tags, markdown, internal thoughts, and formatting notes.
    """
    # Convert dict to string if needed
    content = response.get("content", "") if isinstance(response, dict) else str(response)

    # Remove THINK tags and markdown-style markers
    content = re.sub(r"(\*\*\[?THINK\]?\*\*|\[?THINK\]?)", "", content, flags=re.IGNORECASE)

    # Remove bold markdown
    content = re.sub(r"\*\*(.*?)\*\*", r"\1", content)

    # Remove entire <...> meta-thinking or formatting instructions
    content = re.sub(r"Summary:\s*<.*?>.*?(?=(The paper|This paper|It|AI|Artificial))", "", content, flags=re.DOTALL)

    # Remove internal monologue starting with cue words
    content = re.sub(
        r"(?i)(^|\n)(Okay|Alright|Let me|I need to|I'll|First, I|Got it|They want me to|The user emphasized)[^\n]*\n?", 
        "", 
        content
    )

    # Remove any remaining lines that sound like internal reasoning
    content = re.sub(r"(?i)^.*(I'll structure|I should|I remember|It's crucial|Avoid using).*\n?", "", content)

    # Clean up excess whitespace and newlines
    content = re.sub(r"\n{2,}", "\n", content).strip()

    return content
