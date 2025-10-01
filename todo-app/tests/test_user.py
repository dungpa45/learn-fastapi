from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user_success(test_company):
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
        "first_name": "New",
        "last_name": "User",
        "is_active": True,
        "is_admin": False,
        "company_id": test_company.id
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"

def test_create_user_company_not_exist():
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
        "first_name": "New",
        "last_name": "User",
        "company_id": 999
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Company does not exist"

def test_create_user_duplicate_username(test_user, test_company):
    user_data = {
        "username": "testuser",
        "email": "different@example.com",
        "password": "password123",
        "first_name": "New",
        "last_name": "User",
        "company_id": test_company.id
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_create_user_duplicate_email(test_user, test_company):
    user_data = {
        "username": "differentuser",
        "email": "test@example.com",
        "password": "password123",
        "first_name": "New",
        "last_name": "User",
        "company_id": test_company.id
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_list_users_empty():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []

def test_list_users_with_data(test_user):
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["username"] == "testuser"

def test_get_user_success(test_user):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_update_user_success(test_user, test_company):
    update_data = {
        "first_name": "Updated",
        "last_name": "Name",
        "company_id": test_company.id
    }
    response = client.put(f"/users/{test_user.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"
    assert response.json()["last_name"] == "Name"

def test_update_user_not_found():
    update_data = {"first_name": "Updated"}
    response = client.put("/users/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_delete_user_success(test_user):
    response = client.delete(f"/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"User ID: {test_user.id} has been deleted successfully"
    assert response.json()["user"]["username"] == "testuser"
    assert "password" not in response.json()["user"]

def test_delete_user_not_found():
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
