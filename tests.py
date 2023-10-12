# Test creating a database and collection
import pytest
from flask import Flask
import pymongo

@pytest.fixture
def app():
    app = Flask("__name__")
    app.config['TESTING'] = True

    return app

@pytest.fixture
def mongo(app):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    yield client
    client.drop_database('testdb')

@pytest.mark.parametrize("dbname", ["testdb"], ids=["valid dbname"])
def test_create_db(mongo, dbname):
    # Arrange
    data = {"Operation": "Create Database", "dbname": dbname}
    
    # Act
    response = app.test_client().post('/db', json=data)
    
    # Assert
    assert response.status_code == 200
    assert dbname in mongo.list_database_names()

@pytest.mark.parametrize("collection_name", ["test_collection"], ids=["valid collection name"])
def test_create_collection(mongo, collection_name):
    # Arrange
    data = {"Operation": "Create Collection", 
            "Collection": collection_name,
            "Choose Database": "testdb"}

    # Act 
    response = app.test_client().post('/db', json=data)

    # Assert
    assert response.status_code == 200
    assert collection_name in mongo['testdb'].list_collection_names()

@pytest.mark.parametrize("documents, collection", [
    ([{"name": "John"}, {"name": "Jane"}], "test_collection")
], ids=["valid documents"])  
def test_insert_documents(mongo, documents, collection):
    # Arrange
    data = {"Operation": "Add Data",
            "dataset": documents,
            "choose_collection": collection}
    
    # Act
    response = app.test_client().post('/db', json=data)

    # Assert 
    assert response.status_code == 200
    assert mongo['testdb'][collection].count_documents({}) == len(documents)

@pytest.mark.parametrize("dbname", ["invalid!name"], ids=["invalid dbname"])
def test_create_db_invalid_name(mongo, dbname):
    # Arrange
    data = {"Operation": "Create Database", "dbname": dbname}

    # Act
    response = app.test_client().post('/db', json=data)

    # Assert
    assert response.status_code == 500

@pytest.mark.parametrize("collection_name", ["$invalid"], ids=["invalid collection name"])
def test_create_collection_invalid_name(mongo, collection_name):
    # Arrange
    data = {"Operation": "Create Collection",
            "Collection": collection_name,
            "Choose Database": "testdb"}

    # Act
    response = app.test_client().post('/db', json=data)

    # Assert
    assert response.status_code == 500

@pytest.mark.parametrize("documents, collection", [
    ("not a list", "test_collection")
], ids=["invalid documents type"])
def test_insert_documents_invalid_type(mongo, documents, collection):
    # Arrange
    data = {"Operation": "Add Data",
            "dataset": documents,
            "choose_collection": collection}

    # Act
    response = app.test_client().post('/db', json=data)

    # Assert
    assert response.status_code == 500

