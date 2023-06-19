import io
import os

import PySimpleGUI as sg
from PIL import Image

from compartidos.acceso_a_datos import cargar_rutas_directorio_imagenes
from system.meme.vista_meme.meme_dos_textos import PantallaDosMeme
from system.meme.vista_meme.meme_un_texto import PantallaTresMeme

sg.theme("Black")
ruta_imagenes_meme_gral = cargar_rutas_directorio_imagenes()
ruta_imagenes_meme = ruta_imagenes_meme_gral[0]


class GeneradorMemes:
    def __init__(self):
        self.lista = [
            "inteligente",
            "incendio",
            "spidermans",
            "burns",
            "ruta",
            "tumba",
            "parche",
            "ola",
            "marge",
            "zorro",
        ]
        self.imagen_seleccionada_lista = ""
        self.imagen_seleccionada_png = ""
        self.imagenes_un_solo_texto = {
            "inteligente",
            "incendio",
            "burns",
            "tumba",
            "ola",
            "marge",
            "zorro",
        }
        self.imagen = None
        self.texto = ""
        self.cantidad_txt = 0
        self.ruta = ""

        columna_izquierda = [
            [sg.Text("Seleccionar template", font="Any 15")],
            [
                sg.Listbox(
                    values=self.lista, size=(40, 10), key="-LISTA-", enable_events=True
                )
            ],
            [
                sg.Button(
                    "Seleccionar Imagen",
                    tooltip="Extensión válida .png",
                    key="-SELECCIONAR-",
                    disabled=True,
                )
            ],
        ]
        columna_derecha = [[sg.Text("Imagen Seleccionada")], [sg.Image(key="-IMAGEN-")]]
        self.layout = [
            [
                sg.Text("Generar Meme", font="Any 15"),
                sg.Push(),
                sg.Button("< Volver", font="Any 10", key="-VOLVER-"),
            ],
            [sg.Column(columna_izquierda), sg.Column(columna_derecha)],
            [sg.Push(), sg.Button("Generar", disabled=True, key="-GENERAR-")],
        ]

        self.window = sg.Window("", self.layout)

    def iniciar(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "-VOLVER-":
                self.window.close()
                break
            elif event == "-LISTA-":
                self.imagen_seleccionada_lista = values["-LISTA-"][0]
                self.window["-SELECCIONAR-"].update(disabled=False)
            elif event == "-SELECCIONAR-":
                self.imagen_seleccionada_png = self.imagen_seleccionada_lista + ".png"
                self.ruta = os.path.join(
                    ruta_imagenes_meme, self.imagen_seleccionada_png
                )
                self.mostrar_imagen_meme()
            elif event == "-GENERAR-":
                self.window.close()
                self.cantidad_texto()

    def mostrar_imagen_meme(self):
        """Esta funcion muestra la imagen seleccionada por
        el usuario para realizar el meme"""

        filename = self.ruta
        self.imagen = Image.open(filename)
        imagen_bytes = io.BytesIO()
        self.imagen.save(imagen_bytes, format="PNG")
        self.window["-IMAGEN-"].update(data=imagen_bytes.getvalue())
        self.window["-GENERAR-"].update(disabled=False)

    def cantidad_texto(self):
        """Esta funcion llama a cierta funcion segun la cantidad
        de texto que tenga la imagen seleccionada"""

        if self.imagen_seleccionada_lista in self.imagenes_un_solo_texto:
            PantallaTresMeme(
                self.imagen_seleccionada_png, self.ruta
            ).iniciar()  
        else:
            PantallaDosMeme(self.imagen_seleccionada_png, self.ruta).iniciar()


if __name__ == "__main__":
    pantalla = GeneradorMemes()
    pantalla.iniciar()
