import pandas as pd

class DatasetManager:

    def load_sales(self):
        return pd.read_csv("data/live/sales.csv")

    def load_inventory(self):
        print("📂 Loading inventory.csv")
        df = pd.read_csv("data/live/inventory.csv")
        print("📄 Inventory loaded:")
        print(df)
        return df


    def update_inventory(self, product_id, qty):
        df = self.load_inventory()
        df.loc[df.product_id == product_id, "stock_quantity"] -= qty
        df.to_csv("data/live/inventory.csv", index=False)
