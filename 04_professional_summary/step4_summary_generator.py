import os
import sys
import json

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.AzureConnection import client
from step4_prompts import PROFESSIONAL_SUMMARY_PROMPT, SYSTEM_PROMPT
from src.token_tracker import TokenUsageTracker

class SummaryGenerator:
    """
    Handles the generation of a structured professional summary from an unstructured analysis text.
    """
    def __init__(self, token_tracker: TokenUsageTracker):
        """
        Initializes the SummaryGenerator and sets the LLM client.
        
        Args:
            token_tracker: An instance of TokenUsageTracker.
        """
        self.llm = client
        self.token_tracker = token_tracker

    def generate_summary(self, analysis_text: str) -> dict:
        """
        Generates a structured summary using the LLM.

        Args:
            analysis_text: The unstructured text from the Step 3 analysis.

        Returns:
            A dictionary containing the structured summary.
        """
        print("Generating professional summary...")
        user_prompt = PROFESSIONAL_SUMMARY_PROMPT.format(analysis_text=analysis_text)

        try:
            response = self.llm.chat.completions.create(
                model="DevGPT4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Track token usage
            if response.usage:
                self.token_tracker.add_completion_usage(response.usage)
            
            response_content = response.choices[0].message.content.strip()
            # The LLM response might be wrapped in markdown ```json ... ```, so we clean it.
            if response_content.startswith("```json"):
                response_content = response_content[7:-4].strip()

            summary_json = json.loads(response_content)
            print("Successfully generated and parsed summary.")
            return summary_json
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from LLM response. Details: {e}")
            print(f"LLM Response was: {response_content}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during summary generation: {e}")
            return None
