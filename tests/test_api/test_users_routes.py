import pytest
import random


# end-point /users/create
@pytest.mark.asyncio
async def test_create_user(client):
    test_user = {
        "name": "test_name",
        "surname": "test_surname",
        "email": "test_email@example.com",
        "role": "customer"
    }

    response = await client.post(
        "/users/create",
        json=test_user
    )

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    response_data = response.json()
    assert response_data["status"] == "success", f"Unexpected status: {response_data['status']}"
    assert response_data["message"] == "User created.", (
        f"Unexpected message: {response_data['message']}"
    )
