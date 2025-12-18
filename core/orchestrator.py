from core.dataset_manager import DatasetManager
from agents.inventory_agent import InventoryAgent
from agents.alert_agent import AlertAgent
from rag2.rag_query import ask_rag

class Orchestrator:

    def __init__(self):
        self.data = DatasetManager()
        self.inventory_agent = InventoryAgent()
        self.alert_agent = AlertAgent()

   

    def run_cycle(self):
        inventory = self.data.load_inventory()
        low_stock = self.inventory_agent.detect_low_stock(inventory)

        for _, row in low_stock.iterrows():

        # 🔍 Ask RAG for reasoning
            question = f"""
            Product {row.product_id} has stock {row.stock_quantity}.
            What action should be taken?
            """

            rag_reasoning = ask_rag(question)

            # 🧠 Pass reasoning to alert agent

            self.alert_agent.handle(
            product_id=row.product_id,
            stock=row.stock_quantity,
            reasoning=rag_reasoning
            )
