import uuid
from typing import List

from src.entities.models.order_entity import Order
from src.entities.models.order_item_entity import OrderItem
from src.entities.schemas.order_dto import CreateOrderDTO, CreateOrderItemDTO


class OrderHelper:

    @staticmethod
    def generate_order_request() -> CreateOrderDTO:
        return CreateOrderDTO(
            customer_id=uuid.uuid4()
        )

    @staticmethod
    def generate_order_item_request() -> CreateOrderItemDTO:
        return CreateOrderItemDTO(
            product_id=uuid.uuid4(),
            product_quantity=1
        )

    @staticmethod
    def generate_multiple_orders() -> List[CreateOrderDTO]:
        orders_list = []
        order1 = CreateOrderDTO(
            customer_id=uuid.uuid4()
        )

        order2 = CreateOrderDTO(
            customer_id=uuid.uuid4()
        )
        orders_list.append(order1)
        orders_list.append(order2)
        return orders_list

    @staticmethod
    def generate_order_entity() -> Order:
        return Order.create_new_order(
            customer_id=uuid.uuid4()
        )

    @staticmethod
    def generate_order_item_entity() -> OrderItem:
        return OrderItem.create(
            order_id=uuid.uuid4(),
            product_id=uuid.uuid4(),
            product_quantity=1
        )

    @staticmethod
    def generate_updated_order_entity() -> Order:
        return Order.create_new_order(
            customer_id=uuid.uuid4()
        )

    @staticmethod
    def generate_updated_order_item_entity() -> OrderItem:
        return OrderItem.create(
            order_id=uuid.uuid4(),
            product_id=uuid.uuid4(),
            product_quantity=1
        )

    @staticmethod
    def generate_multiple_order_entities() -> List[Order]:
        orders_list = []
        order1 = Order.create_new_order(
            customer_id=uuid.uuid4()
        )

        order2 = Order.create_new_order(
            customer_id=uuid.uuid4()
        )
        orders_list.append(order1)
        orders_list.append(order2)
        return orders_list
