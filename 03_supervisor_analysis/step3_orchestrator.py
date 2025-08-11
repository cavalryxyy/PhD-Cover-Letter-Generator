# FILE: 03_supervisor_analysis/step3_orchestrator.py
# PURPOSE: Step 3 Orchestrator - Supervisor analysis pipeline

import logging
from typing import Dict
from step3_prompts import SUPERVISOR_SYNTHESIS_PROMPT
from step3_document_processor import DocumentProcessor
from step3_web_searcher import WebSearcher
from base_analyzer import BaseAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupervisorAnalyzer(BaseAnalyzer):
    """
    Orchestrates the supervisor analysis process by inheriting from BaseAnalyzer.
    """
    
    def __init__(self, document_processor: DocumentProcessor, web_searcher: WebSearcher, llm_client, token_tracker):
        """
        Initialize the analyzer.
        Args:
            document_processor: The document processing component.
            web_searcher: The web searching component.
            llm_client: The LLM client for synthesis.
            token_tracker: An instance of TokenUsageTracker.
        """
        super().__init__(llm_client, token_tracker)
        self.document_processor = document_processor
        self.web_searcher = web_searcher

    def analyze(self, professor_name: str, university: str, publication_url: str) -> Dict:
        """
        Analyze a supervisor.
        
        Args:
            professor_name: The name of the professor.
            university: The name of the university.
            publication_url: The URL of the professor's publications page.
            
        Returns:
            Dictionary with the analysis results.
        """
        logger.info(f"Starting analysis for {professor_name} at {university}")
        
        try:
            # 1. Web Search - Get supervisor's research domains
            research_domains = self.web_searcher.search(professor_name, university, publication_url)
            
            # 2. RAG Search - Get relevant information from institutional documents
            rag_context = self._get_rag_context(research_domains)
            
            # 3. Synthesis - Combine information intelligently
            analysis_result = self._synthesize(rag_context, research_domains, professor_name)
            
            return analysis_result
                
        except Exception as e:
            logger.error(f"Error during supervisor analysis: {e}")
            return self._generate_fallback_analysis(professor_name, university)

    def _get_rag_context(self, research_domains: list[str]) -> str:
        """
        Get relevant context from institutional documents using RAG.
        """
        queries = [f"research on {domain}" for domain in research_domains]
        
        all_context = []
        for query in queries:
            try:
                context = self.document_processor.retrieve(query)
                if context:
                    all_context.append(context)
            except Exception as e:
                logger.warning(f"RAG query failed for '{query}': {e}")
        
        return "\n---\n".join(all_context) if all_context else "No relevant information found in institutional documents."

    def _synthesize(self, rag_context: str, research_domains: list[str], professor_name: str) -> Dict:
        """
        Synthesize the final analysis by calling the LLM via the base class.
        """
        clean_analysis = self._execute_llm_call(
            SUPERVISOR_SYNTHESIS_PROMPT,
            rag_context=rag_context,
            research_domains=", ".join(research_domains),
            professor_name=professor_name
        )
        
        detailed_analysis = f"""
        **PROFESSOR RESEARCH PROFILE: {professor_name}**
        **Research Domains:** {', '.join(research_domains)}

        **Professional Summary:**
        {clean_analysis}

        **Raw Information Sources:**
        **From Institutional Documents (RAG):**
        {rag_context}
        """
        
        return {
            'clean_analysis': clean_analysis,
            'detailed_analysis': detailed_analysis.strip(),
            'metadata': {
                'professor_name': professor_name,
                'research_domains': research_domains,
                'rag_chunks_found': len(rag_context.split('---')) if '---' in rag_context else 1,
                'generation_method': 'LLM synthesis'
            }
        }

    def _generate_fallback_analysis(self, professor_name: str, university: str) -> Dict:
        """
        Generate a basic analysis when all other methods fail.
        """
        clean_analysis = f"Professor {professor_name} at {university}. Limited information available due to technical constraints."
        
        detailed_analysis = f"""
        **PROFESSOR RESEARCH PROFILE: {professor_name}**
        **Institution:** {university}

        **Professional Summary:**
        {clean_analysis}

        **Error Note:**
        Limited information available due to technical constraints.
        """
        return {
            'clean_analysis': clean_analysis,
            'detailed_analysis': detailed_analysis.strip(),
            'metadata': {
                'professor_name': professor_name,
                'university': university,
                'generation_method': 'Fallback (error occurred)'
            }
        }
