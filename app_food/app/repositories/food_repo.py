from typing import Optional
from uuid import UUID

from microservice_food_app.app_food.app.models.food import Food
from typing import Optional
foods: list[Food] = [
    Food(food_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), name='test_name_0', description='test_description_0',
         price=270),
    Food(food_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'), name='test_name_1', description='test_description_1',
         price=180),
    Food(food_id=UUID('45309954-8e3c-4635-8066-b342f634252c'), name='test_name_2', description='test_description_2',
         price=230),
]


class FoodRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            foods.clear()

    def get_food(self) -> list[Food]:
        return foods

    def get_food_by_id(self, id: UUID) -> Food:
        for d in foods:
            if d.food_id == id:
                return d

        raise KeyError

    def create_food(self, food: Food) -> Food:
        if len([d for d in foods if d.food_id == food.food_id]) > 0:
            raise KeyError

        foods.append(food)
        return food

    def delete_food(self, id: UUID) -> Optional[Food]:
        for i, food in enumerate(foods):
            if food.food_id == id:
                deleted_food = foods.pop(i)
                return deleted_food

        return None