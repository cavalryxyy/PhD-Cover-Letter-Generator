#!/usr/bin/env python3
"""
Step 3: Supervisor Analysis
Usage: python step3.py "Professor Name" "University Name" "Publication URL" "path/to/position.pdf"
"""

import os
import sys
import logging
from datetime import datetime

# Configure logging to hide verbose HTTP requests and Faiss GPU warnings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('faiss').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

def validate_inputs():
    """Validate command line inputs."""
    if len(sys.argv) != 5:
        print("Usage: python step3.py \"[Professor Name]\" \"[University]\" \"[Publication URL]\" \"[Path to Position]\"")
        print("\nExample:")
        print("  python 03_supervisor_analysis/step3_main.py \"Jane Doe\" \"Example University\" \"http://example.com\" \"./data/institutional/position.pdf\"")
        sys.exit(1)
    
    professor_name = sys.argv[1].strip()
    university = sys.argv[2].strip()
    publication_url = sys.argv[3].strip()
    position_path = sys.argv[4].strip()
    
    if not all([professor_name, university, publication_url, position_path]):
        print("ERROR: All four arguments are required and cannot be empty")
        sys.exit(1)
    
    return professor_name, university, publication_url, position_path

def setup_components():
    """Setup Step 3 components."""
    try:
        # Add parent directory to path for AzureConnection
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, parent_dir)
        
        from step3_orchestrator import SupervisorAnalyzer
        from step3_document_processor import DocumentProcessor
        from step3_web_searcher import WebSearcher
        from src.AzureConnection import embeddings, client
        from src.token_tracker import TokenUsageTracker
        logger.info("Step 3 components loaded successfully")
        return SupervisorAnalyzer, DocumentProcessor, WebSearcher, embeddings, client, TokenUsageTracker
    except ImportError as e:
        logger.error(f"Failed to import Step 3 components: {e}")
        sys.exit(1)

def execute_analysis(professor_name, university, publication_url, position_path, token_tracker):
    """Execute Step 3 analysis."""
    logger.info(f"Starting Step 3 analysis: {professor_name} at {university}")
    
    SupervisorAnalyzer, DocumentProcessor, WebSearcher, embeddings, client, _ = setup_components()
    
    # Initialize components
    document_processor = DocumentProcessor(embedding_client=embeddings)

    # Load institutional document
    if os.path.exists(position_path):
        logger.info(f"Loading institutional document from: {position_path}")
        document_processor.process_and_load([position_path], "institutional", token_tracker)
    else:
        logger.warning(f"Institutional document not found: {position_path}")

    web_searcher = WebSearcher()
    analyzer = SupervisorAnalyzer(document_processor, web_searcher, llm_client=client, token_tracker=token_tracker)
    
    try:
        analysis_result = analyzer.analyze(professor_name, university, publication_url)
        logger.info("Analysis completed successfully")
        
        # Add metadata
        analysis_result['metadata'].update({
            'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'llm_model': 'DevGPT4o',
            'vector_store': 'FAISS with Azure embeddings',
            'data_sources': 'Institutional PDFs + Web scraping'
        })
        
        return analysis_result
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        error_msg = f"ERROR: Analysis failed - {e}"
        return {
            'clean_analysis': error_msg,
            'detailed_analysis': error_msg,
            'metadata': {
                'professor_name': professor_name,
                'university': university,
                'publication_url': publication_url,
                'error': str(e)
            }
        }

def save_results(analysis_data, professor_name, university):
    """Save both clean and detailed results to separate files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    professor_safe = "".join(c for c in professor_name if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')
    
    # Get project root for consistent output path management
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "outputs", "step3")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract data from analysis_data dictionary
    clean_result = analysis_data.get('clean_analysis', '')
    detailed_result = analysis_data.get('detailed_analysis', '')
    metadata = analysis_data.get('metadata', {})
    
    saved_files = []
    
    # 1. Clean output for Step 4
    clean_filename = f"step3_clean_{professor_safe}_{timestamp}.txt"
    clean_filepath = os.path.join(output_dir, clean_filename)
    try:
        with open(clean_filepath, 'w', encoding='utf-8') as f:
            f.write(clean_result)
        logger.info(f"Clean results saved to: {clean_filepath}")
        saved_files.append(clean_filepath)
    except Exception as e:
        logger.error(f"Failed to save clean results: {e}")
    
    # 2. Detailed output for manual review
    detailed_filename = f"step3_detailed_{professor_safe}_{timestamp}.txt"
    detailed_filepath = os.path.join(output_dir, detailed_filename)
    try:
        with open(detailed_filepath, 'w', encoding='utf-8') as f:
            f.write("STEP 3 SUPERVISOR ANALYSIS - DETAILED REVIEW\n")
            f.write("=" * 80 + "\n")
            f.write(f"Professor: {professor_name}\n")
            f.write(f"University: {university}\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Publication URL: {metadata.get('publication_url', 'N/A')}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("CLEAN ANALYSIS (for Step 4):\n")
            f.write("-" * 40 + "\n")
            f.write(clean_result)
            f.write("\n\n")
            
            f.write("DETAILED ANALYSIS (for manual review):\n")
            f.write("-" * 40 + "\n")
            f.write(detailed_result)
            
            # Add metadata section
            if metadata:
                f.write("\n\nMETADATA & SOURCES:\n")
                f.write("-" * 40 + "\n")
                for key, value in metadata.items():
                    f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        
        logger.info(f"Detailed results saved to: {detailed_filepath}")
        saved_files.append(detailed_filepath)
    except Exception as e:
        logger.error(f"Failed to save detailed results: {e}")
    
    return saved_files

def main():
    """Main execution."""
    print("STEP 3: SUPERVISOR ANALYSIS")
    print("=" * 50)
    
    # Validate inputs
    professor_name, university, publication_url, position_path = validate_inputs()
    
    print(f"Professor: {professor_name}")
    print(f"University: {university}")
    print(f"Publication URL: {publication_url}")
    print("-" * 50)

    _, _, _, _, _, TokenUsageTracker = setup_components()
    token_tracker = TokenUsageTracker()
    
    # Execute analysis
    analysis_data = execute_analysis(professor_name, university, publication_url, position_path, token_tracker)
    
    # Save results
    output_files = save_results(analysis_data, professor_name, university)
    
    # Display summary
    print("\n" + "=" * 50)
    print("ANALYSIS COMPLETE")
    print("=" * 50)
    if output_files:
        for file in output_files:
            if "clean" in file:
                print(f"  ? Clean (Step 4): {file}")
            else:
                print(f"  ? Detailed (Review): {file}")
    print(f"Professor: {professor_name}")
    print(f"University: {university}")
    
    token_tracker.display_usage()

    print("\nReady for Step 4 (Professional Summary Generation)")

if __name__ == "__main__":
    main()
