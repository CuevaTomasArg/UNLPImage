import json

from system.meme.settings_meme import PATH_IMAGENES


def obtener_text_boxes(nombre_imagen_png):
    """Esta función retorna las coordenadas donde va a insertarse el texto"""

    with open(PATH_IMAGENES, "r") as archivo:
        archivo_texto = json.load(archivo)
        for item in archivo_texto:
            if item["image"] == nombre_imagen_png:
                return item["text_boxes"]

