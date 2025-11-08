import re
from typing import Dict

class QualityScorer:
    @staticmethod
    def score_accuracy(text: str, fact_check_results: str) -> float:
        text_lower = text.lower()
        fact_lower = fact_check_results.lower()
        
        # Check for verification indicators
        verified_count = fact_lower.count("verified") + fact_lower.count("accurate") + fact_lower.count("correct")
        flagged_count = fact_lower.count("flagged") + fact_lower.count("incorrect") + fact_lower.count("false")
        
        if verified_count > flagged_count:
            return min(0.7 + (verified_count * 0.1), 1.0)
        elif flagged_count > verified_count:
            return max(0.3 - (flagged_count * 0.1), 0.0)
        return 0.5
    
    @staticmethod
    def score_coherence(text: str) -> float:
        if not text or len(text.strip()) < 50:
            return 0.2
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if len(sentences) < 3:
            return 0.3
        
        words = text.split()
        word_count = len(words)
        sentence_count = len(sentences)
        
        # Average sentence length (optimal: 15-20 words)
        avg_sentence_length = word_count / sentence_count
        length_score = 1.0 - abs(avg_sentence_length - 17.5) / 17.5
        length_score = max(0.3, min(1.0, length_score))
        
        # Vocabulary diversity
        unique_words = len(set(w.lower() for w in words))
        diversity_score = min(unique_words / word_count, 0.8)
        
        return (length_score * 0.6 + diversity_score * 0.4)
    
    @staticmethod
    def score_completeness(text: str, required_sections: list) -> float:
        if not required_sections:
            return 0.8
        
        text_lower = text.lower()
        found = 0
        partial = 0
        
        for section in required_sections:
            section_lower = section.lower()
            if section_lower in text_lower:
                found += 1
            elif any(word in text_lower for word in section_lower.split()):
                partial += 0.5
        
        score = (found + partial) / len(required_sections)
        return min(score, 1.0)
    
    @staticmethod
    def score_depth(text: str) -> float:
        """Score content depth based on length and structure"""
        word_count = len(text.split())
        
        if word_count < 100:
            return 0.3
        elif word_count < 300:
            return 0.5
        elif word_count < 500:
            return 0.7
        elif word_count < 1000:
            return 0.9
        else:
            return 1.0
    
    @staticmethod
    def calculate_overall_score(accuracy: float, coherence: float, completeness: float, depth: float) -> float:
        return (accuracy * 0.35 + coherence * 0.25 + completeness * 0.25 + depth * 0.15)
    
    @staticmethod
    def evaluate(text: str, fact_check_results: str, required_sections: list) -> Dict:
        accuracy = QualityScorer.score_accuracy(text, fact_check_results)
        coherence = QualityScorer.score_coherence(text)
        completeness = QualityScorer.score_completeness(text, required_sections)
        depth = QualityScorer.score_depth(text)
        overall = QualityScorer.calculate_overall_score(accuracy, coherence, completeness, depth)
        
        return {
            "accuracy": round(accuracy, 3),
            "coherence": round(coherence, 3),
            "completeness": round(completeness, 3),
            "depth": round(depth, 3),
            "overall": round(overall, 3)
        }
