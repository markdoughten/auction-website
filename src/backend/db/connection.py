import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="password",
    database="auction"
)

print("Connection successful!")
connection.close()
