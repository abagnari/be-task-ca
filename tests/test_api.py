from fastapi import status


class TestUsersAPI:
    async def test_create_user(self, client):
        response = await client.post("/users/", json={
            "first_name": "string",
            "last_name": "string",
            "email": "string@string.com",
            "password": "string",
            "shipping_address": "string"
        })
        assert response.status_code == status.HTTP_201_CREATED
        id = response.json().get("id")
        assert id is not None

    async def test_create_duplicated_user_fails(self, client):
        response = await client.post("/users/", json={
            "first_name": "string",
            "last_name": "string",
            "email": "string@string.com",
            "password": "string",
            "shipping_address": "string"
        })
        assert response.status_code == status.HTTP_201_CREATED
        id = response.json().get("id")
        assert id is not None

        response = await client.post("/users/", json={
            "first_name": "string",
            "last_name": "string",
            "email": "string@string.com",
            "password": "string",
            "shipping_address": "string"
        })
        assert response.status_code == status.HTTP_409_CONFLICT


class TestItemAPI:
    async def test_create_item(self, client):
        response = await client.post("/items/", json={
            "name": "string",
            "description": "string",
            "price": 10,
            "quantity": 10
        })
        assert response.status_code == status.HTTP_201_CREATED
        id = response.json().get("id")
        assert id is not None

        response = await client.get("/items/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1


class TestCartAPI:
    async def test_create_cart_item(self, client):
        response = await client.post("/users/", json={
            "first_name": "string",
            "last_name": "string",
            "email": "string@string.com",
            "password": "string",
            "shipping_address": "string"
        })
        assert response.status_code == status.HTTP_201_CREATED
        id = response.json().get("id")
        assert id is not None

        user_id = response.json().get("id")

        response = await client.post("/items/", json={
            "name": "string",
            "description": "string",
            "price": 10,
            "quantity": 10
        })
        assert response.status_code == status.HTTP_201_CREATED
        id = response.json().get("id")
        assert id is not None

        item_id = response.json().get("id")

        response = await client.post(f"/users/{user_id}/cart", json={
            "item_id": item_id,
            "quantity": 5
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.json()) == 1

    async def test_cart_item_excessive_quantity(self, client):
        response = await client.post("/users/", json={
            "first_name": "string",
            "last_name": "string",
            "email": "string@string.com",
            "password": "string",
            "shipping_address": "string"
        })
        assert response.status_code == status.HTTP_201_CREATED
        id = response.json().get("id")
        assert id is not None

        user_id = response.json().get("id")

        response = await client.post("/items/", json={
            "name": "string",
            "description": "string",
            "price": 10,
            "quantity": 10
        })
        assert response.status_code == status.HTTP_201_CREATED
        id = response.json().get("id")
        assert id is not None

        item_id = response.json().get("id")

        response = await client.post(f"/users/{user_id}/cart", json={
            "item_id": item_id,
            "quantity": 15
        })
        assert response.status_code == status.HTTP_409_CONFLICT


