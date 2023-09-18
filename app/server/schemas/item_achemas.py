def individual_item_serializer(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "model": item["model"],
        "description": item["description"],
        "cost": item["cost"],
        "quantity": item["quantity"]
    }

def item_list_serializer(items) -> list:
    return[individual_item_serializer(item) for item in items]