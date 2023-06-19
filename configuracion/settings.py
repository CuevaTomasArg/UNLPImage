import os

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATH_INDEX = os.path.normpath(PATH + "/" + "index.py")

DATABASE = os.path.normpath(PATH + "/" + "DB")

IMAGENES = os.path.normpath(PATH + "/" + "imagenes")

AVATARS = os.path.normpath(IMAGENES + "/" + "avatars")

DEL_SISTEMA = os.path.normpath(PATH + "/" + "del_sistema")

ARCHIVO_PERFILES_USUARIOS = "perfiles_usuarios.json"

ARCHIVO_USUARIO_LOGUEADO = "usuario_logueado.json"

ARCHIVO_GUARDADO_IMAGENES = "ubicaciones_imagenes.json"

ARCHIVO_LOGS_SISTEMA = "logs_sistema.csv"

AVATAR_PARA_ERROR_USUARIO = "error.png"

PATH_PERFILES = os.path.normpath(DATABASE + "/" + ARCHIVO_PERFILES_USUARIOS)

PATH_USUARIO_LOGUEADO = os.path.normpath(DATABASE + "/" + ARCHIVO_USUARIO_LOGUEADO)

PATH_AVATAR_LOGUEADO_ERROR = os.path.normpath(
    DEL_SISTEMA + "/" + AVATAR_PARA_ERROR_USUARIO
)

CONFIGURACION_GUARDADO_IMAGENES = os.path.normpath(
    DATABASE + "/" + ARCHIVO_GUARDADO_IMAGENES
)

DATABASE_DIR = os.path.abspath(os.path.join(os.path.expanduser("~"), DATABASE)) + os.sep

METADATA_DIR_LOGS = os.path.normpath(DATABASE_DIR + "/" + ARCHIVO_LOGS_SISTEMA)

FUENTE_IMAGENES_POR_DEFECTO = os.path.normpath(IMAGENES + "/" + "repositorio")

GUARDADO_COLLAGES_POR_DEFECTO = os.path.normpath(IMAGENES + "/" + "collages")

GUARDADO_MEMES_POR_DEFECTO = os.path.normpath(IMAGENES + "/" + "memes")

PERFILES_AVATARS = os.path.normpath(IMAGENES + "/" + "avatars")

CONFIGURACION = os.path.normpath(PATH + "/" + "configuracion")
