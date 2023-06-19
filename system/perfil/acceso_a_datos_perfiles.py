import json
import os

from compartidos.acceso_a_datos import info_de_todos_los_perfiles
from configuracion.settings import PATH_PERFILES


def actualizar_perfiles(perfiles_actualizados):
    '''
    Actualiza los datos de todos los usuarios en el archivo json que almacena
    los perfiles.
    Recibe una lista de diccionarios con la informacion actualizada de los perfiles.
    Cada diccionario representa los datos de un usuario, y estos tienen la siguiente
    estructura:

    Parametros:
    perfiles_actualizados = [
        {
            alias (string): un alias,
            nombre (string): un nombre,
            edad (int): una edad,
            genero (string): un genero,
            imagen (string): nombre del archivo de imagen avatar del perfil
        }
    ]
    '''
    with open(PATH_PERFILES, "w") as archivo_perfiles:
        json.dump(perfiles_actualizados, archivo_perfiles)


def guardar_perfil_en_base_de_perfiles(genero, datos):
    '''
    Guarda los datos de un perfil en el archivo json que almacena los perfiles
    de usuarios

    Parametros:
    genero (string):  representa el género elegido para ese perfil

    datos: diccionario con los datos del perfil; incluye:
    "-ALIAS-" (string): un alias,
    "-NOMBRE-" (string): un nombre,
    "-EDAD-" (string): una edad,
    "-ELEGIR ARCHIVO-" (string): ruta del archivo de imagen del perfil
    '''

    valor_imagen = datos["-ELEGIR ARCHIVO-"]
    nombre_archivo = os.path.basename(valor_imagen)
    dicci = {
        "alias": datos["-ALIAS-"],
        "nombre": datos["-NOMBRE-"],
        "edad": datos["-EDAD-"],
        "genero": genero,
        "imagen": nombre_archivo,
    }
    if os.path.isfile(PATH_PERFILES):
        usuarios = info_de_todos_los_perfiles()
    usuarios.append(dicci)
    actualizar_perfiles(usuarios)
