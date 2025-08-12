import os
import sys
import json
import argparse
from datetime import datetime

# Add the project root and current directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
module_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, module_dir)

from step4_summary_generator import SummaryGenerator

def main():
    """
    Main function to execute the professional summary generation step.
    """
    parser = argparse.ArgumentParser(description="Generate a professional summary from a detailed analysis file.")
    parser.add_argument("analysis_file_path", type=str, help="The path to the detailed analysis text file from Step 3.")
    args = parser.parse_args()

    if not os.path.exists(args.analysis_file_path):
        print(f"Error: The file '{args.analysis_file_path}' does not exist.")
        sys.exit(1)

    with open(args.analysis_file_path, 'r', encoding='utf-8') as f:
        analysis_text = f.read()

    summary_generator = SummaryGenerator()
    professional_summary = summary_generator.generate_summary(analysis_text)

    if professional_summary:
        # Create a structured filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        supervisor_name = professional_summary.get("supervisor_profile", {}).get("name", "UnknownSupervisor").replace(" ", "_")
        output_filename = f"summary_{supervisor_name}_{timestamp}.json"
        output_path = os.path.join(project_root, "outputs", "step4", output_filename)

        # Save the structured summary to a file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(professional_summary, f, indent=4)

        print(f"Successfully saved professional summary to '{output_path}'")

if __name__ == "__main__":
    main()
