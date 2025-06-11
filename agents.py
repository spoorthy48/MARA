from autogen import AssistantAgent
import os
from dotenv import load_dotenv
from utils import clean_output

load_dotenv()

class ResearchAgents:
    def __init__(self, groq_api_key):
        self.groq_api_key = groq_api_key
        self.llm_config = {
            'config_list': [{
                'model': 'deepseek-r1-distill-llama-70b',
                'api_key': self.groq_api_key,
                'api_type': 'groq'
            }]
        }

        self.summarizer_agent = AssistantAgent(
            name="summarizer_agent",
            system_message=(
                "You are an academic summarization agent. Summarize research papers in formal IEEE style. "
                "Use precise, objective language and passive voice. Do not include any internal thoughts, reasoning steps, or formatting tags like '<think>' or 'Summary:'. "
                "Only output the summary of the paper in plain text."
                "When you summarize, ensure you only add text and no numbers or bullet points. "
            ),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        self.quality_review_agent = AssistantAgent(
            name="quality_review_agent",
            system_message=(
                "Critically review the paper for quality based on clarity, originality, and methodology. "
                "Use formal academic tone. Do not include meta-thinking, reasoning steps, or '<think>' tags. "
                "Only present the final review analysis."
            ),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        self.recommendation_agent = AssistantAgent(
            name="recommendation_agent",
            system_message=(
                "Suggest further reading or related research topics or papers. "
                "Include both topic areas and example research publications with citation information when applicable. "
                "Do not include meta-thinking, reasoning steps, or tags like '<think>'."
            ),
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

    def summarize_paper(self, paper_summary):
        response = self.summarizer_agent.generate_reply(
            messages=[{"role": "user", "content": (
                "Provide only a plain-text IEEE-style summary of the following research paper. "
                "Use formal, objective academic language. Write in passive voice. "
                "Output only the summary without any explanation, notes, thoughts, or tags.\n\n" + paper_summary
            )}]
        )
        return clean_output(response)

    def review_quality(self, summary):
        response = self.quality_review_agent.generate_reply(
            messages=[{"role": "user", "content": (
                "Review the quality of this paper. Use a formal academic tone. Avoid internal thoughts, reasoning steps, or '<think>' tags.\n\n" + summary
            )}]
        )
        return clean_output(response)

    def recommend_topics(self, summary):
        response = self.recommendation_agent.generate_reply(
            messages=[{"role": "user", "content": (
                "Recommend related research topics or papers based on the following summary. Do not include internal thoughts, reasoning, or '<think>' tags.\n\n" + summary
            )}]
        )
        return clean_output(response)

    def generate_new_paper(self, combined_summaries):
        prompt = (
            "Based on the following summaries of recent research papers, generate a new IEEE-style research paper.\n"
            "Use standard academic English and passive voice. Include the following sections:\n"
            "- Title\n"
            "- Abstract\n"
            "- Keywords\n"
            "- Introduction\n"
            "- Related Work\n"
            "- Methodology (use bullet points)\n"
            "- Experimental Results\n"
            "- Discussion\n"
            "- Conclusion and Future Work\n"
            "Ensure paragraphs are justified. Format and tone must match IEEE publication standards.\n"
            "Do not include internal thoughts, reasoning, or tags like '<think>'.\n\n"
            f"{combined_summaries}"
        )
        try:
            response = self.summarizer_agent.generate_reply(
                messages=[{"role": "user", "content": prompt}]
            )
            return clean_output(response)
        except Exception as e:
            print(f"[ERROR] LLM generation failed: {e}")
            return "Paper generation failed due to internal error."