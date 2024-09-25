from faker import Faker

import pytest

fake = Faker()


@pytest.fixture
def product_data(fake):
    return {
        "name": " ".join(" ".join(fake.words(nb=2))),
        "description": "This is a test product",
        "price": 10.99,
        "stock_quantity": 100,
    }


def test_create_product(client, product_data, products_url):
    response = client.post(products_url, json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["stock_quantity"] == product_data["stock_quantity"]
    assert "id" in data


def test_read_product(client, product_data, products_url):
    create_response = client.post(products_url, json=product_data)
    product_id = create_response.json()["id"]

    response = client.get(f"{products_url}/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["stock_quantity"] == product_data["stock_quantity"]
    assert data["id"] == product_id


def test_update_product(client, product_data, products_url):
    create_response = client.post(products_url, json=product_data)
    product_id = create_response.json()["id"]

    updated_data = product_data.copy()
    updated_data["price"] = 15.99
    response = client.put(f"{products_url}/{product_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == updated_data["price"]


def test_delete_product(client, product_data, products_url):
    create_response = client.post(products_url, json=product_data)
    product_id = create_response.json()["id"]

    response = client.delete(f"{products_url}/{product_id}")
    assert response.status_code == 204

    response = client.get(f"{products_url}/{product_id}")
    assert response.status_code == 404


def test_create_product_with_duplicate_name(client, product_data, products_url):
    response = client.post(products_url, json=product_data)
    assert response.status_code == 201

    response = client.post(products_url, json=product_data)
    assert response.status_code == 400
    data = response.json()
    assert "name" in data["detail"]


@pytest.mark.parametrize(
    "invalid_data, expected_status_code",
    [
        (
            {
                "name": " ".join(fake.words(nb=2)),
                "description": "This is a test product",
                "price": -10.99,
                "stock_quantity": 100,
            },
            422,
        ),
        (
            {
                "name": " ".join(fake.words(nb=2)),
                "description": "This is a test product",
                "price": 10.99,
                "stock_quantity": -100,
            },
            422,
        ),
        (
            {
                "name": " ".join(fake.words(nb=2)),
                "description": "This is a test product",
                "price": 0,
                "stock_quantity": 100,
            },
            422,
        ),
        (
            {
                "name": " ".join(fake.words(nb=2)),
                "description": "This is a test product",
                "price": 10.99,
                "stock_quantity": 0,
            },
            201,
        ),
    ],
)
def test_create_product_with_invalid_params(
    client, products_url, invalid_data, expected_status_code
):
    response = client.post(products_url, json=invalid_data)
    assert response.status_code == expected_status_code
