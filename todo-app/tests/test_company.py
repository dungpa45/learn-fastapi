''' Test cases for company CRUD operations '''
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Simple test functions
def test_create_company():
    company_data = {
        "name": "Test Company",
        "description": "A test company",
        "mode": "public",
        "rating": 5
        }
    response = client.post("/companies/", json=company_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Company"

def test_create_duplicate_company():
    # Create first company
    client.post("/companies/", json={"name": "Same Name"})
    # Try to create duplicate
    response = client.post("/companies/", json={"name": "Same Name"})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_list_empty_companies():
    response = client.get("/companies/")
    assert response.status_code == 200
    assert response.json() == []

def test_list_companies():
    # Create some companies
    client.post("/companies/", json={"name": "Company A"})
    client.post("/companies/", json={"name": "Company B"})
    response = client.get("/companies/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_update_company():
    # Create company first
    create_response = client.post("/companies/", json={"name": "Old Name"})
    company_id = create_response.json()["id"]
    # Update it
    response = client.put(f"/companies/{company_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"

def test_update_nonexistent_company():
    response = client.put("/companies/999", json={"name": "New Name"})
    assert response.status_code == 404

def test_delete_company():
    # Create company first
    create_response = client.post("/companies/", json={"name": "To Delete"})
    company_id = create_response.json()["id"]
    # Delete it
    response = client.delete(f"/companies/{company_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]

def test_delete_nonexistent_company():
    response = client.delete("/companies/999")
    assert response.status_code == 404