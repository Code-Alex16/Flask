import os
from dotenv import load_dotenv
import mysql.connector.pooling
from mysql.connector import Error

class Database:
    
    load_dotenv()

    POOL = None
    POOL_NAME=os.getenv('DB_POOL_NAME')
    POOL_SIZE=int(os.getenv('DB_POOL_SIZE',5))
    HOST=os.getenv('DB_HOST')
    PORT = 3306
    USER=os.getenv('DB_USER')
    PASSWORD=os.getenv('DB_PASSWORD')
    DATABASE=os.getenv('DB_NAME')

    @classmethod
    def GetPool(cls):

        if cls.POOL == None:
            try:
                cls.POOL = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name= cls.POOL_NAME,
                    pool_size= cls.POOL_SIZE,
                    pool_reset_session= True,
                    host = cls.HOST,
                    port = cls.PORT,
                    database = cls.DATABASE,
                    user = cls.USER,
                    password = cls.PASSWORD
                )

            
            except Error as e:
                print(f'Error en la creacion de POOl {e}')

        return cls.POOL

    @classmethod
    def GetConnexion(cls):
        try:
            return cls.GetPool().get_connection()
        except Error as er:
            print(f'Error al querer obtener la conexion: {er}')
        

    @classmethod
    def CloseConexion(cls, connection):
        if connection:
            connection.close()