from uuid import UUID, uuid4

import pytest

from microservice_food_app.app_order.app.models.order import Order, OrderItem, OrderStatus
from microservice_food_app.app_order.app.repositories.order_repo import OrderRepo

food_id_1 = UUID('85db966c-67f1-411e-95c0-f02edfa5464a')
food_id_2 = UUID('31babbb3-5541-4a2a-8201-537cdff25fed')
order_test_repo = OrderRepo()


def test_empty_list() -> None:
    assert order_test_repo.get_order() == []


def test_add_first_order() -> None:
    order = Order(order_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'),
                  items=[OrderItem(food_id=food_id_1, quantity=2)],
                  orderTotal=300.0,
                  status=OrderStatus.CREATE,
                  )
    assert order_test_repo.create_order(order) == order


def test_add_first_order_repeat() -> None:
    order = Order(order_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'),
                  items=[OrderItem(food_id=food_id_1, quantity=2)],
                  orderTotal=300.0,
                  status=OrderStatus.CREATE,
                  )
    # order_test_repo.create_order(order)
    with pytest.raises(KeyError):
        order_test_repo.create_order(order)


def test_get_order_by_id() -> None:
    order = Order(order_id=uuid4(),
                  items=[OrderItem(food_id=food_id_1, quantity=2)],
                  orderTotal=300.0,
                  status=OrderStatus.CREATE,
                  )
    order_test_repo.create_order(order)
    assert order_test_repo.get_order_by_id(order.order_id) == order


def test_get_order_by_id_error() -> None:
    with pytest.raises(KeyError):
        order_test_repo.get_order_by_id(uuid4())


def test_set_status() -> None:
    order = Order(order_id=uuid4(),
                  items=[OrderItem(food_id=food_id_1, quantity=2)],
                  orderTotal=300.0,
                  status=OrderStatus.CREATE,
                  )
    order_test_repo.create_order(order)

    order.status = OrderStatus.CREATE
    assert order_test_repo.set_status(order).status == order.status

    order.status = OrderStatus.PICK_UP
    assert order_test_repo.set_status(order).status == order.status

    order.status = OrderStatus.PAID
    assert order_test_repo.set_status(order).status == order.status

    order.status = OrderStatus.DONE
    assert order_test_repo.set_status(order).status == order.status
