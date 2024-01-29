import json

import pytest

from pytest_bdd import scenario, given, then, when
from starlette import status
from starlette.testclient import TestClient

from src.app import app
from tests.utils.order_helper import OrderHelper

client = TestClient(app)


@pytest.fixture
def generate_order_dto():
    return OrderHelper.generate_order_request()


@pytest.fixture
def generate_multiple_order_dtos():
    return OrderHelper.generate_multiple_orders()


@pytest.fixture
def request_order_creation(generate_order_dto):
    order = generate_order_dto
    req_body = {
        "customer_id": str(order.customer_id)
    }
    headers = {}
    response = client.post("/orders", json=req_body, headers=headers)

    resp_json = json.loads(response.content)
    result = resp_json["result"]
    order_id = result["orderId"]

    yield response
    # Teardown - Removes the order from the database
    client.delete(f"/orders/{order_id}", headers=headers)


@pytest.fixture
def request_multiple_orders_creation(generate_multiple_order_dtos):
    orders_list = generate_multiple_order_dtos
    order_ids_list = []
    headers = {}

    for order in orders_list:
        req_body = {
            "customer_id": str(order.customer_id)
        }
        response = client.post("/orders", json=req_body, headers=headers)

        resp_json = json.loads(response.content)
        result = resp_json["result"]
        order_id = result["orderId"]
        order_ids_list.append(order_id)
    yield order_ids_list
    # Teardown - Removes the order from the database
    for order_id in order_ids_list:
        client.delete(f"/orders/{order_id}", headers=headers)


@pytest.fixture
def create_order_without_teardown(generate_order_dto):
    order = generate_order_dto
    req_body = {
        "customer_id": str(order.customer_id)
    }
    headers = {}
    response = client.post("/orders", json=req_body, headers=headers)
    yield response.content


# Scenario: Get all orders

@scenario('../order.feature', 'Get all orders')
def test_get_all_orders():
    pass


@given('there are existing orders in the system', target_fixture='existing_orders_in_db')
def existing_orders_in_db(request_multiple_orders_creation):
    orders_id_list = request_multiple_orders_creation
    return orders_id_list


@when('I request to get all orders', target_fixture='request_all_orders')
def request_all_orders():
    headers = {}
    response = client.get(f"/orders/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive a list of orders')
def receive_correct_order(existing_orders_in_db, request_all_orders):
    orders_id_list = existing_orders_in_db
    response = request_all_orders
    resp_json = json.loads(response)
    result = resp_json["result"]

    assert type(result) == list

    for item in result:
        assert item["orderId"] in orders_id_list


# Scenario: Create a new order


@scenario('../order.feature', 'Create a new order')
def test_create_order():
    pass


@given('I submit a new order data', target_fixture='i_request_to_create_a_new_order_impl')
def i_request_to_create_a_new_order_impl(generate_order_dto, request_order_creation):
    response = request_order_creation
    return response


@then('the order should be created successfully')
def the_order_should_be_created_successfully_impl(i_request_to_create_a_new_order_impl, generate_order_dto):
    order = generate_order_dto
    resp_json = json.loads(i_request_to_create_a_new_order_impl.content)
    result = resp_json["result"]

    assert result["customerId"] == str(order.customer_id)



# Scenario: Get order by ID

@scenario('../order.feature', 'Get order by ID')
def test_get_order_by_id():
    pass


@given('there is a order with a specific ID', target_fixture='order_with_given_id')
def order_with_given_id(request_order_creation):
    response = request_order_creation
    resp_json = json.loads(response.content)
    result = resp_json["result"]
    return result["orderId"]


@when('I request to get the order by ID', target_fixture='request_order_by_id')
def request_order_by_id(order_with_given_id):
    order_id = order_with_given_id
    headers = {}
    response = client.get(f"/orders/id/{order_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive the order details by ID')
def receive_correct_order(order_with_given_id, request_order_by_id, generate_order_dto):
    order_id = order_with_given_id
    # order = generate_order_dto
    resp_json = json.loads(request_order_by_id)
    result = resp_json["result"]

    assert result["orderId"] == order_id



# Scenario: Remove a order

@scenario('../order.feature', 'Remove a order')
def test_remove_order():
    pass


@given('there is a order on database with specific id', target_fixture='existing_order_to_remove')
def existing_order_to_remove(create_order_without_teardown):
    order = create_order_without_teardown
    return order


@when('I request to remove a order', target_fixture='request_order_update')
def request_order_delete(existing_order_to_remove):
    response = existing_order_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]
    order_id = result["orderId"]

    headers = {}
    response = client.delete(f"/orders/{order_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('the order data is successfully removed')
def receive_correct_order(existing_order_to_remove):
    response = existing_order_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]
    order_id = result["orderId"]

    print(order_id)

    headers = {}
    response = client.get(f"/orders/id/{order_id}", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
