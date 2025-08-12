import os
import sys
import json
import argparse
from datetime import datetime

# Add project root to path to allow imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Add the module's own directory to the path
module_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, module_dir)

from src.AzureConnection import client, embeddings
from step5_rag_retriever import CandidateRetriever
from step5_letter_generator import CoverLetterGenerator
from src.token_tracker import TokenUsageTracker

def main():
    """
    Main function to execute the cover letter generation step.
    """
    parser = argparse.ArgumentParser(description="Generate a cover letter using a professional summary and a candidate vector store.")
    parser.add_argument("summary_file_path", type=str, help="The path to the structured summary JSON file from Step 4.")
    args = parser.parse_args()

    # --- 1. Load Inputs ---
    if not os.path.exists(args.summary_file_path):
        print(f"Error: The summary file '{args.summary_file_path}' does not exist.")
        sys.exit(1)
        
    with open(args.summary_file_path, 'r', encoding='utf-8') as f:
        summary_data = json.load(f)

    vector_store_path = os.path.join(project_root, "vector_stores", "candidate_vector_store.faiss")
    if not os.path.isdir(vector_store_path):
        print(f"Error: The candidate vector store was not found at '{vector_store_path}'.")
        print("Please run Step 2 to generate it first.")
        sys.exit(1)

    # --- 2. Initialize Components ---
    try:
        token_tracker = TokenUsageTracker()
        candidate_retriever = CandidateRetriever(
            vector_store_path=vector_store_path,
            embeddings_client=embeddings
        )
        letter_generator = CoverLetterGenerator(
            candidate_retriever=candidate_retriever,
            llm_client=client,
            token_tracker=token_tracker
        )
    except Exception as e:
        print(f"Error initializing components: {e}")
        sys.exit(1)

    # --- 3. Generate the Cover Letter ---
    cover_letter_text = letter_generator.generate(summary_data)

    # --- 4. Save the Output ---
    if "Error:" not in cover_letter_text:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        supervisor_name = summary_data.get("supervisor_profile", {}).get("name", "UnknownSupervisor").replace(" ", "_")
        output_filename = f"Cover_Letter_for_{supervisor_name}_{timestamp}.txt"
        output_path = os.path.join(project_root, "outputs", "step5", output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cover_letter_text)

        print(f"\nSuccessfully saved cover letter to: '{output_path}'")
        token_tracker.display_usage()
    else:
        print("\nCould not generate the cover letter due to an error.")

if __name__ == "__main__":
    main()
