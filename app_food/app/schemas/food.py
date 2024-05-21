from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID

from microservice_food_app.app_food.app.schemas.base_schema import Base


class Food(Base):
    __tablename__ = 'food'

    food_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
