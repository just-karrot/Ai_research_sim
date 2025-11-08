# -*- coding: utf-8 -*-
"""Test quality metrics system"""
from tools.quality_metrics import QualityScorer

# Test text
sample_text = """
Artificial intelligence has revolutionized healthcare in recent years. Machine learning algorithms 
can now detect diseases from medical images with accuracy comparable to human experts. Natural 
language processing helps analyze patient records and extract valuable insights. Deep learning 
models predict patient outcomes and recommend personalized treatment plans. AI-powered diagnostic 
tools reduce the workload on healthcare professionals while improving patient care quality.
"""

fact_check = "verified: AI in healthcare, verified: machine learning accuracy, verified: NLP applications"

required_sections = ["introduction", "applications", "benefits"]

# Evaluate
scores = QualityScorer.evaluate(sample_text, fact_check, required_sections)

print("Quality Metrics Test:")
print(f"Accuracy: {scores['accuracy']}")
print(f"Coherence: {scores['coherence']}")
print(f"Completeness: {scores['completeness']}")
print(f"Depth: {scores['depth']}")
print(f"Overall: {scores['overall']}")
