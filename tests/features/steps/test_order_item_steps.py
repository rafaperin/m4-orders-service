import json
import uuid

import pytest

from pytest_bdd import scenario, given, then, when
from starlette import status
from starlette.testclient import TestClient

from src.app import app
from tests.utils.order_helper import OrderHelper
from tests.utils.order_item_helper import OrderItemHelper

client = TestClient(app)


@pytest.fixture
def generate_order_dto():
    return OrderHelper.generate_order_request()


@pytest.fixture
def generate_multiple_order_dtos():
    return OrderHelper.generate_multiple_orders()


@pytest.fixture
def generate_order_item_dto():
    return OrderItemHelper.generate_order_item_request()


@pytest.fixture
def generate_update_order_item_dto():
    return OrderItemHelper.generate_updated_order_item_data()


@pytest.fixture
def request_order_item_creation(generate_order_item_dto, generate_order_dto):
    headers = {}

    order = generate_order_dto
    req_body = {
        "customer_id": str(uuid.uuid4()),
    }
    order_response = client.post("/orders", json=req_body, headers=headers)

    order_item = generate_order_item_dto
    req_body = {
        "product_id": str(order_item.product_id),
        "product_quantity": order_item.product_quantity
    }

    # TODO: Deveria ser /orders/{order_id}/items
    response = client.post("/orders/{order_id}/items", json=req_body, headers=headers)

    resp_json = json.loads(response.content)
    result = resp_json["result"]
    product_id = result["productId"]
    delete_body = {

    }

    yield response
    # Teardown - Removes the customer from the database
    # TODO: Deveria ser /orders/{order_id}/items enviando no corpo o product_id
    client.delete(f"/orders/{order_id}/items", json=delete_body, headers=headers)


@pytest.fixture
def create_order_item_without_teardown(generate_order_item_dto):
    order_item = generate_order_item_dto
    req_body = {
        "product_id": str(order_item.product_id),
        "product_quantity": order_item.product_quantity
    }
    headers = {}

    # TODO: Deveria ser /orders/{order_id}/items enviando no corpo o req_body da linha 51
    response = client.post("/orders", json=req_body, headers=headers)
    yield response.content


# Scenario: Create a new order item


@scenario('../order_item.feature', 'Create a new order item')
def test_create_order_item():
    pass


@given('I submit a new order item data', target_fixture='i_request_to_create_a_new_order_item_impl')
def i_request_to_create_a_new_order_item_impl(generate_order_item_dto, request_order_item_creation):
    response = request_order_item_creation
    return response


@then('the order item should be created successfully')
def the_product_should_be_created_successfully_impl(i_request_to_create_a_new_order_item_impl, generate_order_item_dto):
    order_item = generate_order_item_dto
    resp_json = json.loads(i_request_to_create_a_new_order_item_impl.content)
    result = resp_json["result"]

    # TODO: Fiz para acessar a propriedade dentro do objeto order_items, seria assim?
    assert result["order_items"][0]["product_id"] == str(order_item.product_id)
    assert result["order_items"][0]["product_quantity"] == order_item.product_quantity


# Scenario: Update order item data

@scenario('../order_item.feature', 'Update order item data')
def test_update_customer():
    pass


@given('there is a registered order item', target_fixture='existing_order_item')
def existing_order_item(request_order_item_creation):
    response = request_order_item_creation
    resp_json = json.loads(response.content)
    result = resp_json["result"]
    return result


@when('I request to update an order item', target_fixture='request_order_item_update')
def request_order_item_update(existing_order_item, generate_update_order_item_dto):
    order_item = existing_order_item
    order_id = order_item["order_id"]

    updated_order_item = generate_update_order_item_dto
    req_body = {
        "product_id": updated_order_item.product_id,
        "product_quantity": updated_order_item.product_quantity
    }

    headers = {}
    #TODO: Verificar
    response = client.put(f"/orders/{order_id}/items", json=req_body, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('the order item data is successfully updated')
def receive_correct_order_item(request_order_item_update, generate_update_order_item_dto):
    updated_order_item = generate_update_order_item_dto

    response = request_order_item_update
    resp_json = json.loads(response)
    result = resp_json["result"]

    # TODO: Fiz para acessar a propriedade dentro do objeto order_items, seria assim?
    assert result["order_items"][0]["product_id"] == updated_order_item.product_id
    assert result["order_items"][0]["product_quantity"] == updated_order_item.product_quantity


# Scenario: Remove a customer

@scenario('../order_item.feature', 'Remove an order item')
def test_remove_product():
    pass


@given('there is an order item on database with specific id', target_fixture='existing_order_item_to_remove')
def existing_order_item_to_remove(create_order_item_without_teardown):
    order_item = create_order_item_without_teardown
    return order_item


@when('I request to remove a product', target_fixture='request_product_update')
def request_product_delete(existing_product_to_remove):
    response = existing_product_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]
    order_id = result["order_id"]

    headers = {}

    #TODO: Necessario enviar com product id no body
    response = client.delete(f"/orders/{order_id}/items", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('the order item data is successfully removed')
def receive_correct_order_item(existing_order_item_to_remove):
    response = existing_order_item_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]
    order_id = result["order_id"]

    headers = {}

    # TODO: Necessario enviar com product id no body
    response = client.get(f"/orders/{order_id}/items", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
