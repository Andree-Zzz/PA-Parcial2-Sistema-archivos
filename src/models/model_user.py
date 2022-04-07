import re
from string import punctuation
from flask import flash
from werkzeug.security import check_password_hash, generate_password_hash

from config.database import db
from .entitites.user_entity import User

class ModelUser():

    @classmethod
    def login(self, user: User):
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (
                user.email,
            ))
            row = cursor.fetchone()
            cursor.close()
            if row != None:
                user = User(row[0],row[1], row[2],check_password_hash(row[3], user.password))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getUserById(self, id):
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE id = %s", (
                id,
            ))
            row = cursor.fetchone()
            cursor.close()
            if row != None:
                return  User(row[0],row[1],row[2],None)  
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def crearUsuario(self, user: User):
        cursor = db.cursor()
        cursor.execute("INSERT INTO users(username, email, password) values (%s,%s,%s)",(
            user.username,
            user.email,
            generate_password_hash(user.password),
        ))
        cursor.close()
    
    @classmethod
    def emailUsed(self, email):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (
            email,
        ))
        row = cursor.fetchone()
        cursor.close()
        if row != None:
            return True
        else:
            return False
    
    @classmethod
    def emailValido(self, email):
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        return re.match(expresion_regular, email) is not None

    @classmethod
    def isValidForm(self, pagina, user: User):
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
                if not self.emailValido(user.email):
                    isValidEmail = False
                    flash("Ingresa un Email Valido")
                else:
                    if self.emailUsed(user.email):
                        isValidEmail = False
                        flash("El Email ya fue registrado")

            if user.password == "":
                isValidPassword = False
                flash("La Contraseña es requerida")

            if len(user.password) < 8:
                isValidPassword = False
                flash("La Contraseña debe tener minimo 8 caracteres")
            else:
                if any([crt.isdigit() for crt in user.password]):
                    if any([crt.isupper() for crt in user.password]):
                        if any([True if crt in punctuation else False for crt in user.password]):
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