from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá, mundo!"}


def test_create_user(client):
    response = client.post(
        "/users/", json={"name": "Fulano", "email": "gleisson@gmail.com", "password": "123"}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "name": "Fulano", "email": "gleisson@gmail.com"}


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [{"id": 1, "name": "Fulano", "email": "gleisson@gmail.com"}]
    }
    assert isinstance(response.json(), dict)
    assert response.json().keys() == {"users"}
    assert isinstance(response.json().get("users"), list)
    assert response.json().get("users")[0].keys() == {"id", "name", "email"}


def test_update_user(client):
    response = client.put(
        "/users/1", json={"name": "Beltrano", "email": "gleisson@gmail.com", "password": "123"}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "name": "Beltrano", "email": "gleisson@gmail.com"}

    response = client.put(
        "/users/0", json={"name": "Beltrano", "email": "g@email.com", "password": "123"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "usuário não encontrado"}

    response = client.put("/users/1", json={"name": "Beltrano"})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK

    response = client.delete("/users/0")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_books(client):
    response = client.get("/books/", params={"disponivel": True})

    filtered_books = [book for book in response.json().get("books") if not book.get("disponivel")]
    assert filtered_books == []
    assert response.json().get("books")
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json().get("books"), list)
