from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_read_file():
    response = client.post(
        "/files/",
        files={"file": open("ejercicio1.ttl", "rb")},
    )
    assert response.status_code == 200
    assert response.json() == "ok"


def test_read_with_invalid_file():

    response = client.post(
        "/files/",
        files={"file": open("testFile.txt", "rb")},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file"}
