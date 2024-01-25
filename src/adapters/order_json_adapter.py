from typing import List

from src.entities.models.order_entity import Order
from src.entities.models.order_item_entity import OrderItem
from src.utils.utils import camelize_dict


def order_to_json(order: Order):
    if order.order_items:
        items_list = order.__dict__.pop("order_items")
        items_json = order_item_list_to_json(items_list)

        order_json = camelize_dict(order.__dict__)
        order_json["orderItems"] = items_json
    else:
        order.__dict__.pop("order_items")
        order_json = camelize_dict(order.__dict__)
        order_json["orderItems"] = list()
    return order_json


def order_list_to_json(order_list: List[Order]):
    return [order_to_json(order) for order in order_list]


def order_item_to_json(order_item: OrderItem):
    return camelize_dict(order_item.__dict__)


def order_item_list_to_json(order_item_list: List[OrderItem]):
    return [camelize_dict(order_item.__dict__) for order_item in order_item_list]
