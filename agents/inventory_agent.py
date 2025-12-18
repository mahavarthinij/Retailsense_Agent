class InventoryAgent:
    def detect_low_stock(self, df):
        print("📦 Inventory received:")
        print(df)

        low = df[df.stock_quantity < df.threshold]

        print("⚠️ Low stock detected:")
        print(low)

        return low
