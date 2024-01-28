import uuid

from src.config.errors import ResourceNotFound

from src.entities.schemas.order_dto import CreateOrderDTO, UpdateOrderItemDTO, CreateOrderItemDTO
from src.entities.models.order_entity import Order
from src.entities.models.order_item_entity import OrderItem
from src.interfaces.gateways.order_gateway_interface import IOrderGateway
from src.interfaces.use_cases.order_usecase_interface import OrderUseCaseInterface


class OrderUseCase(OrderUseCaseInterface):
    def __init__(self, order_repo: IOrderGateway) -> None:
        self._order_repo = order_repo

    def get_by_id(self, order_id: uuid.UUID):
        result = self._order_repo.get_by_id(order_id)
        if not result:
            raise ResourceNotFound
        else:
            return result

    def get_all(self):
        return self._order_repo.get_all()

    def create_order(self, input_dto: CreateOrderDTO) -> Order:
        order = Order.create_new_order(input_dto.customer_id)
        self._order_repo.create_order(order)
        return order

    def update_quantity(
        self, order_id: uuid.UUID, input_dto: UpdateOrderItemDTO, product_price: float, order_status: str
    ) -> Order:
        order = self._order_repo.get_by_id(order_id)
        item = OrderItem.create(order_id, input_dto.product_id, input_dto.product_quantity)

        order.update_item_quantity(item, product_price, order_status)

        self._order_repo.update_item(item)
        updated_order = self._order_repo.update(order_id, order)
        return updated_order

    def create_order_item(
        self, order_id: uuid.UUID, input_dto: CreateOrderItemDTO, product_price: float, order_status: str
    ) -> Order:
        item = self._order_repo.get_order_item(order_id, input_dto.product_id)

        if item:
            update_dto = UpdateOrderItemDTO(
                order_id=order_id,
                product_id=input_dto.product_id,
                product_quantity=input_dto.product_quantity + item.product_quantity
            )
            return self.update_quantity(order_id, update_dto, product_price, order_status)

        order = self._order_repo.get_by_id(order_id)
        item = OrderItem.create(order_id, input_dto.product_id, input_dto.product_quantity)

        order.add_order_item(item, product_price, order_status)

        self._order_repo.create_order_item(item)
        self._order_repo.update(order_id, order)
        return order

    def remove_order(self, order_id: uuid.UUID, order_status: str) -> None:
        order = self._order_repo.get_by_id(order_id)
        order.check_if_pending_order(order_status)
        self._order_repo.remove_order(order_id)

    def remove_order_item(
        self, order_id: uuid.UUID, product_id: uuid.UUID, product_price: float, order_status: str
    ) -> Order:
        order = self._order_repo.get_by_id(order_id)
        item = self._order_repo.get_order_item(order_id, product_id)

        order.remove_order_item(item, product_price, order_status)

        self._order_repo.remove_order_item(order_id, product_id)
        updated_order = self._order_repo.update(order_id, order)
        return updated_order
