# In this solution, we'll create a multi-file Python project.
# The following project structure is recommended.

# PROJECT STRUCTURE:
# /phd_cover_letter_generator/
# |
# |- data/
# |  |- resume.json
# |  |- university_profile.pdf
# |  |- ... (other PDFs)
# |
# |- main.py                 # Main script to run the workflow
# |- llm_core.py             # Handles all interactions with the LLM
# |- prompts.py              # Stores all prompt templates
# |- AzureConnection.py      # Your provided file for Azure connection
# |- config.py               # Stores API keys and endpoints (NEVER commit this file)
#

# ----------------------------------------------------------------------
# FILE: config.py
# ----------------------------------------------------------------------
# PURPOSE: To securely store credentials.
# IMPORTANT: Add this file to your .gitignore to avoid exposing secrets.

# Azure OpenAI credentials for Chat Completion Model
AZURE_API_KEY = "YOUR_AZURE_CHAT_API_KEY"  # Replace with your key
AZURE_ENDPOINT = "YOUR_AZURE_CHAT_ENDPOINT" # Replace with your endpoint
API_VERSION = "2024-02-01"

# ----------------------------------------------------------------------
# FILE: AzureConnection.py
# ----------------------------------------------------------------------
# This is your provided file. Place it in the project root.
# No changes are needed if it defines the AzureConnection class as provided.
# from openai import AzureOpenAI
# ... (rest of your file)

# ----------------------------------------------------------------------
# FILE: prompts.py
# ----------------------------------------------------------------------
# PURPOSE: To keep prompts separate from application logic for easy management.

# Prompt for Step 4: Professional Summary Generation
SUPERVISOR_SUMMARY_PROMPT = """
You are a research assistant specializing in academic analysis. Your task is to synthesize information about a professor to identify their core research contributions.

Analyze the provided context below, which includes information from a university profile and recent web search results.

**Context:**
```
{context}
```

**Your Task:**

1.  **Identify Key Research Themes:** List the 3-4 primary, recurring research themes in the professor's work.
2.  **List Cutting-Edge Achievements:** Identify the most significant and recent (last 3 years) publications or projects. For each, provide the following meta-information for verification:
    * Paper Title
    * Year of Publication
    * Conference or Journal Venue (e.g., NeurIPS, ICML, Nature)
3.  **Provide an Objective Summary:** Write a concise, professional paragraph (4-6 sentences) summarizing the professor's current research focus, key methodologies, and overall impact. This summary must be objective and based only on the provided context.

Do not include any information not present in the context. Structure your output clearly with the headings "Key Research Themes", "Cutting-Edge Achievements", and "Objective Summary".
"""

# Prompt for Step 5: Cover Letter Generation
COVER_LETTER_PROMPT = """
You are an expert academic career advisor. Your task is to draft a compelling, professional, and highly personalized cover letter for a PhD application in Computer Science.

You will be given three pieces of information: the candidate's resume, a summary of the target supervisor's research, and details about the doctoral program.

**1. Candidate Profile (from JSON Resume):**
```
{candidate_profile}
```

**2. Supervisor's Research Summary:**
```
{supervisor_summary}
```

**3. Doctoral Program & University Context:**
```
{program_context}
```

**Your Task:**

Draft a formal cover letter (approximately 400-500 words) adhering to the following structure and instructions:

* **Paragraph 1: Introduction.** State the purpose of the letter: applying to the PhD program in Computer Science at [University Name] for the [Start Term, e.g., Fall 2026] intake. Immediately express specific interest in working with Professor [Supervisor's Name]. Mention one key theme from their research summary that genuinely excites you.

* **Paragraph 2: Research & Skill Alignment.** This is the most critical paragraph. Select 2-3 of the candidate's most relevant skills or experiences from their resume. For each, create a direct and specific link to the supervisor's research. **Do not just state the skill.** Crucially, for at least one of the connections, propose a potential research direction or project idea. For example: "My experience in [Candidate Skill, e.g., 'optimizing distributed systems'] could be directly applied to your work on [Supervisor's Research, e.g., 'federated learning']. I am particularly interested in exploring how novel consensus algorithms could reduce communication overhead in your framework, potentially leading to..."

* **Paragraph 3: Broader Fit and Long-Term Goals.** Connect the candidate's background to the broader goals of the doctoral program and the university's research environment, using the provided context. Briefly mention how the program's resources or philosophy will support the candidate's long-term career aspirations (e.g., becoming a research scientist or professor).

* **Paragraph 4: Closing.** Reiterate your strong enthusiasm for the opportunity. Thank the professor for their time and consideration, and state your eagerness to discuss your application further.

Maintain a professional, confident, and respectful tone throughout.
"""

# Prompt for Step 6: Iterative Refinement
REFINEMENT_PROMPT = """
You are a writing assistant. You have already generated a draft of a cover letter. The user has provided feedback for revision.

**Original Cover Letter Draft:**
```
{original_draft}
```

**User's Revision Request:**
```
{user_feedback}
```

**Your Task:**

Revise the original cover letter draft based *only* on the user's feedback. Maintain the core structure and content of the letter unless the feedback explicitly asks to change it. Provide only the full text of the revised cover letter as your output.
"""

# ----------------------------------------------------------------------
# FILE: llm_core.py
# ----------------------------------------------------------------------
# PURPOSE: To encapsulate all LLM call logic.

import config
from AzureConnection import AzureConnection
from prompts import SUPERVISOR_SUMMARY_PROMPT, COVER_LETTER_PROMPT, REFINEMENT_PROMPT

class LLMOrchestrator:
    """
    Handles all communication with the Azure OpenAI service.
    """
    def __init__(self):
        # Initialize the connection using your AzureConnection class and config
        azure_conn = AzureConnection(
            api_key=config.AZURE_API_KEY,
            azure_endpoint=config.AZURE_ENDPOINT,
            api_version=config.API_VERSION
        )
        self.client = azure_conn.build_connection()

    def _make_llm_call(self, prompt, system_message="You are a helpful assistant."):
        """
        A generic method to make a call to the LLM.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4", # Or your preferred model deployment name
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=2048,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"An error occurred while calling the LLM: {e}")
            return None

    def generate_supervisor_summary(self, consolidated_context):
        """
        Executes Step 4: Generates a professional summary of the supervisor's work.
        """
        print("Step 4: Generating supervisor summary...")
        prompt = SUPERVISOR_SUMMARY_PROMPT.format(context=consolidated_context)
        return self._make_llm_call(prompt)

    def generate_cover_letter(self, candidate_profile, supervisor_summary, program_context):
        """
        Executes Step 5: Generates the full cover letter.
        """
        print("Step 5: Generating cover letter draft...")
        prompt = COVER_LETTER_PROMPT.format(
            candidate_profile=candidate_profile,
            supervisor_summary=supervisor_summary,
            program_context=program_context
        )
        return self._make_llm_call(prompt, system_message="You are an expert academic career advisor.")

    def refine_cover_letter(self, original_draft, user_feedback):
        """
        Executes Step 6: Refines the cover letter based on user feedback.
        """
        print("Step 6: Refining cover letter based on feedback...")
        prompt = REFINEMENT_PROMPT.format(
            original_draft=original_draft,
            user_feedback=user_feedback
        )
        return self._make_llm_call(prompt, system_message="You are a writing assistant.")

# ----------------------------------------------------------------------
# FILE: main.py
# ----------------------------------------------------------------------
# PURPOSE: To orchestrate the entire workflow from Step 3 onwards.

import json
from llm_core import LLMOrchestrator

# --- Helper Functions to Simulate Previous Steps ---

def load_candidate_profile(file_path="data/resume.json"):
    """
    Simulates Step 2: Loads the candidate's JSON resume into a string.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return json.dumps(data, indent=2)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        # Return a sample profile if file is missing
        return json.dumps({
            "name": "Jane Doe",
            "education": "M.S. in Computer Science, Tech University",
            "experience": "Research Assistant, AI Lab (2 years)",
            "skills": ["Python", "PyTorch", "Graph Neural Networks", "Distributed Systems"]
        }, indent=2)

def perform_agentic_research():
    """
    Simulates Step 3: An agentic call combining RAG and Web Search.
    In a real application, this would involve complex logic with LangChain/LlamaIndex agents.
    Here, we return a hardcoded string representing the synthesized findings.
    """
    print("Step 3: Simulating Agentic Call (RAG + Web Search)...")
    return """
    From supervisor_profile.pdf: Professor John Smith's lab at Prestige University focuses on large-scale machine learning and federated learning. His early work involved foundational algorithms for distributed optimization.
    From web search (NeurIPS 2023): Professor Smith recently published "Scalable and Privacy-Preserving Federated Learning for Medical Imaging," which proposes a novel differential privacy mechanism.
    From web search (ICML 2024): A new paper titled "Adaptive Communication Strategies for Heterogeneous Federated Networks" tackles the issue of non-IID data distribution, a key challenge in the field.
    """

def perform_rag_for_program():
    """
    Simulates the RAG query in Step 5 for program details.
    """
    print("Step 5 (sub-step): Simulating RAG query for program details...")
    return """
    The PhD program at Prestige University emphasizes interdisciplinary research and provides state-of-the-art computational resources. The program's mission is to train the next generation of researchers to tackle real-world problems with societal impact.
    """

def main():
    """
    Main function to run the cover letter generation workflow.
    """
    print("--- Starting PhD Cover Letter Generation Workflow ---")
    
    # Initialize the core LLM component
    orchestrator = LLMOrchestrator()

    # --- Step 3: Supervisor Research Analysis ---
    consolidated_supervisor_context = perform_agentic_research()
    if not consolidated_supervisor_context:
        print("Could not perform supervisor research. Exiting.")
        return

    # --- Step 4: Professional Summary Generation ---
    supervisor_summary = orchestrator.generate_supervisor_summary(consolidated_supervisor_context)
    if not supervisor_summary:
        print("Could not generate supervisor summary. Exiting.")
        return
    print("\n--- Generated Supervisor Summary ---\n")
    print(supervisor_summary)
    print("\n-------------------------------------\n")

    # --- Step 5: Cover Letter Generation ---
    candidate_profile = load_candidate_profile()
    program_context = perform_rag_for_program()
    
    cover_letter_draft = orchestrator.generate_cover_letter(
        candidate_profile=candidate_profile,
        supervisor_summary=supervisor_summary,
        program_context=program_context
    )
    if not cover_letter_draft:
        print("Could not generate cover letter. Exiting.")
        return
    print("\n--- Generated Cover Letter Draft (v1) ---\n")
    print(cover_letter_draft)
    print("\n----------------------------------------\n")

    # --- Step 6: Iterative Refinement ---
    while True:
        feedback = input("Provide feedback for revision, or type 'exit' to finish: ")
        if feedback.lower() == 'exit':
            break
        
        refined_draft = orchestrator.refine_cover_letter(
            original_draft=cover_letter_draft,
            user_feedback=feedback
        )
        
        if refined_draft:
            cover_letter_draft = refined_draft # Update the current draft
            print("\n--- Refined Cover Letter Draft ---\n")
            print(cover_letter_draft)
            print("\n---------------------------------\n")
        else:
            print("Failed to refine the draft.")

    print("--- Workflow Complete ---")

if __name__ == "__main__":
    main()
