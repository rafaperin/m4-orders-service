import uuid
from typing import List

import pytest
from mockito import when, verify, ANY

from src.entities.models.order_entity import Order
from src.entities.models.order_item_entity import OrderItem
from src.interfaces.gateways.order_gateway_interface import IOrderGateway
from tests.utils.order_helper import OrderHelper


class MockRepository(IOrderGateway):

    def get_by_id(self, order_id: uuid.UUID) -> Order:
        pass

    def get_order_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> OrderItem:
        pass

    def get_all(self) -> List[Order]:
        pass

    def create_order(self, order_in: Order) -> Order:
        pass

    def create_order_item(self, item_in: OrderItem) -> OrderItem:
        pass

    def update(self, order_id: uuid.UUID, order_in: Order) -> Order:
        pass

    def update_item(self, obj_in: OrderItem):
        pass

    def remove_order(self, order_id: uuid.UUID) -> None:
        pass

    def remove_order_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> None:
        pass


order_repo = MockRepository()


@pytest.fixture
def unstub():
    from mockito import unstub
    yield
    unstub()


@pytest.fixture
def generate_new_order():
    return OrderHelper.generate_order_entity()


@pytest.fixture
def generate_new_order_item():
    return OrderHelper.generate_order_item_entity()


@pytest.fixture
def generate_updated_order():
    return OrderHelper.generate_updated_order_entity()


@pytest.fixture
def generate_updated_order_item():
    return OrderHelper.generate_updated_order_item_entity()


@pytest.fixture
def generate_multiple_orders():
    return OrderHelper.generate_multiple_order_entities()


def test_should_allow_register_order(generate_new_order, unstub):
    order = generate_new_order

    when(order_repo).create_order(ANY(Order)).thenReturn(order)

    created_order = order_repo.create_order(order)

    verify(order_repo, times=1).create_order(order)

    assert type(created_order) == Order
    assert created_order is not None
    assert created_order == order
    assert order.order_id == created_order.order_id
    assert order.customer_id == created_order.customer_id
    assert order.order_items == created_order.order_items
    assert order.creation_date == created_order.creation_date
    assert order.order_total == created_order.order_total


def test_should_allow_register_order_item(generate_new_order_item, unstub):
    order_item = generate_new_order_item

    when(order_repo).create_order_item(ANY(OrderItem)).thenReturn(order_item)

    created_order_item = order_repo.create_order_item(order_item)

    verify(order_repo, times=1).create_order_item(order_item)

    assert type(created_order_item) == OrderItem
    assert created_order_item is not None
    assert created_order_item == order_item
    assert order_item.order_id == created_order_item.order_id
    assert order_item.product_id == created_order_item.product_id
    assert order_item.product_quantity == created_order_item.product_quantity


def test_should_allow_retrieve_order_by_id(generate_new_order, unstub):
    order = generate_new_order
    order_id = order.order_id

    when(order_repo).get_by_id(ANY(uuid.UUID)).thenReturn(order)

    retrieved_order = order_repo.get_by_id(order_id)

    verify(order_repo, times=1).get_by_id(order_id)

    assert order.order_id == retrieved_order.order_id
    assert order.customer_id == retrieved_order.customer_id
    assert order.order_items == retrieved_order.order_items
    assert order.creation_date == retrieved_order.creation_date
    assert order.order_total == retrieved_order.order_total


def test_should_allow_list_orders(generate_multiple_orders, unstub):
    orders_list = generate_multiple_orders

    when(order_repo).get_all().thenReturn(orders_list)

    result = order_repo.get_all()

    verify(order_repo, times=1).get_all()

    assert type(result) == list
    assert len(result) == len(orders_list)
    for order in orders_list:
        assert order in result


def test_should_allow_retrieve_order_item(generate_new_order_item, unstub):
    order_item = generate_new_order_item
    order_id = order_item.order_id
    product_id = order_item.product_id

    when(order_repo).get_order_item(ANY(uuid.UUID), ANY(uuid.UUID)).thenReturn(order_item)

    retrieved_order = order_repo.get_order_item(order_id, product_id)

    verify(order_repo, times=1).get_order_item(order_id, product_id)

    assert order_item.order_id == retrieved_order.order_id
    assert order_item.product_id == retrieved_order.product_id
    assert order_item.product_quantity == retrieved_order.product_quantity


def test_should_allow_update_order(generate_new_order, generate_updated_order, unstub):
    order = generate_new_order
    order_id = order.order_id

    updated_order = generate_updated_order
    order.order_items = updated_order.order_items
    order.order_total = updated_order.order_total

    when(order_repo).update(ANY(uuid.UUID), ANY(Order)).thenReturn(order)

    created_order = order_repo.update(order_id, order)

    verify(order_repo, times=1).update(order_id, order)

    assert type(created_order) == Order
    assert created_order is not None
    assert created_order == order
    assert order.order_id == created_order.order_id
    assert order.customer_id == created_order.customer_id
    assert order.order_items == created_order.order_items
    assert order.creation_date == created_order.creation_date
    assert order.order_total == created_order.order_total


def test_should_allow_update_order_item(generate_new_order_item, generate_updated_order_item, unstub):
    order_item = generate_new_order_item

    updated_order = generate_updated_order_item
    order_item.product_quantity = updated_order.product_quantity

    when(order_repo).update_item(ANY(OrderItem)).thenReturn()

    order_repo.update_item(order_item)

    verify(order_repo, times=1).update_item(order_item)


def test_should_allow_remove_order(unstub):
    order_id = uuid.uuid4()

    when(order_repo).remove_order(ANY(uuid.UUID)).thenReturn()

    order_repo.remove_order(order_id)

    verify(order_repo, times=1).remove_order(order_id)


def test_should_allow_remove_order_item(unstub):
    order_id = uuid.uuid4()
    product_id = uuid.uuid4()

    when(order_repo).remove_order_item(ANY(uuid.UUID), ANY(uuid.UUID)).thenReturn()

    order_repo.remove_order_item(order_id, product_id)

    verify(order_repo, times=1).remove_order_item(order_id, product_id)
