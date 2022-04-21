import random
import string
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash

from config.database import db
from send_email import emailBienvenida
from .entitites.user_entity import User

class UserModel():

    @classmethod
    def getUserByEmail(self, email):
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (
                email,
            ))
            row = cursor.fetchone()
            cursor.close()
            if row != None:
                return row
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def login(self, user: User):
        try:
            row = self.getUserByEmail(user.email)
            if row != None:
                user = User(
                    id = row[0],
                    username = row[1],
                    email = row[2],
                    password = check_password_hash(row[3],user.password),
                    token = row[4],
                    confirmed= row[5]
                )
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def validateToken(self, token):
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE token = %s", (
                token,
            ))
            row = cursor.fetchone()
            cursor.close()
            if row != None:
                return row[0]
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def confirmUser(self,id):
        try:
            cursor = db.cursor()
            cursor.execute("UPDATE users SET confirmed='true' WHERE  id=%s", (
                id,
            ))
            cursor.close()
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
                user = User(
                    id = row[0],
                    username = row[1],
                    email = row[2],
                    password = None,
                    token = row[4],
                    confirmed= row[5]
                )
                return  user 
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def crearUsuario(self, user: User):
        try:
            token = (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)))
            cursor = db.cursor()
            cursor.execute("INSERT INTO users(username, email, password, token) values (%s,%s,%s,%s)",(
                user.username,
                user.email,
                generate_password_hash(user.password),
                token,
            ))
            url = request.host_url+"confirm/"+token
            cursor.close()
            emailBienvenida(user.username, user.email,url)
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