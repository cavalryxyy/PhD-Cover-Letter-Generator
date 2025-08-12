This code repository serves as a template for learning LLM RAG (Retrieval-Augmented Generation) technology and establishing a pipeline workflow. Since the materials required for this project are all publicly available (e.g., PhD positions, university information, and professor profiles), no additional web scraping techniques are necessary. Additionally, due to its low token consumption, this project is particularly suitable for beginners in LLM to practice building pipeline workflows.

What You'll Learn
By exploring this repository, you will learn how to:
Structure a Multi-Step AI Pipeline: Decouple complex tasks into manageable, reusable steps.
Implement a RAG System: Use FAISS and LangChain to create a vector store from your own documents.
Orchestrate LLM Calls: Build a scalable pattern for managing prompts and interacting with models.(You need lisenced LLM and manage them like I did in /src/AzureConnection.py with your personal api code and endpint to test this project).
Manage Project Dependencies: Set up a clean, reproducible environment for an AI project.

PS: 
You need lisenced LLM and config them in /src/AzureConnection.py with your personal api code and endpint to test this project.
If you have any question (sensitive information regarding the repo/collobration) you can reach me via xuyuanyuan102888@outlook.com / WeChat: 15600159007.

**Disclaimer**: No specific professor names, position titles, or resume details will be included in the code repository.
This is a public educational template. As such, no private or specific data (e.g., real professor names, actual resume details) is included in the repository. You are encouraged to use your own publicly available documents to test the pipeline. 

---

# PhD Cover Letter Generator

**AI-Powered Pipeline for Academic Applications**

## 📂 **Project Structure**

```
PhD-Cover-Letter-Generator/
├── src/
│   ├── AzureConnection.py        # 🔑 Azure LLM & Embedding connections
│   └── token_tracker.py          # 📊 Token usage tracking utility
├── 02_candidate_analysis/        # Step 2: Candidate Resume Processing
│   ├── step2_main.py             # Main entry point for Step 2
│   └── step2_candidate_processor.py # Logic for creating candidate vector store
├── 03_supervisor_analysis/       # Step 3: Supervisor Research Analysis
│   ├── step3_main.py             # Main entry point for Step 3
│   ├── base_analyzer.py          # Abstract base class for LLM logic
│   ├── step3_orchestrator.py     # Analysis orchestration
│   ├── step3_web_searcher.py     # Web scraping logic
│   ├── step3_document_processor.py # PDF processing & RAG
│   └── step3_prompts.py          # Prompt management
├── 04_professional_summary/      # Step 4: Professional Summary Generation
│   ├── step4_main.py             # Main entry point for Step 4
│   ├── step4_summary_generator.py # Logic for generating the summary
│   └── step4_prompts.py          # Prompt management for summary
├── diagrams/                     # 📈 Visual Workflows & Architecture
│   └── step3_data_flow.mmd       # Detailed data flow for Step 3
├── vector_stores/                # 💾 Saved FAISS vector stores
│   └── (candidate_vector_store.faiss/)
├── data/                         # 📄 User-provided input documents
│   ├── candidate/
│   └── institutional/
├── outputs/                      # 📂 Generated outputs from the pipeline
│   ├── step3/
│   └── step4/
└── requirements.txt              # 📦 Project dependencies
```

## 🚀 **Quick Start**

### **1. Setup**
```bash
# Activate your conda environment
conda activate gen_ai

# Install dependencies
pip install -r requirements.txt
```
*Note: `faiss-cpu` is included in `requirements.txt`.*

### **2. Run Step 2: Process Your Resume**
This step only needs to be run once to create your candidate profile.
```bash
python 02_candidate_analysis/step2_main.py "data/candidate/resume.pdf"
```

### **3. Run Step 3: Analyze a Supervisor**
```bash
python 03_supervisor_analysis/step3_main.py "Professor Name" "University" "Publication URL" "data/institutional/position.pdf"
```

## 📈 **Visual Workflows**

All project diagrams are stored in the `diagrams/` folder. They are written in Mermaid format (`.mmd`) and can be viewed with the [Mermaid Live Editor](https://mermaid.live/) or a compatible IDE extension.

## 🛠️ **Technologies Used**

- **LLM**: Azure OpenAI (DevGPT-4o)
- **RAG**: FAISS vector store + Azure Embeddings
- **PDF Processing**: PyMuPDF + LangChain
- **Web Scraping**: Requests + BeautifulSoup
- **Environment**: Conda (`gen_ai`)

## 📋 **Pipeline Steps**

- ✅ **Step 2**: Candidate Resume Analysis (Complete)
- ✅ **Step 3**: Supervisor Research Analysis (Complete)
- ✅ **Step 4**: Professional Summary Generation (Complete)
- ➡️ **Next**: Step 5 (Cover Letter Generation)

## ✨ **Current Status**

The foundational multi-step pipeline is complete and operational. The system can successfully process a candidate's resume, perform a detailed, RAG-powered analysis on a potential supervisor, and distill that analysis into a structured summary. The architecture is now modular and scalable, providing a clear blueprint for future steps.
