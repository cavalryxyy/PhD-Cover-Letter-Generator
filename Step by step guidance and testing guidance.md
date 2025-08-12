# **README: Detailed Workflow for PhD Cover Letter Generator**

## **1. Overview**

This document provides a granular, step-by-step technical guide for the AI-Powered Cover Letter Generator.

## **2. Detailed Architecture & Workflow**

The workflow is a multi-stage pipeline that combines data processing, retrieval-augmented generation (RAG), and language model synthesis. Each step is designed to be a modular component that processes specific inputs and produces outputs for the next stage.

### **High-Level Architecture Flow**

[Step 1: Gather Inputs]
     |
     V
[Step 2: Candidate Resume Processing] --> (Creates & Saves Candidate Vector Store)
     |
     V
[Step 3: Supervisor Research Analysis] --> (Uses Position PDF for RAG)
     |
     V
[Step 4: Professional Summary Generation] --> (Creates & Saves Structured JSON Summary)
     |
     V
[Step 5: Cover Letter Generation] --> (Future - Uses Candidate & Supervisor Summaries)
     |
     V
[Final Output: Cover Letter]

## **3. Step-by-Step Implementation Guide**

### **Step 1: Gather Inputs**

*   **Status:** Prerequisite
*   **Type:** Manual Data Collection
*   **Goal:** Gather all necessary source materials for the pipeline.
*   **Action:** The user must provide two key PDF documents in the `data/` directory.
*   **Input:**
    1.  `data/candidate/resume.pdf`: The candidate's personal resume.
    2.  `data/institutional/position.pdf`: The official description of the PhD position.
*   **Output:** Raw files ready for processing.

### **Step 2: Candidate Resume Processing**

*   **Status:** ? **Implemented**
*   **Type:** Data Processing / Vector Store Creation
*   **Goal:** To process the candidate's resume and create a persistent, searchable knowledge base for later use.
*   **Action:**
    1.  The `02_candidate_analysis/step2_main.py` script is executed.
    2.  It reads the `resume.pdf` provided by the user.
    3.  The text is extracted, cleaned, and split into semantically coherent chunks.
    4.  Each chunk is converted into a numerical vector using an embedding model.
    5.  The vectors are stored in a FAISS index.
    6.  The completed FAISS index is saved to disk at `vector_stores/candidate_vector_store.faiss`.
*   **Input:** `resume.pdf` file path.
*   **Output:** A persistent FAISS vector store representing the candidate's profile.

### **Step 3: Supervisor Research Analysis**

*   **Status:** ? **Implemented**
*   **Type:** Agentic Call (RAG + Web Search)
*   **Goal:** To generate a deep, context-aware profile of a potential supervisor.
*   **Action:**
    1.  The `03_supervisor_analysis/step3_main.py` script is executed.
    2.  It uses its **Web Search tool** to scrape the supervisor's online profile and identify key research domains.
    3.  It then processes the `position.pdf` in-memory, creating a temporary **Institutional Vector Store**.
    4.  The script uses its **RAG tool** to query this institutional store with the domains found online, retrieving the most relevant context.
    5.  An LLM synthesizes the findings from both the web and the document into a comprehensive analysis.
*   **Input:** Professor's Name, University, Publication URL, and the path to `position.pdf`.
*   **Output:** A detailed text file (`step3_detailed_...`) containing the synthesized analysis.

### **Step 4: Professional Summary Generation**

*   **Status:** ? **Implemented**
*   **Type:** LLM Distillation
*   **Goal:** To distill the raw analysis from Step 3 into a structured, actionable JSON summary.
*   **Action:**
    1.  The `04_professional_summary/step4_main.py` script is executed.
    2.  It takes the text output file from Step 3 as input.
    3.  It uses a specifically crafted prompt to ask an LLM to extract key details and structure them.
    4.  The LLM returns a JSON object containing the supervisor's profile, position details, and key alignment points.
    5.  The script saves this JSON to the `outputs/step4/` directory.
*   **Input:** The output text file path from Step 3.
*   **Output:** A structured JSON file (`summary_... .json`) ready for Step 5.

### **Step 5: Cover Letter Generation (Future)**

*   **Status:** ?? Future Work
*   **Type:** LLM Prompt with RAG
*   **Goal:** To draft the complete, personalized cover letter.
*   **Action:** This step will load the **saved candidate vector store** (from Step 2) and the **structured supervisor summary** (from Step 4) to perform RAG queries and generate a highly personalized and targeted cover letter.
*   **Input:**
    1.  The candidate vector store.
    2.  The structured supervisor summary from Step 4.
*   **Output:** The first full draft of the cover letter.