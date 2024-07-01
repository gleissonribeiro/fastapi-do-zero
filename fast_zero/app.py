from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (
    BookListSchema,
    PublicUserListSchema,
    PublicUserSchema,
    UserDBSchema,
    UserSchema,
)

app = FastAPI()

books = [
    {
        'titulo': 'O apanhador no campo de centeio',
        'autor': 'J.D. Salinger',
        'ano': 1945,
        'disponivel': True,
    },
    {
        'titulo': 'O mestre e a margarida',
        'autor': 'Mikhail Bulgákov',
        'ano': 1966,
        'disponivel': True,
    },
    {
        'titulo': 'O senhor dos anéis',
        'autor': 'J.R.R. Tolkien',
        'ano': 1954,
        'disponivel': True,
    },
    {
        'titulo': 'Harry Potter e a pedra filosofal',
        'autor': 'J.K. Rowling',
        'ano': 1997,
        'disponivel': False,
    },
    {
        'titulo': 'Harry Potter e a câmara secreta',
        'autor': 'J.K. Rowling',
        'ano': 1998,
        'disponivel': False,
    },
    {
        'titulo': 'Harry Potter e o prisioneiro de Azkaban',
        'autor': 'J.K. Rowling',
        'ano': 1999,
        'disponivel': True,
    },
    {
        'titulo': 'Harry Potter e o cálice de fogo',
        'autor': 'J.K. Rowling',
        'ano': 2000,
        'disponivel': True,
    },
    {
        'titulo': 'Harry Potter e a ordem da fênix',
        'autor': 'J.K. Rowling',
        'ano': 2003,
        'disponivel': False,
    },
    {
        'titulo': 'Harry Potter e o enigma do príncipe',
        'autor': 'J.K. Rowling',
        'ano': 2005,
        'disponivel': True,
    },
    {
        'titulo': 'Harry Potter e as relíquias da morte',
        'autor': 'J.K. Rowling',
        'ano': 2007,
        'disponivel': True,
    },
]


users = []


@app.get('/')
def read_root():
    return {'message': 'Olá, mundo!'}


@app.get('/books/', response_model=BookListSchema)
def read_books(disponivel: bool = True):
    filtered_books = [book for book in books if book.get('disponivel') == disponivel]

    return {'books': filtered_books}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=PublicUserSchema)
def create_user(incoming_user: UserSchema):
    # ---- Cria um novo usuário e adiciona à lista de usuários ----
    new_user_with_id = UserDBSchema(id=len(users) + 1, **incoming_user.model_dump())
    users.append(new_user_with_id)
    # ------------------------------------------------------------

    # ---- Retorna o usuário criado ----
    return PublicUserSchema(
        **new_user_with_id.model_dump(exclude={'password'}),
    )
    # -----------------------------------


@app.get('/users/', status_code=HTTPStatus.OK, response_model=PublicUserListSchema)
def read_users():
    # ---- Retorna uma lista com todos os usuários ----
    return PublicUserListSchema(
        users=[PublicUserSchema(**user.model_dump(exclude={'password'})) for user in users]
    )
    # -------------------------------------------------


@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=PublicUserSchema)
def read_user(user_id: int):
    # ---- Verifica se o usuário pode existir e retorna um erro 404 se não ----
    if user_id > len(users) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='usuário não encontrado')
    # -------------------------------------------------------------------------

    # ---- Retorna o usuário com o id especificado, se existir ----
    for user in users:
        if user.id == user_id:
            return PublicUserSchema(**user.model_dump(exclude={'password'}))
    # -------------------------------------------------------------

    # ---- Retorna um erro 404 se o usuário não for encontrado ----
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='usuário não encontrado')
    # -------------------------------------------------------------


@app.put('/users/{user_id}', status_code=HTTPStatus.CREATED, response_model=PublicUserSchema)
def update_user(user_id: int, incoming_user: UserSchema):
    # ---- Verifica se o usuário existe e retorna um erro 404 se não existir ----
    if user_id > len(users) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='usuário não encontrado')
    # ---------------------------------------------------------------------------

    # ---- Atualiza o usuário ----
    user_with_id = UserDBSchema(id=user_id, **incoming_user.model_dump())
    users[user_id - 1] = user_with_id
    # ---------------------------

    # ---- Retorna o usuário atualizado ----
    return PublicUserSchema(
        **user_with_id.model_dump(exclude={'password'}),
    )
    # -------------------------------------


@app.delete('/users/{user_id}', status_code=HTTPStatus.OK, response_model=PublicUserSchema)
def delete_user(user_id: int):
    # ---- Verifica se o usuário existe e retorna um erro 404 se não existir ----
    if user_id > len(users) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='usuário não encontrado')
    # ---------------------------------------------------------------------------

    # ---- Remove o usuário ----
    removed_user = users.pop(user_id - 1)
    # ---------------------------

    # ---- Retorna o usuário removido ----
    return PublicUserSchema(**removed_user.model_dump(exclude={'password'}))
    # -----------------------------------
