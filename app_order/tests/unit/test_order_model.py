from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from microservice_food_app.app_order.app.models.order import OrderItem, OrderStatus, Order




# order_id: UUID
# items: [item]
# order_total: float
# doc: str

def test_order_creation():
    order_id = uuid4()
    food_id = uuid4()
    items = OrderItem(food_id=food_id, quantity=2)
    orderTotal = 300
    status = OrderStatus.CREATE

    order = Order(order_id=order_id, items=items, orderTotal=orderTotal, status=status)

    assert order.order_id == order_id
    assert order.items[0].food_id == food_id
    assert order.items[0].quantity == 2
    assert order.orderTotal == 300.0
    assert order.status == OrderStatus.CREATE


def test_order_status_required():
    with pytest.raises(ValidationError):
        Order(order_id=uuid4(),
              items=[OrderItem(food_id=uuid4(), quantity=1)],
              orderTotal="orderTotal",
        )