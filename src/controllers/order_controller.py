import uuid

from fastapi import APIRouter

from src.adapters.order_json_adapter import order_list_to_json, order_to_json
from src.config.errors import RepositoryError, ResourceNotFound, DomainError
from src.entities.errors.order_item_error import OrderItemError
from src.entities.schemas.order_dto import CreateOrderDTO, CreateOrderItemDTO, UpdateOrderItemDTO, RemoveOrderItemDTO
from src.gateways.postgres_gateways.order_gateway import PostgresDBOrderRepository
from src.usecases.order_usecase import OrderUseCase

router = APIRouter()


class OrderController:
    @staticmethod
    async def get_all_orders() -> dict:
        order_gateway = PostgresDBOrderRepository()

        try:
            all_orders = OrderUseCase(order_gateway).get_all()
            result = order_list_to_json(all_orders)
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def get_order_by_id(
        order_id: uuid.UUID
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()

        try:
            order = OrderUseCase(order_gateway).get_by_id(order_id)
            result = order_to_json(order)
        except ResourceNotFound:
            raise ResourceNotFound.get_operation_failed(f"No order with id: {order_id}")
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def create_order(
        request: CreateOrderDTO
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()

        try:
            order = OrderUseCase(order_gateway).create_order(request)
            result = order_to_json(order)
        except Exception as e:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def add_order_items(
        request: CreateOrderItemDTO,
        order_id: uuid.UUID,
        product_price: float,
        order_status: str
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()

        try:
            order = OrderUseCase(order_gateway).create_order_item(order_id, request, product_price, order_status)
            result = order_to_json(order)
        except DomainError:
            raise OrderItemError.modification_blocked()
        except Exception as e:
            print(e)
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def change_order_item_quantity(
        order_id: uuid.UUID,
        request: UpdateOrderItemDTO
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()

        try:
            order = OrderUseCase(order_gateway).update_quantity(order_id, request)
            result = order_to_json(order)
        except DomainError:
            raise OrderItemError.modification_blocked()
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def remove_order(
        order_id: uuid.UUID,
        order_status: str
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()
        try:
            OrderUseCase(order_gateway).remove_order(order_id, order_status)
        except DomainError:
            raise OrderItemError.modification_blocked()
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": "Order removed successfully"}

    @staticmethod
    async def remove_order_item(
        order_id: uuid.UUID,
        request: RemoveOrderItemDTO,
        product_price: float,
        order_status: str
    ) -> dict:
        order_gateway = PostgresDBOrderRepository()

        try:
            OrderUseCase(order_gateway).remove_order_item(order_id, request.product_id, product_price, order_status)
        except DomainError:
            raise OrderItemError.modification_blocked()
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": "Order item removed successfully"}
