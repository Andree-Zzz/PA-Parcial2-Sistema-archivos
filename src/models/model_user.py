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
    def isValidForm(self, pagina, user: User):
        if pagina == 'registro':
            isValid = True
            if user.username == "":
                isValid = False
                flash("El Nombre de usuario es requerido")

            if user.email == "":
                isValid = False
                flash("El Email es requerido")
            else:
                if self.emailUsed(user.email):
                    isValid = False
                    flash("El Email ya fue registrado")

            if user.password == "":
                isValid = False
                flash("La Contraseña es requerida")

            if len(user.password) < 8:
                isValid = False
                flash("La Contraseña debe tener minimo 8 caracteres")
            else:
                if any([crt.isdigit() for crt in user.password]):
                    if any([crt.isupper() for crt in user.password]):
                        if any([True if crt in punctuation else False for crt in user.password]):
                            isValid = True
                        else:
                            isValid = False
                            flash("La Contraseña debe tener: 1 caracter especial.")
                    else:
                        isValid = False
                        flash("La Contraseña debe tener: 1 una Mayuscula")
                else:
                    isValid = False
                    flash("La Contraseña debe tener: 1 numero.")
            
            return isValid
        else:
            if pagina == 'login':
                isValid = True
                if user.email == "":
                    isValid = False
                    flash("El Email es Obligatorio")

                if user.password == "":
                    isValid = False
                    flash("La Contraseña es Obligatoria")

                return isValid