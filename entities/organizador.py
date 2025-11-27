from db import conexao

def menu_organizador():
    while True:
        print("---Cadastro de Organizador---")
        print("1. Buscar Organizadores")
        print("2. Inserir Organizador")
        print("3. Apagar Organizador")
        print("4. Listar todos os Organizadores")
        print("5. Sair do Cadastro")
        print("\n")
        op = int(input('Entre com a sua opção:'))

        #Busca
        if op == 1:
            nome= int(input('Entre com o código do Organizador:'))
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM Organizador where id_organizador = %s", (nome,))
            resultados = cursor.fetchall()
            if not resultados:
                print('Organizador', nome, 'não existe')
            else:
                for linha in resultados:
                    print(linha)
        #Inserção
        elif op == 2:
            nome = input('Entre com o nome do Organizador:')
            comando = "INSERT INTO organizador (nome_organizador) VALUES (%s)"
            con = conexao()
            cursor = con.cursor()
            cursor.execute(comando, (nome,))
            con.commit()
            print(f'Organizador', nome, 'inserido com sucesso!')
        #Deleção
        elif op == 3:
            id_organizador = int(input('Entre com o ID do Organizador:'))
            con = conexao()
            cursor = con.cursor()
            comando = "DELETE FROM organizador where id_organizador = %s"
            cursor.execute(comando,(id_organizador,))
            con.commit()
            print("Organizador deletado com sucesso!")
        #Listagem
        elif op == 4:
            con = conexao()
            cursor = con.cursor()
            cursor.execute("SELECT id_organizador, nome_organizador FROM organizador;")
            resultados = cursor.fetchall()
            for linha in resultados:
                print(linha)
        #Saída
        elif op == 5:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")