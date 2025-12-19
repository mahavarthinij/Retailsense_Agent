import json
from core.orchestrator import Orchestrator

print("🚀 Starting JSON flow test")

with open("inventory.json") as f:
    data = json.load(f)

orch = Orchestrator()
result = orch.run(data)

print("\n✅ FINAL JSON OUTPUT:")
print(result)
