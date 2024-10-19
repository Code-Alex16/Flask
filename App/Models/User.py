from Database.db_config import Database

class User:
    # Consultas SQL
    SELECT_USER_INFO = 'SELECT id, username, password, email FROM tbl_users WHERE id = %s'
    SELECT_USER = 'SELECT id, username FROM tbl_users WHERE email = %s, password = %s'
    ADD_USER = 'INSERT INTO tbl_users (username, email, password) VALUES (%s, %s, %s)'
    UPDATE_USER = 'UPDATE tbl_posts SET email = %s, password = %s WHERE id = %s'
    DELETE_USER = 'DELETE FROM tbl_users WHERE id = %s'

    def __init__(self, id = None, username = None, email = None, password = None):
        self.id         = id
        self.username   = username
        self.email      = email
        self.password   = password


    @classmethod
    def _execute_query(cls, query, params=None, fetch_one=False):
        """Función auxiliar para ejecutar consultas con manejo de conexión"""
        connexion = Database().GetConnexion()
        result = None

        if connexion:
            try:
                cursor = connexion.cursor()
                cursor.execute(query, params or ())

                if fetch_one:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()

                connexion.commit()  # Solo necesario para operaciones de escritura

            except Exception as ex:
                print(f'Error al ejecutar la consulta: {ex}')
            finally:
                cursor.close()
                Database().CloseConexion(connection=connexion)

        return result
    
    def login_user(self):
        """Obtener datos de usuario si estan correctas sus credenciales"""
        result = self._execute_query(self.SELECT_USER, (self.email, self.password), fetch_one=True)
        return result is not None
    
    def save_user(self):
        """Guarda un nuevo usuario en la base de datos"""
        result = self._execute_query(self.ADD_USER, (self.username, self.email, self.password))
        return result is not None

    def update_user(self):
        """Actualiza los datos de un usuario en la base de datos"""
        result = self._execute_query(self.UPDATE_USER, (self.email, self.password, self.id))
        return result is not None

    def delete_user(self):
        """Elimina un usario en la base de datos"""
        result = self._execute_query(self.DELETE_USER, (self.id,))
        return result is not None