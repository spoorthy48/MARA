from autogen import AssistantAgent
import os
from dotenv import load_dotenv

load_dotenv()

class ResearchAgents:
    def __init__(self, api_key):
        self.groq_api_key = api_key
        self.llm_config = {
            'config_list': [{
                'model': 'deepseek-r1-distill-qwen-32b',
                'api_key': self.groq_api_key,
                'api_type': "groq"
            }]
        }

        self.summarizer_agent = AssistantAgent(
            name="summarizer_agent",
            system_message="Summarize the retrieved research papers and present concise summaries.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        self.advantages_disadvantages_agent = AssistantAgent(
            name="advantages_disadvantages_agent",
            system_message="Provide advantages and disadvantages in a pointwise format.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

    def summarize_paper(self, paper_summary):
        response = self.summarizer_agent.generate_reply(
            messages=[{"role": "user", "content": f"Summarize this paper: {paper_summary}"}]
        )
        return response.get("content", "Summarization failed!") if isinstance(response, dict) else str(response)

    def analyze_advantages_disadvantages(self, summary):
        response = self.advantages_disadvantages_agent.generate_reply(
            messages=[{"role": "user", "content": f"Provide advantages and disadvantages for this paper: {summary}"}]
        )
        return response.get("content", "Analysis failed!") if isinstance(response, dict) else str(response)
