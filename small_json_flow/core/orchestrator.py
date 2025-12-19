from core.decision_engine import decide
from agents.alert_agent import AlertAgent

class Orchestrator:

    def __init__(self):
        self.alert = AlertAgent()

    def run(self, input_json):
        decision = decide(input_json)

        for p in decision["products"]:
            if p["send_email"]:
                self.alert.send(
                    product_id=p["product_id"],
                    reason=p["reason"],
                    to_email=p["email"]
                )

        return decision
