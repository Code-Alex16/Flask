from flask import Flask, render_template

app = Flask(__name__)

#Esto sera de prueba pra el paso de datos a los html, despues sera cambiado por una base de datos
POSTS = [
    {
        'id' : 1,
        'title' : 'Posting 1',
        'update' : '16/09/2004',
        'body' : 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum repellat nesciunt ullam provident aperiam officiis iste itaque saepe esse, ea ex ab eos officia ducimus eaque temporibus labore reiciendis magnam!'
    },
    {
        'id' : 2,
        'title' : 'Posting 2',
        'update' : '16/09/2005',
        'body' : 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum repellat nesciunt ullam provident aperiam officiis iste itaque saepe esse, ea ex ab eos officia ducimus eaque temporibus labore reiciendis magnam!'
    },
    {        
        'id' : 3,
        'title' : 'Posting 3',
        'update' : '16/09/2006',
        'body' : 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum repellat nesciunt ullam provident aperiam officiis iste itaque saepe esse, ea ex ab eos officia ducimus eaque temporibus labore reiciendis magnam!'
    }
]

@app.route('/')
def Index():
    return render_template('base.html', Posts = POSTS)


if __name__ == '__main__':
    app.run(debug=True,port=8000)