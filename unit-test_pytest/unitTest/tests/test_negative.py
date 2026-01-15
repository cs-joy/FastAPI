from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_method_not_allowed():
    """
    Test POST method on GET endpoint
    """
    resp = client.post("/")
    assert resp.status_code == 405 # method not allowed
