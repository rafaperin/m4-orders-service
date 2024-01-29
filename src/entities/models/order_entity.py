import datetime
import uuid
from dataclasses import dataclass
from decimal import Decimal
from typing import List

from src.entities.errors.order_error import OrderError
from src.entities.errors.order_item_error import OrderItemError
from src.entities.models.order_item_entity import OrderItem


class OrderStatus:
    PENDING = "Pendente"
    CONFIRMED = "Confirmado"
    IN_PROGRESS = "Em preparo"
    READY = "Pronto"
    FINALIZED = "Finalizado"


class PaymentStatus:
    PENDING = "Pendente"
    CONFIRMED = "Confirmado"
    REFUSED = "Negado"


@dataclass
class Order:
    order_id: uuid.UUID
    customer_id: uuid.UUID
    order_items: List[OrderItem]
    creation_date: datetime.datetime
    order_total: float

    @classmethod
    def create_new_order(cls, customer_id: uuid.UUID) -> "Order":
        order_id = uuid.uuid4()
        return cls(
            order_id,
            customer_id,
            list(),
            datetime.datetime.utcnow(),
            0.0,
        )

    @staticmethod
    def check_if_pending_order(order_status) -> None:
        print(order_status)
        if order_status != OrderStatus.PENDING:
            raise OrderError("Order already confirmed, modification not allowed!")

    def check_payment_status(self) -> None:
        if self.payment_status == PaymentStatus.PENDING:
            raise OrderError("Order payment id pending!")
        if self.payment_status == PaymentStatus.REFUSED:
            raise OrderError("Order payment was refused! Please contact your payment provider.")

    def add_order_item(self, order_item: OrderItem, product_price: float, order_status: str) -> None:
        self.check_if_pending_order(order_status)

        self.order_items.append(order_item)
        self.order_total = Decimal(self.order_total) + Decimal((order_item.product_quantity * product_price))  # type: ignore

    def update_item_quantity(self, order_item: OrderItem, product_price: float, order_status: str) -> None:
        self.check_if_pending_order(order_status)

        old_item = next((item for item in self.order_items if item.product_id == order_item.product_id), None)
        if old_item:
            self.order_total = self.order_total - Decimal((old_item.product_quantity * product_price))  # type: ignore
            self.order_items.remove(old_item)
            self.order_items.append(order_item)
            self.order_total = self.order_total + Decimal((order_item.product_quantity * product_price))  # type: ignore
        else:
            raise OrderItemError("Item not found")

    def remove_order_item(self, order_item: OrderItem, product_price: float, order_status: str) -> None:
        self.check_if_pending_order(order_status)

        self.order_total = Decimal(self.order_total) - Decimal((order_item.product_quantity * product_price))  # type: ignore
        self.order_items.remove(order_item)


def order_factory(
    order_id: uuid.UUID,
    customer_id: uuid.UUID,
    order_items: List[OrderItem],
    creation_date: datetime.datetime,
    order_total: float,
) -> Order:
    return Order(
        order_id=order_id,
        customer_id=customer_id,
        order_items=order_items,
        creation_date=creation_date,
        order_total=order_total,
    )
