# -*- coding: utf-8 -*-
"""Standalone script to visualize the LangGraph workflow"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from workflow.visualizer import get_ascii_diagram, get_mermaid_diagram
except ImportError:
    # Fallback if imports fail
    def get_ascii_diagram():
        return open('workflow/visualizer.py').read().split('return """')[1].split('"""')[0]
    def get_mermaid_diagram():
        return open('workflow/visualizer.py').read().split('return """')[2].split('"""')[0]

print("=" * 70)
print("         LANGGRAPH WORKFLOW VISUALIZATION")
print("=" * 70)
print()

# ASCII Diagram
print(get_ascii_diagram())

print("\n" + "=" * 70)
print("         MERMAID DIAGRAM CODE")
print("=" * 70)
print("\nCopy this code to https://mermaid.live for interactive visualization:\n")
print(get_mermaid_diagram())

print("\n" + "=" * 70)
print("WORKFLOW EXPLANATION")
print("=" * 70)
print("""
This is a LangGraph StateGraph implementation with:

1. STATE MANAGEMENT:
   - ResearchState (TypedDict) shared across all nodes
   - Accumulator pattern for agent_messages

2. NODES (6 total):
   - research: Researcher agent generates content
   - review: Reviewer agent evaluates quality
   - fact_check: Fact checker validates claims
   - citation: Citation validator checks sources
   - editor: Editor refines based on feedback
   - finalize: Prepares final document

3. EDGES:
   - Sequential: research → review → fact_check → citation → editor
   - Conditional: editor → decision (should_continue function)
   - Loop: decision → review (if quality < threshold)
   - Exit: decision → finalize (if converged)

4. CONVERGENCE CRITERIA:
   - quality_score >= CONVERGENCE_THRESHOLD (0.7)
   - OR iteration >= MAX_ITERATIONS (2)

5. EXECUTION:
   - workflow.invoke(state) - Run complete workflow
   - workflow.stream(state) - Stream node outputs in real-time

This enables autonomous multi-agent collaboration with iterative refinement!
""")
