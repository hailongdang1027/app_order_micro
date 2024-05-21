import traceback
from uuid import UUID

from sqlalchemy.orm import Session

from microservice_food_app.app_order.app.database import get_db_order
from microservice_food_app.app_order.app.models.order import Order
from microservice_food_app.app_order.app.schemas.order import Order as DBOrder


class OrderRepo():
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db_order())

    def _map_to_model(self, order: DBOrder) -> Order:
        result = Order.from_orm(order)

        return result

    def _map_to_schema(self, order: Order) -> Order:
        data = dict(order)
        result = Order(**data)
        return result

    def create_order(self, order: Order) -> Order:
        try:
            db_order = self._map_to_schema(order)
            self.db.add(db_order)
            self.db.commit()
            return self._map_to_model(db_order)
        except:
            traceback.print_exc()
            raise KeyError

    def get_order(self) -> list[Order]:
        orders = []
        for d in self.db.query(DBOrder).all():
            orders.append(self._map_to_model(d))

        return orders

    def set_status(self, order: Order) -> Order:
        db_order = self.db.query(DBOrder).filter(
            DBOrder.order_id == order.order_id).first()
        db_order.status = order.status
        self.db.commit()
        return self._map_to_model(db_order)

    def delete_order(self, order_id):
        try:
            self.db.query(DBOrder).delete()
            self.db.commit()
        except Exception as e:
            print(f"Deleting orders: {e}")
            self.db.rollback()
            raise

    def get_order_by_id(self, order_id: UUID):
        order = self.db.query(DBOrder).filter(DBOrder.order_id == id).first()
        if order == None:
            raise KeyError
        return self._map_to_model(order)

    def delete_order_by_id(self, id: UUID) -> Order:
        try:
            # Find the order by its ord_id
            order = self.db.query(DBOrder).filter(DBOrder.order_id == id).one()

            # If the order is found, map it to the model and commit the deletion
            if order:
                deleted_order = self._map_to_model(order)
                self.db.delete(order)
                self.db.commit()
                return deleted_order
            else:
                # Handle the case where no order is found
                raise ValueError(f"No order found with ord_id {id}")
        except Exception as e:
            # Rollback any changes if there's an error
            self.db.rollback()
            # Re-raise the exception so it can be handled elsewhere
            raise e