from flask import Flask, render_template, request, redirect, session, flash
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
db = SQL("sqlite:///cuentas.db")

# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        #print(usuario)
        password = request.form.get("password")
        #print(password)
        confirma = request.form.get("confirmar")
        #print(confirma)
        if not usuario:
            return render_template('register.html')
        if not password:
            return render_template('register.html')
        if not confirma:
            return render_template('register.html')
        if password != confirma:
            flash("claves distintas")
            return render_template('register.html')
        consulta = db.execute("SELECT * FROM Users WHERE name = :usuario", usuario = usuario)
        if len (consulta) == 1:
            flash("Usuario ya existente")
            return render_template('register.html')
        hash = generate_password_hash(password)
        #print(hash)
        insert = db.execute("insert into Users (name, password) values(:usuario,:hash)", usuario = usuario, hash = hash)
        session["users_id"] = insert[0]["id"]
        return redirect("/")
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        usuario = request.form.get("usuario")
        #print(usuario)
        password = request.form.get("password")
        #print(password)
        if not usuario:
            return render_template('register.html')
        if not password:
            return render_template('register.html')
        existe = db.execute("SELECT * FROM Users WHERE name = :usuario", usuario = usuario)
        if len (existe) == 0 or not check_password_hash(existe[0]["password"], password):
            flash("Usuario mal ingresado o clave incorrecta")
            return render_template('login.html')
        #print(existe)
        session["users_id"] = existe[0]["id"]
        return redirect("/")
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)