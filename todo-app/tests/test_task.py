from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_task_success(test_task):
    task_data = {
        "summary": "New Task",
        "description": "Task description",
        "status": True,
        "priority": 3,
        "user_id": test_task.id
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    assert response.json()["summary"] == "New Task"


def test_create_task_user_not_exist(setup_database):
    task_data = {
        "summary": "New Task",
        "description": "Task description",
        "status": True,
        "priority": 3,
        "user_id": 999
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "User does not exist"


def test_list_tasks_empty(setup_database):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks(test_task):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_task(test_task):
    response = client.get(f"/tasks/{test_task.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_task.id


def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task(test_task, test_user):
    update_data = {
        "summary": "Updated Task",
        "description": "Updated description",
        "status": False,
        "priority": 2,
        "user_id": test_user.id
    }
    response = client.put(f"/tasks/{test_task.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["summary"] == "Updated Task"


def test_update_task_not_found():
    update_data = {
        "summary": "Updated Task",
        "description": "Updated description",
        "status": False,
        "priority": 2,
        "user_id": 1
    }
    response = client.put("/tasks/999", json=update_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "task not exists"
