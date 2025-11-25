from db import conexao

def menu_genero():
    print("---Cadastro de Gêneros---")
    print("1. Buscar Gênero")
    print("2. Inserir Gênero")
    print("3. Apagar Gênero")
    print("4. Listar todos os Gênero")
    print("5. Sair do Cadastro")

    while True:
       print("\n")
       op = int(input('Entre com a sua opção:'))
    #Busca
       if op == 1:
           nome= int(input('Entre com o código do Gênero:'))
           con = conexao()
           cursor = con.cursor()
           cursor.execute("SELECT * FROM genero where id_genero = %s", (nome,))
           resultados = cursor.fetchall()
           if not resultados:
               print('Gênero', nome, 'não existe')
           else:

               for linha in resultados:
                   print(linha)
    #Inserção
       elif op == 2:

           nome = input('Entre com o nome do Gênero:')
           con = conexao()
           cursor = con.cursor()
           comando = "INSERT INTO genero (nome) VALUES (%s)"
           cursor.execute(comando, (nome,))
           con.commit()
           print('Gênero', nome, 'inserido com sucesso!')
    #Deleção
       elif op == 3:
           nome = int(input('Entre com o código do Gênero:'))
           con = conexao()
           cursor = con.cursor()
           comando = "DELETE FROM genero where id_genero= %s"
           cursor.execute(comando,(nome,))
           con.commit()
           print(f'Gênero', nome, "Deletado com sucesso!")
    #Listagem
       elif op == 4:
           con = conexao()
           cursor = con.cursor()
           cursor.execute("SELECT id_genero, nome FROM genero;")
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