import csv
import json
from datetime import datetime
from menu_principal import settings
import os

def info_de_todos_los_perfiles():
    '''Retorna una lista de diccionarios con la informacion de la totalidad de usuarios guardados.
    Cada diccionario representa los datos de un usuario, y estos tienen la siguiente estructura:
        dicci = {
        alias: 'un alias',
        nombre: 'un nombre',
        edad: 'una edad',
        genero: 'un genero',
        imagen:'filename avatar'
        }'''
   
    with open(settings.PATH_PERFILES, 'r') as archivo_perfiles:
        todos_los_perfiles = json.load(archivo_perfiles)
        return todos_los_perfiles


def actualizar_perfiles(perfiles_actualizados):
    with open(settings.PATH_PERFILES,"w") as archivo_perfiles:
            json.dump(perfiles_actualizados, archivo_perfiles)


def cargar_varios_perfiles(cantidad_a_cargar, desde_posicion):
    '''Retorna una lista de diccionarios con la cantidad de usuarios solicitados.
    Cada diccionario representa los datos de un usuario, y estos tienen la siguiente estructura:
        dicci = {
        alias: 'un alias',
        nombre: 'un nombre',
        edad: 'una edad',
        genero: 'un genero',
        imagen:'filename avatar'
        }'''
    
    perfiles = info_de_todos_los_perfiles()
    hasta_posicion = desde_posicion + cantidad_a_cargar
    varios_perfiles = perfiles[desde_posicion:hasta_posicion]
    return varios_perfiles


def traer_ruta_imagen(perfil):
    '''Retorna el acceso de ruta del usuario que se envia por parametro'''
    
    ruta= os.path.join(settings.PERFILES_AVATARS,perfil['imagen'])
    return ruta


def cargar_alias_y_avatars(varios_perfiles):
    '''Retorna un diccionario donde sus claves son los nombres usuarios
    y sus valores la ruta donde se almacena la imagen de ese perfil de usuario:
        dicci = {
        un alias: 'una ruta a su avatar',
        otro alias: 'una ruta a su avatar',
        }'''

    alias = [
        perfil['alias']
        for perfil
        in varios_perfiles
        ]
    
    rutas_imagenes_avatars = list(map(traer_ruta_imagen, varios_perfiles))
    
    alias_y_avatars = {
        alias: ruta_a_su_avatar
        for alias, ruta_a_su_avatar
        in zip(alias, rutas_imagenes_avatars)
    }

    return alias_y_avatars


def calcular_cantidad_de_usuarios():
    '''Retorna la cantidad de perfiles almacenados por la aplicacion'''

    return len(info_de_todos_los_perfiles())


def guardar_usuario_logueado(datos_de_usuario):
    with open(settings.PATH_USUARIO, 'w') as archivo:
        json.dump(datos_de_usuario, archivo)


def traer_usuario_logueado():
    with open(settings.PATH_USUARIO, 'r') as archivo:
        datos = json.load(archivo)
        return datos


def buscar_datos_de_usuario(alias):
    todos_los_perfiles = info_de_todos_los_perfiles()
    usuario = dict(filter(lambda x: x[alias] == usuario, todos_los_perfiles))
    return usuario


def registrar_accion_de_usuario(usuario, accion):
    timestamp = datetime.timestamp(datetime.now())
    fecha_hora = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
    with open(settings.METADATA_DIR_LOGS, 'a', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([fecha_hora, usuario, accion])


def guardar_perfil_en_base_de_perfiles(genero, datos):
        """Esta funcion guarda los datos en el archivo json"""

        valor_imagen=datos["-ELEGIR ARCHIVO-"]
        nombre_archivo = os.path.basename(valor_imagen)
        dicci = {
            "alias":datos["-ALIAS-"],
            "nombre": datos["-NOMBRE-"],
            "edad":datos["-EDAD-"],
            "genero":  genero,
            "imagen": nombre_archivo
            }
        if os.path.isfile(settings.PATH_PERFILES):
            with open (settings.PATH_PERFILES,'r') as archivo:
                usuarios=json.load(archivo)
        usuarios.append(dicci) 
        with open(settings.PATH_PERFILES,'w') as archivo:
            json.dump(usuarios,archivo)


def cargar_rutas_directorio_imagenes():
    archivo_ubicaciones = open(settings.PATH_CONFIGURACION, 'r')
    ubicaciones = json.load(archivo_ubicaciones)
    archivo_ubicaciones.close()

    ruta_repositorio = ubicaciones['ubicaciones_usuario']['ubicacion_repositorio']
    
    if (not ruta_repositorio):
        ruta_repositorio = settings.FUENTE_IMAGENES_POR_DEFECTO
    
    ruta_collages = ubicaciones['ubicaciones_usuario']['ubicacion_collages']
    if (not ruta_collages):
        ruta_collages = settings.GUARDADO_COLLAGES_POR_DEFECTO

    ruta_memes = ubicaciones['ubicaciones_usuario']['ubicacion_memes']
    if (not ruta_memes):
        ruta_memes = settings.GUARDADO_MEMES_POR_DEFECTO
    
    return ruta_repositorio, ruta_collages, ruta_memes


def guardar_rutas_directorio_imagenes(ruta_repositorio, ruta_collages, ruta_memes):
    rutas_nuevas_usuario = {
        'ubicacion_repositorio': ruta_repositorio,
        'ubicacion_collages': ruta_collages,
        'ubicacion_memes': ruta_memes
    }

    with open(settings.PATH_CONFIGURACION, 'r+') as archivo_ubicaciones:
        ubicaciones = json.load(archivo_ubicaciones)
        ubicaciones['ubicaciones_usuario'] = rutas_nuevas_usuario
        archivo_ubicaciones.seek(0)
        json.dump(ubicaciones, archivo_ubicaciones)
        archivo_ubicaciones.truncate()


def restaurar_rutas_por_defecto():
    guardar_rutas_directorio_imagenes("", "", "")
    ruta_repositorio, ruta_collages, ruta_memes = cargar_rutas_directorio_imagenes()
    return ruta_repositorio, ruta_collages, ruta_memes