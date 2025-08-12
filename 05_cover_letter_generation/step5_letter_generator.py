import os
import sys
import json
from typing import Dict

# Add project root to path to allow imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.AzureConnection import client
from step5_rag_retriever import CandidateRetriever
from step5_prompts import SYSTEM_PROMPT, COVER_LETTER_PROMPT

class CoverLetterGenerator:
    """
    Orchestrates the generation of the cover letter by combining RAG and LLM synthesis.
    """
    def __init__(self, candidate_retriever: CandidateRetriever, llm_client):
        """
        Initializes the generator.

        Args:
            candidate_retriever (CandidateRetriever): An instance of the retriever for the candidate's vector store.
            llm_client: The client for interacting with the LLM.
        """
        self.retriever = candidate_retriever
        self.llm = llm_client

    def generate(self, summary_data: Dict) -> str:
        """
        Generates the full cover letter.

        Args:
            summary_data (Dict): The structured JSON summary from Step 4.

        Returns:
            str: The generated cover letter text.
        """
        # 1. Extract key terms from the summary to use as queries for RAG
        print("Extracting key terms for RAG queries...")
        required_skills = summary_data.get("position_details", {}).get("required_skills", [])
        preferred_exp = summary_data.get("position_details", {}).get("preferred_experience", [])
        project_summary = summary_data.get("position_details", {}).get("project_summary", "")
        
        # Combine into a list of queries for the retriever
        queries = list(set(required_skills + preferred_exp))
        if project_summary:
            queries.append(f"My experience related to: {project_summary}")

        # 2. Retrieve evidence from the candidate's resume
        candidate_evidence = self.retriever.get_candidate_evidence(queries)

        # 3. Construct the final prompt for the LLM
        print("Constructing final prompt for LLM...")
        # Convert the summary dict back to a formatted string for the prompt
        supervisor_summary_str = json.dumps(summary_data, indent=2)

        user_prompt = COVER_LETTER_PROMPT.format(
            supervisor_summary=supervisor_summary_str,
            candidate_evidence=candidate_evidence
        )

        # 4. Call the LLM to generate the cover letter
        print("Generating cover letter... This may take a moment.")
        try:
            response = self.llm.chat.completions.create(
                model="DevGPT4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7, # Higher temperature for more creative writing
                max_tokens=2000
            )
            cover_letter = response.choices[0].message.content.strip()
            print("Successfully generated cover letter.")
            return cover_letter
        except Exception as e:
            print(f"An error occurred during LLM call: {e}")
            return "Error: Could not generate cover letter."
