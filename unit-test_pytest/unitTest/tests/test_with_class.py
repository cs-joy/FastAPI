from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

class TestClass:
    def test_fifth(self):
        response = client.get("/fifth")
        assert response.status_code == 200
        assert response.json() == {"message": "unit test with class"}