from config.database import db

def guardarFile(nombre, pathFile):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO files(nombre,pathFile) VALUES(%s,%s)", (
                nombre,
                pathFile,
            ))
        except Exception as ex:
            raise Exception(ex)