from flask import Flask, render_template
from DB.db_config import Database

app = Flask(__name__)

#Conexion a la clase DATABASE
#db = Database()

@app.route('/')
def Index():
    # Estableciendo una conexion
    '''
    conexion = db.GetConnexion()
    posts = []
    
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "SELECT title FROM tbl_posts"
            cursor.execute(sql)

            posts = cursor.fetchall()
        
        except Exception as ex:
            print(f'Error al ejecutar la consulta {ex}')
        
        finally:
            cursor.close()
            db.CloseConexion(connection=conexion)
    '''
    return render_template('index.html')

#nos dirigimos a un post especifico para leer su imformacion
@app.route('/<title>')
def page_post(title):
    #ejemplo ficticion
    post = {'title': title, 'content': 'Contenido del post aquí.'}
    return render_template('posts.html',post = post)

if __name__ == '__main__':
    app.run(debug=True,port=8000)