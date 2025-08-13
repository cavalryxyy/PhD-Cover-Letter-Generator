#!/usr/bin/env python3
"""
Main Pipeline Orchestrator
Runs the complete PhD Cover Letter Generation pipeline (Steps 2-5)

Usage: python main_pipeline.py "resume.pdf" "Professor Name" "University" "Publication URL" "position.pdf"

Example:
    python main_pipeline.py "data/resume.pdf" "Prof. Jane Doe" "MIT" "https://web.mit.edu/~janedoe" "data/position.pdf"
"""

import os
import sys
import argparse
import subprocess
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    """Orchestrates the complete cover letter generation pipeline."""
    
    def __init__(self, project_root=None):
        self.project_root = project_root or Path(__file__).parent.absolute()
        self.outputs_dir = self.project_root / "outputs"
    
    def run_step2(self, resume_path):
        """Run Step 2: Candidate Analysis."""
        logger.info("=" * 60)
        logger.info("RUNNING STEP 2: CANDIDATE ANALYSIS")
        logger.info("=" * 60)
        
        cmd = [
            sys.executable, 
            str(self.project_root / "02_candidate_analysis" / "step2_main.py"),
            resume_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        
        if result.returncode != 0:
            logger.error(f"Step 2 failed with return code {result.returncode}")
            logger.error(f"STDOUT: {result.stdout}")
            logger.error(f"STDERR: {result.stderr}")
            return False
        else:
            logger.info("Step 2 completed successfully")
            logger.info(f"STDOUT: {result.stdout}")
            return True
    
    def run_step3(self, professor_name, university, publication_url, position_path):
        """Run Step 3: Supervisor Analysis."""
        logger.info("=" * 60)
        logger.info("RUNNING STEP 3: SUPERVISOR ANALYSIS")
        logger.info("=" * 60)
        
        cmd = [
            sys.executable,
            str(self.project_root / "03_supervisor_analysis" / "step3_main.py"),
            professor_name,
            university,
            publication_url,
            position_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        
        if result.returncode != 0:
            logger.error(f"Step 3 failed with return code {result.returncode}")
            logger.error(f"STDOUT: {result.stdout}")
            logger.error(f"STDERR: {result.stderr}")
            return False, None
        else:
            logger.info("Step 3 completed successfully")
            logger.info(f"STDOUT: {result.stdout}")
            
            # Find the generated clean analysis file for Step 4
            step3_output_dir = self.outputs_dir / "step3"
            if step3_output_dir.exists():
                clean_files = list(step3_output_dir.glob("step3_clean_*.txt"))
                if clean_files:
                    latest_file = max(clean_files, key=lambda x: x.stat().st_mtime)
                    return True, str(latest_file)
            
            logger.error("Could not find Step 3 output file")
            return False, None
    
    def run_step4(self, analysis_file):
        """Run Step 4: Professional Summary."""
        logger.info("=" * 60)
        logger.info("RUNNING STEP 4: PROFESSIONAL SUMMARY")
        logger.info("=" * 60)
        
        cmd = [
            sys.executable,
            str(self.project_root / "04_professional_summary" / "step4_main.py"),
            analysis_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        
        if result.returncode != 0:
            logger.error(f"Step 4 failed with return code {result.returncode}")
            logger.error(f"STDOUT: {result.stdout}")
            logger.error(f"STDERR: {result.stderr}")
            return False, None
        else:
            logger.info("Step 4 completed successfully")
            logger.info(f"STDOUT: {result.stdout}")
            
            # Find the generated summary file for Step 5
            step4_output_dir = self.outputs_dir / "step4"
            if step4_output_dir.exists():
                summary_files = list(step4_output_dir.glob("summary_*.json"))
                if summary_files:
                    latest_file = max(summary_files, key=lambda x: x.stat().st_mtime)
                    return True, str(latest_file)
            
            logger.error("Could not find Step 4 output file")
            return False, None
    
    def run_step5(self, summary_file):
        """Run Step 5: Cover Letter Generation."""
        logger.info("=" * 60)
        logger.info("RUNNING STEP 5: COVER LETTER GENERATION")
        logger.info("=" * 60)
        
        cmd = [
            sys.executable,
            str(self.project_root / "05_cover_letter_generation" / "step5_main.py"),
            summary_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        
        if result.returncode != 0:
            logger.error(f"Step 5 failed with return code {result.returncode}")
            logger.error(f"STDOUT: {result.stdout}")
            logger.error(f"STDERR: {result.stderr}")
            return False
        else:
            logger.info("Step 5 completed successfully")
            logger.info(f"STDOUT: {result.stdout}")
            return True
    
    def run_full_pipeline(self, resume_path, professor_name, university, publication_url, position_path):
        """Run the complete pipeline from Steps 2-5."""
        start_time = datetime.now()
        logger.info("? STARTING COMPLETE PhD COVER LETTER GENERATION PIPELINE")
        logger.info(f"Start time: {start_time}")
        logger.info("=" * 80)
        
        try:
            # Step 2: Candidate Analysis
            if not self.run_step2(resume_path):
                logger.error("? Pipeline failed at Step 2")
                return False
            
            # Step 3: Supervisor Analysis
            step3_success, analysis_file = self.run_step3(professor_name, university, publication_url, position_path)
            if not step3_success:
                logger.error("? Pipeline failed at Step 3")
                return False
            
            # Step 4: Professional Summary
            step4_success, summary_file = self.run_step4(analysis_file)
            if not step4_success:
                logger.error("? Pipeline failed at Step 4")
                return False
            
            # Step 5: Cover Letter Generation
            if not self.run_step5(summary_file):
                logger.error("? Pipeline failed at Step 5")
                return False
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info("=" * 80)
            logger.info("? PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info(f"Total execution time: {duration}")
            logger.info(f"End time: {end_time}")
            logger.info("=" * 80)
            
            return True
            
        except Exception as e:
            logger.error(f"? Pipeline failed with exception: {e}")
            return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='PhD Cover Letter Generation Pipeline',
        epilog='Example: python main_pipeline.py "data/resume.pdf" "Prof. Jane Doe" "MIT" "https://web.mit.edu/~janedoe" "data/position.pdf"'
    )
    parser.add_argument('resume_path', help='Path to candidate resume PDF')
    parser.add_argument('professor_name', help='Professor name')
    parser.add_argument('university', help='University name')
    parser.add_argument('publication_url', help='Professor publication URL')
    parser.add_argument('position_path', help='Path to position description PDF')
    
    args = parser.parse_args()
    
    # Validate input files exist
    if not os.path.exists(args.resume_path):
        logger.error(f"Resume file not found: {args.resume_path}")
        sys.exit(1)
    
    if not os.path.exists(args.position_path):
        logger.error(f"Position file not found: {args.position_path}")
        sys.exit(1)
    
    orchestrator = PipelineOrchestrator()
    
    success = orchestrator.run_full_pipeline(
        resume_path=args.resume_path,
        professor_name=args.professor_name,
        university=args.university,
        publication_url=args.publication_url,
        position_path=args.position_path
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
