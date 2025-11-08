import re
from typing import List, Dict

class CitationTracker:
    def __init__(self):
        self.citations = {}
        self.citation_count = 0
    
    def extract_citations(self, text: str) -> List[str]:
        patterns = [
            r'\[(\d+)\]',
            r'\(([A-Za-z]+\s+\d{4})\)',
            r'\(([A-Za-z]+\s+et\s+al\.\s+\d{4})\)'
        ]
        citations = []
        for pattern in patterns:
            citations.extend(re.findall(pattern, text))
        return citations
    
    def validate_format(self, citation: str) -> bool:
        return len(citation) > 0
    
    def track_provenance(self, claim: str, source: str):
        self.citation_count += 1
        self.citations[self.citation_count] = {
            "claim": claim,
            "source": source
        }
        return self.citation_count
    
    def get_citation_graph(self) -> Dict:
        return self.citations
