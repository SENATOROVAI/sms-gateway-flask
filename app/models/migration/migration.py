# from flask import Flask
# from dotenv import load_dotenv
# import mysql.connector
# import os

# app = Flask(__name__)
# load_dotenv()

# DB_HOST = os.getenv('DB_HOST', 'localhost')
# DB_USER = os.getenv('DB_USER', 'username')
# DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
# DB_NAME = os.getenv('DB_NAME', 'smsgate')

# def get_db_connection():
#     return mysql.connector.connect(
#         host=DB_HOST,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         database=DB_NAME
#     )

# def upgrade():
#     with app.app_context():
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         create_table_query = '''
#         CREATE TABLE logs (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             imei VARCHAR(255),
#             number VARCHAR(255),
#             sms VARCHAR(255),
#             status VARCHAR(255)
#         )
#         '''
#         cursor.execute(create_table_query)
#         conn.commit()
#         cursor.close()
#         conn.close()


# def downgrade():
#     with app.app_context():
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         drop_table_query = '''
#         DROP TABLE logs
#         '''
#         cursor.execute(drop_table_query)
#         conn.commit()
#         cursor.close()
#         conn.close()
