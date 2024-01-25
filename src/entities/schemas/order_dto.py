import datetime
import uuid
from typing import Optional, List

from src.utils.utils import CamelModel


class OrderItemsDTO(CamelModel):
    order_id: uuid.UUID
    product_id: uuid.UUID
    product_quantity: int

    class Config:
        schema_extra = {
            "example": {
                "order_id": "00000000-0000-0000-0000-000000000000",
                "product_id": "00000000-0000-0000-0000-000000000000",
                "product_quantity": 1,
            }
        }


class CreateOrderItemDTO(CamelModel):
    product_id: uuid.UUID
    product_quantity: int

    class Config:
        schema_extra = {
            "example": {
                "product_id": "00000000-0000-0000-0000-000000000000",
                "product_quantity": 1,
            }
        }


class UpdateOrderItemDTO(CamelModel):
    product_id: uuid.UUID
    product_quantity: int

    class Config:
        schema_extra = {
            "example": {
                "product_id": "00000000-0000-0000-0000-000000000000",
                "product_quantity": 1,
            }
        }


class RemoveOrderItemDTO(CamelModel):
    product_id: uuid.UUID

    class Config:
        schema_extra = {
            "example": {
                "product_id": "00000000-0000-0000-0000-000000000000",
            }
        }


class OrderItemDTOResponse(CamelModel):
    result: OrderItemsDTO


class OrderItemDTOListResponse(CamelModel):
    result: List[OrderItemsDTO]


class OrderDTO(CamelModel):
    order_id: uuid.UUID
    customer_id: uuid.UUID
    order_items: List[OrderItemsDTO]
    creation_date: datetime.datetime
    order_total: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "order_id": "00000000-0000-0000-0000-000000000000",
                "customer_id": "00000000-0000-0000-0000-000000000000",
                "order_items": [
                    {
                        "order_id": "00000000-0000-0000-0000-000000000000",
                        "product_id": "00000000-0000-0000-0000-000000000000",
                        "product_quantity": 1,
                    }
                ],
                "creation_date": "2022-12-27 08:26:49.219717",
                "order_total": 0.0,
            }
        }


class CreateOrderDTO(CamelModel):
    customer_id: uuid.UUID

    class Config:
        schema_extra = {
            "example": {
                "customer_id": "00000000-0000-0000-0000-000000000000"
            }
        }


class OrderDTOResponse(CamelModel):
    result: OrderDTO


class OrderWithQrCodeDTO(CamelModel):
    order: OrderDTO
    qr_code: str


class OrderWithQrCodeDTOResponse(CamelModel):
    result: OrderWithQrCodeDTO


class OrderDTOListResponse(CamelModel):
    result: List[OrderDTO]
