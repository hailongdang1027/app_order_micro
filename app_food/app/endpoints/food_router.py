from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from microservice_food_app.app_food.app.models.food import Food, CreateFoodModel
from microservice_food_app.app_food.app.services.food_service import FoodService

food_router = APIRouter(prefix='/food', tags=['Food'])


@food_router.get('/')
def get_food(food_service: FoodService = Depends(FoodService)) -> list[Food]:
    return food_service.get_food()


@food_router.post('/', response_model=Food)
def add_food(
        food_info: CreateFoodModel,
        food_service: FoodService = Depends(FoodService)
) -> Food:
    try:
        return food_service.create_food(food_info.name, food_info.description, food_info.price)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


def update_food(
        food_id: UUID,
        food_info: CreateFoodModel,
        food_service: FoodService = Depends(FoodService)
) -> Food:
    try:
        return food_service.update_food(food_id, food_info.name, food_info.description, food_info.price)
    except KeyError:
        raise HTTPException(status_code=404, detail="Not found")


def delete_food(
        food_id: UUID,
        food_service: FoodService = Depends(FoodService)
) -> bool:
    success = food_service.delete_food(food_id)
    if not success:
        raise HTTPException(status_code=404, detail="Not found")
    return success
