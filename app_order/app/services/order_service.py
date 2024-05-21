from typing import List, Optional
from uuid import uuid4, UUID

from fastapi import Depends

from microservice_food_app.app_order.app.models.order import Order, OrderItem, OrderStatus
from microservice_food_app.app_order.app.repositories.db_order_repo import OrderRepo


class OrderService():
    order_repo: OrderRepo

    def __init__(self, order_repo: OrderRepo = Depends(OrderRepo), ) -> None:
        self.order_repo = order_repo

    def get_order(self) -> list[Order]:
        return self.order_repo.get_order()

    def create_order(self, items: List[OrderItem], order_total: float) -> Order:
        order = Order(
            order_id=uuid4(),
            items=items,
            order_total=order_total,
            status=OrderStatus.CREATE
        )
        return self.order_repo.create_order(order)

    def update_order_status(self, order_id: UUID, new_status: OrderStatus) -> Optional[Order]:
        try:
            order = self.order_repo.get_order_by_id(order_id)
            order.status = new_status
            return self.order_repo.set_status(order)
        except KeyError:
            return None

    def cancel_order(self, order_id: UUID) -> Optional[Order]:
        try:
            order = self.order_repo.get_order_by_id(order_id)
            if order and order.status == OrderStatus.CREATE:
                order.status = OrderStatus.CANCELLED
                return self.order_repo.set_status(order)
            return None
        except KeyError:
            return None

    def delete_order(self, order_id: UUID) -> Optional[Order]:
        return self.order_repo.delete_order(order_id)
