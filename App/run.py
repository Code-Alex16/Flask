from flask import Flask, render_template, request, redirect, url_for

from Database.db_config import Database

app: Flask = Flask(__name__)

db: Database = Database()

#Pagina principal
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post')
def pagina_principal():
    connexion = db.GetConnexion()
    posts = []

    if connexion:
        try:
            query = connexion.cursor()
            sql = "SELECT id, title FROM tbl_posts"
            query.execute(sql)

            posts = query.fetchall()

        except Exception as ex:
            print(f'Error al ejecutar la consulta: {ex}')

        finally:
            query.close()
            db.CloseConexion(connection=connexion)

    return render_template('pagina_principal.html', posts=posts)




@app.route('/post/<int:id>')
def show_post(id):
    connexion = db.GetConnexion()

    post = {}

    if connexion:
        try:
            query = connexion.cursor()
            sql = 'SELECT title, content, created_at FROM tbl_posts WHERE id = %s'
            value = (id,)
            query.execute(sql, value)

            result = query.fetchone()

            if result:
                post = {
                    'id': id,
                    'title': result[0],
                    'content': result[1],
                    'date_at': result[2].strftime("%Y-%m-%d %H:%M:%S")
                }

        except Exception as ex:
            print(f'Error al obtener la información: {ex}')

        finally:
            query.close()
            db.CloseConexion(connection=connexion)

    return render_template('posts.html', post=post)



@app.route('/submit_post', methods=["GET", "POST"])
def submit_post():
    
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


@app.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    connexion = db.GetConnexion()

    if request.method == 'POST':
        new_title = request.form.get('title')
        new_content = request.form.get('content')

        if connexion:
            try:
                query = connexion.cursor()
                sql = 'UPDATE tbl_posts SET title = %s, content = %s WHERE id = %s'
                values = (new_title, new_content, id)

                query.execute(sql, values)
                connexion.commit()

                return redirect(url_for('show_post', id=id))

            except Exception as ex:
                print(f'Error al modificar los datos: {ex}')

            finally:
                query.close()
                db.CloseConexion(connection=connexion)

    # Lógica para el GET: mostrar el formulario con los datos actuales
    data = {}

    if connexion:
        try:
            query = connexion.cursor()

            sql = 'SELECT id, title, content FROM tbl_posts WHERE id = %s'
            values = (id,)

            query.execute(sql, values)

            response = query.fetchone()

            if response:
                data = {
                    'id': response[0],
                    'title': response[1],
                    'content': response[2]
                }

        except Exception as ex:
            print(f'Error al obtener los datos: {ex}')

        finally:
            query.close()
            db.CloseConexion(connection=connexion)

    return render_template('posts_edit.html', post=data)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
