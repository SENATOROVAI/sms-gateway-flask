import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME')
        )

    def execute_query(self, query, params=None):
        result = None
        try:
            connection = self.connection
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.with_rows:
                    result = cursor.fetchall()
            connection.commit()
        except mysql.connector.Error as error:
            print(f"Error executing query: {error}")
        finally:
            if connection:
                connection.close()
        return result


class MessageLogModel:
    @staticmethod
    def save_message(modem_port, phone_number, message, status):
        db = Database()
        query = "INSERT INTO `logs` (`id`, `imei`, `number`, `sms`, `status`) VALUES (NULL, %s, %s, %s, %s);"
        db.execute_query(query, (modem_port, phone_number, message, status))

    @staticmethod
    def get_data():
        db = Database()
        query = "SELECT * FROM logs;"
        return db.execute_query(query) 

    @staticmethod
    def delete_messages():
        db = Database()
        query = "DELETE FROM logs;"
        db.execute_query(query)