from db import conexao

def menu_artista():
    print("---Cadastro de Artista---")
    print("1. Buscar Artista")
    print("2. Inserir Artista")
    print("3. Apagar Artista")
    print("4. Listar todos os Artistas")
    print("5. Vincular Gênero ao Artista")
    print("6. Sair do Cadastro")

    while True:
        print("\n")
        op = int(input('Entre com a sua opção:'))
    #Busca
        if op == 1:
            id_artista = int(input('Entre com o código do Artista:'))
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM Artista where id_artista = %s", int(id_artista,))
            resultados = cursor.fetchall()
            if not resultados:
                print('Artista', id_artista, 'não existe')
            else:
                for linha in resultados:
                    print(linha)
    #Inserção
        elif op == 2:
            nome = input('Entre com o nome do Artista:')
            descricao = input('Entre com a descrição do Artista:')

            con = conexao()
            cursor = con.cursor()

            #Inserção nome descrição
            comando = 'INSERT INTO Artista (nome, descricao) VALUES (%s, %s)'
            cursor.execute(comando, (nome, descricao))
            con.commit()

            #Pegar ID artista
            cursor.execute("SELECT id_artista FROM Artista where nome = %s",(nome,))
            id_artista = cursor.fetchone()

            #Pergunta se tem evento
            tem_evento = input("O artista tem algum evento? (S/N):")
            if tem_evento.lower() == "s":
                print("Eventos cadastrados")
                cursor.execute("SELECT id_evento, nome FROM Evento")
                eventos = cursor.fetchall()
                for evento in eventos:
                    print(evento)
                id_evento = int(input("Digite o ID do evento desejado: "))
                #Vínculo artista_evento
                comando_evento = "INSERT INTO Artista_Evento (id_artista, id_evento) VALUES (%s, %s)"
                cursor.execute(comando_evento, (id_artista, id_evento))
                con.commit()
                print("Artista vinculado com sucesso!")

            #Adicionar Gênero
            genero = input("Deseja adicionar algum gênero ao artista? (S/N): ")
            while genero.lower() == "s":
                print("Gêneros Cadastrados")
                cursor.execute("SELECT id_genero, nome FROM Genero")
                generos = cursor.fetchall()
                for genero in generos:
                    print(genero)
                id_genero = int(input("Digite o ID do genero desejado: "))
                #Verifica se o Gênero ja foi atribuído
                cursor.execute("SELECT * FROM Artista_Genero WHERE id_artista = %s AND id_genero = %s",(id_artista, id_genero,))
                ja_vinculado = cursor.fetchone()
                if ja_vinculado:
                    print("Este gênero já está vinculado ao artista", nome)
                else:
                    comando_genero = "INSERT INTO Artista_Genero (id_artista, id_genero) VALUES (%s, %s)"
                    cursor.execute(comando_genero, (id_artista, id_genero))
                    con.commit()
                    cursor.execute("SELECT * FROM Artista_Genero WHERE id_genero = %s",(id_genero,))
                    nome_genero = cursor.fetchone()
                    print("Gênero", nome_genero, "adicionado ao artista", nome, "com sucesso!")
                genero = input("Deseja adicionar mais um gênero? (S/N)")
            con.close()
            print('Artista', nome, 'inserido com sucesso!')
    #Deleção
        elif op == 3:
            id_artista = int(input('Entre com o código do Artista:'))
            con = conexao()
            cursor = con.cursor()
            comando = 'DELETE FROM Artista where id_artista =' +str(id_artista)
            cursor.execute(comando)
            con.commit()
            con.close()
            print('Artista', id_artista, "Excluído com sucesso!")
    #Listagem
        elif op == 4:
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT*FROM Artista")
            resultados = cursor.fetchall()
            con.commit()
            con.close()
            for linha in resultados:
                 print(linha)
    #Vincular Gênero ao Artista
        elif op == 5:
            id_artista = int(input("ID do Artista: "))
            id_genero = int(input('Entre com o ID do Gênero do Artista:'))
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT id_artista FROM Artista WHERE id_artista = %s",(id_artista,))
            if not cursor.fetchone():
                print("Artista não encontrado.")
            cursor.execute("SELECT id_genero FROM Genero where id_genero = %s",(id_genero,))
            if not cursor.fetchone():
                print("Genero não encontrado.")
            cursor.execute("SELECT * FROM Artista_Genero WHERE id_artista = %s AND id_genero = %s",(id_artista, id_genero,))
            if cursor.fetchone():
                print("Genero já vinculado.")
            cursor.execute("INSERT INTO Artista_Genero (id_artista, id_genero) VALUES (%s, %s)",(id_artista, id_genero,))
            con.commit()
            con.close()
            print("Gênero inserido com sucesso!")
    #Saída
        elif op == 6:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            print('Fim do cadastro!')