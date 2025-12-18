print("✅ test_run.py started")

from core.orchestrator import Orchestrator

orch = Orchestrator()
print("✅ Orchestrator created")

orch.run_cycle()

print("✅ run_cycle finished")
