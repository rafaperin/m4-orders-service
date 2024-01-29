import uuid

from src.entities.schemas.order_dto import CreateOrderItemDTO, UpdateOrderItemDTO


class OrderItemHelper:

    @staticmethod
    def generate_order_item_request() -> CreateOrderItemDTO:
        return CreateOrderItemDTO(
            product_id=str(uuid.uuid4()),
            product_quantity=1
        )

    @staticmethod
    def generate_updated_order_item_data() -> UpdateOrderItemDTO:
        return UpdateOrderItemDTO(
            product_id=str(uuid.uuid4()),
            product_quantity=1
        )
