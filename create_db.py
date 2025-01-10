import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ishan"
    )
    
    if connection.is_connected():
        print("Connected to MySQL Server")
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS IMS")
        print("Database created successfully!")
        cursor.execute("USE IMS")
        cursor.execute("CREATE TABLE IF NOT EXISTS employee (eid INT AUTO_INCREMENT PRIMARY KEY,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)")
        cursor.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTO_INCREMENT,name text,contact text,description text)")
        print("Table created successfully!")
except Error as e:
    print("Error while connecting to MySQL:", e)
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
