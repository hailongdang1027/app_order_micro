from uuid import UUID, uuid4

import pytest

from microservice_food_app.app_food.app.models.food import Food
from microservice_food_app.app_food.app.repositories.db_food_repo import FoodRepo


@pytest.fixture()
def food_repo() -> FoodRepo:
    repo = FoodRepo()
    return repo


@pytest.fixture(scope='session')
def food_id() -> UUID:
    return uuid4()


@pytest.fixture(scope='session')
def first_food() -> Food:
    return Food(food_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), name='test_name_1',
                description='test_description_1', price=300)


def second_food() -> Food:
    return Food(food_id=UUID('14ccc207-9a81-47e6-98ac-53857e32954c'), name='test_name_2',
                description='test_description_2', price=300)


def test_add_first_food(first_food: Food, food_repo: FoodRepo) -> None:
    assert food_repo.create_food(first_food) == first_food


def test_add_first_food_repeat(first_food: Food, food_repo: FoodRepo) -> None:
    with pytest.raises(KeyError):
        food_repo.create_food(first_food)


def test_get_food_by_id(first_food: Food, food_repo: FoodRepo) -> None:
    assert food_repo.get_food_by_id(first_food.ord_id) == first_food


def test_get_food_by_id_error(food_repo: FoodRepo) -> None:
    with pytest.raises(KeyError):
        food_repo.get_food_by_id(uuid4())


def test_add_second_food(first_food: Food, second_food: Food, food_repo: FoodRepo) -> None:
    assert food_repo.create_food(second_food) == second_food
    foods = food_repo.get_food()
    assert len(foods) == 2
    assert foods[0] == first_food
    assert foods[1] == second_food


def test_delete_food(first_food: Food, food_repo: FoodRepo) -> None:
    assert food_repo.delete_food_by_id(first_food.food_id) == first_food
