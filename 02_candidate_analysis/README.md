# Step 2: Candidate Resume Analysis

**Document Processing & Vector Store Creation with Token Tracking**

## Overview

Processes candidate resumes into searchable vector stores using FAISS embeddings. This foundational step creates the candidate knowledge base that powers the RAG system in Step 5, enabling intelligent retrieval of relevant candidate experience for cover letter generation.

## Usage

### Standalone Execution
```bash
python 02_candidate_analysis/step2_main.py "path/to/resume.pdf"
```

### As Part of Main Pipeline
```bash
python main_pipeline.py "resume.pdf" "Professor Name" "University" "Publication URL" "position.pdf"
```

## Components

```
02_candidate_analysis/
├── step2_main.py               # Main entry point with token tracking
└── step2_candidate_processor.py # CandidateProcessor class with PDF processing
```

## Core Technologies

- **PDF Processing**: PyMuPDF for text extraction
- **Text Chunking**: LangChain RecursiveCharacterTextSplitter
- **Vector Store**: FAISS with Azure OpenAI embeddings
- **Token Tracking**: Complete embedding token monitoring

## Input Requirements

| Parameter | Description | Example |
|-----------|-------------|---------|
| Resume Path | Path to candidate's resume PDF | "data/candidate/resume.pdf" |

## Processing Workflow

1. **Input Validation**: Checks resume file existence and format
2. **Text Extraction**: PyMuPDF extracts text from PDF pages
3. **Text Chunking**: Splits content into 1000-character chunks with 100-character overlap
4. **Token Counting**: Tracks embedding tokens for each chunk
5. **Vector Store Creation**: FAISS vectorization with Azure embeddings
6. **Timestamped Storage**: Saves with candidate name and timestamp

## Token Usage

Step 2 typically consumes:
- **Embedding Tokens**: ~489 (varies by resume length)
- **LLM Tokens**: 0 (no LLM calls in this step)
- **Total**: ~489 tokens for average resume

## Output Files

Generated in `outputs/step2/`:
- **Format**: `candidate_vector_store_[resume_name]_[timestamp].faiss/`
- **Contents**: 
  - `index.faiss` - FAISS vector index
  - `index.pkl` - Metadata and document references
- **Usage**: Consumed by Step 5 for RAG retrieval

## Key Features

- **Token Tracking**: Complete monitoring of embedding token usage
- **Robust PDF Processing**: Handles various PDF formats and encodings
- **Intelligent Chunking**: Optimized chunk size for retrieval accuracy
- **Timestamped Output**: Organized file management with unique naming
- **Error Handling**: Graceful handling of corrupt or unreadable PDFs

## Technical Details

### **Text Processing Parameters**
- **Chunk Size**: 1000 characters (optimal for embeddings)
- **Chunk Overlap**: 100 characters (preserves context across boundaries)
- **Encoding**: tiktoken cl100k_base for accurate token counting

### **Vector Store Configuration**
- **Embedding Model**: Azure OpenAI text-embedding-ada-002
- **Vector Dimensions**: 1536 (standard for OpenAI embeddings)
- **Similarity Metric**: Cosine similarity
- **Storage Format**: FAISS binary format for fast retrieval

## Quality Assurance

- **File Validation**: Ensures PDF exists and is readable
- **Content Verification**: Checks that text extraction succeeded
- **Token Accuracy**: Precise counting using OpenAI's tiktoken library
- **Error Recovery**: Continues processing even if individual pages fail

## Dependencies

| Technology | Purpose | Version |
|-----------|---------|---------|
| PyMuPDF | PDF text extraction | Latest |
| FAISS | Vector similarity search | faiss-cpu |
| LangChain | Text splitting utilities | Latest |
| Azure OpenAI | Embedding generation | Latest |
| tiktoken | Token counting | Latest |

## Performance Characteristics

- **Processing Speed**: ~5-10 seconds per resume
- **Memory Usage**: Low (streaming text processing)
- **Storage Efficiency**: Compressed vector format
- **Scalability**: Can process multiple resumes in batch

## Limitations

- **PDF Only**: Currently supports PDF format only
- **Text-Based**: Images and tables may not be processed optimally
- **English Optimized**: Best performance with English language content
- **File Size**: Very large PDFs (>10MB) may require additional processing time

## Integration Points

**Inputs**: Resume PDF files
**Outputs**: FAISS vector store for Step 5
**Dependencies**: Azure OpenAI embeddings service
**Next Step**: Vector store consumed by Step 5 RAG system

**Ready for Step 3: Supervisor Analysis**