from config.database import db

def guardarFile(filenameEditar, nombre, filename, pathFile, type, megas, userId):
    try:
        cursor = db.cursor()
        if filenameEditar == '':
            cursor.execute("INSERT INTO files(nombre,filename,pathFile,type,megas,user_id) VALUES(%s,%s,%s,%s,%s,%s)", (
                nombre,
                filename,
                pathFile,
                type,
                megas,
                userId,
            ))

        else:
            cursor.execute("UPDATE files SET nombre=%s, filename=%s, pathFile=%s, type=%s, megas=%s WHERE filename=%s", (
                nombre,
                filename,
                pathFile,
                type,
                megas,
                filenameEditar,
            ))

        cursor.close()
    except Exception as ex:
        raise Exception(ex)
    
def getFilesByUderId(userId):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM files WHERE user_id = %s", (
            userId,
        ))
        files = cursor.fetchall()
        cursor.close()
        return files
    except Exception as ex:
        raise Exception(ex)

def deleteFile(filename):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM files WHERE filename = %s", (
            filename,
        ))
    except Exception as ex:
        raise Exception(ex)