from tools.search import KnowledgeRetriever
from tools.citation import CitationTracker
from tools.quality_metrics import QualityScorer
from tools.bias_detector import BiasDetector
from tools.fact_validator import FactValidator

class ToolManager:
    def __init__(self, retrieval_model="gemini"):
        self.retriever = KnowledgeRetriever(retrieval_model)
        self.citation_tracker = CitationTracker()
        self.quality_scorer = QualityScorer()
        self.bias_detector = BiasDetector()
        self.fact_validator = FactValidator()
    
    def retrieve_knowledge(self, topic: str) -> str:
        return self.retriever.retrieve(topic)
    
    def validate_citations(self, text: str) -> dict:
        citations = self.citation_tracker.extract_citations(text)
        return {
            "citations_found": len(citations),
            "citations": citations,
            "citation_graph": self.citation_tracker.get_citation_graph()
        }
    
    def evaluate_quality(self, text: str, fact_check_results: str, required_sections: list) -> dict:
        return self.quality_scorer.evaluate(text, fact_check_results, required_sections)
    
    def detect_bias(self, text: str) -> dict:
        return self.bias_detector.analyze(text)
    
    def validate_facts(self, text: str, reference: str = "") -> dict:
        return self.fact_validator.validate_claims(text, reference)
