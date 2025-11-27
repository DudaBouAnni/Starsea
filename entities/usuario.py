from db import conexao


def menu_usuario():
    while True:
        print("---Cadastro de Usuário---")
        print("1. Buscar Usuário")
        print("2. Inserir Usuário")
        print("3. Apagar Usuário")
        print("4. Listar todos os Usuários")
        print("5. Inserir Usuário em Evento")
        print("6. Sair do Cadastro")
        op = int(input('Entre com a sua opção:'))
        # Busca
        if op == 1:
            nome = str(input('Entre com o nome do usuário:'))
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM Usuario where nome: = %s" + str(nome, ))
            resultados = cursor.fetchall()
            if not resultados:
                print('Usuário', nome, 'não existe')
            else:
                print('(id_usuario,nome,email,senha,data_nascimento,genero_preferencia,endereco)')
                for linha in resultados:
                    print(linha)
        # Inserção
        elif op == 2:
            nome = input('Entre com o nome de usuário:')
            email = input('Entre com o e-mail:')
            senha = input('Entre com a senha:')
            data_nascimento = str(input('Entre com a data de nascimento (yyyy-mm-dd):'))

            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT id_genero, nome FROM Genero")
            generos = cursor.fetchall()
            print("Gêneros disponíveis")
            for genero in generos:
                print(genero)
            genero_preferencia = input('Entre com o gênero de preferência musical:')
            endereco = input('Entre com o endereço:')
            comando = 'INSERT INTO Usuario (nome, email, senha, data_nascimento,genero_preferencia,endereco) VALUES(%s, %s, %s, %s, %s, %s)'
            con = conexao()
            cursor = con.cursor()
            cursor.execute(comando, (nome, email, senha, data_nascimento, genero_preferencia, endereco))
            con.commit()
            con.close()
            print('Usuario', nome, 'inserido com sucesso!')
        # Deleção
        elif op == 3:
            id_usuario = int(input('Entre com o id'))
            con = conexao()
            cursor = con.cursor()
            comando = 'DELETE FROM Usuario where id_usuario =' + str(id_usuario)
            cursor.execute(comando)
            con.commit()
            con.close()
            print('Usuario', id_usuario, "deletado com sucesso!")
        # Listagem
        elif op == 4:
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT * from Usuario;")
            resultados = cursor.fetchall()
            for linha in resultados:
                print(linha)
        # Inserir usuário em evento
        elif op == 5:
            id_usuario = int(input("ID do usuário: "))
            id_evento = int(input("ID do evento: "))
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT id_usuario FROM Usuario WHERE id_usuario = %s", (id_usuario,))
            if not cursor.fetchone():
                print("Usuário não encontrado.")
                con.close()
                continue
            cursor.execute("SELECT id_evento FROM Eventos WHERE id_evento = %s", (id_evento,))
            if not cursor.fetchone():
                print("Evento não encontrado.")
                con.close()
                continue
            # Insere na tabela intermediária
            cursor.execute("INSERT INTO Usuario_Eventos (id_usuario, id_evento) VALUES (%s, %s)",
                           (id_usuario, id_evento))
            con.commit()
            con.close()
            print("Usuário adicionado ao evento com sucesso!")
        # Saída
        elif op == 6:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
