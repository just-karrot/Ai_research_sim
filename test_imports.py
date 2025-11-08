# -*- coding: utf-8 -*-
"""Test script to verify all imports work"""
import sys

try:
    from config.settings import GOOGLE_API_KEY, GROQ_API_KEY
    print("[OK] Config imports")
except Exception as e:
    print(f"[ERROR] Config import: {e}")

try:
    from config.models import ModelFactory
    print("[OK] Model factory imports")
except Exception as e:
    print(f"[ERROR] Model factory import: {e}")

try:
    from agents.base_agent import BaseAgent
    print("[OK] Base agent imports")
except Exception as e:
    print(f"[ERROR] Base agent import: {e}")

try:
    from agents.agent_factory import AgentFactory
    print("[OK] Agent factory imports")
except Exception as e:
    print(f"[ERROR] Agent factory import: {e}")

try:
    from workflow.state import ResearchState
    print("[OK] Workflow state imports")
except Exception as e:
    print(f"[ERROR] Workflow state import: {e}")

try:
    from workflow.runner import WorkflowRunner
    print("[OK] Workflow runner imports")
except Exception as e:
    print(f"[ERROR] Workflow runner import: {e}")

try:
    from tools.tool_manager import ToolManager
    print("[OK] Tool manager imports")
except Exception as e:
    print(f"[ERROR] Tool manager import: {e}")

print("\nImport test complete!")
