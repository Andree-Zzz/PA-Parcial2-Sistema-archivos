from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

from models.entitites.user_entity import User
from models.model_user import ModelUser
from send_email import emailBienvenida, sendEmail
from config.settings import SECRET_KEY

app = Flask(__name__)

app.secret_key = SECRET_KEY
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.getUserById(id)

@app.get("/")
def index():
    return redirect(url_for("login"))

@app.get("/home")
@login_required
def home():
    return render_template("home.html")

@app.get("/registro")
def registro():
    return render_template("/auth/registro_login.html", pagina = 'Registro')

@app.post("/registro")
def registrarUsuario():
    user = User(
        0,
        request.form.get('username'),
        request.form.get('email'),
        request.form.get('password')
    )
    isValid = ModelUser.isValidForm('registro',user)
    if isValid == False:
        return render_template(
            "/auth/registro_login.html",
            pagina = 'Registro',
            username = user.username,
            email = user.email
        )
    else:
        ModelUser.crearUsuario(user)
        emailBienvenida(user.email)
        return redirect(url_for('login'))

@app.get("/login")
def login():
    return render_template("/auth/registro_login.html", pagina = 'Iniciar sesion')

@app.post("/login")
def loginPost():
    user = User(0,None,request.form.get('email'),request.form.get('password'))
    
    isValid = ModelUser.isValidForm('login',user)
    if isValid == False:
        return render_template(
            "/auth/registro_login.html",
            pagina = 'Iniciar sesion',
            username = user.username,
            email = user.email
        )
    else:
        user_logeado = ModelUser.login(user)
        if user_logeado != None:
            if user_logeado.password:
                login_user(user_logeado)
                return redirect(url_for('home'))
            else:
                flash("Contraseña invalida.")
                return render_template("/auth/registro_login.html", pagina = 'Iniciar sesion', email = user.email)
        else:
            flash("Usuario no encontrado.")
            return render_template("/auth/registro_login.html", pagina = 'Iniciar sesion', email = user.email)

@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>404: Pagina no encontrada :/<h1/>"

app.register_error_handler(401,status_401)
app.register_error_handler(404,status_404)
csrf.init_app(app)
app.run(debug=True)