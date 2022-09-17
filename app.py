from flask import Flask,render_template

app = Flask(__name__, static_folder='assets')
app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql://root@localhost/onlineqa'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/follow')
def follow():
    return render_template('follow.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/mine')
def mine():
    return render_template('mine.html')

@app.route('/detail')
def detail():
    return render_template('detail.html')