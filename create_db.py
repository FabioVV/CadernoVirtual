import mysql.connector

# ROdar este arquivo apenas uma vez.


my = mysql.connector.connect(
    host='localhost',
    user='root (provavelmente root tbm se vc nao mudou)',
    passwd='sua senha do MYsql (provavelmente root tbm se vc nao mudou)'
)

c = my.cursor()

c.execute('CREATE DATABASE caderno')
print('Database criado.')
