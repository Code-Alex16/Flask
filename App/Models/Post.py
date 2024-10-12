from Database.db_config import Database

'''
Class Post:
    - get_by_id
    - get_by_title
    - delete_by_title
    - update_post
    - save_post
'''
class Post:

    #Consultas Habituales
    SELECT_POST_TITLE = 'SELECT id, title FROM tbl_post LIMIT 10 OFFSET 0'
    SELECT_POST = 'SELECT id, title, content, date_at FROM tbl_post WHERE title = %s'
    ADD_POST = 'INSERT INTO tbl_post (author, title, content) VALUES (%s,%s,%s)'
    UPDATE_POST = 'UPDATE tbl_post SET title = %s, content = %s WHERE id = %s'
    DELETE_POST = 'DELETE FROM tbl_post WHERE title = %s'

    def __init__(self, id = None, author=None, title=None, content=None, tag=None):
        self.id       = id
        self.author   = author
        self.title    = title
        self.content  = content
        self.tag      = tag

    #obtener las constantes de clase
    @classmethod
    def get_by_id(cls):
        pass

    @classmethod
    def get_by_title(cls):
        pass

    @classmethod
    def save_post(cls):
        pass

    @classmethod
    def update_post(cls):
        pass

    @classmethod
    def delete_post(cls):
        pass