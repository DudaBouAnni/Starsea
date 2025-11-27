from db import conexao


def menu_genero():
    while True:
        print("---Cadastro de Gêneros---")
        print("1. Buscar Gênero")
        print("2. Inserir Gênero")
        print("3. Apagar Gênero")
        print("4. Listar todos os Gêneros")
        print("5. Sair do Cadastro")
        print("\n")

        op = int(input('Entre com a sua opção:'))
        # Busca
        if op == 1:
            con = conexao()
            cursor = con.cursor()
            nome = int(input('Entre com o código do Gênero:'))
            cursor.execute("SELECT * FROM genero where id_genero = %s", (nome,))
            resultados = cursor.fetchall()
            if not resultados:
                print('Gênero', nome, 'não existe')
            else:

                for linha in resultados:
                    print(linha)
        # Inserção
        elif op == 2:
            con = conexao()
            cursor = con.cursor()
            nome = input('Entre com o nome do Gênero:')
            comando = "INSERT INTO genero (nome) VALUES (%s)"
            cursor.execute(comando, (nome,))
            con.commit()
            print('Gênero', nome, 'inserido com sucesso!')
        # Deleção
        elif op == 3:
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT id_genero, nome FROM genero;")
            resultados = cursor.fetchall()
            for linha in resultados:
                print(linha)
            nome = int(input('Entre com o código do Gênero:'))
            comando = "DELETE FROM genero where id_genero= %s"
            cursor.execute(comando, (nome,))
            con.commit()
            print(f'Gênero', nome, "Deletado com sucesso!")
        # Listagem
        elif op == 4:
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT id_genero, nome FROM genero;")
            resultados = cursor.fetchall()
            for linha in resultados:
                print(linha)
            # Saída
        elif op == 5:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
