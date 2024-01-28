import json
import uuid

import httpx
from fastapi import APIRouter, status

from src.api.errors.api_errors import APIErrorMessage
from src.config.config import settings
from src.config.errors import RepositoryError, ResourceNotFound, DomainError
from src.controllers.order_controller import OrderController
from src.entities.errors.order_item_error import OrderItemError
from src.entities.schemas.order_dto import OrderDTOListResponse, OrderDTOResponse, CreateOrderDTO, CreateOrderItemDTO, \
    UpdateOrderItemDTO, RemoveOrderItemDTO

router = APIRouter()


@router.get(
    "/orders", tags=["Orders"],
    response_model=OrderDTOListResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_all_orders() -> dict:
    try:
        result = await OrderController.get_all_orders()
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/orders/id/{order_id}", tags=["Orders"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_order_by_id(
    order_id: uuid.UUID
) -> dict:
    try:
        result = await OrderController.get_order_by_id(order_id)
    except ResourceNotFound:
        raise ResourceNotFound.get_operation_failed(f"No order with id: {order_id}")
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.post(
    "/orders",  tags=["Orders"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def create_order(
    request: CreateOrderDTO
) -> dict:
    try:
        result = await OrderController.create_order(request)
        order_id = result["result"]["orderId"]

        headers = {
            #     "Authorization": f"Bearer {access_token}",
        }

        params = {
            "order_id": str(order_id)
        }

        httpx.post(
            f"{settings.ORDERS_STATUS_SERVICE}/order-status",
            headers=headers, json=params
        )

        httpx.post(
            f"{settings.PAYMENTS_SERVICE}/payments",
            headers=headers, json=params
        )

    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return result


@router.post(
    "/orders/{order_id}/items", tags=["Order Items"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def add_order_items(
    request: CreateOrderItemDTO,
    order_id: uuid.UUID
) -> dict:
    try:
        headers = {
            #     "Authorization": f"Bearer {access_token}",
        }

        r = httpx.get(f"{settings.PRODUCTS_SERVICE}/products/id/{request.product_id}", headers=headers)
        json_response = json.loads(r.content)
        product = json_response["result"]

        r = httpx.get(f"{settings.ORDERS_STATUS_SERVICE}/order-status/id/{order_id}/status", headers=headers)
        json_response = json.loads(r.content)
        order_status = json_response["result"]

        result = await OrderController.add_order_items(
            request, order_id, product["price"], order_status["orderStatus"]
        )
    except DomainError:
        raise OrderItemError.modification_blocked()
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/orders/{order_id}/items",  tags=["Order Items"],
    response_model=OrderDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def change_order_item_quantity(
    order_id: uuid.UUID,
    request: UpdateOrderItemDTO
) -> dict:
    try:
        result = await OrderController.change_order_item_quantity(order_id, request)
    except DomainError:
        raise OrderItemError.modification_blocked()
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.delete(
    "/orders/{order_id}", tags=["Orders"],
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def remove_order(
    order_id: uuid.UUID
) -> dict:
    try:
        headers = {
            #     "Authorization": f"Bearer {access_token}",
        }

        r = httpx.get(f"{settings.ORDERS_STATUS_SERVICE}/order-status/id/{order_id}/status", headers=headers)
        json_response = json.loads(r.content)
        order_status = json_response["result"]

        await OrderController.remove_order(order_id, order_status)
    except DomainError:
        raise OrderItemError.modification_blocked()
    except Exception:
        raise RepositoryError.save_operation_failed()

    return {"result": "Order removed successfully"}


@router.delete(
    "/orders/{order_id}/items", tags=["Order Items"],
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def remove_order_item(
    order_id: uuid.UUID,
    request: RemoveOrderItemDTO
) -> dict:
    try:
        headers = {
            #     "Authorization": f"Bearer {access_token}",
        }

        r = httpx.get(f"{settings.PRODUCTS_SERVICE}/products/id/{request.product_id}", headers=headers)
        json_response = json.loads(r.content)
        product = json_response["result"]

        r = httpx.get(f"{settings.ORDERS_STATUS_SERVICE}/order-status/id/{order_id}/status", headers=headers)
        json_response = json.loads(r.content)
        order_status = json_response["result"]

        await OrderController.remove_order_item(order_id, request, product["price"], order_status["orderStatus"])
    except DomainError:
        raise OrderItemError.modification_blocked()
    except Exception:
        raise RepositoryError.save_operation_failed()

    return {"result": "Order item removed successfully"}
