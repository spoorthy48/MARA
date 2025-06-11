from utils import clean_output

raw_outputs = [
    {
        "content": "Summary: <think>Alright, I need to help the user by summarizing a research paper...</think> The paper introduces a framework called AI-ing with five competencies..."
    },
    {
        "content": "<THINK>First I must read this carefully...</THINK> Summary: The study focuses on using generative AI in clinical diagnostics..."
    },
    "Summary: [THINK]The article discusses how machine learning transforms data analysis in finance."
]

print("Cleaned Outputs:\n")
for i, raw in enumerate(raw_outputs):
    cleaned = clean_output(raw)
    print(f"{i+1}. {cleaned}\n")
