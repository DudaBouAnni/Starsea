from db import conexao

def menu_eventos():
    print("---Cadastro de Eventos---")
    print("1. Buscar Evento")
    print("2. Inserir Evento")
    print("3. Apagar Evento")
    print("4. Listar todos os Eventos")
    print("5. Sair do Cadastro")

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
            data = input('Entre com a data:')
            valor =float(input('Entre com o valor:'))
            artistas = input('Entre com os artistas:')
            informacoes = input('Entre com as informações do evento:')
            link_site_vendas = input('Entre com o link do site de vendas:')
            id_genero = input('Entre com o id do genero:')
            id_organizador = input('Entre com o id do organizador:')
            endereco = input('Entre com o endereco:')
            con = conexao()
            cursor = con.cursor()
            comando = 'INSERT INTO eventos (nome, data, valor, artistas, informacoes, link_site_vendas, id_genero, id_organizador, endereco) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(comando, (nome, data, valor, artistas, informacoes, link_site_vendas, id_genero, id_organizador, endereco))
            con.commit()
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
    #Saída
        elif op == 5:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            print('Fim do cadastro!')