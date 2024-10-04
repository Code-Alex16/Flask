import os
from dotenv import load_dotenv
import mysql.connector.pooling
from mysql.connector import Error

class Database:
    
    load_dotenv()

    POOL = None
    POOL_NAME=os.getenv('DB_POOL_NAME')
    POOL_SIZE=int(os.getenv('DB_POOL_SIZE'))
    HOST=os.getenv('DB_HOST')
    PORT = os.getenv('DB_PORT')
    USER=os.getenv('DB_USER')
    PASSWORD=os.getenv('DB_PASSWORD')
    DATABASE=os.getenv('DB_NAME')

    @classmethod
    def GetPool(cls):

        if cls.POOL is None:
            try:
                cls.pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name= cls.POOL_NAME,
                    pool_size= cls.POOL_SIZE,
                    host = cls.HOST,
                    port = cls.PORT,
                    database = cls.DATABASE,
                    user = cls.USER,
                    password = cls.PASSWORD
                )
            
            except Error as e:
                print(f'Error en la creacion de POOl {e}')

        return cls.pool

    @classmethod
    def GetConnexion(cls):
        return cls.GetPool().get_connection()

    @classmethod
    def CloseConexion(cls, connection):
        if connection:
            connection.close()