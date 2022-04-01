from flask import Flask, render_template, request, redirect, url_for, flash
from models import registro_model

app = Flask(__name__)

app.secret_key = '#andSecretKey'

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/registro")
def registrarUsuario():
    return render_template("/usuarios/registro.html")

@app.post("/registro")
def registrarUsuarioPost():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    isValid = True

    if name == "":
        isValid = False
        flash("El Nombre es Obligatorio")

    if email == "":
        isValid = False
        flash("El correo es Obligatorio")

    if password == "":
        isValid = False
        flash("La Contraseña es Obligatorio")

    if isValid == False:
        return render_template("/usuarios/registro.html", name = name, email = email)

    registro_model.crearUsuario(name=name, email=email, password=password)

    return redirect(url_for("index"))

app.run(debug=True)