import PySimpleGUI as sg


def advertencia_error_escritura(nombre_archivo):
    """
    Muestra una advertencia de error al escribir un archivo.

    Parametros:
        nombre_archivo (string): nombre del archivo que causó el error.
    """
    sg.popup_error(
        f"Error al escribir archivo {nombre_archivo}"
    )
    sg.popup_error(
        "Cierre la aplicacion, otorgue",
        "los permisos necesarios",
        "a los archivos de la aplicacion",
        "y luego ejecutela nuevamente",
    )


def advertencia_error_lectura(nombre_archivo):
    """
    Muestra una advertencia de error al leer un archivo

    Parametros:
        nombre_archivo (string): nombre del archivo que causó el error
    """
    sg.popup_error(
        f"Error al leer archivo {nombre_archivo}"
    )
    sg.popup_error(
        "Cierre la aplicacion, otorgue",
        "los permisos necesarios",
        "a los archivos de la aplicacion",
        "y luego ejecutela nuevamente",
    )


def advertencia_error_usuario_logueado():
    """
    Muestra una advertencia de error al no encontrar el archivo login de usuario
    """
    sg.popup_error(
        "Archivo de login usuario",
        "no encontrado",
        "Cierre la aplicacion",
        "y logueese nuevamente",
    )

def advertencia_error_no_encontrado(nombre_archivo):
    """
    Muestra una advertencia de error cuando no encuentra un archivo

    Parametros:
        nombre_archivo (string): nombre del archivo no encontrado
    """
    sg.popup_error(
        f"Archivo {nombre_archivo}",
        "no encontrado",
)
