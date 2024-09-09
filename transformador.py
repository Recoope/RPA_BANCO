import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

db_host1 = os.getenv('DB_HOST1')
db_database1 = os.getenv('DB_DATABASE1')
db_user1 = os.getenv('DB_USER1')
db_password1 = os.getenv('DB_PASSWORD1')
db_port1 = os.getenv('DB_PORT1')

db_database2 = os.getenv('DB_DATABASE2')

print("DB_HOST1:", os.getenv('DB_HOST1'))
print("DB_DATABASE1:", os.getenv('DB_DATABASE1'))
print("DB_USER1:", os.getenv('DB_USER1'))
print("DB_PASSWORD1:", os.getenv('DB_PASSWORD1'))
print("DB_PORT1:", os.getenv('DB_PORT1'))
print("DB_DATABASE2:", os.getenv('DB_DATABASE2'))

# BANCO DO PRIMEIRO ANO========================================

print('Começando===============================================')
try:
    # Conectar ao banco de dados
    conn = psycopg2.connect(
        host=db_host1,
        database=db_database1,
        user=db_user1,
        password=db_password1,
        port=db_port1
    )
    print("Conexão estabelecida com sucesso!")
except psycopg2.OperationalError as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    exit()  # Saia se a conexão falhar

try:
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM Cooperativa''')
    results = cursor.fetchall()
    
    # Criar DataFrame
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(results, columns=columns)

    cursor.execute('''SELECT * FROM Cooperativa''')
    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()
    df_cooperativa = pd.DataFrame(results, columns=columns)
    
finally:
    # Fechar o cursor e a conexão
    cursor.close()
    conn.close()

# BANCO DO SEGUNDO ANO ========================================

print('Começando===============================================')
try:
    # Conectar ao banco de dados
    conn = psycopg2.connect(
        host=db_host1,
        database=db_database2,
        user=db_user1,
        password=db_password1,
        port=db_port1
    )
    print("Conexão estabelecida com sucesso!")
except psycopg2.OperationalError as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    exit()  # Saia se a conexão falhar


try:
    cursor = conn.cursor()

    cursor.execute('DELETE FROM cooperativa') # deleta todos os registros para garantir que não vai pegar dados duplicados e garante que todos os valores do banco apagados ou alterados seram registrados
                   
    for i in range(len(df_cooperativa)):
        cursor.execute('CALL insert_cooperativa(%s, %s, %s, %s)', 
                       (df_cooperativa['cnpj'][i], df_cooperativa['nome'][i], df_cooperativa['email'][i], df_cooperativa['senha'][i]))

    # Confirme as alterações
    conn.commit()
    print("Deu Green")
except Exception as e:
    print(f"Erro ao executar a procedure: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()

cursor.close()
conn.close()