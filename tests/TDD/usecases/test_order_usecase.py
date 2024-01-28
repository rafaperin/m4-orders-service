import uuid
from typing import List

import pytest
from mockito import when, verify, ANY

from src.config.errors import ResourceNotFound
from src.entities.models.order_entity import Order, OrderStatus
from src.entities.models.order_item_entity import OrderItem
from src.interfaces.gateways.order_gateway_interface import IOrderGateway
from src.interfaces.use_cases.order_usecase_interface import OrderUseCaseInterface
from src.usecases.order_usecase import OrderUseCase
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

    def create_order_item(self, item_in: OrderItem) -> Order:
        pass

    def update(self, order_id: uuid.UUID, order_in: Order) -> Order:
        pass

    def update_item(self, obj_in: OrderItem):
        pass

    def remove_order(self, order_id: uuid.UUID) -> None:
        pass

    def remove_order_item(self, order_id: uuid.UUID, product_id: uuid.UUID) -> None:
        pass


class MockUsecase(OrderUseCaseInterface):
    pass


order_repo = MockRepository()
order_usecase = OrderUseCase(order_repo)


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
def generate_new_order_dto():
    return OrderHelper.generate_order_request()


@pytest.fixture
def generate_new_order_item_dto():
    return OrderHelper.generate_order_item_request()


@pytest.fixture
def generate_updated_order():
    return OrderHelper.generate_updated_order_entity()


@pytest.fixture
def generate_multiple_orders():
    return OrderHelper.generate_multiple_order_entities()


def test_should_allow_register_order(generate_new_order_dto, unstub):
    order_dto = generate_new_order_dto
    order_entity = Order.create_new_order(
        customer_id=order_dto.customer_id
    )

    when(order_repo).create_order(ANY(Order)).thenReturn(order_entity)

    created_order = order_usecase.create_order(order_dto)

    assert created_order is not None
    assert order_entity.customer_id == created_order.customer_id
    assert order_entity.order_items == created_order.order_items
    assert order_entity.order_total == created_order.order_total


def test_should_allow_adding_item(generate_new_order, generate_new_order_item_dto, unstub):
    order = generate_new_order
    order_item_dto = generate_new_order_item_dto

    when(order_repo).get_order_item(ANY(uuid.UUID), ANY(uuid.UUID)).thenReturn()
    when(order_repo).get_by_id(ANY(uuid.UUID)).thenReturn(order)

    created_order = order_usecase.create_order_item(
        order.order_id, order_item_dto, 9.99, "Pendente"
    )

    verify(order_repo, times=1).get_order_item(order.order_id, order_item_dto.product_id)
    verify(order_repo, times=1).get_by_id(order.order_id)

    assert created_order is not None
    assert created_order.order_items is not None
    assert type(created_order.order_items) is list


def test_should_allow_retrieve_order_by_id(generate_new_order, unstub):
    order_entity = generate_new_order
    order_id = order_entity.order_id

    when(order_repo).get_by_id(ANY(uuid.UUID)).thenReturn(order_entity)

    retrieved_order = order_usecase.get_by_id(order_id)

    verify(order_repo, times=1).get_by_id(order_id)

    assert retrieved_order is not None
    assert order_entity.order_id == retrieved_order.order_id
    assert order_entity.customer_id == retrieved_order.customer_id
    assert order_entity.order_total == retrieved_order.order_total
    assert order_entity.order_items == retrieved_order.order_items


def test_should_raise_exception_invalid_id(unstub):
    order_id = uuid.uuid4()

    when(order_repo).get_by_id(ANY(uuid.UUID)).thenReturn()

    try:
        order_usecase.get_by_id(order_id)
        assert False
    except ResourceNotFound:
        assert True

    verify(order_repo, times=1).get_by_id(order_id)


def test_should_allow_list_orders(generate_multiple_orders, unstub):
    orders_list = generate_multiple_orders

    when(order_repo).get_all().thenReturn(orders_list)

    result = order_usecase.get_all()

    verify(order_repo, times=1).get_all()

    assert type(result) == list
    assert len(result) == len(orders_list)
    for order in orders_list:
        assert order in result


def test_should_allow_list_empty_orders(generate_multiple_orders, unstub):
    when(order_repo).get_all().thenReturn(list())

    result = order_usecase.get_all()

    assert result == list()
    verify(order_repo, times=1).get_all()


def test_should_allow_remove_order(generate_new_order, unstub):
    order = generate_new_order
    order_id = order.order_id
    order_status = OrderStatus.PENDING

    when(order_repo).get_by_id(ANY(uuid.UUID)).thenReturn(order)
    when(order_repo).remove_order(ANY(uuid.UUID)).thenReturn()

    order_usecase.remove_order(order_id, order_status)

    verify(order_repo, times=1).remove_order(order_id)


def test_should_allow_remove_order_item(generate_new_order, generate_new_order_item, unstub):
    order = generate_new_order
    order_item = generate_new_order_item

    order.order_items.append(order_item)
    order_id = order.order_id
    order_item.order_id = order_id
    order_status = OrderStatus.PENDING

    when(order_repo).get_by_id(ANY(uuid.UUID)).thenReturn(order)
    when(order_repo).get_order_item(ANY(uuid.UUID), ANY(uuid.UUID)).thenReturn(order_item)
    when(order_repo).remove_order_item(ANY(uuid.UUID), ANY(uuid.UUID)).thenReturn()

    order_usecase.remove_order_item(order_id, order_item.product_id, 9.99, order_status)

    verify(order_repo, times=1).get_by_id(order_id)
    verify(order_repo, times=1).get_order_item(order_id, order_item.product_id)
    verify(order_repo, times=1).remove_order_item(order_id, order_item.product_id)
