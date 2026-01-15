# Testing
# source: https://fastapi.tiangolo.com/tutorial/testing/

# # Using TestClient
# Workflow
#1. Import "TestClient"
#2. Create TestClient by passing your FastAPI application to it
#3. Create functions with a name that starts with `test_` (stadard pytest conventions).
#4. Use the `TestClient` object the same way as we do with httpx
#5. Write simple assert statements with the standard Python expressions that we need to check (again, standard `pytest`)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """
    test the root endpoint returns correct response
    """
    response  = client.get("/")
    assert response.status_code == 200
    assert response.json() == { "message": "Hello FastAPI!" }

def test_read_second():
    """
    # test read second endpoint
    """
    response = client.get("/second")
    #assert  response.status_code == 400
    assert response.json() == { "status": "success" }


def test_read_third():
    """
    # test third endpoit
    """
    res = client.get("/third")
    assert res.json() == {"domain": "data privacy and security"}

def test_read_fourth():
    """
    # test fourth endpoint
    """
    resp = client.get("/fourth")
    assert resp.status_code == 200
    assert resp.json() == { "domain": "f for financial mathematics" }