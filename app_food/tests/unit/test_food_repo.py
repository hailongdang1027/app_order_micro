from uuid import UUID, uuid4
import pytest
from microservice_food_app.app_food.app.models.food import Food
from microservice_food_app.app_food.app.repositories.food_repo import FoodRepo

food_test_repo = FoodRepo()
def test_empty_list() -> None:
    assert food_test_repo.get_food() == []

def test_create_first_food() -> None:
    food = Food(food_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), name='test_name_0',
                  description='test_description_0', price=200)
    assert food_test_repo.create_food(food) == food


def test_add_first_food_repeat() -> None:
    food = Food(food_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), name='test_name_0',
                description='test_description_0', price=200)
    with pytest.raises(KeyError):
        food_test_repo.create_food(food)


def test_get_food_by_id() -> None:
    food = Food(food_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), name='test_name_0',
                description='test_description_0', price=200)
    food_test_repo.create_food(food)
    assert food_test_repo.get_food_by_id(food.food_id) == food


def test_get_food_by_id_error() -> None:
    with pytest.raises(KeyError):
        food_test_repo.get_food_by_id(uuid4())