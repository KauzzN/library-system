import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="senha",
    database="library_db",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()