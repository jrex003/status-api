from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data
    assert "uptime" in json_data
    assert "top_processes" in json_data

def test_uptime():
    response = client.get("/uptime")
    assert response.status_code == 200
    json_data = response.json()
    assert "uptime" in json_data
    assert "components" in json_data
    assert "total_seconds" in json_data
    assert isinstance(json_data["total_seconds"], int)

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data
    assert json_data["status"] in ["healthy", "degraded", "unhealthy"]
    assert "metrics" in json_data
    assert "cpu" in json_data["metrics"]
    assert "memory" in json_data["metrics"]
    assert "disk" in json_data["metrics"]

def test_top_processes_default():
    response = client.get("/top-processes")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert "processes" in json_data["data"]
    assert isinstance(json_data["data"]["processes"], list)
    assert len(json_data["data"]["processes"]) <= 10

def test_top_processes_sort_by_memory():
    response = client.get("/top-processes?sort_by=memory&limit=5")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["metadata"]["sorted_by"] == "memory"
    assert json_data["metadata"]["returned_processes"] == 5

def test_top_processes_invalid_sort_by():
    response = client.get("/top-processes?sort_by=invalid")
    assert response.status_code == 400
    assert "sort_by must be either" in response.json()["detail"]

def test_top_processes_invalid_limit():
    response = client.get("/top-processes?limit=1000")
    assert response.status_code == 400
    assert "limit must be between" in response.json()["detail"]
