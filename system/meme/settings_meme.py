import os

from configuracion.settings import CONFIGURACION, DATABASE

PATH_IMAGENES = os.path.normpath(DATABASE + "/" + "coordenadas.json")

PATH_FUENTES = os.path.normpath(CONFIGURACION + "/" + "fuentes")

MENSAJE_MEME = "nuevo_meme"
