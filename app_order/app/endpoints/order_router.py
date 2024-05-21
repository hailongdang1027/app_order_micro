from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from microservice_food_app.app_order.app.models.order import Order, OrderItem, OrderStatus
from microservice_food_app.app_order.app.services.order_service import OrderService

order_router = APIRouter(prefix='/orders', tags=['Orders'])


@order_router.get('/')
def get_order(order_service: OrderService = Depends(OrderService)) -> list[Order]:
    return order_service.get_order()


@order_router.post('/', response_model=Order)
def create_order(
        order_items: list[OrderItem],
        order_total: float,
        order_service: OrderService = Depends(OrderService)
) -> Order:
    try:
        return order_service.create_order(order_items, order_total)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@order_router.delete('/{order_id}', response_model=bool)
def delete_order(
        order_id: UUID,
        order_service: OrderService = Depends(OrderService)
) -> bool:
    success = order_service.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return success


@order_router.put('/{order_id}/status', response_model=Order)
def update_order_status(
        order_id: UUID,
        new_status: OrderStatus,
        order_service: OrderService = Depends(OrderService)
) -> Order:
    try:
        return order_service.update_order_status(order_id, new_status)
    except KeyError:
        raise HTTPException(status_code=404, detail="Order not found")
