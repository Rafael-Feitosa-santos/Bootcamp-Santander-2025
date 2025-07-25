import psycopg2
from psycopg2.extras import RealDictCursor

conexao = psycopg2.connect("dbname=postgres user=postgres password=123456")
cursor = conexao.cursor(cursor_factory=RealDictCursor)


def criar_tabela():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            email VARCHAR(150)
        );
    """)
    conexao.commit()


def inserir_registro(nome, email):
    cursor.execute("INSERT INTO clientes (nome, email) VALUES (%s, %s);", (nome, email))
    conexao.commit()
    print(f"Registro criado para {nome} com o e-mail {email}.")


def atualizar_registro(nome, email, id):
    try:
        cursor.execute(
            "UPDATE clientes SET nome = %s, email = %s WHERE id = %s;",
            (nome, email, id)
        )

        if cursor.rowcount == 0:
            print(f"Nenhum registro com ID {id} foi encontrado.")
        else:
            conexao.commit()
            print(f"Registro com ID {id} atualizado com sucesso!")

    except Exception as e:
        conexao.rollback()
        print(f"Erro ao atualizar o registro: {e}")


def excluir_registro(id):
    cursor.execute("DELETE FROM clientes WHERE id=%s RETURNING id;", (id,))
    excluido = cursor.fetchone()
    if excluido:
        print(f"Registro com ID {id} excluído com sucesso!")
    else:
        print(f"Nenhum registro encontrado com ID {id}.")
    conexao.commit()


def inserir_muitos(dados):
    cursor.executemany("INSERT INTO clientes (nome, email) VALUES (%s, %s);", dados)
    conexao.commit()
    print(f"{len(dados)} registros criados com sucesso.")


def recuperar_cliente(id):
    cursor.execute("SELECT id, nome, email FROM clientes WHERE id=%s;", (id,))
    return cursor.fetchone()


def listar_clientes():
    cursor.execute("SELECT * FROM clientes ORDER BY nome;")
    clientes = cursor.fetchall()
    for cliente in clientes:
        print(f"ID: {cliente['id']}")
        print(f"Nome: {cliente['nome']}")
        print(f"E-mail: {cliente['email']}")
        print("-" * 25)
    return clientes


criar_tabela()

# Teste simples
inserir_registro("João", "joao@email.com")
listar_clientes()

clientes = [
    ("Rafael", "rafael@email.com"),
    ("Charlie", "charlie@email.com")
]

inserir_muitos(clientes)

listar_clientes()
