import os
import mysql.connector
from dotenv import load_dotenv

# from mysql.connector import Error

load_dotenv()

# test db connection
# try:
#     connection = mysql.connector.connect(
#         host=os.getenv("MYSQL_HOST"),
#         database=os.getenv("MYSQL_DB"),
#         user=os.getenv("MYSQL_USER"),
#         password=os.getenv("MYSQL_PASSWORD"),
#     )

#     if connection.is_connected():
#         print("Connected to MySQL database!")
#         # optional: check server info
#         db_info = connection.get_server_info()
#         print("MySQL server version:", db_info)
# except Error as e:
#     print("Error while connecting:", e)
# finally:
#     if connection.is_connected():
#         connection.close()
#         print("Connection closed")


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        database=os.getenv("MYSQL_DB"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
    )
