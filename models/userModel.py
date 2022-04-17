from werkzeug.security import check_password_hash, generate_password_hash

from config.database import db
from .entitites.user_entity import User

class UserModel():

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
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users(username, email, password) values (%s,%s,%s)",(
                user.username,
                user.email,
                generate_password_hash(user.password),
            ))
            cursor.close()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def emailUsed(self, email):
        try:
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
        except Exception as ex:
            raise Exception(ex)