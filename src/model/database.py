import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

class DatabaseModel:
    def __init__(self):
        load_dotenv()

        self.host = os.getenv("MYSQL_HOST")
        self.port = os.getenv("MYSQL_PORT")
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DATABASE")

    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Error as e:
            print(f"Помилка з'єднання: {e}")
            return None
    def init_db(self):
        conn=self.get_connection()
        if conn:
            try:
                cursor=conn.cursor()
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.database}")
                cursor.execute(f"USE {self.database}")
                cursor.execute(
                    """
CREATE TABLE IF NOT EXISTS network_logs (
id INT AUTO_INCREMENT PRIMARY KEY,
target VARCHAR(255),
status VARCHAR(50),
response_time FLOAT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
                    """
                )
                conn.commit()
                print(f"База {self.database} та таблиця готові.")
            finally:
                cursor.close()
                conn.close()

    def save_log(self, target, status, response_time):
        conn=self.get_connection()
        if conn:
            try:
                cursor=conn.cursor()
                query="INSERT INTO network_logs (target, status, response_time) VALUES (%s, %s, %s)"
                values = (target, status, response_time)
                cursor.execute(query, values)
                conn.commit()
                print(f"Збережено в БД: {target} | {status} | {response_time}ms")
            except Error as e:
                print(f"Помилка запису в БД: {e}")
            finally:
                cursor.close()
                conn.close()

