from random import randint

from sqlalchemy import select

from fast_zero.models import User

"""
==== ENGINE ====
A Engine do SQLAlchemy é o ponto de contato com o banco de dados,
estabelendo e gerenciando as conexões. Ela é instanciada por meio
da função create_engine(), que recebe as credenciais de acesso ao
banco de dados, o endereço de conexão e o tipo de banco de dados.
A Engine é responsável por criar e destruir conexões, além de
gerenciar o pool de conexões.
"""

"""
==== SESSION ====
Quanto à persistência de dados e consultas ao banco de dados
utilizando o ORM do SQLAlchemy, a Session é a principal interface.
Ela atua como um intermediário entre o código Python e o banco de
dados, mediada pela Engine. A Session é ecncarregada de todas as
transações, forncecendo API para conduzir operações de CRUD.
"""


def test_create_user(session):
    # # engine = create_engine('sqlite:///database.db')
    # engine = create_engine('sqlite:///:memory:')

    # table_registry.metadata.create_all(bind=engine)

    # with Session(engine) as session:
    random_part = randint(0, 10000)
    user = User(name=f'Fulano{random_part}', email=f'{random_part}gleisson@email', password='123')
    random_part = randint(0, 10000)
    usera = User(
        name=f'Cic{random_part}',
        email=f'{random_part}g@email',
        password='123',
    )

    session.add(user)
    session.add(usera)
    session.commit()
    res = session.scalars(select(User)).all()
    # [session.refresh(obj) for obj in [user, usera]]

    assert len(res) == len([u.name for u in res])
    assert user.id == 1
    # assert user.name == 'Fulano'
    # assert user.email == 'gleisson@email.com'
    # assert user.password == '123'


# test_create_user()
