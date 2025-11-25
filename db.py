import pymysql

#Conexão com o banco de dados
def conexao():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="toor",
        database="Starsea"
    )


