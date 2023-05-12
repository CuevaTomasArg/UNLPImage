import os


PATH = os.getcwd()
PATH_INDEX = os.path.normpath(os.getcwd() + "/" +"index.py")
DATABASE = os.path.normpath(os.getcwd() + "/" + "DB")
MULTIMEDIA = os.path.normpath(os.getcwd() + "/" +"multimedia")

DATABASE_DIR = os.path.abspath(os.path.join(os.path.expanduser("~"), DATABASE)) + os.sep
METADATA_DIR = DATABASE_DIR + "metadata.csv"

METADATA_DIR_LOGS = DATABASE_DIR + "logs_sistema.csv"


LOGOS_APLICACION = os.path.normpath(MULTIMEDIA + "/" +"imagenes_logos")
LOGO_UNLPIMAGE = os.path.normpath(LOGOS_APLICACION + "/" +"unlpimage_logo.png")
LOGO_UNLP = os.path.normpath(LOGOS_APLICACION + "/" +"unlp_logo.png")
LOGO_INFORMATICA = os.path.normpath(LOGOS_APLICACION + "/" +"informatica_logo.png")

PATH_PERFILES = os.path.normpath(DATABASE + "/" + "perfiles_usuarios.json")
PERFILES_AVATARS = os.path.normpath(MULTIMEDIA + "/" +"imagenes_perfil")
AVATAR_PREDEFINIDO = os.path.normpath(PERFILES_AVATARS + "/" + "perfil3.png")

PATH_CONFIGURACION = os.path.normpath(os.getcwd()+ "/"+ "DB" + "/" + "ubicaciones_imagenes.json")

FUENTE_IMAGENES_POR_DEFECTO = os.path.normpath(os.getcwd()+ "/" + "multimedia" + "/" + "imagenes")
GUARDADO_COLLAGES_POR_DEFECTO = os.path.normpath(os.getcwd()+ "/" + "multimedia" + "/" + "collages")
GUARDADO_MEMES_POR_DEFECTO = os.path.normpath(os.getcwd()+ "/" + "multimedia" + "/" + "memes")

PATH_USUARIO = os.path.normpath(DATABASE + "/" +"usuario_logueado.json")