import uuid
from abc import ABC

from src.entities.models.order_entity import Order, PaymentStatus
from src.entities.models.order_item_entity import OrderItem
from src.entities.schemas.order_dto import CreateOrderDTO, CreateOrderItemDTO
from src.interfaces.gateways.order_gateway_interface import IOrderGateway


class OrderUseCaseInterface(ABC):
    def __init__(self, order_repo: IOrderGateway) -> None:
        raise NotImplementedError

    def get_by_id(self, order_id: uuid.UUID):
        pass

    def get_all(self):
        pass

    def create_order(self, input_dto: CreateOrderDTO) -> Order:
        pass

    def get_order_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> OrderItem:
        pass

    def add_item(
        self, order_id: uuid.UUID, input_dto: CreateOrderItemDTO, product_price: float, order_status: str
    ) -> Order:
        pass

    def remove_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> Order:
        pass

    def remove_order(self, order_id: uuid.UUID, order_status: str) -> None:
        pass

    def remove_order_item(
        self, order_id: uuid.UUID, product_id: uuid.UUID, product_price: float, order_status: str
    ) -> None:
        pass
