from datetime import datetime
import os
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

def guardarFile(nombre, file, userId, filenameEditar = ''):
    date = str(datetime.now().microsecond)+str(datetime.now().second)+str(datetime.now().hour)+str(datetime.now().day)+str(datetime.now().month)
    # Guardar el file del formulario
    filename = date+file.filename
    pathFile = '/static/files/'+filename
    file.save('.'+pathFile)
    type = getTypeFileByFilename(file.filename)
    megas = (os.path.getsize('.'+pathFile))/1048576

    fileModel.guardarFile(filenameEditar,nombre, filename, pathFile, type, megas, userId)

def getFilesByUderId(userId):
    return fileModel.getFilesByUderId(userId)

def getFileByFilename(filename: str):
    return fileModel.getFileByFilename(filename)

def deleteFile(filename: str):
    fileModel.deleteFile(filename)

def getTypeFileByFilename(filename: str):
    tipo = filename.split('.')
    return tipo[tipo.__len__()-1]

def setPreviewFileByFilename(filename: str):
    tipo = filename.split('.')
    return tipo[tipo.__len__()-1]