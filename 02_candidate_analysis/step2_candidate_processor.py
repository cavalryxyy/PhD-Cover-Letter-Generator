# FILE: 02_candidate_analysis/step2_candidate_processor.py
# PURPOSE: To process the candidate's resume, create a vector store, and save it.

import os
import fitz  # PyMuPDF
import logging
import tiktoken
from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CandidateProcessor:
    """Processes the candidate's resume and manages the vector store."""

    def __init__(self, embedding_client):
        """Initializes the processor with an embedding client."""
        self.embedding_client = embedding_client
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.encoding = tiktoken.get_encoding("cl100k_base")
        # Get project root for consistent output path management
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.vector_store_path = os.path.join(self.project_root, "outputs", "step2")

    def _count_tokens(self, text: str) -> int:
        """Counts the number of tokens in a string."""
        return len(self.encoding.encode(text))

    def process_and_save(self, resume_path: str, token_tracker):
        """
        Processes the resume PDF, creates a vector store, and saves it to disk.

        Args:
            resume_path (str): The file path to the candidate's resume.
            token_tracker: An instance of TokenUsageTracker.
        """
        if not os.path.exists(resume_path):
            logger.error(f"Resume file not found at: {resume_path}")
            return

        logger.info(f"Processing candidate resume: {resume_path}")
        try:
            with fitz.open(resume_path) as doc:
                text = "".join(page.get_text() for page in doc)
            
            chunks = self.text_splitter.split_text(text)
            if not chunks:
                logger.warning("No text could be extracted from the resume.")
                return

            logger.info(f"Extracted {len(chunks)} chunks from the resume.")

            # Track embedding tokens
            for chunk in chunks:
                token_tracker.add_embedding_tokens(self._count_tokens(chunk))

            # Create and save the vector store with timestamped naming
            vector_store = FAISS.from_texts(texts=chunks, embedding=self.embedding_client)
            
            # Create timestamped filename for better organization
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Extract candidate name from resume path if possible
            resume_basename = os.path.splitext(os.path.basename(resume_path))[0]
            candidate_name = resume_basename.replace(" ", "_") if resume_basename else "candidate"
            vector_store_filename = f"candidate_vector_store_{candidate_name}_{timestamp}.faiss"
            
            save_path = os.path.join(self.vector_store_path, vector_store_filename)
            
            # Ensure output directory exists
            os.makedirs(self.vector_store_path, exist_ok=True)
            
            vector_store.save_local(save_path)
            logger.info(f"Candidate vector store saved successfully to: {save_path}")
            
            # Return the save path for use by other steps
            return save_path

        except Exception as e:
            logger.error(f"Failed to process and save candidate resume: {e}")
