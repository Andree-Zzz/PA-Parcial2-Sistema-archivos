import re
from string import punctuation
from flask import flash
from models.userModel import UserModel
from models.entitites.user_entity import User

def login(user: User):
    row = UserModel.getUserByEmail(user.email)
    if row != None:
        if row[5] == 'false':
            flash("Usuario sin confirmar")
            return None
        else:
            user = UserModel.login(user)
            if user != None:
                if user.password:
                    return user
                else:
                    flash("Contraseña invalida.")
                    return None
            else:
                flash("Usuario no encontrado.")
                return user
    else:
        flash("Usuario no encontrado")
        return None

def getUserById(id):
    return UserModel.getUserById(id)

def crearUsuario(user: User):
    UserModel.crearUsuario(user)

def emailUsed(email):
    return UserModel.emailUsed(email)

def emailValido(email):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, email) is not None

def validateToken(token):
    return UserModel.validateToken(token)

def confirmUser(id):
    UserModel.confirmUser(id)

def isValidForm(pagina, user: User):
    isValidUsername = True
    isValidEmail = True
    isValidPassword = True
    if pagina == 'registro':
        
        if user.username == "":
            isValidUsername = False
            flash("El Nombre de usuario es requerido")

        if user.email == "":
            isValidEmail = False
            flash("El Email es requerido")
        else:
            if not emailValido(user.email):
                isValidEmail = False
                flash("Ingresa un Email Valido")
            else:
                if emailUsed(user.email):
                    isValidEmail = False
                    flash("El Email ya fue registrado")

        if user.password == "":
            isValidPassword = False
            flash("La Contraseña es requerida")

        if len(user.password) < 8:
            isValidPassword = False
            flash("La Contraseña debe tener minimo 8 caracteres")
        else:
            if any([caracter.isdigit() for caracter in user.password]):
                if any([caracter.isupper() for caracter in user.password]):
                    if any([True if caracter in punctuation else False for caracter in user.password]):
                        isValidPassword = True
                    else:
                        isValidPassword = False
                        flash("La Contraseña debe tener: 1 caracter especial.")
                else:
                    isValidPassword = False
                    flash("La Contraseña debe tener: 1 una Mayuscula")
            else:
                isValidPassword = False
                flash("La Contraseña debe tener: 1 numero.")
        
        return (isValidUsername and isValidEmail and isValidPassword)
    else:
        if pagina == 'login':
            if user.email == "":
                isValidEmail = False
                flash("El Email es Obligatorio")

            if user.password == "":
                isValidPassword = False
                flash("La Contraseña es Obligatoria")

        return (isValidUsername and isValidEmail and isValidPassword)