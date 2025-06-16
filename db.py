import os
import mysql.connector
from flask import current_app

def get_db_connection():
    return mysql.connector.connect(
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD'],
        host=current_app.config['DB_HOST'],
        database=current_app.config['DB_NAME'],
        port=current_app.config['DB_PORT']
    )
