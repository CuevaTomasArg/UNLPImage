import PySimpleGUI as sg

from compartidos.acceso_a_datos import (
    traer_ruta_imagen,
    traer_usuario_logueado,
)
from compartidos.mostrar_pantalla import mostrar_pantalla
from ...ayuda.vista_ayuda.ayuda import Ayuda
from ...collage.vista_collage.generador_collage import GeneradorCollage
from ...configuracion.vista_configuracion.configuracion import ejecutar as ec
from ...etiquetar_imagen.vista_etiquetar_imagen.etiquetar_imagenes import EtiquetarImagenes
from ...meme.vista_meme.generador_memes import GeneradorMemes
from ...perfil.vista_perfil.editar_perfil import EditarPerfil

sg.theme('Black')

class MenuPrincipal:
    """
    Clase que representa la interfaz principal de la aplicación.
    Permite acceder a diferentes funcionalidades y opciones del sistema.
    """

    def __init__(self):
        """
        Inicializa la interfaz del menú principal.

        Crea los elementos de la interfaz y define los eventos asociados a cada uno.
        """

        user = traer_usuario_logueado()
        imagen_path = traer_ruta_imagen(user)
        nick = [
            [sg.Image(filename=imagen_path, pad=(0, 0), enable_events=True, key="-EDITAR PERFIL-")],
            [sg.Text(user["alias"], font=("Helvetica", 20), pad=(0, 0))]
        ]
        
        menu = [
            [sg.Button("Etiquetar imagenes", key="-ETIQUETAR IMAGENES-")],
            [sg.Button("Generar meme", key="-GENERAR MEME-")],
            [sg.Button("Generar collage", key="-GENERAR COLLAGE-")],
            [sg.Button("Salir", key="-SALIR-", size=(15, 2), font=("Helvetica", 14))],
        ]
        configuracion_ayuda = [
            [sg.Button("Configuración", key="-CONFIGURACION-", font=("Helvetica", 10)), sg.Button("Ayuda", key="-AYUDA-", font=("Helvetica", 10))]
        ]

        layout = [
            [sg.Column(nick, element_justification="center", vertical_alignment="top", pad=(0, 0)),
             sg.Column(menu, element_justification="center", vertical_alignment="center", pad=((180, 180), (128, 128))),
             sg.Column(configuracion_ayuda, element_justification="center", vertical_alignment="top", pad=(0, 0))]
        ]

        self.window = sg.Window("Menú principal", layout, size=(1024, 768), margins=(64, 72), resizable=True, finalize=True)

        self.events = {
            "-AYUDA-": lambda values: Ayuda().iniciar(),
            "-ETIQUETAR IMAGENES-": lambda values: EtiquetarImagenes().iniciar(),
            "-CONFIGURACION-": lambda values: ec(),
            "-GENERAR MEME-": lambda values: GeneradorMemes().iniciar(),
            "-GENERAR COLLAGE-": lambda values: GeneradorCollage().iniciar(),
            "-EDITAR PERFIL-": lambda values: self.actualizar_imagen(),
        }

    def actualizar_imagen(self):
        """
        Actualiza la imagen de perfil del usuario después de editar el perfil.
        """
        EditarPerfil().iniciar()
        user = traer_usuario_logueado()
        imagen_path = traer_ruta_imagen(user)
        self.window["-EDITAR PERFIL-"].update(filename=imagen_path)

    def iniciar(self):
        """
        Inicia la interfaz del menú principal y muestra la ventana.

        Permite al usuario interactuar con los elementos de la interfaz y realizar diferentes acciones.
        """
        mostrar_pantalla(self.window, self.events)

