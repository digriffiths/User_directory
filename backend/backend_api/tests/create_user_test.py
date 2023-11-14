from fastapi.testclient import TestClient
from backend.backend_api.api import app
import pytest
from ..services.DatabaseManager import DatabaseManager
from ..models import users_table
from ...utils.databases import SQLDB

client = TestClient(app)
db = SQLDB(
    "postgres", "postgres", "db", "5432", "fast_api_db", [users_table])


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    # Setup: Add the user to the database
    name = "test"
    email = "test@example.com"
    user = users_table(name=name, email=email)
    user_id = db.add_data(user)

    yield user_id  # this is where the testing happens

    # Teardown: Remove the user from the database
    db.delete_record(users_table, user_id)


@pytest.fixture(scope="module")
def user_id(setup_teardown):
    return setup_teardown


def test_get_user(user_id):
    response = client.get(f"/get_user/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "test"
    assert response.json()["email"] == "test@example.com"

# def test_read_form():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert "add_user.html" in response.text


# def test_create_user():
#     response = client.post(
#         "/add_user",
#         # replace with your actual data
#         json={"name": "test", "email": "test@example.com"},
#     )
#     assert response.status_code == 200
#     assert response.json()["name"] == "test"
#     assert response.json()["email"] == "test@example.com"


# def test_email_schema():
#     response = client.post(
#         "/add_user",
#         # replace with your actual data
#         json={"name": "test", "email": "test"},
#     )
#     assert response.status_code == 422


# def test_find_user(user_id):  # pytest will automatically pass the user_id from the fixture
#     response = client.get(f"/find_user/{user_id}")
#     assert response.status_code == 200
#     assert response.json()["name"] == "test"
#     assert response.json()["email"] == "test@example.com"
