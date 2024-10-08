from flask import Flask, render_template, request, redirect, url_for
from Database.db_config import DataBase

app = Flask(__name__)

#Conexion a la clase DATABASE
db = DataBase()

@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/post')
def Pagina_principal():
    # Estableciendo una conexion
    
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

    return render_template('pagina_principal.html', posts = posts)

#nos dirigimos a un post especifico para leer su imformacion
@app.route('/post/<title>')
def show_post(title):
    conexion = db.GetConnexion()

    post = {}

    if conexion:
        try:
            cursor = conexion.cursor()
            sql = 'SELECT title, content, created_at FROM tbl_posts WHERE title = %s'
            value = (title,)
            cursor.execute(sql,value)

            result = cursor.fetchone()

            if result:
                post = {
                    'title' : result[0],
                    'content' : result[1],
                    'date_at' : result[2].strftime("%Y-%m-%d %H:%M:%S")
                }
        
        except Exception as ex:
            print(f'Error al obtener la informacion {ex}')
        
        finally:
            cursor.close()
            db.CloseConexion(connection = conexion)

    return render_template('posts.html',post = post)

@app.route('/submit_post', methods = ["GET","POST"])
def submit_post():

    conexion = db.GetConnexion()

    if request.method == "POST":
            
        if conexion:
            try:
                cursor = conexion.cursor()

                new_title = request.form.get('title')
                new_content = request.form.get('content')

                sql = "INSERT INTO tbl_posts (title, content) VALUES (%s,%s)"
                values = (new_title, new_content)

                cursor.execute(sql,values)
                conexion.commit()

            except Exception as ex:
                print(f'Error al ingresar los datos {ex}')

            finally:
                cursor.close()
                db.CloseConexion(connection=conexion)


        return redirect(url_for('show_post', title = new_title))
    
    return render_template('submit_post.html')


@app.route('/post/edit/<title>')
def edit_post():
    #TODO -> completar la edicion de los post   
    pass

if __name__ == '__main__':
    app.run(debug=True,port=8000)