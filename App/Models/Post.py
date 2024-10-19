from Database.db_config import Database

class Post:
    # Consultas SQL
    SELECT_POST_SIMPLE = 'SELECT id, title FROM tbl_posts LIMIT 10 OFFSET 0'
    SELECT_POST_TITLE = 'SELECT id, title, content, created_at FROM tbl_posts WHERE title = %s'
    SELECT_POST_ID = 'SELECT id, title, content, created_at FROM tbl_posts WHERE id = %s'
    ADD_POST = 'INSERT INTO tbl_posts (title, content) VALUES (%s, %s)'
    UPDATE_POST = 'UPDATE tbl_posts SET title = %s, content = %s WHERE id = %s'
    DELETE_POST = 'DELETE FROM tbl_posts WHERE id = %s'

    def __init__(self, id=None, author=None, title=None, content=None, created_at = None, tag=None):
        self.id         = id
        self.author     = author
        self.title      = title
        self.content    = content
        self.created_at = created_at
        self.tag        = tag

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

    @classmethod
    def get_by_id(cls, post_id):
        """Obtiene un post por su ID"""
        result = cls._execute_query(cls.SELECT_POST_ID, (post_id,), fetch_one=True)
        if result:
            return cls(id=result[0], title=result[1], content=result[2], created_at=result[3])
        return None

    @classmethod
    def get_by_title(cls, post_title):
        """Obtiene un post por su título"""
        result = cls._execute_query(cls.SELECT_POST_TITLE, (post_title,), fetch_one=True)
        if result:
            return cls(id=result[0], title=result[1], content=result[2], tag=None)
        return None

    def save_post(self):
        """Guarda un nuevo post en la base de datos"""
        result = self._execute_query(self.ADD_POST, (self.title, self.content))
        return result is not None

    def update_post(self):
        """Actualiza el post en la base de datos"""
        result = self._execute_query(self.UPDATE_POST, (self.title, self.content, self.id))
        return result is not None

    def delete_post(self):
        """Elimina el post actual en la base de datos"""
        result = self._execute_query(self.DELETE_POST, (self.id,))
        return result is not None

    @classmethod
    def get_all_posts(cls):
        """Obtiene una lista de todos los posts con información básica"""
        results = cls._execute_query(cls.SELECT_POST_SIMPLE)
        posts = [cls(id=row[0], title=row[1]) for row in results] if results else []
        return posts
