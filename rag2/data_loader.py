import pandas as pd
from langchain.schema import Document

def load_inventory_docs(csv_path="data/inventory.csv"):
    df = pd.read_csv(csv_path)

    docs = []
    for _, row in df.iterrows():
        text = (
            f"Product {row['product_id']} has stock "
            f"{row['stock_quantity']} with threshold {row['threshold']}."
        )
        docs.append(Document(page_content=text))

    return docs
