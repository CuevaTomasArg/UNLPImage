import json

from compartidos.acceso_a_datos import (
    cargar_rutas_directorio_imagenes,
    generar_archivo_rutas_directorio_imagenes,
    )
from compartidos.advertencias_errores import (
    advertencia_error_escritura,
    )
from configuracion.settings import CONFIGURACION_GUARDADO_IMAGENES


def guardar_rutas_directorio_imagenes(ruta_repositorio, ruta_collages, ruta_memes):
    """
    Guarda las rutas de los directorios donde se guardarán las imágenes
    del repositorio, collages y memes elegidas por el usuario en un archivo
    en formato json.

    Parametros:
    ruta_repositorio (string): ruta de directorio donde se guardarán las imágenes
    del repositorio
    ruta_collages (string): ruta de directorio donde se guardarán los collages generados
    ruta_memes (string): ruta de directorio donde se guardarán los memes generados

    """
    rutas_nuevas_usuario = {
        "ubicacion_repositorio": ruta_repositorio,
        "ubicacion_collages": ruta_collages,
        "ubicacion_memes": ruta_memes,
    }

    try:
        with open(CONFIGURACION_GUARDADO_IMAGENES, "r") as archivo_ubicaciones:
            ubicaciones = json.load(archivo_ubicaciones)
            ubicaciones["ubicaciones_usuario"] = rutas_nuevas_usuario
        with open(CONFIGURACION_GUARDADO_IMAGENES, "w") as archivo_ubicaciones:
            json.dump(ubicaciones, archivo_ubicaciones)
    except FileNotFoundError:
        generar_archivo_rutas_directorio_imagenes(rutas_nuevas_usuario)
    except PermissionError:
        advertencia_error_escritura(CONFIGURACION_GUARDADO_IMAGENES)


def restaurar_rutas_por_defecto():
    """
    Reestablece las rutas por defecto de la aplicacion de repositorio de imágenes,
    collages y memes, vaciando de contenido las proporcionadas porel usuario
    """
    guardar_rutas_directorio_imagenes("", "", "")
    ruta_repositorio, ruta_collages, ruta_memes = cargar_rutas_directorio_imagenes()
    return ruta_repositorio, ruta_collages, ruta_memes
