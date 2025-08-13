# Step 3: Supervisor Research Analysis

**Intelligent Analysis of PhD Supervisors Using RAG + LLM**

## Usage

### Standalone Execution
```bash
python 03_supervisor_analysis/step3_main.py "Professor Name" "University" "Publication URL" "path/to/position.pdf"
```

### As Part of Main Pipeline
```bash
python main_pipeline.py "resume.pdf" "Professor Name" "University" "Publication URL" "position.pdf"
```

## Architecture Components

```
03_supervisor_analysis/
├── step3_main.py               # Main entry point with token tracking
├── base_analyzer.py            # Abstract base class for LLM operations
├── step3_orchestrator.py       # SupervisorAnalyzer - main orchestration
├── step3_web_searcher.py       # Web scraping for research domains
├── step3_document_processor.py # PDF processing & FAISS RAG system
└── step3_prompts.py            # Structured prompt management
```

## Core Technologies

- **RAG System**: FAISS vector store with Azure embeddings
- **LLM Integration**: Azure OpenAI with token tracking
- **Web Scraping**: Requests + BeautifulSoup for publication analysis
- **Document Processing**: PyMuPDF + LangChain text splitting

## Input Requirements

| Parameter | Description | Example |
|-----------|-------------|---------|
| Professor Name | Full name of the supervisor | "Prof. Elena Andersson" |
| University | Institution name | "Royal Institute of Technology" |
| Publication URL | Professor's publication/profile page | "https://www.kth.se/profile/elena" |
| Position PDF | PhD position description file | "data/position.pdf" |

## Output Files

The pipeline generates two timestamped files in `outputs/step3/`:

1. **Clean Analysis** (`step3_clean_[Professor]_[timestamp].txt`)
   - Structured summary for Step 4 input
   - Focused on key research areas and alignment

2. **Detailed Analysis** (`step3_detailed_[Professor]_[timestamp].txt`) 
   - Comprehensive analysis with metadata
   - Includes raw web scraping results and RAG context
   - Useful for manual review and debugging

## Token Usage

Step 3 typically consumes:
- **Embedding Tokens**: ~470 (for document processing and RAG queries)
- **LLM Tokens**: ~266 (112 prompt + 154 completion)
- **Total**: ~737 tokens

## Processing Workflow

1. **Document Processing**: Loads and chunks position PDF into FAISS vector store
2. **Web Scraping**: Extracts research domains from professor's publication page
3. **RAG Retrieval**: Queries institutional documents for relevant context
4. **LLM Synthesis**: Combines all information into structured analysis
5. **Output Generation**: Creates both clean and detailed analysis files

## Key Features

- **Token Tracking**: Complete monitoring of embedding and LLM usage
- **Error Handling**: Graceful fallback when web scraping fails
- **RAG Integration**: Intelligent retrieval from institutional documents
- **Structured Output**: Clean separation for downstream processing
- **Metadata Preservation**: Full traceability of analysis sources

## Detailed Architecture

See **[Step 3 Data Flow Diagram](../diagrams/step3_data_flow.mmd)** for complete visualization including:
- Component interaction patterns
- RAG retrieval workflow
- LLM synthesis process
- Error handling pathways

**Ready for Step 4: Professional Summary Generation**
