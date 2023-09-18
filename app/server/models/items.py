from pydantic import BaseModel, PositiveInt
from typing import Optional


class CreateItemsRequest(BaseModel):
    name: str
    model: str or None = None
    description: str or None = None
    cost: float
    quantity: PositiveInt


class UpdateItemsRequest(BaseModel):
    name: Optional[str]
    model: Optional[str]
    description: Optional[str]
    cost: Optional[float]
    quantity: Optional[PositiveInt]