def individual_user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "password": user["password"],
        "email": user["email"],
        "name": user["name"],
        "is_active": user["is_active"],
        "is_admin": user["is_admin"]
    }

def user_list_serializer(users) -> list:
    return[individual_user_serializer(user) for user in users]