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
├── main_pipeline.py              # 🚀 Complete pipeline orchestrator (Steps 2-5)
├── src/
│   ├── AzureConnection.py        # 🔑 Azure LLM & Embedding connections
│   └── token_tracker.py          # 📊 Token usage tracking utility
├── 02_candidate_analysis/        # Step 2: Candidate Resume Processing
│   ├── step2_main.py             # Main entry point for Step 2
│   ├── step2_candidate_processor.py # Logic for creating candidate vector store
│   └── README.md                 # Step 2 documentation
├── 03_supervisor_analysis/       # Step 3: Supervisor Research Analysis
│   ├── step3_main.py             # Main entry point for Step 3
│   ├── base_analyzer.py          # Abstract base class for LLM logic
│   ├── step3_orchestrator.py     # Analysis orchestration
│   ├── step3_web_searcher.py     # Web scraping logic
│   ├── step3_document_processor.py # PDF processing & RAG
│   ├── step3_prompts.py          # Prompt management
│   └── README.md                 # Step 3 documentation
├── 04_professional_summary/      # Step 4: Professional Summary Generation
│   ├── step4_main.py             # Main entry point for Step 4
│   ├── step4_summary_generator.py # Logic for generating the summary
│   ├── step4_prompts.py          # Prompt management for summary
│   └── README.md                 # Step 4 documentation
├── 05_cover_letter_generation/   # Step 5: Final Cover Letter Generation
│   ├── step5_main.py             # Main entry point for Step 5
│   ├── step5_letter_generator.py # Logic for RAG and LLM synthesis
│   ├── step5_rag_retriever.py    # Logic for querying the candidate vector store
│   ├── step5_prompts.py          # Prompts for the cover letter
│   └── README.md                 # Step 5 documentation
├── diagrams/                     # 📈 Visual Workflows & Architecture
│   ├── step2_data_flow.mmd       # Step 2 data flow diagram
│   ├── step3_data_flow.mmd       # Step 3 data flow diagram
│   ├── step4_data_flow.mmd       # Step 4 data flow diagram
│   ├── step5_data_flow.mmd       # Step 5 data flow diagram
│   ├── pipeline_visualization.html # Complete interactive pipeline
│   └── README.md                 # Diagram documentation
├── vector_stores/                # 💾 Saved FAISS vector stores
│   └── (candidate_vector_store.faiss/)
├── data/                         # 📄 User-provided input documents
│   ├── candidate/
│   └── institutional/
├── outputs/                      # 📂 Generated outputs from the pipeline
│   ├── step2/                    # Vector stores from candidate analysis
│   ├── step3/                    # Supervisor analysis results
│   ├── step4/                    # Professional summaries (JSON)
│   └── step5/                    # Final cover letters
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

### **2. Configure Azure Connections**
Update `/src/AzureConnection.py` with your Azure OpenAI API credentials:
- LLM API key and endpoint
- Embedding API key and endpoint

### **3. Run Complete Pipeline**
Execute all steps (2-5) in one command:
```bash
python main_pipeline.py "path/to/resume.pdf" "Professor Name" "University Name" "https://professor-profile-url.edu" "path/to/position.pdf"
```

**Example:**
```bash
python main_pipeline.py "data/candidate/resume.pdf" "Prof. Jane Doe" "MIT" "https://web.mit.edu/~janedoe" "data/institutional/position.pdf"
```

### **4. Run Individual Steps (Optional)**
You can also run steps individually:

**Step 2: Process Resume**
```bash
python 02_candidate_analysis/step2_main.py "data/candidate/resume.pdf"
```

**Step 3: Analyze Supervisor**
```bash
python 03_supervisor_analysis/step3_main.py "Professor Name" "University" "Publication URL" "data/institutional/position.pdf"
```

**Step 4: Generate Professional Summary**
```bash
python 04_professional_summary/step4_main.py "outputs/step3/step3_clean_*.txt"
```

**Step 5: Generate Cover Letter**
```bash
python 05_cover_letter_generation/step5_main.py "outputs/step4/summary_*.json"
```

## 📈 **Visual Workflows**

Complete technical diagrams are available in the `diagrams/` folder:
- **Individual Step Diagrams**: `step2_data_flow.mmd` through `step5_data_flow.mmd`
- **Interactive Overview**: `pipeline_visualization.html` (open in browser)
- **Viewing**: Use [Mermaid Live Editor](https://mermaid.live/) for `.mmd` files

Each step includes comprehensive documentation in its respective `README.md` file.

## 🛠️ **Technologies Used**

- **LLM**: Azure OpenAI (DevGPT-4o)
- **RAG**: FAISS vector store + Azure Embeddings
- **PDF Processing**: PyMuPDF + LangChain
- **Web Scraping**: Requests + BeautifulSoup
- **Environment**: Conda (`gen_ai`)

## 📋 **Pipeline Steps**

- ✅ **Step 2**: Candidate Resume Analysis - Creates vector store from resume
- ✅ **Step 3**: Supervisor Research Analysis - Web scraping + RAG analysis
- ✅ **Step 4**: Professional Summary Generation - Structured JSON summary
- ✅ **Step 5**: Cover Letter Generation - RAG-powered personalized letter
- ✅ **Main Pipeline**: Complete orchestrator with error handling and logging
- ✅ **Token Tracking**: Comprehensive usage monitoring across all steps

## 📊 **Token Usage Tracking**

The system includes comprehensive token tracking across all components:
- **Embedding Tokens**: Vector store creation and document processing
- **LLM Prompt Tokens**: Input tokens for all language model calls
- **LLM Completion Tokens**: Generated output tokens
- **Total Usage**: Complete pipeline consumption summary

## ✨ **Current Status**

**🎉 PRODUCTION READY** - The complete AI-powered pipeline is fully operational with:

- **End-to-End Automation**: Single command execution of all 4 steps
- **Robust Error Handling**: Comprehensive validation and error recovery
- **Token Optimization**: Efficient usage monitoring and optimization
- **Modular Architecture**: Each step can be run independently or as part of the complete pipeline
- **Professional Output**: High-quality, personalized cover letters ready for academic applications

**Performance**: Typical execution time is 30-45 seconds for complete pipeline including LLM calls, embeddings, and RAG retrieval.

## 🔧 **Output Files**

The pipeline generates organized outputs in the `outputs/` directory:
- **Step 2**: FAISS vector stores for candidate analysis
- **Step 3**: Clean analysis (for Step 4) + detailed analysis (for review)
- **Step 4**: Structured JSON summaries with supervisor insights
- **Step 5**: Professional cover letters ready for submission
