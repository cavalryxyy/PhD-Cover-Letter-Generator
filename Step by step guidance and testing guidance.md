# **README: Detailed Workflow for PhD Cover Letter Generator - LLM part**

## **1\. Overview**

This document provides a granular, step-by-step technical guide for the AI-Powered Cover Letter Generator.

## **2\. Detailed Architecture & Workflow**

The workflow is a multi-stage pipeline that combines data processing, retrieval, and generation. Each step builds upon the last to create a final product that is accurate, personalized, and compelling.

### **High-Level Architecture Flow**

\[Step 0: Initial Input\]  
     |  
     V  
\[Step 1: PDF Processing & Vectorization\] \-\> (Data Processing)  
     |  
     V  
\[Step 2: Candidate Data Ingestion\] \-\> (Data Processing)  
     |  
     V  
\[Step 3: Supervisor Research Analysis\] \-\> (Agentic Call: RAG \+ Web Search)  
     |  
     V  
\[Step 4: Professional Summary Generation\] \-\> (LLM Prompt)  
     |  
     V  
\[Step 5: Cover Letter Generation\] \-\> (LLM Prompt with RAG)  
     |  
     V  
\[Step 6: Iterative Refinement\] \-\> (LLM Prompt)  
     |  
     V  
\[Final Output: Cover Letter\]

## **3\. Step-by-Step Implementation Guide**

### **Step 0: Initial Input**

* **Type:** Manual Data Collection  
* **Goal:** Gather all necessary source materials.  
* **Action:** The user provides the required files.  
* **Input:**  
  1. resume.json: The candidate's personal resume in a structured JSON format.  
  2. university\_profile.pdf: Document describing the university and department.  
  3. supervisor\_profile.pdf: Document with the professor's details and research interests.  
  4. program\_directions.pdf: Document outlining the PhD program's focus areas.  
* **Output:** Raw files ready for processing.

### **Step 1: PDF Processing & Vectorization**

* **Type:** Data Processing / Data Ingestion  
* **Goal:** To make the content of the PDF documents searchable and accessible for the RAG system.  
* **Action:**  
  1. Use a library (e.g., PyMuPDF) to extract raw text from the three PDF files.  
  2. Perform basic data cleaning on the extracted text (e.g., remove strange characters, fix broken line breaks).  
  3. Chunk the cleaned text into smaller, semantically coherent segments (e.g., 500 tokens per chunk with some overlap).  
  4. Use a text-embedding model to convert each text chunk into a numerical vector.  
  5. Store these vectors, along with their source document metadata, in a Vector Database (e.g., FAISS, ChromaDB).  
* **Input:** university\_profile.pdf, supervisor\_profile.pdf, program\_directions.pdf.  
* **Output:** A populated and indexed Vector Database.

### **Step 2: Candidate Data Ingestion**

* **Type:** Data Processing  
* **Goal:** To parse and prepare the candidate's personal data for use in prompts.  
* **Action:** Load the resume.json file into a structured object or dictionary that can be easily serialized into a string for the LLM prompt.  
* **Input:** resume.json.  
* **Output:** A clean, string-formatted version of the candidate's resume (candidate\_profile\_string).

### **Step 3: Supervisor Research Analysis**

* **Type:** Agentic Call (RAG \+ Web Search)  
* **Goal:** To gather the most current and comprehensive information on the supervisor's research, overcoming the limitations of potentially stale PDFs.  
* **Action:**  
  1. The system triggers an agent with the high-level query: "Find the latest and most significant academic achievements of Professor \[Name\] from \[University\]."  
  2. The agent first uses its **RAG tool** to perform a similarity search on the Vector Database (from Step 1\) to find relevant info in the provided PDFs.  
  3. The agent then uses its **Web Search tool** to query academic portals (e.g., Google Scholar, Semantic Scholar) for recent papers, talks, or grants associated with the professor.  
  4. The agent synthesizes the findings from both tools into a single, consolidated context block.  
* **Input:** Professor's Name and University (extracted from supervisor\_profile.pdf or user input).  
* **Output:** A single text block (consolidated\_supervisor\_context) containing both foundational information from the PDFs and cutting-edge information from the web.

### **Step 4: Professional Summary Generation**

* **Type:** LLM Prompt  
* **Goal:** To distill the raw data from the previous step into a structured, verifiable summary.  
* **Action:** The system feeds the consolidated\_supervisor\_context into the "Supervisor Analysis & Professional Summary" prompt (from the Prompt Pipeline document). The LLM executes the instructions to identify themes and list achievements with citations.  
* **Input:** consolidated\_supervisor\_context.  
* **Output:** A structured text block containing the "Key Research Themes," "Cutting-Edge Achievements," and "Objective Summary" (supervisor\_summary\_output).

### **Step 5: Cover Letter Generation**

* **Type:** LLM Prompt with RAG  
* **Goal:** To draft the complete, personalized cover letter.  
* **Action:**  
  1. The system performs one final RAG query on the Vector Database to retrieve specific context about the university and program philosophy (using a query like "university research mission" or "doctoral program structure").  
  2. The system assembles the final, comprehensive prompt using the "Cover Letter Generation" template.  
* **Input:**  
  1. candidate\_profile\_string (from Step 2).  
  2. supervisor\_summary\_output (from Step 4).  
  3. Retrieved context about the program and university (from the RAG query in this step).  
* **Output:** The first full draft of the cover letter (cover\_letter\_draft\_v1).

### **Step 6: Iterative Refinement**

* **Type:** LLM Prompt  
* **Goal:** To allow the user to fine-tune the generated draft.  
* **Action:**  
  1. The cover\_letter\_draft\_v1 is presented to the user.  
  2. The user provides feedback in natural language (e.g., "Make the second paragraph more concise").  
  3. The system uses the "Supplemental Prompt for Iterative Refinement" template, feeding it both the original draft and the user's feedback.  
  4. This process can be repeated until the user is satisfied.  
* **Input:** The current cover letter draft and a user feedback string.  
* **Output:** A revised cover letter draft (cover\_letter\_draft\_v2, v3, etc.).