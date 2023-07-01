import csv
import os
from datetime import datetime

from PIL import Image
from PySimpleGUI import popup

from compartidos.acceso_a_datos import registrar_accion_de_usuario
from system.etiquetar_imagen.settings import (
    MENSAJE_MODIFICACION,
    MENSAJE_NUEVA_CLASIFICACION,
)


def generate_file_to_project(path_metadata):
    """
    Genera un archivo de metadatos en el proyecto.

    Parameters:
        path_metadata (str): Ruta del archivo de metadatos.

    Raises:
        None

    Returns:
        None
    """
    file_ = path_metadata
    try:
        metadata_csv = open(file_, mode="w")
        metadata_csv.write("ruta_relativa,texto descriptivo,resolucion,tamanio,tipo,lista de tags,ultimo perfil que actualizo,ultima aztualizacion\n")
        metadata_csv.close()
    except Exception as e:
        popup(f"Error al generar el archivo de metadatos: {e}")


def save_metadata(metadata, path_metadata, alias):
    """
    Guarda los metadatos de una imagen en el archivo de metadatos.

    Parameters:
        metadata (dict): Metadatos de la imagen.
        path_metadata (str): Ruta del archivo de metadatos.
        alias (str): Alias del usuario.

    Raises:
        None

    Returns:
        None
    """
    image_save = {
        'ruta_relativa': metadata['ruta_relativa'],
        'texto descriptivo': metadata['texto descriptivo'],
        'resolucion': metadata['resolucion'],
        'tamanio': metadata['tamanio'],
        'tipo': metadata['tipo'],
        'lista de tags': metadata['lista de tags'],
        'ultimo perfil que actualizo': alias,
        'ultima aztualizacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    data_cleaned = {}
    header = None

    try:
        with open(path_metadata, mode="r") as metadata_csv:
            csv_reader = csv.reader(metadata_csv)
            data = list(csv_reader)

            if len(data) > 0:
                header = data[0]
                data = data[1:]

            for tupla in data:
                if tupla and tupla[0] == image_save['ruta_relativa']:
                    tupla = tuple(image_save.values())
                data_cleaned[tupla[0]] = tupla

    except FileNotFoundError:
        try:
            generate_file_to_project(path_metadata)
            save_metadata(metadata, path_metadata, alias)
        except Exception as e:
            popup(f"Error al crear el archivo de metadatos: {e}")
    else:
        if image_save['ruta_relativa'] not in data_cleaned:
            data_cleaned[image_save['ruta_relativa']] = tuple(image_save.values())

        try:
            with open(path_metadata, mode="w", newline="") as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                if header:
                    escritor_csv.writerow(header)
                for tupla in data_cleaned.values():
                    escritor_csv.writerow(tupla)
        except Exception as e:
            popup(f"Error al guardar los metadatos: {e}")

        if metadata['etiqueta']:
            registrar_accion_de_usuario(usuario=alias, accion=MENSAJE_MODIFICACION)
        else:
            registrar_accion_de_usuario(usuario=alias, accion=MENSAJE_NUEVA_CLASIFICACION)
            metadata['etiqueta'] = True


def get_info_image(value_path, path_metadata, path_repositorio):
    """
    Obtiene la información de una imagen a partir de su ruta.

    Parameters:
        value_path (str): Ruta de la imagen.
        path_metadata (str): Ruta del archivo de metadatos.
        path_repositorio (str): Ruta del repositorio de imágenes.

    Raises:
        None

    Returns:
        dict: Información de la imagen.
    """
    data_cleaned = {}

    try:
        with open(path_metadata, mode="r") as metadata_csv:
            csv_reader = csv.reader(metadata_csv)
            data = list(csv_reader)

            if len(data) > 0:
                header = data[0]
                data = data[1:]

            for row in data:
                if row:
                    data_cleaned[row[0]] = row

    except FileNotFoundError:
        try:
            generate_file_to_project(path_metadata)
        except Exception as e:
            popup(f"Error al crear el archivo de metadatos: {e}")

    if value_path in data_cleaned:
        row = data_cleaned[value_path]
        info_imagen = {
            'ruta_relativa': row[0],
            'texto descriptivo': row[1],
            'resolucion': row[2],
            'tamanio': row[3],
            'tipo': row[4],
            'lista de tags': row[5],
            'ultimo perfil que actualizo': row[6],
            'ultima aztualizacion': row[7],
            'etiqueta': True
        }
        return info_imagen
    else:
        file_path = os.path.normpath(path_repositorio + "/" + value_path)
        img = Image.open(file_path)
        width, height = img.size
        size = os.path.getsize(file_path)
        size_kilobytes = size / 1024
        size_megabytes = size_kilobytes / 1024
        mimetype = Image.MIME[img.format]

        info = {
            'ruta_relativa': value_path,
            'texto descriptivo': '',
            'resolucion': f'{width} x {height}',
            'tamanio': f'{size_megabytes} MB',
            'tipo': mimetype,
            'lista de tags': [],
            'ultimo perfil que actualizo': '',
            'ultima aztualizacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'etiqueta': False
        }
        return info
