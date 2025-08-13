#!/usr/bin/env python3
# FILE: 02_candidate_analysis/step2_main.py
# PURPOSE: Main entry point for Step 2 - Candidate Resume Processing.

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('faiss').setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def setup_components():
    """Sets up and imports necessary components."""
    try:
        # Add project root to path to allow importing from src
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
        
        from src.AzureConnection import embeddings
        from src.token_tracker import TokenUsageTracker
        from step2_candidate_processor import CandidateProcessor
        logger.info("Step 2 components loaded successfully.")
        return embeddings, CandidateProcessor, TokenUsageTracker
    except ImportError as e:
        logger.error(f"Failed to import Step 2 components: {e}")
        sys.exit(1)

def main():
    """Main execution function."""
    print("STEP 2: CANDIDATE RESUME ANALYSIS")
    print("=" * 50)

    if len(sys.argv) != 2:
        print("Usage: python 02_candidate_analysis/step2_main.py \"[Path to Resume]\"")
        print("\nExample:")
        print("  python 02_candidate_analysis/step2_main.py \"./data/candidate/resume.pdf\"")
        sys.exit(1)

    resume_path = sys.argv[1]
    print(f"Resume Path: {resume_path}")
    print("-" * 50)

    embeddings, CandidateProcessor, TokenUsageTracker = setup_components()
    
    token_tracker = TokenUsageTracker()
    processor = CandidateProcessor(embedding_client=embeddings)
    vector_store_path = processor.process_and_save(resume_path, token_tracker)

    print("\n" + "=" * 50)
    print("CANDIDATE ANALYSIS COMPLETE")
    print("=" * 50)
    if vector_store_path:
        print(f"Vector store saved to: {vector_store_path}")
    else:
        print("Vector store creation completed.")
    
    token_tracker.display_usage()
    
    print("\nReady for Step 3 (Supervisor Analysis)")

if __name__ == "__main__":
    main()
