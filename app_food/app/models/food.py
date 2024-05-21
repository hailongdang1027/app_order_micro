from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Food(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    food_id: UUID
    name: str
    description: str
    price: float


class CreateFoodModel(BaseModel):
    name: str
    description: str
    price: float
