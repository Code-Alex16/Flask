from flask import Flask, render_template, request, redirect, url_for
from flask_caching import Cache
from Models.Post import Post
from Models.User import User
from Database.db_config import Database

#inicializacion de la App con flask
app: Flask = Flask(__name__)

#Manejo de cache de memoria, optimizacion de recursos
#app.config['CACHE_TYPE'] = 'SimpleCache'
#tiempo en segundos de timepor fuera - 300 (5 minutos)
#app.config['CACHE_DEFAULT_TIMEOUT'] = 300

#cache = Cache(app)


@app.route('/')
def index():
    return render_template('index.html')

"""
Usuarios - Authores
"""
@app.route('/Login', methods = ["POST"])
def Login_user():
    if request.method == 'POST':
        user_email = request.form.get('user_email')
        password = request.form.get('user_password')
    return render_template("Login.html")

@app.route('/Regristro', methods = ["POST"])
def Registre_user():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email_user = request.form.get('user_email')
        password = request.form.get('user_password')

        new_user = User(username=user_name, email=email_user,password=password)

        if new_user.save_user():
            return redirect(url_for('Login_user'))
        else:
            print('Error al registrar usuario')
            
    return render_template('Register.html')

""""
Post
"""
@app.route('/post')
def pagina_principal():
    """Lista de Publicaciones"""
    posts = Post.get_all_posts()
    return render_template('pagina_principal.html', posts=posts)


@app.route('/post/<int:id>')
def show_post(id):
    """Ver publicacion especifica"""

    post = Post.get_by_id(id)

    if not post:
        return 'Publicacion no encontrada', 404
    
    return render_template('posts.html', post=post)



@app.route('/submit_post', methods=["GET", "POST"])
def submit_post():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')

        new_post = Post(title=title, content=content)
        if new_post.save_post():
            return redirect(url_for('pagina_principal'))
        else:
            print('Error al guardar el post.')

    return render_template('submit_post.html')



@app.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    """Editar una publicacion existente"""
    
    post = Post.get_by_id(id)

    if not post:
        return 'Publicacion no existente', 404

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.update_post()
        return redirect(url_for('show_post', id = post.id))

    #para el metodo get usamos los datos obtendidos del objeto
    return render_template('posts_edit.html', post=post)

@app.delete('')
def delete_post(id):
    """Eliminar una publicacion existente"""
    Post.delete_post(id)
    return redirect(url_for('pagina_principal'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
