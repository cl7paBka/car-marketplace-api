import pytest
from tests.utils.config import (
    CAR_CREATE_VALID,
    CAR_CREATE_ANOTHER,
    CAR_UPDATE_VALID,
    NON_EXISTENT_ID
)


@pytest.mark.asyncio
async def test_add_car_success(client):
    """
    Test successful creation of a new car.
    Expects a 200 status code and "Car created." message.
    """
    response = await client.post("/cars/add", json=CAR_CREATE_VALID)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "success", f"Unexpected status: {data['status']}"
    assert data["message"] == "Car created.", f"Unexpected message: {data['message']}"

    car = data["data"]
    for key, value in CAR_CREATE_VALID.items():
        assert car[key] == value, f"Mismatch in field '{key}'"
    assert "id" in car, "Created car object is missing 'id'."
    assert "created_at" in car, "Created car object is missing 'created_at'."


@pytest.mark.asyncio
async def test_add_car_conflict_vin(client):
    """
    Test that creating a car with a duplicate VIN returns a 409 Conflict.
    """
    # First creation
    first_resp = await client.post("/cars/add", json=CAR_CREATE_VALID)
    assert first_resp.status_code == 200, f"Error during first creation: {first_resp.text}"

    # Second creation with the same VIN should fail
    second_resp = await client.post("/cars/add", json=CAR_CREATE_VALID)
    assert second_resp.status_code == 409, f"Expected 409, got {second_resp.status_code}"
    detail = second_resp.json()["detail"]
    expected_detail = f"Car with vin_number: '{CAR_CREATE_VALID['vin_number']}' already exists."
    assert expected_detail in detail, f"Unexpected conflict message: {detail}"


@pytest.mark.asyncio
async def test_get_car_by_id_success(client):
    """
    Test retrieval of a car by its ID.
    Expects a 200 status code and the correct car data.
    """
    create_resp = await client.post("/cars/add", json=CAR_CREATE_VALID)
    assert create_resp.status_code == 200, f"Error creating car: {create_resp.text}"
    car_id = create_resp.json()["data"]["id"]

    get_resp = await client.get(f"/cars/{car_id}")
    assert get_resp.status_code == 200, f"Expected 200, got {get_resp.status_code}"
    data = get_resp.json()
    assert data["status"] == "success", "Unexpected status when retrieving car by ID."
    assert data["message"] == "Car found.", "Unexpected message when retrieving car by ID."
    assert data["data"]["id"] == car_id, "Returned car ID does not match the created car."


@pytest.mark.asyncio
async def test_get_car_by_id_not_found(client):
    """
    Test retrieval of a car with a non-existent ID.
    Expects a 404 status code with "Car not found." message.
    """
    response = await client.get("/cars/9999999")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    assert detail == "Car not found.", f"Unexpected detail message: {detail}"


@pytest.mark.asyncio
async def test_get_car_by_vin_success(client):
    """
    Test retrieval of a car by its VIN number.
    Expects a 200 status code and the correct car data.
    """
    create_resp = await client.post("/cars/add", json=CAR_CREATE_VALID)
    assert create_resp.status_code == 200, f"Error creating car: {create_resp.text}"
    vin_number = create_resp.json()["data"]["vin_number"]

    get_resp = await client.get(f"/cars/vin/{vin_number}")
    assert get_resp.status_code == 200, f"Expected 200, got {get_resp.status_code}"
    data = get_resp.json()
    assert data["status"] == "success", "Unexpected status when retrieving car by VIN."
    assert data["message"] == "Car found.", "Unexpected message when retrieving car by VIN."
    assert data["data"]["vin_number"] == vin_number, "Returned VIN does not match the requested VIN."


@pytest.mark.asyncio
async def test_get_car_by_vin_not_found(client):
    """
    Test retrieval of a car with a non-existent VIN.
    Expects a 404 status code with "Car not found." message.
    """
    response = await client.get("/cars/vin/INVALIDVIN123")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    detail = response.json()["detail"]
    assert detail == "Car not found.", f"Unexpected detail message: {detail}"


@pytest.mark.asyncio
async def test_get_cars_by_engine_success(client):
    """
    Test retrieval of cars filtered by engine type.
    Expects the response to include created cars with the specified engine.
    """
    # Create two cars with 'gasoline' engine.
    car1_resp = await client.post("/cars/add", json=CAR_CREATE_VALID)
    assert car1_resp.status_code == 200, f"Error creating first car: {car1_resp.text}"

    car2_data = CAR_CREATE_ANOTHER.copy()
    car2_data["engine"] = "gasoline"
    car2_resp = await client.post("/cars/add", json=car2_data)
    assert car2_resp.status_code == 200, f"Error creating second car: {car2_resp.text}"

    engine_resp = await client.get("/cars/engine/gasoline")
    assert engine_resp.status_code == 200, f"Expected 200, got {engine_resp.status_code}"
    data = engine_resp.json()
    if data["status"] == "success":
        assert data["message"] == "Cars found.", "Unexpected message when filtering by engine."
        returned_ids = [car["id"] for car in data["data"]]
        assert car1_resp.json()["data"]["id"] in returned_ids, "First car not found in engine filter."
        assert car2_resp.json()["data"]["id"] in returned_ids, "Second car not found in engine filter."
    else:
        pytest.fail(f"Expected success status, got {data['status']}: {data}")


@pytest.mark.asyncio
async def test_get_cars_by_engine_empty(client):
    """
    Test retrieval of cars filtered by engine type when no cars match.
    Expects an error status with message "No cars found." and an empty data list.
    """
    engine_resp = await client.get("/cars/engine/electric")
    assert engine_resp.status_code == 200, f"Expected 200, got {engine_resp.status_code}"
    data = engine_resp.json()
    assert data["status"] == "error", f"Expected error status, got {data['status']}"
    assert data["message"] == "No cars found.", f"Unexpected message: {data['message']}"
    assert data["data"] == [], "Expected an empty list when no cars are found."


@pytest.mark.asyncio
async def test_get_cars_by_transmission_success(client):
    """
    Test retrieval of cars filtered by transmission type.
    Expects the response to include created cars with the specified transmission.
    """
    # Create two cars with 'automatic' transmission.
    car1_data = CAR_CREATE_VALID.copy()
    car1_data["transmission"] = "automatic"
    car1_resp = await client.post("/cars/add", json=car1_data)
    assert car1_resp.status_code == 200, f"Error creating first car: {car1_resp.text}"

    car2_data = CAR_CREATE_ANOTHER.copy()
    car2_data["transmission"] = "automatic"
    car2_resp = await client.post("/cars/add", json=car2_data)
    assert car2_resp.status_code == 200, f"Error creating second car: {car2_resp.text}"

    trans_resp = await client.get("/cars/transmission/automatic")
    assert trans_resp.status_code == 200, f"Expected 200, got {trans_resp.status_code}"
    data = trans_resp.json()
    if data["status"] == "success":
        assert data["message"] == "Cars found.", "Unexpected message when filtering by transmission."
        returned_ids = [car["id"] for car in data["data"]]
        assert car1_resp.json()["data"]["id"] in returned_ids, "First car not found in transmission filter."
        assert car2_resp.json()["data"]["id"] in returned_ids, "Second car not found in transmission filter."
    else:
        pytest.fail(f"Expected success status, got {data['status']}: {data}")


@pytest.mark.asyncio
async def test_get_all_cars(client):
    """
    Test retrieval of all cars.
    Expects the response to include all created car records.
    """
    resp1 = await client.post("/cars/add", json=CAR_CREATE_VALID)
    resp2 = await client.post("/cars/add", json=CAR_CREATE_ANOTHER)
    assert resp1.status_code == 200, f"Error creating first car: {resp1.text}"
    assert resp2.status_code == 200, f"Error creating second car: {resp2.text}"

    all_resp = await client.get("/cars/")
    assert all_resp.status_code == 200, f"Error retrieving all cars: {all_resp.text}"
    data = all_resp.json()
    if data["status"] == "success":
        assert data["message"] == "All cars found.", "Unexpected message when retrieving all cars."
        returned_ids = [car["id"] for car in data["data"]]
        assert resp1.json()["data"]["id"] in returned_ids, "First car not found in all cars list."
        assert resp2.json()["data"]["id"] in returned_ids, "Second car not found in all cars list."
    else:
        pytest.fail(f"Expected success status, got {data['status']}: {data}")


@pytest.mark.asyncio
async def test_update_car_success(client):
    """
    Test successful update of a car's details.
    Expects a 200 status code and updated fields matching the payload.
    """
    create_resp = await client.post("/cars/add", json=CAR_CREATE_VALID)
    assert create_resp.status_code == 200, f"Error creating car: {create_resp.text}"
    car_id = create_resp.json()["data"]["id"]

    patch_resp = await client.patch(f"/cars/patch/{car_id}", json=CAR_UPDATE_VALID)
    assert patch_resp.status_code == 200, f"Expected 200, got {patch_resp.status_code}"
    data = patch_resp.json()
    assert data["status"] == "success", "Unexpected status after update."
    assert data["message"] == "Car updated.", "Unexpected update message."
    updated_car = data["data"]
    for key, value in CAR_UPDATE_VALID.items():
        assert updated_car[key] == value, f"Field '{key}' was not updated correctly."


@pytest.mark.asyncio
async def test_update_car_conflict_vin(client):
    """
    Test that updating a car's VIN to one that already exists results in a 409 Conflict.
    """
    car1_resp = await client.post("/cars/add", json=CAR_CREATE_VALID)
    assert car1_resp.status_code == 200, f"Error creating first car: {car1_resp.text}"
    car2_resp = await client.post("/cars/add", json=CAR_CREATE_ANOTHER)
    assert car2_resp.status_code == 200, f"Error creating second car: {car2_resp.text}"

    car1_vin = car1_resp.json()["data"]["vin_number"]
    car2_id = car2_resp.json()["data"]["id"]

    patch_resp = await client.patch(f"/cars/patch/{car2_id}", json={"vin_number": car1_vin})
    assert patch_resp.status_code == 409, f"Expected 409, got {patch_resp.status_code}"
    detail = patch_resp.json()["detail"]
    expected_detail = f"Car with vin_number: '{car1_vin}' already exists."
    assert expected_detail in detail, f"Unexpected conflict message: {detail}"


@pytest.mark.asyncio
async def test_update_car_not_found(client):
    """
    Test updating a non-existent car.
    Expects a 404 status code with an appropriate error message.
    """
    patch_resp = await client.patch(f"/cars/patch/{NON_EXISTENT_ID}", json=CAR_UPDATE_VALID)
    assert patch_resp.status_code == 404, f"Expected 404, got {patch_resp.status_code}"
    detail = patch_resp.json()["detail"]
    expected_detail = f"Car with id: '{NON_EXISTENT_ID}' does not exist."
    assert detail == expected_detail, f"Unexpected detail message: {detail}"


@pytest.mark.asyncio
async def test_delete_car_success(client):
    """
    Test successful deletion of a car.
    Expects a 200 status code with confirmation message and that subsequent retrieval fails.
    """
    create_resp = await client.post("/cars/add", json=CAR_CREATE_VALID)
    assert create_resp.status_code == 200, f"Error creating car: {create_resp.text}"
    car_id = create_resp.json()["data"]["id"]

    delete_resp = await client.delete(f"/cars/delete/{car_id}")
    assert delete_resp.status_code == 200, f"Expected 200, got {delete_resp.status_code}"
    message = delete_resp.json()["message"]
    expected_msg = f"Car with id {car_id} deleted."
    assert expected_msg in message, f"Unexpected delete confirmation message: {message}"

    get_resp = await client.get(f"/cars/{car_id}")
    assert get_resp.status_code == 404, "Expected 404 after deletion."
    assert get_resp.json()["detail"] == "Car not found.", "Unexpected message when retrieving a deleted car."


@pytest.mark.asyncio
async def test_delete_car_not_found(client):
    """
    Test deletion of a non-existent car.
    Expects a 404 status code with an appropriate error message.
    """
    delete_resp = await client.delete(f"/cars/delete/{NON_EXISTENT_ID}")
    assert delete_resp.status_code == 404, f"Expected 404, got {delete_resp.status_code}"
    detail = delete_resp.json()["detail"]
    expected_detail = f"No car with id: '{NON_EXISTENT_ID}' found."
    assert expected_detail in detail, f"Unexpected detail message: {detail}"
