# FILE: 03_supervisor_analysis/base_analyzer.py
# PURPOSE: To provide a base class for analysis components that interact with LLMs.

from abc import ABC, abstractmethod
from typing import Dict
from step3_prompts import PromptManager
from src.token_tracker import TokenUsageTracker

class BaseAnalyzer(ABC):
    """
    An abstract base class for analyzers that execute LLM calls.
    """
    def __init__(self, llm_client, token_tracker: TokenUsageTracker):
        """
        Initializes the BaseAnalyzer.

        Args:
            llm_client: The client for interacting with the Large Language Model.
            token_tracker: An instance of TokenUsageTracker.
        """
        self.llm_client = llm_client
        self.token_tracker = token_tracker

    def _execute_llm_call(self, prompt_manager: PromptManager, **kwargs) -> str:
        """
        Executes a call to the LLM using a structured prompt from the PromptManager.

        Args:
            prompt_manager (PromptManager): The prompt manager instance containing the templates.
            **kwargs: The variables to format the user prompt template.

        Returns:
            str: The cleaned content from the LLM's response.
        """
        user_prompt = prompt_manager.format_user_prompt(**kwargs)
        
        response = self.llm_client.chat.completions.create(
            model="DevGPT4o",
            messages=[
                {"role": "system", "content": prompt_manager.system_instruction},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        # Track completion tokens
        if response.usage:
            self.token_tracker.add_completion_usage(response.usage)
            
        return response.choices[0].message.content.strip()

    @abstractmethod
    def analyze(self, *args, **kwargs) -> Dict:
        """
        This method must be implemented by subclasses to perform the specific analysis.
        """
        pass
