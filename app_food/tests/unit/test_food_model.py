from uuid import uuid4

from microservice_food_app.app_food.app.models.food import Food


def test_order_creation():
    food_id = uuid4()
    name = "Name"
    description = "description"
    price = 200

    food = Food(food_id=food_id, name=name, description=description, price=price)

    assert dict(food) == {'food_id': food_id, 'name': name, 'description': description,
                          'price': price}
