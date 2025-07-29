import psycopg2
from psycopg2.extras import RealDictCursor

# Conexão com o banco de dados
conexao = psycopg2.connect("dbname=postgres user=postgres password=123456")
cursor = conexao.cursor(cursor_factory=RealDictCursor)


def criar_tabela():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes_2 (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            email VARCHAR(150)
        );
    """)
    conexao.commit()

criar_tabela()

try:
    cursor.execute("DELETE FROM clientes_2 WHERE id = 4;")
    conexao.commit()

    cursor.execute("INSERT INTO clientes_2 (nome, email) VALUES (%s, %s)", ("Teste 3", "teste3@gmail.com"))
    cursor.execute("INSERT INTO clientes_2 (id, nome, email) VALUES (%s, %s, %s)", (2, "Teste 4", "teste4@gmail.com"))
    conexao.commit()

except Exception as exc:
    print(f"Ops! um erro ocorreu! {exc}")
    conexao.rollback()

# Encerrar a conexão
cursor.close()
conexao.close()
