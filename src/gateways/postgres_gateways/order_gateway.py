import uuid
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.config import settings

from src.entities.models.order_entity import order_factory, Order
from src.entities.models.order_item_entity import OrderItem, order_item_factory
from src.gateways.orm.order_orm import Order_Items, Orders
from src.interfaces.gateways.order_gateway_interface import IOrderGateway

connection_uri = settings.db.SQLALCHEMY_DATABASE_URI

engine = create_engine(
    connection_uri
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class PostgresDBOrderRepository(IOrderGateway):
    @staticmethod
    def item_to_entity(order_item: Order_Items) -> OrderItem:
        return order_item_factory(order_item.order_id, order_item.product_id, order_item.product_quantity)

    @staticmethod
    def items_to_entity(order_items: List[Order_Items]) -> List[OrderItem]:
        items = []
        for item in order_items:
            item = order_item_factory(
                item.order_id,
                item.product_id,
                item.product_quantity,
            )
            items.append(item)
        return items

    @staticmethod
    def order_to_entity(order: Orders, items: List[OrderItem]) -> Order:
        order = order_factory(
            order.order_id,
            order.customer_id,
            items,
            order.creation_date,
            order.order_total,
        )
        return order

    def get_by_id(self, order_id: uuid.UUID) -> Optional[Order]:
        with SessionLocal() as db:
            order_db = db.query(Orders).filter(Orders.order_id == order_id).first()
            items_db = db.query(Order_Items).filter(Order_Items.order_id == order_id).all()

        if items_db:
            items = self.items_to_entity(items_db)  # type: ignore
        else:
            items = []

        if order_db:
            return self.order_to_entity(order_db, items)  # type: ignore
        else:
            return None

    def get_order_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> Optional[OrderItem]:
        with SessionLocal() as db:
            item_db = db.query(Order_Items)\
                .filter(Order_Items.order_id == order_id,
                        Order_Items.product_id == product_id)\
                .first()

            if item_db:
                return self.item_to_entity(item_db)  # type: ignore
            else:
                return None

    def get_all(self) -> List[Order]:
        result = []
        with SessionLocal() as db:
            orders = db.query(Orders).order_by(Orders.creation_date).all()
            if orders:
                for order in orders:
                    items_db = db.query(Order_Items).filter(Order_Items.order_id == order.order_id).all()  # type: ignore
                    items = self.items_to_entity(items_db)  # type: ignore
                    order_entity = self.order_to_entity(order, items)  # type: ignore
                    result.append(order_entity)
        return result

    def create_order(self, obj_in: Order) -> Order:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        obj_in_data.pop("order_items")
        db_obj = Orders(**obj_in_data)  # type: ignore

        with SessionLocal() as db:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        new_order = self.order_to_entity(db_obj, list())
        return new_order

    def create_order_item(self, obj_in: Order_Items) -> List[OrderItem]:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = Order_Items(**obj_in_data)  # type: ignore

        with SessionLocal() as db:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        item_list = [db_obj]
        return self.items_to_entity(item_list)

    def update_item(self, obj_in: OrderItem):
        item_in = vars(obj_in)
        with SessionLocal() as db:
            db_obj = db.query(Order_Items)\
                .filter(Order_Items.order_id == obj_in.order_id,
                        Order_Items.product_id == obj_in.product_id).first()
            obj_data = jsonable_encoder(db_obj, by_alias=False)
            for field in obj_data:
                if field in item_in:
                    setattr(db_obj, field, item_in[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            print(self.items_to_entity([db_obj]))  # type: ignore

    def update(self, order_id: uuid.UUID, obj_in: Order) -> Order:
        order_in = vars(obj_in)
        with SessionLocal() as db:
            db_obj = db.query(Orders).filter(Orders.order_id == order_id).first()
            obj_data = jsonable_encoder(db_obj, by_alias=False)
            for field in obj_data:
                if field in order_in:
                    setattr(db_obj, field, order_in[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        with SessionLocal() as db:
            items_db = db.query(Order_Items).filter(Order_Items.order_id == order_id).all()

        items = self.items_to_entity(items_db)  # type: ignore
        updated_order = self.order_to_entity(db_obj, items)  # type: ignore
        return updated_order

    def remove_order(self, order_id: uuid.UUID) -> None:
        with SessionLocal() as db:
            order = db.query(Orders).filter(Orders.order_id == order_id).first()
            db.delete(order)

            items = db.query(Order_Items).filter(Order_Items.order_id == order_id).all()
            for item in items:
                db.delete(item)
            db.commit()

    def remove_order_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> None:
        with SessionLocal() as db:
            item = db.query(Order_Items).filter(Order_Items.order_id == order_id).filter(
                Order_Items.product_id == product_id).first()
            db.delete(item)
            db.commit()

