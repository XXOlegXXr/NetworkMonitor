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
            return connection
        except Error as e:
            print(f"Помилка з'єднання: {e}")
            return None
    def init_db(self):
        conn=self.get_connection()
        if conn:
            try:
                cursor=conn.cursor()
                cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {self.database}")
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
        print(" Пробую підключитися до бази...")
        conn = self.get_connection()
        
        if not conn:
            print("Не вдалося підключитися до бази! conn = None")
            return None

        try:
            cursor = conn.cursor()
            query = "INSERT INTO network_logs (target, status, response_time) VALUES (%s, %s, %s)"
            values = (target, status, response_time)
            
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid
            print(f"Дані записано! Згенерований ID: {new_id}")
            return new_id
        except Exception as e:
            print(f"Помилка SQL: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    
    def get_all_logs(self):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, target, status, response_time FROM network_logs ORDER BY id DESC")
                return cursor.fetchall()
            except Exception as e:
                print(f"Помилка завантаження історії: {e}")
                return []
            finally:
                cursor.close()
                conn.close()
        return []


    def delete_log(self, log_id):
        #13
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM network_logs WHERE id = %s", (log_id,))
                conn.commit()
            except Error as e:
                print(f"Помилка видалення з БД: {e}")
            finally:
                cursor.close()
                conn.close()

    def clear_all_logs(self):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("TRUNCATE TABLE network_logs") 
                conn.commit()
                return True
            except Exception as e:
                print(f"Помилка очищення БД: {e}")
                return False
            finally:
                cursor.close()
                conn.close()
        return False   
