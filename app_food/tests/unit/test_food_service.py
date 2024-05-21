import pytest

from microservice_food_app.app_food.app.repositories.food_repo import FoodRepo
from microservice_food_app.app_food.app.services.food_service import FoodService


@pytest.fixture(scope='session')
def food_service() -> FoodService:
    return FoodService(FoodRepo(clear=True))


@pytest.fixture(scope='session')
def first_food_data() -> tuple[str, str, float]:
    return 'test_name_1', 'test_description_1', 300


def second_food_data() -> tuple[str, str, float]:
    return 'test_name_2', 'test_description_2', 300


def test_empty_food(food_service: FoodService) -> None:
    assert food_service.get_food() == []


def test_create_first_food(
        first_food_data: tuple[str, str, float],
        food_service: FoodService
) -> None:
    name, description, price = first_food_data
    food = food_service.create_food(name, description, price)
    assert food.name == name
    assert food.description == description
    assert food.price == price


def test_create_second_food(
        second_food_data: tuple[str, str, float],
        food_service: FoodService
) -> None:
    name, description, price = second_food_data
    food = food_service.create_food(name, description, price)
    assert food.name == name
    assert food.description == description
    assert food.price == price


def test_get_food(
        first_food_data: tuple[str, str, float],
        second_food_data: tuple[str, str, float],
        food_service: FoodService
) -> None:
    foods = food_service.get_food()
    assert len(foods) == 1
    assert foods[0].name == first_food_data[0]
    assert foods[1].name == second_food_data[0]
