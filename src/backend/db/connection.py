import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="password@123",
    database="auction"
)

print("Connection successful!")
connection.close()
