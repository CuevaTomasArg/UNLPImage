import csv
import json
import os
from datetime import datetime

from configuracion import settings
from compartidos import advertencias_errores as adv


def info_de_todos_los_perfiles():
    '''
    Devuelve una lista de diccionarios con la informacion de la totalidad
    de usuarios guardados, donde cada diccionario representa los datos
    de un usuario

    Retorno:
    todos_los_perfiles = [
        {
            alias (string): un alias,
            nombre (string): un nombre,
            edad (int): una edad,
            genero (string): un genero,
            imagen (string): nombre del archivo de imagen avatar del perfil
        }
    ]

    El archivo desde donde se obtiene la informacion de usuarios debe tener
    esa misma estructura en formato json
    '''
    todos_los_perfiles = []
    try:
        with open(settings.PATH_PERFILES, 'r') as archivo_perfiles:
            todos_los_perfiles = json.load(archivo_perfiles)
    except FileNotFoundError:
        adv.advertencia_error_no_encontrado(settings.PATH_PERFILES)
    except PermissionError:
        adv.advertencia_error_lectura(settings.PATH_PERFILES)
    return todos_los_perfiles


def traer_ruta_imagen(perfil):
    '''
    Devuelve la ubicacion donde está almacenada la imagen elegida como avatar por
    el usuario que se solicita

    Parametros:
    perfil = [
        {
            alias (string): un alias,
            nombre (string): un nombre,
            edad (int): una edad,
            genero (string): un genero,
            imagen (string): nombre del archivo de imagen avatar del perfil
        }
    ]

    Retorno:
    ruta: la ruta de acceso a la imagen del avatar del usuario
    '''
    ruta = os.path.join(settings.PERFILES_AVATARS, perfil['imagen'])
    return ruta


def generar_usuario_error():
    ''' '''
    usuario_error = {
        'alias': 'ERROR',
        'nombre': 'ERROR',
        'edad': 1,
        'genero': 'ERROR',
        'imagen': settings.PATH_AVATAR_LOGUEADO_ERROR,
    }
    return usuario_error


def guardar_usuario_logueado(datos_de_usuario):
    '''
    Almacena en un archivo json el usuario que se loguea en la aplicación,
    que recibe a través de parametro

    Parametro:
    perfil =  {
        alias (string): un alias,
        nombre (string): un nombre,
        edad (int): una edad,
        genero (string): un genero,
        imagen (string): nombre del archivo de imagen avatar del perfil
    }
    '''
    try:
        with open(settings.PATH_USUARIO_LOGUEADO, 'w') as archivo:
            json.dump(datos_de_usuario, archivo)
    except PermissionError:
        adv.advertencia_error_escritura(settings.PATH_USUARIO_LOGUEADO)


def traer_usuario_logueado():
    '''
    Devuelve la información del usuario que se loguea en la aplicación

    Retorna:
    datos =  {
        alias (string): un alias,
        nombre (string): un nombre,
        edad (int): una edad,
        genero (string): un genero,
        imagen (string): nombre del archivo de imagen avatar del perfil
    }
    '''
    try:
        with open(settings.PATH_USUARIO_LOGUEADO, 'r') as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        adv.advertencia_error_usuario_logueado()
        datos = generar_usuario_error()
    except PermissionError:
        adv.advertencia_error_lectura(settings.PATH_USUARIO_LOGUEADO)
        datos = generar_usuario_error()
    return datos


def generar_archivo_de_logs():
    """
    Genera un archivo de logs con las columnas 'fecha', 'usuario', 'accion',
    'valor' y 'texto', el cual sirve para registrar acciones del usuario.
    """
    columnas = ['fecha', 'usuario', 'accion', 'valor', 'texto']    
    try:
        with open(settings.METADATA_DIR_LOGS, 'w', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(columnas)
    except PermissionError:
        adv.advertencia_error_escritura(settings.METADATA_DIR_LOGS)


def registrar_accion_de_usuario(usuario, accion, valor=None, texto=None):
    '''
    Registra una acción realizada por el usuario en un archivo de registro de logs.

    Parametros:
    usuario (dict): Un diccionario que contiene información del usuario que realizó
    la acción
        usuario =  {
            alias (string): un alias,
            nombre (string): un nombre,
            edad (int): una edad,
            genero (string): un genero,
            imagen (string):'filename avatar

    accion (string): una descripción de la acción realizada por el usuario

    valor (string o lista de strings): valor(lista de strings) es una lista de nombres
    de archivos para un collage; valor(string) es el nombre de un archivo de un meme

    texto (string o lista de strings): texto(string) es el titulo
    de un collage agregado; texto(lista de strings) son textos agregados a un meme
    '''
    timestamp = datetime.timestamp(datetime.now())
    fecha_hora = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
    if valor and type(valor) is list:
        valor = ';'.join(valor)
    if texto and type(texto) is list:
        texto = ';'.join(texto)
    try:
        with open(settings.METADATA_DIR_LOGS, 'a', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([fecha_hora, usuario, accion, valor, texto])
    except FileNotFoundError:
        adv.advertencia_error_no_encontrado(settings.METADATA_DIR_LOGS)
        generar_archivo_de_logs()
    except PermissionError:
        adv.advertencia_error_lectura(settings.METADATA_DIR_LOGS)


def generar_archivo_rutas_directorio_imagenes(rutas_nuevas_usuario):
    """
    Genera un archivo de configuración para las rutas de directorios
    de imágenes repositorio, de guardado de memes y guardado de collage
    utilizados por el usuario
    
    Parámetros:
    - rutas_nuevas_usuario (tupla): las rutas de los directorios
    para el repositorio de imágenes, collages y memes, en ese orden
    """
    try:
        ubicaciones = {'ubicaciones_usuario': rutas_nuevas_usuario}
        with open(settings.CONFIGURACION_GUARDADO_IMAGENES, 'w') as archivo_ubicaciones:
            json.dump(ubicaciones, archivo_ubicaciones)
    except PermissionError:
        adv.advertencia_error_escritura(settings.CONFIGURACION_GUARDADO_IMAGENES)


def cargar_rutas_directorio_imagenes():
    '''
    Devuelve las rutas de los directorios de imágenes a partir de la información
    guardada en un archivo json.
    Si las ubicaciones se encuentran vacias, o si las rutas guardadas en el archivo
    no existen, devuelve las rutas por defecto de la aplicacion

    Retorna:
        ruta_repositorio, ruta_collages, ruta_memes (strings): una tupla con las rutas
        de los directorios para el repositorio de imágenes, collages y memes,
        en ese orden.
    '''
    ruta_repositorio = ''
    ruta_collages = ''
    ruta_memes = ''
    try:
        with open(settings.CONFIGURACION_GUARDADO_IMAGENES, 'r') as archivo_ubicaciones:
            ubicaciones = json.load(archivo_ubicaciones)
        ruta_repositorio = ubicaciones['ubicaciones_usuario']['ubicacion_repositorio']
        ruta_collages = ubicaciones['ubicaciones_usuario']['ubicacion_collages']
        ruta_memes = ubicaciones['ubicaciones_usuario']['ubicacion_memes']
    except FileNotFoundError:
        adv.advertencia_error_no_encontrado(settings.CONFIGURACION_GUARDADO_IMAGENES)
    except PermissionError:
        adv.advertencia_error_escritura(settings.CONFIGURACION_GUARDADO_IMAGENES)
    if not ruta_repositorio or not os.path.isdir(ruta_repositorio):
        ruta_repositorio = settings.FUENTE_IMAGENES_POR_DEFECTO
    if not ruta_collages or not os.path.isdir(ruta_collages):
        ruta_collages = settings.GUARDADO_COLLAGES_POR_DEFECTO
    if not ruta_memes or not os.path.isdir(ruta_memes):
        ruta_memes = settings.GUARDADO_MEMES_POR_DEFECTO
    return ruta_repositorio, ruta_collages, ruta_memes
