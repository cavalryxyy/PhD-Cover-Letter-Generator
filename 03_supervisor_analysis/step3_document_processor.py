# FILE: 03_supervisor_analysis/step3_document_processor.py
# PURPOSE: Manages the processing of documents and vector stores.

import fitz  # PyMuPDF
import os
from typing import List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
import tiktoken

class DocumentProcessor:
    """
    Processes PDF documents and manages FAISS vector stores.
    """
    def __init__(self, embedding_client=None):
        """
        Initializes the document processor.
        """
        self.candidate_store = None
        self.institutional_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len
        )
        # This should be replaced with a proper way to get the embedding client
        self.embedding_client = embedding_client or AzureOpenAIEmbeddings()
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def _count_tokens(self, text: str) -> int:
        """Counts the number of tokens in a string."""
        return len(self.encoding.encode(text))

    def process_and_load(self, pdf_paths: List[str], store_type: str, token_tracker) -> None:
        """
        Processes PDFs and loads them into the specified vector store.
        Args:
            pdf_paths: A list of file paths to the PDF documents.
            store_type: The type of store to create (e.g., "institutional").
            token_tracker: An instance of TokenUsageTracker.
        """
        logger.info(f"Processing {len(pdf_paths)} PDF(s) for {store_type} store...")
        all_chunks = []
        for path in pdf_paths:
            try:
                if not os.path.exists(path):
                    logger.warning(f"File not found: {path}")
                    continue
                
                with fitz.open(path) as doc:
                    text = "".join(page.get_text() for page in doc)
                    chunks = self.text_splitter.split_text(text)
                    all_chunks.extend(chunks)
                    
                    # Track embedding tokens
                    for chunk in chunks:
                        token_tracker.add_embedding_tokens(self._count_tokens(chunk))

                logger.info(f"Processed {path}: extracted {len(chunks)} chunks")
            except Exception as e:
                logger.error(f"Error processing file {path}: {e}")

        if not all_chunks:
            logger.warning(f"No text could be extracted from the PDFs for {store_type} store.")
            return

        vector_store = FAISS.from_texts(texts=all_chunks, embedding=self.embedding_client)
        if store_type == "institutional":
            self.institutional_store = vector_store
        
        logger.info(f"{store_type.capitalize()} vector store created successfully.")

    def retrieve(self, query: str, k: int = 3) -> str:
        """
        Retrieves relevant context from the institutional vector store.
        """
        if not self.institutional_store:
            return "Error: Institutional vector store is not initialized."
        
        logger.info(f"Retrieving context for query: '{query}'")
        try:
            docs = self.institutional_store.similarity_search(query, k=k)
            return "\\n---\\n".join([doc.page_content for doc in docs])
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return f"Error retrieving context: {e}"


