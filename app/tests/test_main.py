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
        "Class": 41,
        "ObjectProperty": 7,
        "DataProperty": 1,
        "Individual": 9,
        "Subclass": 36,
        "DisjointClasses": 0,
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


def test_get_classes_hierarchy():
    client.post(
        "/files/",
        files={"file": open(testFilesDirectory + "pizza.ttl", "rb")},
    )
    response = client.get("/classesHierarchy/")
    assert response.status_code == 200
    assert response.json()["https://www.w3.org/2002/07/owl#/Thing"][2][1][2] == [
        "http://www.pizzaowl.org/Interesting_Pizza",
        [],
    ]


def test_get_object_properties_hierarchy():
    client.post(
        "/files/",
        files={"file": open(testFilesDirectory + "pizza.ttl", "rb")},
    )
    response = client.get("/objectPropertiesHierarchy/")
    assert response.status_code == 200
    assert response.json()["https://www.w3.org/2002/07/owl#/topObjectProperty"][2][1][
        1
    ] == ["http://www.pizzaowl.org/is_Topping_Of", []]


def test_get_data_properties_hierarchy():
    client.post(
        "/files/",
        files={"file": open(testFilesDirectory + "pizza.ttl", "rb")},
    )
    response = client.get("/dataPropertiesHierarchy/")
    assert response.status_code == 200
    assert response.json() == {
        "https://www.w3.org/2002/07/owl#/topDataProperty": [
            [
                "http://www.pizzaowl.org/has_Calorific_Content_Value",
                [],
            ]
        ]
    }
