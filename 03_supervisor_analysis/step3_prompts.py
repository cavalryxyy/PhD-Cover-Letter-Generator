# FILE: 03_supervisor_analysis/step3_prompts.py
# PURPOSE: To store and manage structured prompts for LLM interaction.

import textwrap
from langchain.prompts import PromptTemplate

class PromptManager:
    """A class to manage a structured prompt, including system and user messages."""
    def __init__(self, system_instruction: str, user_template: str, input_variables: list):
        """
        Initializes the PromptManager.

        Args:
            system_instruction (str): The instruction for the system role.
            user_template (str): The template for the user role message.
            input_variables (list): A list of input variables for the user template.
        """
        self.system_instruction = textwrap.dedent(system_instruction)
        self.user_prompt_template = PromptTemplate(
            template=textwrap.dedent(user_template),
            input_variables=input_variables
        )

    def format_user_prompt(self, **kwargs) -> str:
        """Formats the user prompt template with the given inputs."""
        return self.user_prompt_template.format(**kwargs)

# --- Prompt Definitions ---

SUPERVISOR_SYNTHESIS_PROMPT = PromptManager(
    system_instruction="""
        You are a highly capable research analyst AI. Your task is to synthesize information about a professor's research profile.
        Combine the following pieces of context into a single, coherent, and comprehensive summary detailing the research profile of the professor.
        Focus on integrating the findings smoothly. The final output should be a single block of text.
    """,
    user_template="""
        **Institutional Document Context:**
        {rag_context}

        **Professor's Research Domains:**
        {research_domains}

        **Synthesized Research Profile for {professor_name}:**
    """,
    input_variables=["rag_context", "research_domains", "professor_name"]
)
