import os


def archivo_mismo_nombre(ruta_nueva_imagen, nuevo_nombre):
    """Chequea si ya existe un archivo con el mismo nombre"""

    cumple = False
    if not os.path.exists(os.path.join(ruta_nueva_imagen, nuevo_nombre)):
        cumple = True
    return cumple
