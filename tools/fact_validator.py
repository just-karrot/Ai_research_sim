import re
from typing import List, Dict

class FactValidator:
    def extract_claims(self, text: str) -> List[str]:
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        claims = [s for s in sentences if len(s.split()) > 5]
        return claims
    
    def cross_reference(self, claim: str, context: str) -> bool:
        claim_words = set(claim.lower().split())
        context_words = set(context.lower().split())
        overlap = len(claim_words & context_words)
        return overlap > len(claim_words) * 0.3
    
    def validate_claims(self, text: str, reference_text: str = "") -> Dict:
        claims = self.extract_claims(text)
        validated = []
        flagged = []
        
        for claim in claims:
            if reference_text and self.cross_reference(claim, reference_text):
                validated.append(claim)
            else:
                if len(claim.split()) > 15:
                    flagged.append(claim)
        
        return {
            "total_claims": len(claims),
            "validated": validated,
            "flagged": flagged,
            "confidence": len(validated) / len(claims) if claims else 0
        }
