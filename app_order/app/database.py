from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from microservice_food_app.app_food.app.settings import settings

engine_order = create_engine(settings.postgres_url, echo=True)

SessionLocalOrder = sessionmaker(autocommit=False, autoflush=False, bind=engine_order)


def get_db_order():
    db_order = SessionLocalOrder()
    try:
        yield db_order
    finally:
        db_order.close()
