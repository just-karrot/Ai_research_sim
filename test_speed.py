# -*- coding: utf-8 -*-
"""Test pipeline speed"""
import time
from workflow.runner import WorkflowRunner

print("Testing pipeline speed...")
print("=" * 50)

topic = "AI in Healthcare"
start_time = time.time()

runner = WorkflowRunner()

print(f"Topic: {topic}")
print("Starting workflow...\n")

for i, output in enumerate(runner.stream(topic)):
    elapsed = time.time() - start_time
    for node_name, node_output in output.items():
        print(f"[{elapsed:.1f}s] Node: {node_name}")
        if 'agent_messages' in node_output:
            for msg in node_output['agent_messages']:
                print(f"  Agent: {msg['agent']}")
                print(f"  Response length: {len(msg['content'])} chars")

total_time = time.time() - start_time
print(f"\n{'=' * 50}")
print(f"Total time: {total_time:.2f} seconds")
print(f"Average per node: {total_time / max(i+1, 1):.2f} seconds")
