Feature: Order Item Management

  Scenario: Create a new order item
    Given I submit a new order item data
    Then the order item should be created successfully

  Scenario: Update order item data
    Given there is a registered order item
    When I request to update an order item
    Then the order item data is successfully updated

  Scenario: Remove an order item
    Given there is an order item on database with specific id
    When I request to remove an order item
    Then the order item data is successfully removed