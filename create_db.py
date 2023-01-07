import mysql.connector

## ROdar este arquivo apenas uma vez.
##      JA FOI RODADO             #######################

my = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd = 'guerra998'
)

c = my.cursor()

c.execute('CREATE DATABASE caderno')
print('Database criado.')