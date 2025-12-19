def decide(json_data):
    result = {"products": []}

    for p in json_data["products"]:
        send_email = p["stock"] < p["threshold"]

        result["products"].append({
            "product_id": p["product_id"],
            "send_email": send_email,
            "reason": (
                "Stock below threshold"
                if send_email else
                "Stock sufficient"
            ),
            "email": p["email"]
        })

    return result
