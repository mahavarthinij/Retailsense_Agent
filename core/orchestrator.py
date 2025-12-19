from core.dataset_manager import DatasetManager
from agents.inventory_agent import InventoryAgent
from agents.alert_agent import AlertAgent
from rag2.rag_query import ask_rag
import json
class Orchestrator:

    def __init__(self):
        self.data = DatasetManager()
        self.inventory_agent = InventoryAgent()
        self.alert_agent = AlertAgent()

   


    def run_cycle(self):
        inventory = self.data.load_inventory()
        low_stock = self.inventory_agent.detect_low_stock(inventory)

        for _, row in low_stock.iterrows():

            
           rag_result = ask_rag(question)
           for product_id, info in rag_result.items():
                if info["send_email"]:
                    alert_agent.handle(
                    product_id=product_id,
                    stock=inventory_stock,
                    reasoning=info["reason"]
                        )
