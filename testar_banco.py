
from sqlalchemy import text
from app.database import engine

try:
    with engine.connect() as conexao:
        resultado = conexao.execute(
            text("SELECT current_database(), version()")
        )
        banco, versao = resultado.fetchone()

        print("Conexão realizada com sucesso!")
        print("Banco:", banco)
        print("PostgreSQL:", versao)

except Exception as erro:
    print("Falha ao conectar ao banco:")
    print(erro)
