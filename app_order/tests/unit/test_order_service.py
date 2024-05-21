from typing import Tuple, List
from uuid import uuid4, UUID

import pytest

from microservice_food_app.app_order.app.models.order import CreateOrder, OrderItem, OrderStatus
from microservice_food_app.app_order.app.repositories.order_repo import OrderRepo
from microservice_food_app.app_order.app.services.order_service import OrderService


@pytest.fixture(scope='session')
def order_service() -> OrderService:
    return OrderService(OrderRepo(clear=True))


@pytest.fixture(scope='session')
def first_order_data() -> tuple[list[OrderItem], float]:
    items = [
        OrderItem(food_id=uuid4(), quantity=2),
        OrderItem(food_id=uuid4(), quantity=3)
    ]
    return items, 300.0


@pytest.fixture(scope='session')
def second_order_data() -> tuple[list[OrderItem], float]:
    items = [
        OrderItem(food_id=uuid4(), quantity=2),
        OrderItem(food_id=uuid4(), quantity=3)
    ]
    return items, 300.0


def test_empty_order(order_service: OrderService) -> None:
    assert order_service.get_order() == []


def test_create_first_order(
        first_order_data: tuple[list[OrderItem], float],
        order_service: OrderService
) -> None:
    items, orderTotal = first_order_data
    order = order_service.create_order(items, orderTotal)
    assert order.items == items
    assert order.orderTotal == orderTotal
    assert order.status == OrderStatus.CREATE


def test_create_second_order(
        first_order_data: tuple[list[OrderItem], float],
        order_service: OrderService
) -> None:
    items, orderTotal = first_order_data
    order = order_service.create_order(items, orderTotal)
    assert order.items == items
    assert order.orderTotal == orderTotal
    assert order.status == OrderStatus.CREATE


def test_get_order(
        first_order_data: tuple[list[OrderItem], float],
        second_order_data: tuple[list[OrderItem], float],
        order_service: OrderService
) -> None:
    orders = order_service.get_order()
    assert len(orders) == 2
    assert orders[0].items == first_order_data[0]
    assert orders[0].orderTotal == first_order_data[1]
    assert orders[1].items == second_order_data[0]
    assert orders[1].orderTotal == second_order_data[1]


