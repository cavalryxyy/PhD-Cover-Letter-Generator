import os
import sys
from typing import List
import faiss
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

# Add project root to path to allow imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.AzureConnection import embeddings as azure_embeddings

class CandidateRetriever:
    """
    Handles loading the candidate's FAISS vector store and retrieving relevant information.
    """
    def __init__(self, vector_store_path: str, embeddings_client: Embeddings):
        """
        Initializes the retriever and loads the FAISS index.

        Args:
            vector_store_path (str): The path to the FAISS vector store directory.
            embeddings_client (Embeddings): The embeddings client to use.
        """
        if not os.path.isdir(vector_store_path):
            raise FileNotFoundError(f"Vector store not found at path: {vector_store_path}")

        print("Loading candidate vector store...")
        self.vector_store = FAISS.load_local(vector_store_path, embeddings_client, allow_dangerous_deserialization=True)
        print("Candidate vector store loaded successfully.")

    def get_candidate_evidence(self, queries: List[str], top_k: int = 3) -> str:
        """
        Retrieves relevant text chunks from the candidate's resume based on a list of queries.

        Args:
            queries (List[str]): A list of queries to search for (e.g., "experience with Python").
            top_k (int): The number of top documents to retrieve for each query.

        Returns:
            str: A consolidated string of the most relevant text snippets from the resume.
        """
        print(f"Retrieving candidate evidence for queries: {queries}")
        all_evidence = []
        for query in queries:
            try:
                # Perform similarity search
                documents = self.vector_store.similarity_search(query, k=top_k)
                for doc in documents:
                    if doc.page_content not in all_evidence:
                        all_evidence.append(doc.page_content)
            except Exception as e:
                print(f"An error occurred during similarity search for query '{query}': {e}")
        
        if not all_evidence:
            return "No specific evidence found in the candidate's resume for the given queries."

        return "\n\n---\n\n".join(all_evidence)

# Example Usage (for testing purposes)
if __name__ == '__main__':
    store_path = os.path.join(project_root, "vector_stores", "candidate_vector_store.faiss")
    
    if os.path.isdir(store_path):
        retriever = CandidateRetriever(vector_store_path=store_path, embeddings_client=azure_embeddings)
        test_queries = ["What is my experience with Python and Machine Learning?", "Tell me about my research projects."]
        evidence = retriever.get_candidate_evidence(test_queries)
        print("\n--- Retrieved Evidence ---")
        print(evidence)
    else:
        print(f"Test could not be run. Vector store not found at: {store_path}")
        print("Please run Step 2 to generate the candidate vector store first.")
