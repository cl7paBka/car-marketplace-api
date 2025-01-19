import pytest

TEST_USER_CUSTOMER = {
    "name": "Lera",
    "surname": "Novikova",
    "email": "LeraNovik33@yandex.ru",
    "role": "customer"
}

TEST_USER_MANAGER = {
    "name": "Boris",
    "surname": "Sokolov",
    "email": "SokolBorya21@gmail.com",
    "role": "manager"
}


@pytest.mark.asyncio
async def test_create_user_success(client):
    """
    Test for successful user creation.
    """

    response = await client.post("/users/create", json=TEST_USER_CUSTOMER)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    response_data = response.json()
    assert response_data["status"] == "success", f"Unexpected status: {response_data['status']}"
    assert response_data["message"] == "User created.", (
        f"Unexpected message: {response_data['message']}"
    )


@pytest.mark.asyncio
async def test_create_user_not_unique_user(client):
    """
    Test to create a user with an existing email address.
    First we create a user, then we try to create another one with the same email address.
    """

    # First user creation
    response = await client.post("/users/create", json=TEST_USER_CUSTOMER)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    response_data = response.json()
    assert response_data["status"] == "success", f"Unexpected status: {response_data['status']}"
    assert response_data["message"] == "User created.", (
        f"Unexpected message: {response_data['message']}"
    )

    # Second user creation with not unique email

    test_user_not_unique = {
        "name": "Valerka",
        "surname": "Drozdov",
        "email": TEST_USER_CUSTOMER["email"],
        "role": "customer"
    }

    response = await client.post("/users/create", json=TEST_USER_CUSTOMER)
    assert response.status_code == 409, f"Unexpected status code: {response.status_code, response.json}"

    response_data = response.json()
    expected_detail = f"User with email: '{test_user_not_unique['email']}' already exists."
    assert response_data["detail"] == expected_detail, f"Unexpected detail: {response_data['detail']}"
