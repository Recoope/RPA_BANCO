import psycopg
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('DB_HOST1')
db_database1 = os.getenv('DB_DATABASE1')
db_user = os.getenv('DB_USER1')
db_password = os.getenv('DB_PASSWORD1')
db_port = os.getenv('DB_PORT1')

db_database2 = os.getenv('DB_DATABASE2')

# BANCO DO PRIMEIRO ANO========================================

print('Começando===============================================')
try:
    # Conectar ao banco de dados
    conn_1ano = psycopg.connect(host=db_host,
                                port=db_port,
                                dbname=db_database1,
                               user=db_user,
                                password=db_password)
    print("Conexão estabelecida com sucesso!")

except psycopg.OperationalError as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    exit()  # Saia se a conexão falhar

try:
    cursor_1ano = conn_1ano.cursor()

    cursor_1ano.execute('''SELECT * FROM Cooperativa''')
    columns = [desc[0] for desc in cursor_1ano.description]
    results = cursor_1ano.fetchall()
    df_cooperativa = pd.DataFrame(results, columns=columns)

    cursor_1ano.execute('''SELECT * FROM Endereco''')
    columns = [desc[0] for desc in cursor_1ano.description]
    results = cursor_1ano.fetchall()
    df_endereco = pd.DataFrame(results, columns=columns)

    cursor_1ano.execute('''SELECT * FROM Leilao''')
    columns = [desc[0] for desc in cursor_1ano.description]
    results = cursor_1ano.fetchall()
    df_leilao = pd.DataFrame(results, columns=columns)

    cursor_1ano.execute('''SELECT * FROM Produto''')
    columns = [desc[0] for desc in cursor_1ano.description]
    results = cursor_1ano.fetchall()
    df_produto = pd.DataFrame(results, columns=columns)

    cursor_1ano.execute('''SELECT * FROM Imagem''')
    columns = [desc[0] for desc in cursor_1ano.description]
    results = cursor_1ano.fetchall()
    df_foto = pd.DataFrame(results, columns=columns)

except psycopg.OperationalError as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    exit()  # Saia se a conexão falhar

# BANCO DO SEGUNDO ANO ========================================

print('Começando===============================================')
try:
    # Conectar ao banco de dados
    conn = psycopg.connect(host=db_host,
                                port=db_port,
                                dbname=db_database2,
                               user=db_user,
                                password=db_password)

    print("Conexão estabelecida com sucesso!")
except psycopg.OperationalError as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    exit()  # Saia se a conexão falhar

#================================================Coopertiva
try:
    cursor = conn.cursor()
    cursor_1ano = conn_1ano.cursor()

    for i in range(len(df_cooperativa)):
        if df_cooperativa['dados_status'][i] == 'Ativo':
            try:
                # Tenta inserir no banco de dados
                cursor.execute('CALL insert_cooperativa(%s, %s, %s, %s, %s)',
                    (df_cooperativa['cnpj'][i], df_cooperativa['nome'][i], df_cooperativa['email'][i], df_cooperativa['senha'][i],
                    df_cooperativa['ativo'][i]))
                
                conn.commit()

            except Exception as e:
                print(f'Erro {e.__class__.__name__}: {e}')
                print(f"Fazendo Update!!!===========================")
                conn.rollback()

                try:
                    # Tenta fazer o update
                    cursor.execute('UPDATE cooperativa SET nome_cooperativa=%s, email_cooperativa=%s, senha_cooperativa=%s, status=%s where cnpj_cooperativa=%s',
                               (df_cooperativa['nome'][i], df_cooperativa['email'][i], df_cooperativa['senha'][i],df_cooperativa['ativo'][i], df_cooperativa['cnpj'][i]))

                    # Confirma o update
                    conn.commit()

                except Exception as e_update:
                    conn.rollback()
                    print(f"Erro no update: {e_update}")

        print("Deu Green")

except Exception as e:
    conn.rollback()
    print(f"Erro ao executar: {e}")

finally:
    try:
        for i in range(len(df_cooperativa)):
            cursor_1ano.execute('UPDATE cooperativa SET dados_status=%s where cnpj=%s',
                                ('Inativo', df_cooperativa['cnpj'][i]))

        conn_1ano.commit()
    except Exception as e:
        print(f"Erro no finally ao tentar atualizar status: {e}")

#================================================Endereco
try:
    cursor = conn.cursor()
    cursor_1ano = conn_1ano.cursor()

    for i in range(len(df_endereco)):
        if df_endereco['dados_status'][i] == 'Ativo':  # Corrige a verificação do status
            id_endereco = int(df_endereco['id'][i])
            cidade = str(df_endereco['cidade'][i])
            logradouro = str(df_endereco['logradouro'][i])
            numero = int(df_endereco['numero'][i])
            status = str(df_endereco['ativo'][i])

            try:
                # Tenta inserir no banco de dados
                cursor.execute('CALL insert_endereco(%s::int, %s::varchar, %s::varchar, %s::int, %s::varchar)',
                    (id_endereco, cidade, logradouro, numero, status))
                
                conn.commit()

            except Exception as e:
                # Caso o insert falhe, tenta fazer o update
                print(f"Falha ao inserir, tentando atualizar: {e}")
                conn.rollback()
                print('Update sendo feito============')
                try:
                    # Tenta fazer o update
                    cursor.execute('UPDATE endereco SET cidade=%s, rua=%s, numero=%s, status=%s WHERE id_endereco=%s',
                    (cidade, logradouro, numero, status, id_endereco))

                    # Confirma o update
                    conn.commit()

                except Exception as e_update:
                    conn.rollback()
                    print(f"Erro no update: {e_update}")

    print("Deu Green")

except Exception as e:
    # Faz rollback em caso de erro
    conn.rollback()
    print(f"Erro ao executar: {e}")

finally:
    try:
        # Atualiza o campo dados_status na outra tabela
        for i in range(len(df_endereco)):
            id_endereco = int(df_endereco['id'][i])
            # Atualiza o status se a inserção for bem-sucedida
            cursor_1ano.execute('UPDATE endereco SET dados_status=%s WHERE id=%s',
                            ('Inativo', id_endereco))

        conn_1ano.commit()
    except Exception as e:
        print(f"Erro no finally ao tentar atualizar status: {e}")

#================================================Produto
print(df_produto)
print(df_leilao)
print(df_foto)
try:
    cursor = conn.cursor()
    cursor_1ano = conn_1ano.cursor()

    for i in range(len(df_produto)):
        # Verifica se o status é True
        if df_produto['dados_status'][i] == 'Ativo':
            try:
                cursor.execute('''CALL insert_produto (%s::integer, %s::varchar, %s::numeric, %s::numeric, %s::varchar, %s::varchar)''',
                    (int(df_produto['id'][i]),
                        df_produto['material'][i],
                        float(df_leilao['valor_inicial'][i]),
                        float(df_produto['peso'][i]),
                        df_foto['imagem'][i],
                        df_produto['ativo'][i]))


            except Exception as e:
                # Faz rollback após erro no insert
                conn.rollback()
                print(f"Erro no insert: {e.__class__.__name__}: {e}")
                print("Fazendo Update================")

                try:
                    cursor.execute('''UPDATE produto SET tipo_produto=%s, valor_inicial_produto=%s, peso_produto=%s,
                                    foto_produto=%s, status=%s WHERE id_produto=%s''',
                                    (df_produto['material'][i], float(df_leilao['valor_inicial'][i]),
                                    float(df_produto['peso'][i]), df_foto['imagem'][i], df_produto['ativo'][i], int(df_produto['id'][i])))

                    # Confirma o update
                    conn.commit()

                except Exception as e_update:
                    conn.rollback()
                    print(f"Erro no update: {e.__class__.__name__}: {e_update}")

    print("Deu Green")

except Exception as e:
    # Faz rollback se ocorrer erro geral
    conn.rollback()
    print(f"Erro ao executar: {e}")

finally:
    try:
        # Atualiza o campo dados_status na outra tabela
        for i in range(len(df_produto)):
            cursor_1ano.execute('UPDATE produto SET dados_status=%s WHERE id=%s',
                                ('Inativo', int(df_produto['id'][i])))

        conn_1ano.commit()
    except Exception as e:
        print(f"Erro no finally ao tentar atualizar status: {e}")

#================================================Leilão
try:
    cursor = conn.cursor()
    cursor_1ano = conn_1ano.cursor()

    for i in range(len(df_leilao)):
        if df_leilao['dados_status'][i] == 'Ativo':
            try:
                # Tenta inserir no banco de dados
                cursor.execute('CALL insert_leilao(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (int(df_leilao['id_endereco'][i]), df_leilao['id_cooperativa'][i], df_leilao['data_inicio'][i],
                     df_leilao['data_fim'][i] ,df_leilao['detalhe'][i] ,int(df_leilao['id'][i]), df_leilao['hora_fim'][i],
                     int(df_leilao['id_produto'][i]),df_leilao['ativo'][i]))

                conn.commit()

                print('passei aqui')
            except Exception as e:
                print(f'Erro: {e}')
                print(f"Update feito==============")
                conn.rollback()

                try:
                    cursor.execute('UPDATE leilao SET data_inicio_leilao=%s, data_fim_leilao=%s, hora_leilao=%s, id_endereco=%s, detalhes_leilao=%s, id_produto=%s, ativo=%s WHERE id_leilao=%s',
                    (df_leilao['data_inicio'][i], df_leilao['data_fim'][i], df_leilao['hora_fim'][i],
                     int(df_leilao['id_endereco'][i]), df_leilao['detalhe'][i], int(df_leilao['id_produto'][i]), df_leilao['ativo'][i],int(df_leilao['id'][i])))

                    conn_1ano.commit()
                except Exception as e:
                    print(f"Erro no update: {e}")
                    conn.rollback()

    # Confirma as alterações
    conn.commit()
    print("Deu Green")

except Exception as e:
    # Faz rollback em caso de erro
    conn.rollback()
    print(f"Erro ao executar: {e}")

finally:
    try:
        for i in range(len(df_leilao)):
            cursor_1ano.execute('UPDATE leilao SET dados_status=%s WHERE id=%s',
                                ('Inativo', int(df_leilao['id'][i])))

        conn_1ano.commit()
    except Exception as e:
        print(f"Erro no finally ao tentar atualizar status: {e}")
    # Fechar o cursor e a conexão
    cursor.close()
    conn.close()
    cursor_1ano.close()
    conn_1ano.close()