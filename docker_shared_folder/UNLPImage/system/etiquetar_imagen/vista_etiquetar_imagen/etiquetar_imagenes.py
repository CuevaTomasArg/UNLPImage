import os

import PySimpleGUI as sg

from compartidos.acceso_a_datos import (
    cargar_rutas_directorio_imagenes,
    traer_ruta_imagen_avatar,
    traer_usuario_logueado,
)
from compartidos.mostrar_pantalla import mostrar_pantalla
from system.etiquetar_imagen.acceso_db import get_info_image, save_metadata
from system.etiquetar_imagen.settings import METADATA_DIR
from system.etiquetar_imagen.utils_tags_text import append_text, delete_tag


class EtiquetarImagenes:
    """
    Clase para etiquetar imágenes y guardar los metadatos.

    Attributes:
        repositorio (str): Ruta del repositorio de imágenes.
        alias (str): Alias del usuario.
        ruta_imagen (str): Ruta de la imagen seleccionada.
        window (sg.Window): Ventana de la interfaz gráfica.
        events (dict): Diccionario de eventos de la interfaz gráfica.

    Methods:
        upload_metadata: Guarda los metadatos en la base de datos.
        drop_tag: Elimina una etiqueta de la lista de etiquetas.
        add_text: Agrega un texto a la lista de etiquetas o modifica el texto descriptivo de la imagen.
        set_window: Actualiza la ventana con la información de la imagen seleccionada.
        iniciar: Inicia la interfaz gráfica de etiquetado de imágenes.
    """

    def __init__(self):
        """
        Inicializa la clase EtiquetarImagenes.

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        """
        self.repositorio = cargar_rutas_directorio_imagenes()
        diccionario = traer_usuario_logueado()
        self.alias = diccionario["alias"]
        self.ruta_imagen = traer_ruta_imagen_avatar(diccionario)

        archivos = os.listdir(self.repositorio[0]) # Crea una lista de nombres con los archivos y directorios dentro de la rusta especificada por el parametro

        selector = [
            [sg.Listbox(values=archivos, size=(30, 6), key='-LIST-', enable_events=True)],
            [sg.Text('Etiquetas:')],
            [sg.Input(key='-TAG-'), sg.Button('Agregar', key='-ADD-')],
            [sg.Input(key='-TAG DROP-'), sg.Button('Quitar', key='-DROP-')],
            [sg.Text('Añade un texto descriptivo')],
            [sg.Input(key='-TEXT-'), sg.Button('Modificar', key='-ADD TEXT-')],
        ]
        visor = [
            [sg.Text('', key='-NOMBRE ARCHIVO-')],
            [sg.Image(key='-IMAGE-')],
            [sg.Text('Descripción:')],
            [sg.Text(key='-DESCRIPTION-')],
            [sg.Text('', key='-TIPO-'), sg.Text(' | '), sg.Text('', key='-RESOLUCION-'), sg.Text(' | '),
             sg.Text('', key='-TAMANIO-')],
            [sg.Text('Etiquetas:'), sg.Text('', key='-VIEW TAGS-')],
        ]
        layout = [
            [sg.Text('Etiquetar imagenes'), sg.Button('< Volver', key='-SALIR-')],
            [sg.Column(selector), sg.Column(visor)],
            [sg.Text(' '), sg.Button('Guardar', key='-SAVE-')]
        ]
        self.window = sg.Window('Etiquetar imagenes', layout, finalize=True, metadata={})

        self.events = {
            '-LIST-': self.set_window,
            '-ADD-': lambda values: self.add_text(values, "-TAG-"),
            '-ADD TEXT-': lambda values: self.add_text(values, "-TEXT-"),
            '-SAVE-': self.upload_metadata,
            '-DROP-': self.drop_tag,
        }

    def upload_metadata(self, values):
        """
        Guarda los metadatos en la base de datos.

        Parameters:
            values (dict): Valores de la ventana de la interfaz gráfica.

        Raises:
            None

        Returns:
            None
        """
        save_metadata(self.window.metadata, METADATA_DIR, self.alias)
        sg.popup('Cambios guardados correctamente.')

    def drop_tag(self, values):
        """
        Elimina una etiqueta de la lista de etiquetas.

        Parameters:
            values (dict): Valores de la ventana de la interfaz gráfica.

        Raises:
            None

        Returns:
            None
        """
        delete_tag(self.window.metadata, values, self.window)

    def add_text(self, values, agree):
        """
        Agrega un texto a la lista de etiquetas o modifica el texto descriptivo de la imagen.

        Parameters:
            values (dict): Valores de la ventana de la interfaz gráfica.
            agree (str): Identificador del campo de entrada de texto.

        Raises:
            None

        Returns:
            None
        """
        append_text(values, agree, self.window)

    def set_window(self, values):
        """
        Actualiza la ventana con la información de la imagen seleccionada.

        Parameters:
            values (dict): Valores de la ventana de la interfaz gráfica.

        Raises:
            None

        Returns:
            None
        """
        if values["-LIST-"][0].endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")):
            self.window.metadata = get_info_image(values["-LIST-"][0], METADATA_DIR, self.repositorio[0])
            path_image = os.path.join(self.repositorio[0], self.window.metadata['ruta_relativa'])
            self.window['-IMAGE-'].update(filename=path_image)
            self.window['-TIPO-'].update(self.window.metadata['tipo'])
            self.window['-NOMBRE ARCHIVO-'].update(self.window.metadata['ruta_relativa'])
            self.window['-DESCRIPTION-'].update(self.window.metadata['texto descriptivo'])
            self.window['-RESOLUCION-'].update(self.window.metadata['resolucion'])
            self.window['-TAMANIO-'].update(self.window.metadata['tamanio'])
            self.window['-TEXT-'].update(self.window.metadata['texto descriptivo'])

            tags = self.window.metadata['lista de tags']
            if isinstance(tags, str):
                tags = eval(tags)
            tags = " ".join(tags)
            self.window['-VIEW TAGS-'].update(tags)
        else:
            sg.popup('No se puede mostrar el archivo seleccionado porque tiene que ser una imagen')

    def iniciar(self):
        """
        Inicia la interfaz gráfica de etiquetado de imágenes.

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        """
        mostrar_pantalla(self.window, self.events)
