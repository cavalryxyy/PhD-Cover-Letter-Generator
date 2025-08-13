# Project Diagrams

**Visual Documentation & Architecture Diagrams for the PhD Cover Letter Generator Pipeline**

## Available Diagrams

### **Step 2: Candidate Resume Processing**

#### `step2_data_flow.mmd`
- **Purpose**: Data flow visualization for candidate resume processing
- **Shows**: PDF ingestion → text extraction → chunking → FAISS vector store creation
- **Best for**: Understanding document processing and embedding generation
- **Token Usage**: Embedding token consumption patterns

### **Step 3: Supervisor Analysis**

#### `step3_data_flow.mmd`
- **Purpose**: Complete end-to-end data flow for supervisor research analysis
- **Shows**: Web scraping → RAG retrieval → LLM synthesis → structured output
- **Best for**: Understanding the most complex pipeline component
- **Features**: Component interactions, error handling, token tracking

### **Step 4: Professional Summary Generation**

#### `step4_data_flow.mmd`
- **Purpose**: JSON structuring and LLM synthesis workflow
- **Shows**: Text analysis → LLM processing → JSON validation → structured output
- **Best for**: Understanding data transformation and validation processes
- **Features**: Error recovery, token tracking, schema validation

### **Step 5: Cover Letter Generation**

#### `step5_data_flow.mmd`
- **Purpose**: RAG-powered cover letter creation workflow
- **Shows**: Multi-input RAG → query generation → evidence retrieval → LLM synthesis
- **Best for**: Understanding complex RAG operations and creative writing
- **Features**: Multi-query RAG, evidence consolidation, creative prompting

### **Complete Pipeline Architecture**

#### `pipeline_visualization.html`
- **Purpose**: Interactive visualization of the complete pipeline
- **Shows**: All 4 steps with data flow and dependencies
- **Best for**: Understanding overall system architecture
- **Features**: Token usage tracking, output file relationships

## How to View Diagrams

### **Mermaid Diagrams (`.mmd`)**
1. **Online**: Copy content to [Mermaid Live Editor](https://mermaid.live/)
2. **IDE Extensions**: 
   - VS Code: "Mermaid Preview"
   - IntelliJ: "Mermaid Plugin"
3. **GitHub/GitLab**: Automatic rendering in markdown files

### **HTML Diagrams**
1. **Browser**: Open `.html` files directly in web browser
2. **Live Server**: Use IDE live server extension for interactive features

## Diagram Coverage

| Component | Data Flow | Architecture | Token Usage | Error Handling |
|-----------|-----------|--------------|-------------|----------------|
| Step 2 | Complete | Complete | Complete | Complete |
| Step 3 | Complete | Complete | Complete | Complete |
| Step 4 | Complete | Complete | Complete | Complete |
| Step 5 | Complete | Complete | Complete | Complete |
| Main Pipeline | Complete | Complete | Complete | Complete |

## Technical Documentation

The diagrams provide technical insights into:
- **Data Flow Patterns**: How information moves between components
- **Token Consumption**: Where and how tokens are used across the pipeline
- **Error Handling**: Fallback mechanisms and error recovery
- **Component Architecture**: Modular design and dependencies
- **Performance Characteristics**: Bottlenecks and optimization opportunities

## Updates

Diagrams are maintained to reflect the current state of the production pipeline, including:
- Token tracking implementation
- Main pipeline orchestrator
- Error handling improvements
- Performance optimizations