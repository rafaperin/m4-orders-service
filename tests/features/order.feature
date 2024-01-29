Feature: Order Management

  Scenario: Create a new order
    Given I submit a new order data
    Then the order should be created successfully

  Scenario: Get order by ID
    Given there is a order with a specific ID
    When I request to get the order by ID
    Then I should receive the order details by ID

  Scenario: Get all orders
    Given there are existing orders in the system
    When I request to get all orders
    Then I should receive a list of orders

  Scenario: Remove a order
    Given there is a order on database with specific id
    When I request to remove a order
    Then the order data is successfully removed