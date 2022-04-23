import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

from models.entitites.user_entity import User
from controllers import fileController
from controllers import userController
from config.settings import SECRET_KEY
from send_email import emailCambiarPassword

app = Flask(__name__)

app.secret_key = SECRET_KEY
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return userController.getUserById(id)

@app.get("/")
def index():
    return redirect(url_for("login"))

@app.get("/home")
@login_required
def home():
    userId = current_user.id
    files = fileController.getFilesByUderId(userId)
    
    return render_template("/home/home.html", files=files)

@app.get("/subir-archivos")
@login_required
def subirArchivos():
    return render_template("/home/subirArchivos.html",action='subir')

@app.post("/subir-archivos")
@login_required
def subirArchivosPost():
    userId = current_user.id
    nombre = request.form.get("nombreArchivo")
    file = request.files['file']

    isValidForm= fileController.isValidFormUpload(nombre,file)
    if isValidForm == False:
        return render_template("/home/subirArchivos.html", nombre=nombre,action='subir')
    
    fileController.guardarFile(nombre,file,userId)
    return redirect(url_for("home"))

@app.get("/editar-archivo/<nombre>/<filename>")
@login_required
def editarArchivo(nombre,filename):
    return render_template("/home/subirArchivos.html",nombre=nombre,filename=filename,action='editar')

@app.post("/editar-archivo/<nombre>/<filename>")
@login_required
def editarArchivoPost(nombre,filename):

    userId = current_user.id
    nombre = request.form.get("nombreArchivo")
    file = request.files['file']

    isValidForm= fileController.isValidFormUpload(nombre,file)
    if isValidForm == False:
        return render_template("/home/subirArchivos.html", nombre=nombre,filename=filename,action='editar')

    fileController.guardarFile(nombre,file,userId,filenameEditar=filename)
    os.remove("./static/files/"+filename)
    return redirect(url_for("home"))

@app.get("/eliminar-archivo/<filename>")
def eliminarArchivo(filename):
    fileController.deleteFile(filename)
    os.remove("./static/files/"+filename)
    return redirect(url_for("home"))

@app.get("/registro")
def registro():
    return render_template("/auth/registro_login.html", pagina = 'Registro')

@app.post("/registro")
def registrarUsuario():
    user = User(0,request.form.get('username'),request.form.get('email'),request.form.get('password'),None,None)
    isValid = userController.isValidForm('registro',user)
    if isValid == False:
        return render_template(
            "/auth/registro_login.html",
            pagina = 'Registro',
            username = user.username,
            email = user.email
        )
    else:
        userController.crearUsuario(user)
        return redirect(url_for('login'))

@app.get("/login")
def login():
    return render_template("/auth/registro_login.html", pagina = 'Iniciar sesion')

@app.post("/login")
def loginPost():
    user = User(0,None,request.form.get('email'),request.form.get('password'),None,None)
    
    isValid = userController.isValidForm('login',user)
    if isValid == False:
        return render_template(
            "/auth/registro_login.html",
            pagina = 'Iniciar sesion',
            username = user.username,
            email = user.email
        )
    else:
        user_logeado = userController.login(user)
        if user_logeado != None:
            login_user(user_logeado)
            return redirect(url_for('home'))
        else:
            return render_template("/auth/registro_login.html", pagina = 'Iniciar sesion', email = user.email)

@app.get("/cambiar-contraseña")
def cambiarPassword():
    return render_template('/auth/emailCambiarPassword.html')

@app.post("/cambiar-contraseña")
def cambiarPasswordPost():
    user = User(0,'',request.form.get('email'),None,None,None)
    isValid = userController.isValidForm('email-cambiar-contraseña',user)
    if isValid == False:
        return render_template("/auth/emailCambiarPassword.html")
    else:
        row = userController.getUserByEmail(user.email)
        user.id = row[0]
        user.username = row[1]
        token = userController.generarToken(user.email)
        url = request.host_url+"cambiar-contraseña/"+token
        emailCambiarPassword(user.username, user.email, url)
        return redirect(url_for('login'))

@app.get("/cambiar-contraseña/<token>")
def cambiarPasswordToken(token):
    validToken = userController.validToken(token)
    if validToken != None:
        return render_template('/auth/cambiarPassword.html',token=token)
    else:
        return redirect(url_for('login'))

@app.post("/cambiar-contraseña/cambiar")
def cambiarPasswordTokenPost():
    token = request.form.get("token")
    isValidToken = userController.validToken(token)
    if isValidToken != None:
        password = request.form.get("password")
        user = User(0,None,None,password,None,None)
        isValidForm = userController.isValidForm("cambiar-contraseña",user)
        if isValidForm == False:
            return render_template("/auth/cambiarPassword.html")
        else:
            userController.cambiarContraseña(password,token)
            return redirect(url_for('login'))
    else:
        return "Token perdido o invalido"

@app.get("/confirm/<token>")
def confirm(token):
    token = userController.validToken(token)
    if id!= None:
        userController.confirmUser(token)
        # TODO: Template de cuenta validada
        return render_template('/auth/confirm.html')
    else:
        return "Token invalido: "+token

@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>404: Pagina no encontrada...<h1/>"

app.register_error_handler(401,status_401)
app.register_error_handler(404,status_404)
csrf.init_app(app)
app.run(debug=True)