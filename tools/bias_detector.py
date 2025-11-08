from typing import List, Dict

class BiasDetector:
    def __init__(self):
        self.bias_keywords = [
            "always", "never", "obviously", "clearly", "everyone knows",
            "undoubtedly", "certainly", "absolutely", "definitely"
        ]
        self.contradiction_markers = [
            "however", "but", "although", "despite", "nevertheless"
        ]
    
    def detect_bias(self, text: str) -> List[str]:
        found_biases = []
        text_lower = text.lower()
        for keyword in self.bias_keywords:
            if keyword in text_lower:
                found_biases.append(f"Potential bias: '{keyword}'")
        return found_biases
    
    def detect_contradictions(self, text: str) -> List[Dict]:
        sentences = text.split('.')
        contradictions = []
        
        for i, sentence in enumerate(sentences):
            for marker in self.contradiction_markers:
                if marker in sentence.lower():
                    contradictions.append({
                        "sentence": sentence.strip(),
                        "marker": marker,
                        "position": i
                    })
        return contradictions
    
    def analyze(self, text: str) -> Dict:
        return {
            "biases": self.detect_bias(text),
            "contradictions": self.detect_contradictions(text),
            "bias_count": len(self.detect_bias(text)),
            "contradiction_count": len(self.detect_contradictions(text))
        }
