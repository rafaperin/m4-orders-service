import uuid
from dataclasses import dataclass

from src.entities.errors.order_item_error import OrderItemError


@dataclass
class OrderItem:
    order_id: uuid.UUID
    product_id: uuid.UUID
    product_quantity: int

    @classmethod
    def create(cls, order_id: uuid.UUID, product_id: uuid.UUID, product_quantity: int) -> "OrderItem":
        if not order_id:
            raise OrderItemError("Order id is required!")
        if not product_id:
            raise OrderItemError("Product id is required!")
        if not product_quantity:
            raise OrderItemError("Product quantity is required!")

        return cls(order_id, product_id, product_quantity)


def order_item_factory(order_id: uuid.UUID, product_id: uuid.UUID, product_quantity: int) -> OrderItem:
    return OrderItem(order_id=order_id, product_id=product_id, product_quantity=product_quantity)
