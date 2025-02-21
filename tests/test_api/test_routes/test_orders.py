import pytest

# Provided test data for users
USER_CUSTOMER = {
    "name": "Lera",
    "surname": "Novikova",
    "email": "LeraNovik33@yandex.ru",
    "role": "customer"
}

USER_MANAGER = {
    "name": "Boris",
    "surname": "Sokolov",
    "email": "SokolBorya21@gmail.com",
    "role": "manager"
}

# Provided test data for cars
CAR_CREATE_VALID = {
    "brand": "Toyota",
    "model": "Camry",
    "price": 30000,
    "year": 2020,
    "color": "Blue",
    "mileage": 15000,
    "transmission": "automatic",  # valid values: 'automatic', 'manual'
    "engine": "gasoline",  # valid values: 'electric', 'gasoline', 'diesel'
    "vin_number": "VIN1234567890"
}

NON_EXISTENT_ID = 9999999  # A high number assumed to be non-existent in the test DB


# ---------------------------
# Fixtures to create required entities
# ---------------------------
@pytest.fixture
async def customer(client):
    """
    Create a customer using the provided USER_CUSTOMER data.
    """
    response = await client.post("/users/create", json=USER_CUSTOMER)
    assert response.status_code == 200, f"Failed to create customer: {response.text}"
    return response.json()["data"]


@pytest.fixture
async def manager(client):
    """
    Create a manager (salesperson) using the provided USER_MANAGER data.
    """
    response = await client.post("/users/create", json=USER_MANAGER)
    assert response.status_code == 200, f"Failed to create manager: {response.text}"
    return response.json()["data"]


@pytest.fixture
async def car(client):
    """
    Create a car using the provided CAR_CREATE_VALID data.
    """
    response = await client.post("/cars/add", json=CAR_CREATE_VALID)
    assert response.status_code == 200, f"Failed to create car: {response.text}"
    return response.json()["data"]


@pytest.fixture
async def order_payload(customer, manager, car):
    """
    Build a valid order creation payload using IDs from created entities.
    OrderCreateSchema requires: user_id, car_id, salesperson_id, status, and comments.
    """
    return {
        "user_id": customer["id"],
        "car_id": car["id"],
        "salesperson_id": manager["id"],
        "status": "pending",  # valid statuses: pending, completed, canceled
        "comments": "Test order creation."
    }


# ---------------------------
# POST /orders/create tests
# ---------------------------
@pytest.mark.asyncio
async def test_create_order_success(client, order_payload):
    """
    Test successful creation of a new order.
    Expects a 200 status code with "Order created." message and valid order data.
    """
    response = await client.post("/orders/create", json=order_payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "success", f"Unexpected status: {data['status']}"
    assert data["message"] == "Order created.", f"Unexpected message: {data['message']}"
    order = data["data"]
    # Validate that each field matches the payload
    for key, value in order_payload.items():
        assert order[key] == value, f"Mismatch for field '{key}': expected {value}, got {order.get(key)}"
    assert "id" in order, "Created order is missing an 'id'."
    assert "created_at" in order, "Created order is missing 'created_at'."


@pytest.mark.asyncio
async def test_create_order_nonexistent_customer(client, order_payload):
    """
    Test creating an order when the customer does not exist.
    Expects a 404 error with a message indicating that the customer was not found.
    """
    payload = order_payload.copy()
    payload["user_id"] = NON_EXISTENT_ID
    response = await client.post("/orders/create", json=payload)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    expected_detail = f"Customer with ID: '{NON_EXISTENT_ID}' was not found."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


@pytest.mark.asyncio
async def test_create_order_customer_role_mismatch(client, order_payload, manager):
    """
    Test creating an order when the provided customer ID belongs to a non-customer.
    Expects a 400 error indicating role mismatch.
    """
    payload = order_payload.copy()
    # Use manager's ID instead of a customer's ID
    payload["user_id"] = manager["id"]
    response = await client.post("/orders/create", json=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    detail = response.json()["detail"]
    expected_detail = f"The user with ID: '{manager['id']}' is a manager, not a customer."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


@pytest.mark.asyncio
async def test_create_order_nonexistent_salesperson(client, order_payload):
    """
    Test creating an order when the salesperson does not exist.
    Expects a 404 error with a message indicating that the salesperson was not found.
    """
    payload = order_payload.copy()
    payload["salesperson_id"] = NON_EXISTENT_ID
    response = await client.post("/orders/create", json=payload)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    expected_detail = f"Salesperson with ID: '{NON_EXISTENT_ID}' was not found."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


@pytest.mark.asyncio
async def test_create_order_salesperson_role_mismatch(client, order_payload, customer):
    """
    Test creating an order when the salesperson's ID belongs to a non-manager.
    Expects a 400 error indicating role mismatch.
    """
    payload = order_payload.copy()
    # Use customer's ID as salesperson
    payload["salesperson_id"] = customer["id"]
    response = await client.post("/orders/create", json=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    detail = response.json()["detail"]
    expected_detail = f"The user with ID: '{customer['id']}' is a customer, not a manager."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


@pytest.mark.asyncio
async def test_create_order_nonexistent_car(client, order_payload):
    """
    Test creating an order when the car does not exist.
    Expects a 404 error with a message indicating that the car was not found.
    """
    payload = order_payload.copy()
    payload["car_id"] = NON_EXISTENT_ID
    response = await client.post("/orders/create", json=payload)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    expected_detail = f"Car with ID: '{NON_EXISTENT_ID}' was not found."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


# ---------------------------
# GET /orders/{order_id} tests
# ---------------------------
@pytest.mark.asyncio
async def test_get_order_by_id_success(client, order_payload):
    """
    Test retrieving an order by its ID.
    Expects a 200 status code and that the order data matches the created order.
    """
    create_resp = await client.post("/orders/create", json=order_payload)
    assert create_resp.status_code == 200, f"Error creating order: {create_resp.text}"
    order_id = create_resp.json()["data"]["id"]

    get_resp = await client.get(f"/orders/{order_id}")
    assert get_resp.status_code == 200, f"Expected 200, got {get_resp.status_code}"
    data = get_resp.json()
    assert data["status"] == "success", "Unexpected status in order retrieval."
    assert data["message"] == "Order found.", "Unexpected message in order retrieval."
    assert data["data"]["id"] == order_id, "Returned order ID does not match the created order."


@pytest.mark.asyncio
async def test_get_order_by_id_not_found(client):
    """
    Test retrieving an order with a non-existent ID.
    Expects a 404 error with an 'Order not found.' message.
    """
    response = await client.get(f"/orders/{NON_EXISTENT_ID}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    assert detail == "Order not found.", f"Unexpected detail message: {detail}"


# ---------------------------
# GET /orders/status/{status} tests
# ---------------------------
@pytest.mark.asyncio
async def test_get_orders_by_status_success(client, order_payload):
    """
    Test retrieving orders by status.
    Expects the created order(s) with the specified status to be returned.
    """
    create_resp = await client.post("/orders/create", json=order_payload)
    assert create_resp.status_code == 200, f"Error creating order: {create_resp.text}"

    status_resp = await client.get("/orders/status/pending")
    assert status_resp.status_code == 200, f"Expected 200, got {status_resp.status_code}"
    data = status_resp.json()
    if data["status"] == "success":
        assert "pending" in data["message"], "Unexpected message for orders by status."
        returned_ids = [order["id"] for order in data["data"]]
        assert create_resp.json()["data"]["id"] in returned_ids, "Created order not found in status filter."
    else:
        pytest.fail(f"Expected success status, got {data['status']}: {data}")


@pytest.mark.asyncio
async def test_get_orders_by_status_empty(client):
    """
    Test retrieving orders by a status when no orders exist with that status.
    Expects an 'error' status with an appropriate message and an empty list.
    """
    # Assuming no orders with status "canceled" exist at the start of the test.
    status_resp = await client.get("/orders/status/canceled")
    assert status_resp.status_code == 200, f"Expected 200, got {status_resp.status_code}"
    data = status_resp.json()
    assert data["status"] == "error", f"Expected error status, got {data['status']}"
    expected_msg = "No orders with status: 'canceled' found."
    assert expected_msg in data["message"], f"Unexpected message: {data['message']}"
    assert data["data"] == [] or data["data"] is None, "Expected an empty list when no orders are found."


# ---------------------------
# GET /orders/customer_id/{customer_id} tests
# ---------------------------
@pytest.mark.asyncio
async def test_get_orders_by_customer_id_success(client, order_payload, customer):
    """
    Test retrieving orders by customer ID.
    Expects orders associated with the given customer to be returned.
    """
    create_resp = await client.post("/orders/create", json=order_payload)
    assert create_resp.status_code == 200, f"Error creating order: {create_resp.text}"

    cust_resp = await client.get(f"/orders/customer_id/{customer['id']}")
    assert cust_resp.status_code == 200, f"Expected 200, got {cust_resp.status_code}"
    data = cust_resp.json()
    if data["status"] == "success":
        expected_msg = f"Orders for customer with ID: '{customer['id']}' found."
        assert expected_msg in data["message"]
        returned_ids = [order["id"] for order in data["data"]]
        assert create_resp.json()["data"]["id"] in returned_ids, "Created order not found for customer."
    else:
        pytest.fail(f"Expected success status, got {data['status']}: {data}")


@pytest.mark.asyncio
async def test_get_orders_by_customer_id_nonexistent(client):
    """
    Test retrieving orders by a non-existent customer ID.
    Expects a 404 error indicating that the customer was not found.
    """
    response = await client.get(f"/orders/customer_id/{NON_EXISTENT_ID}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    expected_detail = f"Customer with ID: '{NON_EXISTENT_ID}' was not found."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


@pytest.mark.asyncio
async def test_get_orders_by_customer_id_role_mismatch(client, manager):
    """
    Test retrieving orders using a customer ID that belongs to a non-customer.
    Expects a 400 error indicating a role mismatch.
    """
    response = await client.get(f"/orders/customer_id/{manager['id']}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    detail = response.json()["detail"]
    expected_detail = f"The user with ID: '{manager['id']}' is a manager, not a customer."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


# ---------------------------
# GET /orders/salesperson_id/{salesperson_id} tests
# ---------------------------
@pytest.mark.asyncio
async def test_get_orders_by_salesperson_id_success(client, order_payload, manager):
    """
    Test retrieving orders by salesperson ID.
    Expects orders associated with the given salesperson to be returned.
    """
    create_resp = await client.post("/orders/create", json=order_payload)
    assert create_resp.status_code == 200, f"Error creating order: {create_resp.text}"

    sp_resp = await client.get(f"/orders/salesperson_id/{manager['id']}")
    assert sp_resp.status_code == 200, f"Expected 200, got {sp_resp.status_code}"
    data = sp_resp.json()
    if data["status"] == "success":
        expected_msg = f"Orders for salesperson with ID: '{manager['id']}' found."
        assert expected_msg in data["message"]
        returned_ids = [order["id"] for order in data["data"]]
        assert create_resp.json()["data"]["id"] in returned_ids, "Created order not found for salesperson."
    else:
        pytest.fail(f"Expected success status, got {data['status']}: {data}")


@pytest.mark.asyncio
async def test_get_orders_by_salesperson_id_nonexistent(client):
    """
    Test retrieving orders by a non-existent salesperson ID.
    Expects a 404 error indicating that the salesperson was not found.
    """
    response = await client.get(f"/orders/salesperson_id/{NON_EXISTENT_ID}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    expected_detail = f"Salesperson with ID: '{NON_EXISTENT_ID}' was not found."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


@pytest.mark.asyncio
async def test_get_orders_by_salesperson_id_role_mismatch(client, customer):
    """
    Test retrieving orders using a salesperson ID that belongs to a non-manager.
    Expects a 400 error indicating a role mismatch.
    """
    response = await client.get(f"/orders/salesperson_id/{customer['id']}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    detail = response.json()["detail"]
    expected_detail = f"The user with ID: '{customer['id']}' is a customer, not a manager."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


# ---------------------------
# GET /orders/car_id/{car_id} tests
# ---------------------------
@pytest.mark.asyncio
async def test_get_orders_by_car_id_success(client, order_payload, car):
    """
    Test retrieving orders by car ID.
    Expects orders associated with the given car to be returned.
    """
    create_resp = await client.post("/orders/create", json=order_payload)
    assert create_resp.status_code == 200, f"Error creating order: {create_resp.text}"

    car_resp = await client.get(f"/orders/car_id/{car['id']}")
    assert car_resp.status_code == 200, f"Expected 200, got {car_resp.status_code}"
    data = car_resp.json()
    if data["status"] == "success":
        expected_msg = f"Orders for car with ID: '{car['id']}' found."
        assert expected_msg in data["message"]
        returned_ids = [order["id"] for order in data["data"]]
        assert create_resp.json()["data"]["id"] in returned_ids, "Created order not found for car."
    else:
        pytest.fail(f"Expected success status, got {data['status']}: {data}")


@pytest.mark.asyncio
async def test_get_orders_by_car_id_nonexistent(client):
    """
    Test retrieving orders by a non-existent car ID.
    Expects a 404 error indicating that the car was not found.
    """
    response = await client.get(f"/orders/car_id/{NON_EXISTENT_ID}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    expected_detail = f"Car with ID: '{NON_EXISTENT_ID}' was not found."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


# ---------------------------
# GET /orders/ tests
# ---------------------------
@pytest.mark.asyncio
async def test_get_all_orders(client, order_payload):
    """
    Test retrieving all orders in the system.
    Expects all created orders to appear in the returned list.
    """
    # Create two orders.
    resp1 = await client.post("/orders/create", json=order_payload)
    resp2 = await client.post("/orders/create", json=order_payload)
    assert resp1.status_code == 200, f"Error creating first order: {resp1.text}"
    assert resp2.status_code == 200, f"Error creating second order: {resp2.text}"

    all_resp = await client.get("/orders/")
    assert all_resp.status_code == 200, f"Error retrieving all orders: {all_resp.text}"
    data = all_resp.json()
    if data["status"] == "success":
        assert data["message"] == "All orders found.", "Unexpected message when retrieving all orders."
        returned_ids = [order["id"] for order in data["data"]]
        assert resp1.json()["data"]["id"] in returned_ids, "First order not found in all orders list."
        assert resp2.json()["data"]["id"] in returned_ids, "Second order not found in all orders list."
    else:
        pytest.fail(f"Expected success status, got {data['status']}: {data}")


# ---------------------------
# PATCH /orders/patch/{order_id} tests
# ---------------------------
@pytest.mark.asyncio
async def test_update_order_success(client, order_payload):
    """
    Test successful update of an order's details.
    Expects a 200 status code and that the updated fields reflect the payload.
    Note: We include all related entity IDs in the update payload to ensure that
    the repository update function receives a complete set of fields.
    """
    # Create an order first.
    create_resp = await client.post("/orders/create", json=order_payload)
    assert create_resp.status_code == 200, f"Error creating order: {create_resp.text}"
    order_id = create_resp.json()["data"]["id"]

    # Prepare an update payload including all related IDs.
    update_payload = {
        "comments": "Updated order comment",
        "status": "completed",
        "user_id": order_payload["user_id"],
        "car_id": order_payload["car_id"],
        "salesperson_id": order_payload["salesperson_id"]
    }
    patch_resp = await client.patch(f"/orders/patch/{order_id}", json=update_payload)
    assert patch_resp.status_code == 200, f"Expected 200, got {patch_resp.status_code}. Error: {patch_resp.text}"

    data = patch_resp.json()
    assert data["status"] == "success", "Unexpected status after update."
    expected_msg = f"Order with id: '{order_id}' successfully updated."
    assert expected_msg in data["message"], "Unexpected update confirmation message."

    updated_order = data["data"]
    for key, value in update_payload.items():
        assert updated_order[key] == value, f"Field '{key}' was not updated correctly."


@pytest.mark.asyncio
async def test_update_order_nonexistent(client):
    """
    Test updating a non-existent order.
    Expects a 404 error with a message indicating that the order does not exist.
    """
    update_payload = {
        "comments": "Updated order comment",
        "status": "completed"
    }
    response = await client.patch(f"/orders/patch/{NON_EXISTENT_ID}", json=update_payload)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    expected_detail = f"Order with id: '{NON_EXISTENT_ID}' does not exist."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


@pytest.mark.asyncio
async def test_update_order_invalid_payload(client, order_payload):
    """
    Test updating an order with an empty payload.
    Expects a 400 error from the payload validator.
    """
    create_resp = await client.post("/orders/create", json=order_payload)
    assert create_resp.status_code == 200, f"Error creating order: {create_resp.text}"
    order_id = create_resp.json()["data"]["id"]

    patch_resp = await client.patch(f"/orders/patch/{order_id}", json={})
    # Assuming that the payload validator returns 400 if the payload is empty.
    assert patch_resp.status_code == 400, f"Expected 400, got {patch_resp.status_code}"


@pytest.mark.asyncio
async def test_update_order_invalid_related_entity(client, order_payload):
    """
    Test updating an order by changing a related entity (e.g., customer) to a non-existent value.
    Expects a 404 error indicating the related entity was not found.
    """
    create_resp = await client.post("/orders/create", json=order_payload)
    assert create_resp.status_code == 200, f"Error creating order: {create_resp.text}"
    order_id = create_resp.json()["data"]["id"]

    payload = {"user_id": NON_EXISTENT_ID}
    patch_resp = await client.patch(f"/orders/patch/{order_id}", json=payload)
    assert patch_resp.status_code == 404, f"Expected 404, got {patch_resp.status_code}"
    detail = patch_resp.json()["detail"]
    expected_detail = f"Customer with ID: '{NON_EXISTENT_ID}' was not found."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"


# ---------------------------
# DELETE /orders/delete/{order_id} tests
# ---------------------------
@pytest.mark.asyncio
async def test_delete_order_success(client, order_payload):
    """
    Test successful deletion of an order.
    Expects a 200 status code with a confirmation message and that subsequent retrieval fails.
    """
    create_resp = await client.post("/orders/create", json=order_payload)
    assert create_resp.status_code == 200, f"Error creating order: {create_resp.text}"
    order_id = create_resp.json()["data"]["id"]

    delete_resp = await client.delete(f"/orders/delete/{order_id}")
    assert delete_resp.status_code == 200, f"Expected 200, got {delete_resp.status_code}"
    message = delete_resp.json()["message"]
    expected_msg = f"Order with id {order_id} deleted."
    assert expected_msg in message, f"Unexpected delete confirmation message: {message}"

    # Verify that the order no longer exists.
    get_resp = await client.get(f"/orders/{order_id}")
    assert get_resp.status_code == 404, "Expected 404 after deletion."
    assert get_resp.json()["detail"] == "Order not found.", "Unexpected message when retrieving a deleted order."


@pytest.mark.asyncio
async def test_delete_order_not_found(client):
    """
    Test deletion of a non-existent order.
    Expects a 404 error with an appropriate message.
    """
    delete_resp = await client.delete(f"/orders/delete/{NON_EXISTENT_ID}")
    assert delete_resp.status_code == 404, f"Expected 404, got {delete_resp.status_code}"
    detail = delete_resp.json()["detail"]
    expected_detail = f"No order with id: '{NON_EXISTENT_ID} found."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"
