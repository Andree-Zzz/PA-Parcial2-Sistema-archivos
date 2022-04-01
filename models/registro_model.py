from config.database import db

def crearUsuario(name, email, password):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users(name, email, password) values (%s,%s,%s)",(
        name,
        email,
        password,
    ))
    cursor.close()
