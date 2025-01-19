import pytest

# Sample user data for testing
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

INVALID_ROLE_USER = {
    "name": "Invalid",
    "surname": "Role",
    "email": "invalid-role@example.com",
    "role": "supervisor"  # Not in valid enum
}

MISSING_FIELDS_USER = {
    # "name" is deleted to simulate missing required fields
    "surname": "NoName",
    "email": "missing@example.com",
    "role": "customer"
}


@pytest.mark.asyncio
async def test_create_user_success(client):
    """
    Checks successful creation of a new user.
    Expects status_code 200 and 'User created.' message.
    """
    response = await client.post("/users/create", json=USER_CUSTOMER)
    assert response.status_code == 200, f"Got {response.status_code} instead of 200."
    data = response.json()

    # Basic validations
    assert data["status"] == "success", f"Unexpected status: {data['status']}"
    assert data["message"] == "User created."
    assert data["data"]["email"] == USER_CUSTOMER["email"], "Email mismatch after creation."
    assert "id" in data["data"], "Created user object is missing 'id'."


@pytest.mark.asyncio
async def test_create_user_conflict_email(client):
    """
    Ensures that creating a user with an existing email returns 409 Conflict.
    """
    # First user creation should succeed
    resp_1 = await client.post("/users/create", json=USER_CUSTOMER)
    assert resp_1.status_code == 200, f"First creation failed: {resp_1.text}"

    # Second user with the same email should fail
    resp_2 = await client.post("/users/create", json=USER_CUSTOMER)
    assert resp_2.status_code == 409, f"Expected 409, got {resp_2.status_code}"
    data_2 = resp_2.json()
    # This detail is defined by your service layer
    assert "already exists" in data_2["detail"], "Conflict detail message is not as expected."


@pytest.mark.asyncio
async def test_create_user_invalid_role(client):
    """
    Tries to create a user with an invalid 'role' that doesn't exist in the Role enum.
    Expects a 422 Unprocessable Entity from FASTAPI.
    """
    response = await client.post("/users/create", json=INVALID_ROLE_USER)
    # Adjust to whatever status code your app returns for invalid enum values
    assert response.status_code == 422, f"Expected 422 for invalid role, got {response.status_code}"


@pytest.mark.asyncio
async def test_create_user_missing_fields(client):
    """
    Attempts to create a user with some missing required fields.
    Expects 422 validation error.
    """
    response = await client.post("/users/create", json=MISSING_FIELDS_USER)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}."
    # Check for typical validation detail if needed
    details = response.json()
    assert "name" in str(details), "The validation errors do not mention the missing 'name' field."


@pytest.mark.asyncio
async def test_get_user_by_id_success(client):
    """
    Creates a user, then retrieves it by ID.
    Expects status_code 200 and matching user data.
    """
    create_resp = await client.post("/users/create", json=USER_CUSTOMER)
    assert create_resp.status_code == 200, f"Create user failed: {create_resp.text}"
    created_user = create_resp.json()["data"]
    user_id = created_user["id"]

    get_resp = await client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200, f"GET by ID failed: {get_resp.text}"
    data = get_resp.json()
    assert data["status"] == "success"
    assert data["message"] == "User found."
    assert data["data"]["id"] == user_id, "Returned user ID does not match the created user."


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(client):
    """
    Tries to retrieve a user by a non-existent ID.
    Expects status_code 404 and an appropriate 'User not found.' detail message.
    """
    response = await client.get("/users/99999999")
    assert response.status_code == 404, f"Expected 404 for non-existent user, got {response.status_code}"
    data = response.json()
    assert data["detail"] == "User not found.", "Detail message does not match 'User not found.'"


@pytest.mark.asyncio
async def test_get_user_by_email_success(client):
    """
    Creates a user, then fetches it by email.
    Expects 200 with 'User found.'.
    """
    create_resp = await client.post("/users/create", json=USER_MANAGER)
    assert create_resp.status_code == 200, f"Failed to create manager user: {create_resp.text}"
    created_user = create_resp.json()["data"]
    user_email = created_user["email"]

    get_resp = await client.get(f"/users/email/{user_email}")
    assert get_resp.status_code == 200, f"Failed to GET user by email: {get_resp.text}"
    data = get_resp.json()
    assert data["status"] == "success"
    assert data["message"] == "User found."
    assert data["data"]["email"] == user_email, "Email in response does not match requested email."


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(client):
    """
    Tries to retrieve user by a non-existent email.
    Expects status_code 404 and 'User not found.' detail message.
    """
    response = await client.get("/users/email/no_such_user@example.com")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}."
    data = response.json()
    assert data["detail"] == "User not found.", "The detail message is unexpected."


@pytest.mark.asyncio
async def test_get_users_by_role_success(client):
    """
    Creates two users with different roles, then fetches them by role.
    Expects 200 with either 'Users found.' or 'No users found.' depending on the data.
    """
    # Create a customer
    cust_resp = await client.post("/users/create", json=USER_CUSTOMER)
    assert cust_resp.status_code == 200, "Failed to create customer user."
    cust_data = cust_resp.json()["data"]
    cust_id = cust_data["id"]

    # Create a manager
    mgr_resp = await client.post("/users/create", json=USER_MANAGER)
    assert mgr_resp.status_code == 200, "Failed to create manager user."
    mgr_id = mgr_resp.json()["data"]["id"]

    # Verify we can get customers
    role_resp_cust = await client.get("/users/role/customer")
    assert role_resp_cust.status_code == 200, "GET by role=customer failed."
    data_cust = role_resp_cust.json()
    assert data_cust["status"] == "success"
    assert data_cust["message"] == "Users found."
    # Check if our newly created customer user is in the list
    assert any(u["id"] == cust_id for u in data_cust["data"]), "Customer user not found in role=customer response."

    # Verify we can get managers
    role_resp_mgr = await client.get("/users/role/manager")
    assert role_resp_mgr.status_code == 200, "GET by role=manager failed."
    data_mgr = role_resp_mgr.json()
    assert data_mgr["status"] == "success"
    assert data_mgr["message"] == "Users found."
    # Check if our newly created manager user is in the list
    assert any(u["id"] == mgr_id for u in data_mgr["data"]), "Manager user not found in role=manager response."


@pytest.mark.asyncio
async def test_get_all_users(client):
    """
    Creates two users, then calls /users/ to retrieve all.
    Verifies both users appear in the list.
    """
    resp_1 = await client.post("/users/create", json=USER_CUSTOMER)
    resp_2 = await client.post("/users/create", json=USER_MANAGER)
    assert resp_1.status_code == 200
    assert resp_2.status_code == 200

    resp_all = await client.get("/users/")
    assert resp_all.status_code == 200, f"GET /users/ failed: {resp_all.text}"
    data_all = resp_all.json()

    # 'status' might be 'success' if users exist, or 'error' if none found.
    if data_all["status"] == "success":
        assert data_all["message"] == "All users found."
        all_users = data_all["data"]
        id1 = resp_1.json()["data"]["id"]
        id2 = resp_2.json()["data"]["id"]

        # Make sure both user IDs are found
        assert any(u["id"] == id1 for u in all_users), "USER_CUSTOMER not found in all users."
        assert any(u["id"] == id2 for u in all_users), "USER_MANAGER not found in all users."
    else:
        # If for some reason 'error' occurs, test fails because we DID create users.
        pytest.fail(f"Expected 'success' but got {data_all['status']}: {data_all}")


# TODO Make more patch tests
@pytest.mark.asyncio
async def test_update_user_success(client):
    """
    Creates a user, then updates their surname via PATCH.
    Expects 200 and the updated surname in the response.
    """
    create_resp = await client.post("/users/create", json=USER_CUSTOMER)
    assert create_resp.status_code == 200
    user_id = create_resp.json()["data"]["id"]

    update_data = {"surname": "UpdatedSurname"}
    patch_resp = await client.patch(f"/users/patch/{user_id}", json=update_data)
    assert patch_resp.status_code == 200, f"PATCH failed with {patch_resp.text}"
    updated_user = patch_resp.json()["data"]

    assert updated_user["surname"] == "UpdatedSurname", "Surname was not updated correctly."


@pytest.mark.asyncio
async def test_update_user_email_conflict(client):
    """
    Creates two users, then tries updating the second user's email to the first user's email.
    Expects 409 Conflict due to duplicate email.
    """
    user_1_resp = await client.post("/users/create", json=USER_CUSTOMER)
    user_2_resp = await client.post("/users/create", json=USER_MANAGER)
    assert user_1_resp.status_code == 200
    assert user_2_resp.status_code == 200

    user_1_email = user_1_resp.json()["data"]["email"]
    user_2_id = user_2_resp.json()["data"]["id"]

    patch_resp = await client.patch(f"/users/patch/{user_2_id}", json={"email": user_1_email})
    assert patch_resp.status_code == 409, f"Expected 409, got {patch_resp.status_code}"
    detail_msg = patch_resp.json()["detail"]
    assert "already exists" in detail_msg, "Conflict detail does not mention existing email."


@pytest.mark.asyncio
async def test_update_user_not_found(client):
    """
    Attempts to update a non-existent user ID.
    Expects 404 Not Found.
    """
    fake_id = 999999999
    patch_resp = await client.patch(f"/users/patch/{fake_id}", json={"surname": "DoesNotMatter"})
    assert patch_resp.status_code == 404, f"Expected 404, got {patch_resp.status_code}"
    detail_msg = patch_resp.json()["detail"]
    assert f"User with id: '{fake_id}' does not exist." in detail_msg


@pytest.mark.asyncio
async def test_delete_user_success(client):
    """
    Creates a user, deletes them, and verifies they can no longer be retrieved by ID.
    """
    create_resp = await client.post("/users/create", json=USER_CUSTOMER)
    assert create_resp.status_code == 200
    user_id = create_resp.json()["data"]["id"]

    delete_resp = await client.delete(f"/users/delete/{user_id}")
    assert delete_resp.status_code == 200, f"Delete failed: {delete_resp.text}"
    msg = delete_resp.json()["message"]
    assert f"User with id {user_id} deleted." in msg, "Unexpected delete response message."

    # Verify the user is gone
    get_resp = await client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404, "Expected 404 after deletion."
    assert get_resp.json()["detail"] == "User not found."


@pytest.mark.asyncio
async def test_delete_user_not_found(client):
    """
    Attempts to delete a non-existent user.
    Expects 404 status code.
    """
    fake_id = 123456789
    delete_resp = await client.delete(f"/users/delete/{fake_id}")
    assert delete_resp.status_code == 404, f"Expected 404, got {delete_resp.status_code}"
    detail_msg = delete_resp.json()["detail"]
    assert f"No user with id: '{fake_id}' found." in detail_msg, "Unexpected detail message."
