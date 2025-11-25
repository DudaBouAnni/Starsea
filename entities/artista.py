from db import conexao

def menu_artista():
    print("---Cadastro de Artista---")
    print("1. Buscar Artista")
    print("2. Inserir Artista")
    print("3. Apagar Artista")
    print("4. Listar todos os Artistas")
    print("5. Sair do Cadastro")

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
            eventos = input('Entre com o nome do Evento:')
            descricao = input('Entre com a descrição do Artista:')
            con = conexao()
            cursor = con.cursor()
            comando = 'INSERT INTO Artista (nome, eventos, descricao) VALUES (%s, %s, %s)'
            cursor.execute(comando, (nome, eventos, descricao))
           # event = 'INSERT INTO Artista (evento) VALUES (%s)'
           # descrit =  'INSERT INTO Artista (descricao) VALUES (%s)'
            con.commit()
            con.close()
            print('Artista','inserido com sucesso!')
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
    #Saída
        elif op == 5:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            print('Fim do cadastro!')