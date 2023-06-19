from system.etiquetar_imagen.settings import METADATA_DIR
import csv


def chequear_campo_lista_tags(nombre_imagen):
    """Esta funcion abre el archivo metadata para verificar
    si la imagen que selecciono el usuario esta etiquetada.
    Devuelve True si esta sin etiqueta
    Devuelve False si esta con etiqueta
    Lanza FileNotFoundError si no se puede abrir el archivo de metadatos
    """
    try:
        no_existe_imagen = True
        with open(METADATA_DIR, "r") as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            for fila in lector:
                if fila["ruta_relativa"] == nombre_imagen:
                    lista_tags = eval(fila["lista de tags"])
                    if lista_tags:
                        no_existe_imagen = False
                        break
        return no_existe_imagen
    except FileNotFoundError:
        raise FileNotFoundError("No existe el archivo de metadatos.")
    except PermissionError:
        raise PermissionError(
            "No se tienen los permisos adecuados para abrir el archivo."
        )
