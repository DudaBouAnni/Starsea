from entities.artista import menu_artista
from entities.eventos import menu_eventos
from entities.genero import menu_genero
from entities.usuario import menu_usuario
from entities.organizador import menu_organizador
def menu_principal():
    while True:
        print("\n--- Menu Principal ---")
        print("1. Cadastro de Artistas")
        print("2. Cadastro de Eventos")
        print("3. Cadastro de Gêneros")
        print("4. Cadastro de Usuários")
        print("5. Cadastro de Organizadores")
        print("6. Sair")

        op = input("Escolha uma opção: ")

        if op == "1":
            menu_artista()
        elif op == "2":
            menu_eventos()
        elif op == "3":
            menu_genero()
        elif op == "4":
            menu_usuario()
        elif op == "5":
            menu_organizador()
        elif op == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu_principal()
