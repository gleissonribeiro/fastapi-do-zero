from pydantic import BaseModel, EmailStr


# ---- Schemas para o modelo de dados de um usuário ----
class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserDBSchema(UserSchema):
    id: int


class PublicUserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr


class PublicUserListSchema(BaseModel):
    users: list[PublicUserSchema]


# -----------------------------------------------------


class BookSchema(BaseModel):
    titulo: str
    autor: str
    ano: int
    disponivel: bool


class BookListSchema(BaseModel):
    books: list[BookSchema]
