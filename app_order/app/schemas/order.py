import enum

from sqlalchemy import Column, Float, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from microservice_food_app.app_order.app.schemas.base_schema import Base


class OrderStatus(enum.Enum):
    CREATE = 'create'
    ACCEPTED = 'accepted'
    PICK_UP = 'pick_up'
    CANCELLED = 'cancelled'
    PAID = 'paid'
    DONE = 'done'


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(UUID(as_uuid=True), primary_key=True)
    order_total = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)

    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'

    item_id = Column(UUID(as_uuid=True), primary_key=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.order_id'))
    food_id = Column(UUID(as_uuid=True), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
