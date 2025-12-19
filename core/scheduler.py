import time
from core.orchestrator import Orchestrator

orch = Orchestrator()

while True:
    print("executeddd-scheduler.....")
    orch.run_cycle()
    time.sleep(1)
