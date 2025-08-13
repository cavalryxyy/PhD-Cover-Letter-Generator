# Step 4: Professional Summary Generation

**Structured Analysis Synthesis with Token Tracking**

## Overview

Transforms unstructured supervisor analysis from Step 3 into structured JSON format. Acts as the critical bridge between raw analysis and cover letter generation, ensuring clean, actionable input for the final step.

## Usage

### Standalone Execution
```bash
python 04_professional_summary/step4_main.py "outputs/step3/step3_clean_Professor_Name_YYYYMMDD_HHMMSS.txt"
```

### As Part of Main Pipeline
```bash
python main_pipeline.py "resume.pdf" "Professor Name" "University" "Publication URL" "position.pdf"
```

## Components

```
04_professional_summary/
├── step4_main.py               # Main entry point with token tracking
├── step4_summary_generator.py  # SummaryGenerator class with LLM integration
└── step4_prompts.py            # Structured prompt templates
```

## Processing Workflow

1. **Input Validation**: Checks for Step 3 clean analysis file
2. **LLM Processing**: Uses specialized prompts to act as "Senior Academic Analyst"
3. **JSON Generation**: Parses unstructured text into structured format
4. **Output Saving**: Stores timestamped JSON in `outputs/step4/`
5. **Token Tracking**: Monitors and displays LLM usage

## Structured Output Format

```json
{
  "supervisor_profile": {
    "name": "Prof. Elena Andersson",
    "university": "Royal Institute of Technology",
    "primary_research_themes": ["Environmental Science", "Climate Change"]
  },
  "position_details": {
    "project_title": "Climate Change Adaptation Strategies",
    "project_summary": "Detailed project description...",
    "required_skills": ["Data Analytics", "Environmental Modeling"],
    "preferred_experience": ["Sustainability Practices"]
  },
  "alignment_summary": {
    "key_talking_points": ["Candidate's expertise aligns with..."],
    "suggested_questions_for_supervisor": ["How do you envision..."]
  }
}
```

## Token Usage

Step 4 typically consumes:
- **LLM Prompt Tokens**: ~564 (analysis text processing)
- **LLM Completion Tokens**: ~340 (JSON generation)
- **Total**: ~904 tokens

## Key Features

- **Token Tracking**: Complete monitoring of LLM usage
- **JSON Validation**: Automatic parsing and error handling
- **Structured Format**: Consistent output schema for Step 5
- **Error Recovery**: Graceful handling of malformed LLM responses
- **Timestamped Output**: Organized file management

## Input Requirements

| Input | Source | Format |
|-------|--------|--------|
| Analysis File | Step 3 clean output | `.txt` file with supervisor analysis |
| Token Tracker | Main pipeline | `TokenUsageTracker` instance |

## Output Files

Generated in `outputs/step4/`:
- **Format**: `summary_[Supervisor_Name]_[timestamp].json`
- **Content**: Structured JSON ready for Step 5 processing
- **Schema**: Consistent format for cover letter generation

## Quality Assurance

- **JSON Validation**: Automatic detection and fixing of malformed responses
- **Schema Consistency**: Enforced structure for downstream compatibility
- **Error Logging**: Detailed error reporting for debugging
- **Fallback Handling**: Graceful degradation when LLM fails

**Ready for Step 5: Cover Letter Generation**
