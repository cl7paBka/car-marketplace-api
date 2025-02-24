import pytest
from tests.utils.config import (
    USER_CUSTOMER,
    USER_MANAGER,
    INVALID_ROLE_USER,
    MISSING_FIELDS_USER,
    NON_EXISTENT_ID
)


@pytest.mark.asyncio
async def test_create_user_success(client):
    """
    Test successful creation of a new user.
    Expects a 200 status code and "User created." message.
    """
    response = await client.post("/users/create", json=USER_CUSTOMER)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert data["status"] == "success", f"Unexpected status: {data['status']}"
    assert data["message"] == "User created.", "Unexpected message."
    assert data["data"]["email"] == USER_CUSTOMER["email"], "Mismatch in email after user creation."
    assert "id" in data["data"], "Created user object is missing an 'id' field."


@pytest.mark.asyncio
async def test_create_user_conflict_email(client):
    """
    Test that creating a user with an existing email results in a 409 Conflict.
    """
    first_response = await client.post("/users/create", json=USER_CUSTOMER)
    assert first_response.status_code == 200, f"Error during first creation: {first_response.text}"

    second_response = await client.post("/users/create", json=USER_CUSTOMER)
    assert second_response.status_code == 409, f"Expected 409, got {second_response.status_code}"
    detail = second_response.json()["detail"]
    assert "already exists" in detail, "Conflict message does not mention that the email already exists."


@pytest.mark.asyncio
async def test_create_user_invalid_role(client):
    """
    Test creation of a user with an invalid role.
    Expects a 422 Unprocessable Entity error.
    """
    response = await client.post("/users/create", json=INVALID_ROLE_USER)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"


@pytest.mark.asyncio
async def test_create_user_missing_fields(client):
    """
    Test creation of a user with missing required fields.
    Expects a 422 validation error.
    """
    response = await client.post("/users/create", json=MISSING_FIELDS_USER)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    errors = response.json()
    assert "name" in str(errors), "Validation errors do not mention the missing 'name' field."


@pytest.mark.asyncio
async def test_get_user_by_id_success(client):
    """
    Create a user and retrieve it by ID.
    Expects a 200 status code and matching user data.
    """
    create_resp = await client.post("/users/create", json=USER_CUSTOMER)
    assert create_resp.status_code == 200, f"Error creating user: {create_resp.text}"
    created_user = create_resp.json()["data"]
    user_id = created_user["id"]

    get_resp = await client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200, f"Error retrieving user by ID: {get_resp.text}"
    data = get_resp.json()
    assert data["status"] == "success", "Unexpected status in response."
    assert data["message"] == "User found.", "Unexpected message in response."
    assert data["data"]["id"] == user_id, "Returned user ID does not match the created user's ID."


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(client):
    """
    Attempt to retrieve a user with a non-existent ID.
    Expects a 404 status code and "User not found." message.
    """
    response = await client.get("/users/99999999")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = response.json()
    assert data["detail"] == "User not found.", "Unexpected detail message; expected 'User not found.'"


@pytest.mark.asyncio
async def test_get_user_by_email_success(client):
    """
    Create a manager user and retrieve it by email.
    Expects a 200 status code and correct user data.
    """
    create_resp = await client.post("/users/create", json=USER_MANAGER)
    assert create_resp.status_code == 200, f"Error creating manager user: {create_resp.text}"
    created_user = create_resp.json()["data"]
    user_email = created_user["email"]

    get_resp = await client.get(f"/users/email/{user_email}")
    assert get_resp.status_code == 200, f"Error retrieving user by email: {get_resp.text}"
    data = get_resp.json()
    assert data["status"] == "success", "Unexpected status in response."
    assert data["message"] == "User found.", "Unexpected message in response."
    assert data["data"]["email"] == user_email, "Returned email does not match the requested email."


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(client):
    """
    Attempt to retrieve a user by a non-existent email.
    Expects a 404 status code and "User not found." message.
    """
    response = await client.get("/users/email/no_such_user@example.com")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = response.json()
    assert data["detail"] == "User not found.", "Unexpected detail message; expected 'User not found.'"


@pytest.mark.asyncio
async def test_get_users_by_role_success(client):
    """
    Create a customer and a manager, then retrieve them by role.
    """
    cust_resp = await client.post("/users/create", json=USER_CUSTOMER)
    assert cust_resp.status_code == 200, "Failed to create customer user."
    cust_id = cust_resp.json()["data"]["id"]

    mgr_resp = await client.post("/users/create", json=USER_MANAGER)
    assert mgr_resp.status_code == 200, "Failed to create manager user."
    mgr_id = mgr_resp.json()["data"]["id"]

    role_resp_cust = await client.get("/users/role/customer")
    assert role_resp_cust.status_code == 200, "Error retrieving users with role 'customer'."
    data_cust = role_resp_cust.json()
    assert data_cust["status"] == "success", "Unexpected status for customer role."
    assert data_cust["message"] == "Users found.", "Unexpected message for customer role."
    assert any(user["id"] == cust_id for user in data_cust["data"]), "Customer user not found."

    role_resp_mgr = await client.get("/users/role/manager")
    assert role_resp_mgr.status_code == 200, "Error retrieving users with role 'manager'."
    data_mgr = role_resp_mgr.json()
    assert data_mgr["status"] == "success", "Unexpected status for manager role."
    assert data_mgr["message"] == "Users found.", "Unexpected message for manager role."
    assert any(user["id"] == mgr_id for user in data_mgr["data"]), "Manager user not found."


@pytest.mark.asyncio
async def test_get_all_users(client):
    """
    Create two users and retrieve all users.
    Expects both users to appear in the list.
    """
    resp_1 = await client.post("/users/create", json=USER_CUSTOMER)
    resp_2 = await client.post("/users/create", json=USER_MANAGER)
    assert resp_1.status_code == 200, "Error creating the first user."
    assert resp_2.status_code == 200, "Error creating the second user."

    all_resp = await client.get("/users/")
    assert all_resp.status_code == 200, f"Error retrieving all users: {all_resp.text}"
    data_all = all_resp.json()
    if data_all["status"] == "success":
        assert data_all["message"] == "All users found.", "Unexpected message when retrieving all users."
        all_users = data_all["data"]
        id1 = resp_1.json()["data"]["id"]
        id2 = resp_2.json()["data"]["id"]
        assert any(user["id"] == id1 for user in all_users), "USER_CUSTOMER not found in all users."
        assert any(user["id"] == id2 for user in all_users), "USER_MANAGER not found in all users."
    else:
        pytest.fail(f"Expected success but got {data_all['status']}: {data_all}")


@pytest.mark.asyncio
async def test_update_user_success(client):
    """
    Create a user, update their surname, and verify the update.
    """
    create_resp = await client.post("/users/create", json=USER_CUSTOMER)
    assert create_resp.status_code == 200, "Error creating user."

    user_id = create_resp.json()["data"]["id"]
    update_payload = {"surname": "UpdatedSurname"}
    patch_resp = await client.patch(f"/users/patch/{user_id}", json=update_payload)
    assert patch_resp.status_code == 200, f"Error updating user: {patch_resp.text}"
    updated_user = patch_resp.json()["data"]
    assert updated_user["surname"] == "UpdatedSurname", "Surname was not updated correctly."


@pytest.mark.asyncio
async def test_update_user_email_conflict(client):
    """
    Create two users and attempt to update the second user's email to match the first.
    Expects a 409 Conflict error.
    """
    user1_resp = await client.post("/users/create", json=USER_CUSTOMER)
    user2_resp = await client.post("/users/create", json=USER_MANAGER)
    assert user1_resp.status_code == 200, "Error creating the first user."
    assert user2_resp.status_code == 200, "Error creating the second user."

    user1_email = user1_resp.json()["data"]["email"]
    user2_id = user2_resp.json()["data"]["id"]
    patch_resp = await client.patch(f"/users/patch/{user2_id}", json={"email": user1_email})
    assert patch_resp.status_code == 409, f"Expected 409, got {patch_resp.status_code}"
    detail = patch_resp.json()["detail"]
    assert "already exists" in detail, "Conflict message does not mention duplicate email."


@pytest.mark.asyncio
async def test_update_user_not_found(client):
    """
    Attempt to update a non-existent user.
    Expects a 404 Not Found status code.
    """
    patch_resp = await client.patch(f"/users/patch/{NON_EXISTENT_ID}", json={"surname": "DoesNotMatter"})
    assert patch_resp.status_code == 404, f"Expected 404, got {patch_resp.status_code}"
    detail = patch_resp.json()["detail"]
    assert f"User with id: '{NON_EXISTENT_ID}' does not exist." in detail, "Unexpected message for non-existent user."


@pytest.mark.asyncio
async def test_delete_user_success(client):
    """
    Create a user, delete them, and verify they cannot be retrieved.
    """
    create_resp = await client.post("/users/create", json=USER_CUSTOMER)
    assert create_resp.status_code == 200, "Error creating user."

    user_id = create_resp.json()["data"]["id"]
    delete_resp = await client.delete(f"/users/delete/{user_id}")
    assert delete_resp.status_code == 200, f"Error deleting user: {delete_resp.text}"
    message = delete_resp.json()["message"]
    assert f"User with id {user_id} deleted." in message, "Unexpected delete confirmation message."

    get_resp = await client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404, "Expected 404 after deletion."
    assert get_resp.json()["detail"] == "User not found.", "Unexpected message when retrieving a deleted user."


@pytest.mark.asyncio
async def test_delete_user_not_found(client):
    """
    Attempt to delete a non-existent user.
    Expects a 404 status code.
    """
    delete_resp = await client.delete(f"/users/delete/{NON_EXISTENT_ID}")
    assert delete_resp.status_code == 404, f"Expected 404, got {delete_resp.status_code}"
    detail = delete_resp.json()["detail"]
    assert f"No user with id: '{NON_EXISTENT_ID}' found." in detail, "Unexpected detail message for non-existent user."
