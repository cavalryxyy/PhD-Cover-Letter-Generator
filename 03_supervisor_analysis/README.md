# 03_supervisor_analysis

**Step 3: Supervisor Research Analysis Pipeline**

## 🚀 **Usage**

```bash
python 03_supervisor_analysis/step3_main.py "Professor Name" "University" "URL" "path/to/resume.pdf" "path/to/position.pdf"
```

## 📁 **Pipeline Components**

```
03_supervisor_analysis/
├── step3_main.py             # Main entry point & DI
├── base_analyzer.py          # Abstract base class for LLM logic
├── step3_orchestrator.py     # Analysis orchestration
├── step3_web_searcher.py     # Web scraping
├── step3_document_processor.py # PDF processing & RAG
└── step3_prompts.py          # Prompt management
```

## 📋 **Requirements**

### Input Data
The script requires paths to the following two PDF files as command-line arguments:
- Your resume/CV
- The official PhD position description

### Environment
- **Conda Environment**: `gen_ai`
- **Dependencies**: FAISS, OpenAI, LangChain
- **Azure Connections**: Must be configured in `AzureConnection.py` at the project root.

## 📊 **Output**

The pipeline generates two timestamped files:
1.  `step3_clean_[Professor]_[timestamp].txt`: A clean summary suitable for use in later steps.
2.  `step3_detailed_[Professor]_[timestamp].txt`: A comprehensive analysis including raw data for review.

## 🔄 **Detailed Workflow**

See the **[Step 3 Data Flow Diagram](../diagrams/step3_data_flow.mmd)** for a complete visualization of the architecture, including:
- 📊 Step-by-step data flow
- 🔧 Component responsibilities
- 🎯 The RAG retrieval process
- 🤖 The LLM synthesis workflow

**Ready for Step 4: Professional Summary Generation**
