from datetime import datetime
from flask import flash
from models import fileModel

def isValidFormUpload(nombre, file):
    isValidNombre = True
    isValidFile = True
    if nombre == '':
        isValidNombre = False
        flash("El Nombre del Archivo es requerido")
    if not file:
        isValidFile = False
        flash("El Archivo es requerido")
    
    return (isValidNombre and isValidFile)

def guardarFile(nombre,file):
    date = str(datetime.now().day)+str(datetime.now().month)+str(datetime.now().hour)+str(datetime.now().second)+str(datetime.now().microsecond)
    # date => 2242228856873
    
    # Guardar el file del formulario
    file.save('./static/files/'+date+file.filename)
    pathFile = '/static/files/'+date+file.filename
    # http://127.0.0.1:5000/static/images/Night-Raid.jpg => ruta de acceso publico a la imagen

    fileModel.guardarFile(nombre,pathFile)