from db import conexao

def menu_eventos():
    print("---Cadastro de Eventos---")
    print("1. Buscar Evento")
    print("2. Inserir Evento")
    print("3. Apagar Evento")
    print("4. Listar todos os Eventos")
    print("5. Listar todos os Usuários que vão em algum evento")
    print("6. Listar todos os Artistas de algum evento")
    print("7. Sair do Cadastro")

    while True:
        print("\n")
        op = int(input('Entre com a sua opção:'))
    #Busca
        if op == 1:
            id_evento = str(input('Entre com o ID do evento:'))
            con = conexao()
            cursor = con.cursor()
            cursor.execute = "SELECT * FROM eventos WHERE id_evento = %s" + (id_evento)
            resultados = cursor.fetchall()
            if not resultados:
                print('Evento:', id_evento, 'não existe')
            else:
                print('(id_evento,nome,data,valor,artistas,informacoes,link_site_vendas,id_genero,id_organizador,endereco)')
                for linha in resultados:
                    print(linha)
            con.commit()
            con.close()
    #Inserção
        elif op == 2:
            nome = input('Entre com o nome do evento:')
            data = input('Entre com a data (yyyy-mm-dd):')
            valor =float(input('Entre com o valor:'))
            informacoes = input('Entre com as informações do evento:')
            link_site_vendas = input('Entre com o link do site de vendas:')
            id_genero = input('Entre com o id do genero:')
            id_organizador = input('Entre com o id do organizador:')
            endereco = input('Entre com o endereço:')

            con = conexao()
            cursor = con.cursor()

            #Inserir evento
            comando = "INSERT INTO Eventos (nome, data, valor, informacoes, link_site_vendas, id_genero, id_organizador, endereco) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(comando, (nome, data, valor, informacoes, link_site_vendas, id_genero, id_organizador, endereco))
            con.commit()

            #Pega ID do evento criado
            cursor.execute("SELECT id_evento FROM Eventos WHERE nome = %s AND data = %s ", (nome, data))
            id_evento = cursor.fetchone()

            #Lista artistas para a primeira inserção
            while True:
                print("Artistas cadastrados")
                cursor.execute("SELECT id_artista, nome FROM Artista")
                artistas = cursor.fetchall()
                for artista in artistas:
                    print(artista)
                id_artista = int(input("Digite o ID do artista que deseja inserir ao evento:"))

                #Verifica se o artista já foi inserido no evento
                cursor.execute("SELECT * FROM Evento_Artista WHERE id_evento = %s AND id_artista =%s", (id_evento, id_artista))
                ja_vinculado = cursor.fetchone()
                if ja_vinculado:
                    print("Este artista já foi vinculado ao evento")
                else:
                    comando_artista = "INSERT INTO Evento_Artista (id_evento, id_artista) VALUES(%s, %s)"
                    cursor.execute(comando_artista,(id_evento, id_artista))
                    con.commit()

                #Pergunta se deseja adicionar mais artistas
                adc_mais = input("Adicionar mais artistas? (S/N): ")
                if adc_mais.lower() != "s":
                    break

            con.close()
            print('Evento', nome, 'inserido com sucesso!')
    #Deleção
        elif op == 3:
            id_evento = int(input('Entre com o id'))
            con = conexao()
            cursor = con.cursor()
            comando = 'DELETE FROM eventos where id_evento =' + str(id_evento)
            cursor.execute(comando)
            con.commit()
            con.close()
            print('Evento', id_evento, "deletado com sucesso!")
    #Listagem
        elif op == 4:
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT * from eventos;")
            resultados = cursor.fetchall()
            for linha in resultados:
                print(linha)

    #Listar usuários que vão em cada evento
        elif op == 5:
            id_evento = int(input('Entre com o id do evento: '))
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT usuario.nome FROM Usuario_Eventos JOIN Usuario ON Usuario_Eventos.id_usuario = Usuario.id_usuario WHERE Usuario_Eventos.id_evento = %s;",(id_evento,))
            evento = cursor.fetchone()
            if not evento:
                print("Evento não encontrado")
            print("Evento:", evento)
            cursor.execute("SELECT usuario.nome FROM Usuario_Eventos JOIN Usuario ON Usuario_Eventos.id_usuario = Usuario.id_usuario WHERE Usuario_Eventos.id_evento = %s;",(id_evento,))
            usuarios = cursor.fetchall()
            if not usuarios:
                print("Nenhum usuário tem presença confirmada neste evento.")
            else:
                print("Usuários que tem presença confirmada neste evento:")
                for usuario in usuarios:
                    print(usuario)
    #Listar todos os artistas de um evento
        elif op == 6:
            id_evento = int(input("Entre com o ID do evento: "))
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT nome FROM eventos WHERE id_evento = %s", (id_evento,))
            evento = cursor.fetchone()

            if not evento:
                print("Evento não encontrado.")
            print("Artista do Evento:", evento)
            cursor.execute("SELECT Artista.nome FROM Evento_Artista JOIN Artista ON Evento_Artista.id_artista = Artista.id_artista WHERE Evento_Artista.id_evento = %s;",(id_evento,))

            artistas = cursor.fetchall()

            if not artistas:
                print("Nenhum artista vinculado a este evento.")
            else:
                print("Lineup:")
                for artista in artistas:
                    print(artista)
    #Saída
        elif op == 7:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            print('Fim do cadastro!')