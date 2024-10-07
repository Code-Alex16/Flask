
# Importa la base de datos después de añadir la ruta
from App.Database.db_config import DataBase


# Código para probar la conexión
DB = DataBase()
connection_db = DB.GetConnexion()

sql = "SELECT * FROM tbl_posts"
cursor_ = connection_db.cursor()
cursor_.execute(sql)

post = cursor_.fetchall()
print(post)

DB.CloseConexion(connection=connection_db)