import os
from fastapi.testclient import TestClient
from app import main

testFilesDirectory = os.getcwd() + "/tests/testFiles/"
client = TestClient(main.app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_read_metrics():
    client.post(
        "/files/",
        files={"file": open(testFilesDirectory + "pizza.ttl", "rb")},
    )
    response = client.get("/metrics/")
    assert response.status_code == 200
    assert response.json() == {
        "Class": 42,
        "ObjectProperty": 7,
        "DataProperty": 1,
        "Individual": 9,
        "Subclass": 55,
        "DisjointClasses": 7,
        "EquivalentClass": 7,
        "SubObjectProperty": 4,
        "Inverse": 2,
        "FunctionalProperty": 0,
        "TransitiveProperty": 0,
        "AsymmetricProperty": 0,
        "SymmetricProperty": 0,
        "IrreflexiveProperty": 0,
        "ReflexiveProperty": 0,
    }


def test_read_file():
    response = client.post(
        "/files/",
        files={"file": open(testFilesDirectory + "basicOntology.ttl", "rb")},
    )
    assert response.status_code == 200
    assert response.json() == "ok"


def test_read_with_invalid_file():

    response = client.post(
        "/files/",
        files={"file": open(testFilesDirectory + "plainText.txt", "rb")},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file"}
