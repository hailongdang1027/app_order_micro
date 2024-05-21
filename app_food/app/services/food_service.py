from typing import Optional
from uuid import uuid4, UUID

from microservice_food_app.app_food.app.models.food import Food
from microservice_food_app.app_food.app.repositories.db_food_repo import FoodRepo

from fastapi import Depends


class FoodService():
    food_repo: FoodRepo

    def __init__(self, food_repo: FoodRepo = Depends(FoodRepo)) -> None:
        self.food_repo = food_repo

    def get_food(self) -> list[Food]:
        return self.food_repo.get_food()

    def create_food(self, name: str, description: str, price: float) -> Food:
        new_food = Food(food_id=uuid4(), name=name, description=description, price=price)
        return self.food_repo.create_food(new_food)

    def update_food(self, food_id: uuid4(), name: Optional[str] = None, description: Optional[str] = None,
                    price: Optional[float] = None) -> Optional[Food]:
        food = self.food_repo.get_food_by_id(food_id)
        if food is None:
            return None
        if name is not None:
            food.name = name
        if description is not None:
            food.description = description
        if price is not None:
            food.price = price
        # Normally you would save the updated object here
        return food

    def delete_food(self, food_id: UUID) -> bool:
        try:
            self.food_repo.delete_food(food_id)
            return True
        except KeyError:
            return False
