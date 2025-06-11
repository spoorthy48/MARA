# Import BaseAgent from its module
from agents.base_agent import BaseAgent  # Adjust the path as necessary

class IeeeFormatter(BaseAgent):
    def __init__(self, name="ieee_formatter", llm=None, prompt_template=None):
        """
        Initializes the IeeeFormatter agent.

        Args:
        name (str): Name of the agent.
        llm (object): The language model to be used for text formatting.
        prompt_template (str): The template to format the raw content into IEEE style.
        """
        super().__init__(name)
        self.llm = llm
        self.prompt_template = prompt_template if prompt_template else self._default_prompt_template()

    def _default_prompt_template(self):
        """
        Returns the default prompt template for IEEE formatting if none is provided.

        Returns:
        str: The default IEEE paper formatting prompt template.
        """
        return """
        You are an academic research assistant tasked with formatting the following content into IEEE-style research paper format.
        Organize the text into the following sections:
        1. Abstract
        2. Introduction
        3. Related Work / Literature Survey
        4. Methodology
        5. Experiments & Results
        6. Future Work

        Ensure the output includes:
        - Proper section headers.
        - Clear, concise language, following IEEE standards.
        - No internal tags or metadata in the response.
        - The formatting should be in a clean, academic style.

        {text}
        """

    def run(self, input_data):
        """
        Takes in a dictionary with a 'text' key containing raw content, formats it, and returns the IEEE-style output.

        Args:
        input_data (dict): The input dictionary containing raw content under the 'text' key.

        Returns:
        str: The IEEE-formatted text.
        """
        raw_text = input_data.get("text", "")
        
        # Constructing the prompt to pass to the language model
        prompt = self.prompt_template.format(text=raw_text)
        
        # Calling the language model to generate IEEE-style formatted output
        response = self.llm(prompt)
        
        return response.strip()  # Ensure the output is clean without extra spaces
