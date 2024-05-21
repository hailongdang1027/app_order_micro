from uuid import UUID, uuid4

import pytest

from microservice_food_app.app_order.app.models.order import Order, OrderItem, OrderStatus
from microservice_food_app.app_order.app.repositories.db_order_repo import OrderRepo


@pytest.fixture()
def order_repo() -> OrderRepo:
    repo = OrderRepo()
    return repo


@pytest.fixture(scope='session')
def order_id() -> UUID:
    return uuid4()


@pytest.fixture(scope='session')
def first_order() -> Order:
    OrderItem(food_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), quantity=2)
    item = list[OrderItem]
    return Order(order_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'), items=item, orderTotal=400,
                 status=OrderStatus.CREATE,
                 )


def second_order() -> Order:
    OrderItem(food_id=UUID('14ccc207-9a81-47e6-98ac-53857e32954c'), quantity=2)
    item = list[OrderItem]
    return Order(order_id=UUID('14ccc207-9a81-47e6-98ac-53857e32954c'), items=item, orderTotal=400,
                 status=OrderStatus.CREATE,
                 )


def test_add_first_order(first_order: Order, order_repo: OrderRepo) -> None:
    assert order_repo.create_order(first_order) == first_order


def test_add_first_order_repeat(first_order: Order, order_repo: OrderRepo) -> None:
    with pytest.raises(KeyError):
        order_repo.create_order(first_order)


def test_get_order_by_id(first_order: Order, order_repo: OrderRepo) -> None:
    assert order_repo.get_order_by_id(first_order.ord_id) == first_order


def test_get_order_by_id_error(order_repo: OrderRepo) -> None:
    with pytest.raises(KeyError):
        order_repo.get_order_by_id(uuid4())


def test_add_second_order(first_order: Order, second_order: Order, order_repo: OrderRepo) -> None:
    assert order_repo.create_order(second_order) == second_order
    order = order_repo.get_order()
    assert len(order) == 2
    assert order[0] == first_order
    assert order[1] == second_order


def test_set_status(first_order: Order, order_repo: OrderRepo) -> None:
    first_order.status = OrderStatus.ACCEPTED
    assert order_repo.set_status(first_order).status == first_order.status

    first_order.status = OrderStatus.PICK_UP
    assert order_repo.set_status(first_order).status == first_order.status

    first_order.status = OrderStatus.PAID
    assert order_repo.set_status(first_order).status == first_order.status

    first_order.status = OrderStatus.DONE
    assert order_repo.set_status(first_order).status == first_order.status


def test_delete_order(first_order: Order, second_order: Order, order_repo: OrderRepo) -> None:
    assert order_repo.delete_order_by_id(first_order.order_id) == first_order
    assert order_repo.delete_order_by_id(second_order.order_id) == second_order
