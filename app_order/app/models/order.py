import enum
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrderStatus(enum.Enum):
    CREATE = 'create'
    ACCEPTED = 'accepted'
    PICK_UP = 'pick_up'
    CANCELLED = 'cancelled'
    PAID = 'paid'
    DONE = 'done'


class OrderItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    food_id: str
    quantity: int


class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_id: UUID
    items: List[OrderItem]
    orderTotal: float
    status: OrderStatus


class CreateOrder(BaseModel):
    items: List[OrderItem]
    orderTotal: float
