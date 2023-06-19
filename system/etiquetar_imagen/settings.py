import os
from configuracion.settings import DATABASE_DIR

METADATA_DIR = os.path.normpath(DATABASE_DIR + "metadata.csv")

MENSAJE_NUEVA_CLASIFICACION = 'nueva_imagen_clasificada'

MENSAJE_MODIFICACION = 'cambio_imagen_clasificada'