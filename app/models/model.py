import os
from dotenv import load_dotenv
import sqlite3
from typing import Optional, Tuple, List, Dict

load_dotenv()


class Database:
    def __init__(self) -> None:
        print(os.getenv("DATABASE_FILE"))
        self.connection = sqlite3.connect(os.getenv("DATABASE_FILE"))

    def execute_query(
        self, query: str, params: Optional[Tuple] = None
    ) -> Optional[List[Tuple]]:
        result: Optional[List[Tuple]] = None
        try:
            connection = self.connection
            cursor = connection.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            result = cursor.fetchall()
            connection.commit()
        except sqlite3.Error as error:
            print(f"Error executing query: {error}")
        finally:
            if connection:
                connection.close()
        return result


class MessageLogModel:
    @staticmethod
    def save_message(
        modem_port: str, phone_number: str, message: str, status: int
    ) -> None:
        db: Database = Database()
        query: str = "INSERT INTO logs (id, imei, number, sms, status) VALUES (NULL, ?, ?, ?, ?);"
        db.execute_query(query, (modem_port, phone_number, message, status))

    @staticmethod
    def get_data() -> Optional[List[Tuple]]:
        db: Database = Database()
        query: str = "SELECT * FROM logs;"
        return db.execute_query(query)

    @staticmethod
    def delete_messages() -> None:
        db: Database = Database()
        query: str = "DELETE FROM logs;"
        db.execute_query(query)
