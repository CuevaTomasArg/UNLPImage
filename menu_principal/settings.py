import os
# La idea de este archivo es que se guarden las rutas acá de la base de datos acá
PATH = os.getcwd()
DATABASE = os.path.normpath(PATH + "/" +"DB")

DATABASE_DIR = os.path.abspath(os.path.join(os.path.expanduser("~"), DATABASE)) + os.sep
METADATA_DIR = DATABASE_DIR + "metadata.csv"

USUARIO_LOGUEADO = None

#Cambiar esto por la ruta del repositorio real de imageness
REPOSITORIO = os.path.normpath(PATH + "/" +"Repositorio")

