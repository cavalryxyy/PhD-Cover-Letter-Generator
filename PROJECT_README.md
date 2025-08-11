# PhD Cover Letter Generator

**AI-Powered Pipeline for Academic Applications**

## ? **Project Structure**

```
PhD-Cover-Letter-Generator/
������ 03_supervisor_analysis/          # Step 3: Supervisor Research Analysis
��   ������ step3_main.py                # Main entry point
��   ������ step3_orchestrator.py        # Analysis logic
��   ������ step3_web_searcher.py        # Web scraping & search
��   ������ step3_document_processor.py  # PDF processing & RAG
��   ������ step3_prompts.py             # LLM prompts
��   ������ README.md                    # Usage instructions
��   ������ WORKFLOW.md                  # Technical workflow
������ diagrams/                        # ? Visual Workflows
��   ������ step3_workflow.mmd           # High-level data flow
��   ������ step3_detailed_architecture.mmd # Technical architecture
��   ������ README.md                    # Diagram documentation
������ data/                            # ? User Documents
��   ������ resume.pdf                   # Your resume
��   ������ [position].pdf               # Position descriptions
������ AzureConnection.py               # ?? Azure LLM connections
������ requirements.txt                 # ? Dependencies
������ [workflow docs...]               # Additional documentation
```

## ? **Quick Start**

### **Step 3: Supervisor Analysis**
```bash
conda activate gen_ai
python 03_supervisor_analysis/step3_main.py "Professor Name" "University" "Publication URL"
```

### **Requirements Setup**
```bash
pip install -r requirements.txt
pip install faiss-cpu -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## ? **Visual Workflows**

All project diagrams are stored in the `diagrams/` folder:
- **Workflow Diagrams**: `.mmd` files (Mermaid format)
- **Architecture Views**: Component relationships and data flow
- **Easy Viewing**: Use [Mermaid Live Editor](https://mermaid.live/) or VS Code

## ? **Technologies Used**

- **LLM**: Azure OpenAI (DevGPT4o)
- **RAG**: FAISS vector store + Azure embeddings
- **PDF Processing**: PyMuPDF + LangChain
- **Web Scraping**: Requests + BeautifulSoup
- **Environment**: Conda `gen_ai`

## ? **Pipeline Steps**

- ? **Step 3**: Supervisor Research Analysis (Complete)
- ? **Step 1**: Resume Analysis (Future)
- ? **Step 2**: Position Analysis (Future)  
- ? **Step 4**: Professional Summary (Future)
- ? **Step 5**: Cover Letter Writing (Future)

## ? **Current Status**

**Step 3 Complete**: Production-ready supervisor analysis with:
- Sophisticated vector store RAG
- Real-time publication scraping
- Azure LLM synthesis
- Comprehensive output analysis

**Ready for Step 4 development!** ?
