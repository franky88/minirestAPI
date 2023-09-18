from fastapi import APIRouter, HTTPException, status, Depends
from server.models.items import CreateItemsRequest, UpdateItemsRequest
from server.config.database import item_col
from server.schemas.item_achemas import item_list_serializer
from bson import ObjectId
from typing import Annotated
from server.routes.auth import oauth_scheme, get_current_user


router = APIRouter(
    prefix="/items",
    tags=["items"]
)

current_user = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def get_items(auth_user: current_user):
    try:
        items = item_list_serializer(item_col.find())
        return {
            "status": HTTPException(status_code=status.HTTP_200_OK, detail="Items successfully retrieved"),
            "items": items
        }
    except Exception as error:
        return {
            "Something went wrong %s" % error
        }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(item: CreateItemsRequest, auth_user: current_user):
    try:
        _id = item_col.insert_one(dict(item))
        item = item_list_serializer(item_col.find({"_id": _id.inserted_id}))
        return HTTPException(status_code=status.HTTP_201_CREATED, detail="Item created successfully")
    except Exception as error:
        return {
            "Something went wrong %s" % error
        }

@router.get("/{item_id}", status_code=status.HTTP_200_OK)
async def get_item(item_id: str, auth_user: current_user):
    try:
        instace = item_list_serializer(item_col.find({"_id": ObjectId(item_id)}))
        print(instace)
        return {
            "status": HTTPException(status_code=status.HTTP_200_OK, detail="Item found successfully"),
            "user": instace
            }
    except Exception as error:
        return {
            "Something went wrong %s" % error
        }

@router.put("/{item_id}", status_code=status.HTTP_200_OK)
async def update_item(item_id: str, item: UpdateItemsRequest, auth_user: current_user):
    try:
        instace = item_col.find_one_and_update({"_id": ObjectId(item_id)}, {"$set": dict(item)})
        print(instace)
        return HTTPException(status_code=status.HTTP_200_OK, detail="Item updated successfully")
    except Exception as error:
        return {
            "Something went wrong %s" % error
        }


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_item(item_id: str, auth_user: current_user):
    try:
        item_col.find_one_and_delete({"_id": ObjectId(item_id)})
        return HTTPException(status_code=status.HTTP_200_OK, detail="Item deleted successfully")
    except Exception as error:
        return {
            "Something went wrong %s" % error
        }