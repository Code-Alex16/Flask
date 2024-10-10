
from typing import Any

from flask import Flask, render_template, request, redirect, url_for

from Database.db_config import DataBase

app: Flask = Flask(__name__)

db: DataBase = DataBase()

#Pagina principal
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post')
def pagina_principal():

    global query

    connexion = db.GetConnexion()
    posts = []

    if connexion:
        try:
            query = connexion.cursor()
            sql = "SELECT title FROM tbl_posts"
            query.execute(sql)

            posts = query.fetchall()

        except Exception as ex:
            print(f'Error al ejecutar la consulta {ex}')

        finally:
            query.close()
            db.CloseConexion(connection=connexion)

    return render_template('pagina_principal.html', posts=posts)



@app.route('/post/<title>')
def show_post(title):

    global query
    connexion = db.GetConnexion()

    post = {}

    if connexion:
        try:
            query = connexion.cursor()
            sql = 'SELECT title, content, created_at FROM tbl_posts WHERE title = %s'
            value = (title,)
            query.execute(sql, value)

            result = query.fetchone()

            if result:
                post = {
                    'title': result[0],
                    'content': result[1],
                    'date_at': result[2].strftime("%Y-%m-%d %H:%M:%S")
                }

        except Exception as ex:
            print(f'Error al obtener la informacion {ex}')

        finally:
            query.close()
            db.CloseConexion(connection=connexion)

    return render_template('posts.html', post=post)


@app.route('/submit_post', methods=["GET", "POST"])
def submit_post():
    global cursor, title
    connexion = db.GetConnexion()

    if request.method == "POST":

        if connexion:
            try:
                cursor = connexion.cursor()

                title: str | None = request.form.get('title')
                content = request.form.get('content')

                sql = "INSERT INTO tbl_posts (title, content) VALUES (%s,%s)"
                values = (title, content)

                cursor.execute(sql, values)
                connexion.commit()

            except Exception as ex:
                print(f'Error al ingresar los datos {ex}')

            finally:
                cursor.close()
                db.CloseConexion(connection=connexion)

        return redirect(url_for('show_post', title=title))

    return render_template('submit_post.html')


@app.route('/post/edit/<title>', methods = ['GET'])
def edit_post(title):

    global query, data
    connexion = db.GetConnexion()

    if request.method == 'GET':
        if connexion:
            try:
                query = connexion.cursor()
                sql = "SELECT id, title, content FROM tbl_posts WHERE title = %s"
                values = (title,)

                query.execute(sql, values)

                response = query.fetchone()

                data: dict[str, Any] = {
                    'id' : response[0],
                    'title' : response[1],
                    'content' : response[2]
                }

                #obtener informacion editada
                title: str | None = request.form.get('title')
                content = request.form.get('content')

                sql = "UPDATE tbl_posts SET VALUES(title = %s, content = %s) WHERE id_post = $s"
                values = (title, content, data.get('id'))

                query.execute(sql, values)
                connexion.commit()

            except Exception as ex:
                print(f'Error al obtener la informacion {ex}')

            finally:
                query.close()
                db.CloseConexion(connection=connexion)

        return redirect(url_for('show_post', title = title))

    return render_template('posts_edit.html', post = data)



if __name__ == '__main__':
    app.run(debug=True, port=8000)
