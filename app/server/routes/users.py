from fastapi import APIRouter, HTTPException, status, Depends
from server.models.users import CreateUserRequest, UpdateUserRequest
from server.config.database import user_col
from server.schemas.users_schemas import user_list_serializer, individual_user_serializer
from bson import ObjectId
from server.routes.auth import pwd_context
from server.routes.auth import get_current_user
from typing import Annotated

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

current_user = Annotated[dict, Depends(get_current_user)]

@router.get("/")
async def get_users(auth_user: current_user):
    users = user_list_serializer(user_col.find())
    return {
        "users": users
    }

@router.get("/me")
async def get_users(user: current_user):
    return {
        "users": user
    }

@router.post("/")
async def create_user(auth_user: current_user, user: CreateUserRequest):
    pwd_hash = pwd_context.hash(user.password)
    query_user = user_list_serializer(user_col.find({"username": user.username}))
    print(query_user)
    data = {
            "username": user.username,
            "email": user.email,
            "password": pwd_hash,
            "name": user.name,
            "is_active": user.is_active,
            "is_admin": user.is_admin
        }
    if not query_user:
        _id = user_col.insert_one(dict(data))
        user = user_list_serializer(user_col.find({"_id": _id.inserted_id}))
    else:
        return {"message": "User already exists"}
    return {
        "user": user
    }

@router.get("/{user_id}")
async def get_user(user_id: str, auth_user: current_user):
    instance = user_list_serializer(user_col.find({"_id": ObjectId(user_id)}))
    return {
        "user": instance
    }

@router.put("/{user_id}")
async def update_user(user_id: str, user: UpdateUserRequest, auth_user: current_user):
    instance = user_list_serializer(user_col.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": dict(user)}))
    return {
        "user": instance
    }

@router.delete("/{user_id}")
async def delete_user(user_id: str, auth_user: current_user):
    instance = user_list_serializer(user_col.find({"_id": ObjectId(user_id)}))
    if instance is None:
        print(instance)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found")
    else:
        # print(instance)
        user_col.find_one_and_delete({"_id": ObjectId(user_id)})
        return {
            "message": "Deleted sucessfully"
        }