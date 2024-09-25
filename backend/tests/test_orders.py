import pytest
from core.models.orders import OrderStatus


@pytest.fixture(scope="function")
def create_product(client, fake, products_url):
    product_data = {
        "name": " ".join(fake.words(nb=2)),
        "description": "some desc",
        "price": 10.0,
        "stock_quantity": 100,
    }
    response = client.post(products_url, json=product_data)
    assert response.status_code == 201
    return response.json()["id"]


@pytest.fixture(scope="function")
def create_order(client, orders_url, create_product):
    product_id = create_product
    response = client.post(
        orders_url, json={"items": [{"product_id": product_id, "quantity": 2}]}
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_create_order(client, orders_url, create_product):
    product_id = create_product
    response = client.post(
        orders_url, json={"items": [{"product_id": product_id, "quantity": 2}]}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == OrderStatus.IN_PROCESS.value
    assert "id" in data


def test_get_order(client, orders_url, create_order):
    order_id = create_order
    response = client.get(f"{orders_url}/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == OrderStatus.IN_PROCESS.value


def test_update_order_status(client, orders_url, create_order):
    order_id = create_order
    response = client.patch(
        f"{orders_url}/{order_id}/status", json={"status": "Shipped"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == OrderStatus.SHIPPED.value


def test_get_nonexistent_order(client, orders_url):
    response = client.get(f"{orders_url}/999")
    assert response.status_code == 404


def test_create_order_invalid_product(client, orders_url):
    response = client.post(
        orders_url, json={"items": [{"product_id": 999, "quantity": 2}]}
    )
    assert response.status_code == 400


def test_create_order_insufficient_stock(client, orders_url, create_product):
    product_id = create_product
    response = client.post(
        orders_url, json={"items": [{"product_id": product_id, "quantity": 101}]}
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not enough stock"


def test_product_quantity_lowers_after_order_creation(
    client, orders_url, products_url, create_product
):
    product_id = create_product
    product_response = client.get(f"{products_url}/{product_id}")
    assert product_response.status_code == 200
    initial_product_data = product_response.json()
    initial_stock_quantity = initial_product_data["stock_quantity"]

    order_response = client.post(
        orders_url, json={"items": [{"product_id": product_id, "quantity": 2}]}
    )
    assert order_response.status_code == 201

    product_response = client.get(f"{products_url}/{product_id}")
    assert product_response.status_code == 200
    updated_product_data = product_response.json()
    updated_stock_quantity = updated_product_data["stock_quantity"]

    assert updated_stock_quantity == initial_stock_quantity - 2
