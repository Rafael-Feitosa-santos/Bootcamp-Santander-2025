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


def atualizar_registro(nome, email, id):
    cursor.execute("UPDATE clientes SET nome=%s, email=%s WHERE id=%s;", (nome, email, id))
    conexao.commit()


def excluir_registro(id):
    cursor.execute("DELETE FROM clientes WHERE id=%s;", (id,))
    conexao.commit()


def inserir_muitos(dados):
    cursor.executemany("INSERT INTO clientes (nome, email) VALUES (%s, %s);", dados)
    conexao.commit()


def recuperar_cliente(id):
    cursor.execute("SELECT id, nome, email FROM clientes WHERE id=%s;", (id,))
    return cursor.fetchone()


def listar_clientes():
    cursor.execute("SELECT * FROM clientes ORDER BY nome DESC;")
    return cursor.fetchall()


criar_tabela()

# Teste simples
inserir_registro("João", "joao@email.com")
clientes = listar_clientes()
for cliente in clientes:
    print(f"ID: {cliente['id']}")
    print(f"Nome: {cliente['nome']}")
    print(f"E-mail: {cliente['email']}")
