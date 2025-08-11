# FILE: 02_candidate_analysis/step2_candidate_processor.py
# PURPOSE: To process the candidate's resume, create a vector store, and save it.

import os
import fitz  # PyMuPDF
import logging
import tiktoken
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
        self.vector_store_path = "vector_stores"

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

            # Create and save the vector store
            vector_store = FAISS.from_texts(texts=chunks, embedding=self.embedding_client)
            save_path = os.path.join(self.vector_store_path, "candidate_vector_store.faiss")
            vector_store.save_local(save_path)
            logger.info(f"Candidate vector store saved successfully to: {save_path}")

        except Exception as e:
            logger.error(f"Failed to process and save candidate resume: {e}")
