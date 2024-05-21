from typing import Optional
from uuid import UUID

from microservice_food_app.app_food.app.repositories.food_repo import foods
from microservice_food_app.app_order.app.models.order import Order, OrderItem, OrderStatus

orders: list[Order] = [
    Order(
        order_id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'),
        items=[OrderItem(food_id=foods[0].food_id, quantity=2)],
        orderTotal=25.98,
        status=OrderStatus.CREATE
    ),
    Order(
        order_id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
        items=[OrderItem(food_id=foods[1].food_id, quantity=2)],
        orderTotal=27.98,
        status=OrderStatus.CREATE
    ),
    Order(
        order_id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
        items=[OrderItem(food_id=foods[2].food_id, quantity=2)],
        orderTotal=28.98,
        status=OrderStatus.CREATE
    ),

]


class OrderRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            orders.clear()

    def get_order(self) -> list[Order]:
        return orders

    def get_order_by_id(self, id: UUID) -> Order:
        for d in orders:
            if d.order_id == id:
                return d

        raise KeyError

    def create_order(self, order: Order) -> Order:
        if len([d for d in orders if d.order_id == order.order_id]) > 0:
            raise KeyError

        orders.append(order)
        return order

    def set_status(self, order: Order) -> Order:
        for d in orders:
            if d.order_id == order.order_id:
                d.status = order.status
                break

        return order

    def delete_order(self, id: UUID) -> Optional[Order]:
        for i, order in enumerate(orders):
            if order.order_id == id:
                deleted_order = orders.pop(i)
                return deleted_order

        return None