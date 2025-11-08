# Pure Python visualization - no external dependencies needed

def get_mermaid_diagram():
    """Get Mermaid diagram code for the workflow"""
    return """
graph TD
    START([START]) --> Research[🔍 Research Node<br/>Researcher Agent]
    Research --> Review[📝 Review Node<br/>Reviewer Agent]
    Review --> FactCheck[✅ Fact Check Node<br/>Fact Checker Agent]
    FactCheck --> Citation[📚 Citation Node<br/>Citation Validator]
    Citation --> Editor[✏️ Editor Node<br/>Editor Agent]
    Editor --> Decision{Quality Check}
    Decision -->|Score < Threshold<br/>OR<br/>Iteration < Max| Review
    Decision -->|Score ≥ Threshold<br/>AND<br/>Iteration ≥ Max| Finalize[🎯 Finalize Node]
    Finalize --> END([END])
    
    style START fill:#90EE90
    style Research fill:#87CEEB
    style Review fill:#FFB6C1
    style FactCheck fill:#98FB98
    style Citation fill:#DDA0DD
    style Editor fill:#F0E68C
    style Decision fill:#FFA500
    style Finalize fill:#90EE90
    style END fill:#FF6B6B
"""

def get_ascii_diagram():
    """Get ASCII art representation of the workflow"""
    return """
╔════════════════════════════════════════════════════════════════╗
║           LangGraph Multi-Agent Research Workflow              ║
╚════════════════════════════════════════════════════════════════╝

                         ┌─────────┐
                         │  START  │
                         └────┬────┘
                              │
                    ┌─────────▼──────────┐
                    │  🔍 RESEARCH NODE  │
                    │  Researcher Agent  │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  📝 REVIEW NODE    │
                    │  Reviewer Agent    │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  ✅ FACT CHECK     │
                    │  Fact Checker      │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  📚 CITATION NODE  │
                    │  Citation Validator│
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  ✏️ EDITOR NODE    │
                    │  Editor Agent      │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │   ❓ DECISION      │
                    │  Quality Check?    │
                    └──┬──────────────┬──┘
                       │              │
            ┌──────────▼──┐      ┌───▼────────┐
            │  Continue?  │      │ Finalize?  │
            │ (Loop Back) │      │   (Exit)   │
            └──────┬──────┘      └─────┬──────┘
                   │                   │
                   │                   │
                   └──────► REVIEW ◄───┘
                              │
                    ┌─────────▼──────────┐
                    │  🎯 FINALIZE NODE  │
                    └─────────┬──────────┘
                              │
                         ┌────▼────┐
                         │   END   │
                         └─────────┘

╔════════════════════════════════════════════════════════════════╗
║  Iterative Loop: Editor → Review (until convergence)          ║
║  Convergence: quality_score ≥ threshold OR iteration ≥ max    ║
╚════════════════════════════════════════════════════════════════╝
"""
