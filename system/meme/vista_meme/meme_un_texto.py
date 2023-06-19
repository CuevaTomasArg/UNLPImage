import io
import os

import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont

from compartidos.acceso_a_datos import (cargar_rutas_directorio_imagenes,
                                        registrar_accion_de_usuario,
                                        traer_usuario_logueado)
from system.meme.acceso_a_datos_memes import obtener_text_boxes
from system.meme.settings_meme import MENSAJE_MEME, PATH_FUENTES
from system.meme.validacion_imagen import archivo_mismo_nombre

sg.theme("Black")
ruta_nuevos_memes = cargar_rutas_directorio_imagenes()
ruta_nuevos_memes = ruta_nuevos_memes[2]


class PantallaTresMeme:
    def __init__(self, imagen_recibida, ruta_recibida):
        self.nombre_imagen_png = imagen_recibida
        self.ruta_imagen = ruta_recibida
        self.imagen_seleccionada_lista = ""
        self.imagen_seleccionada_png = ""
        self.fuente = ["Arial", "Times New Roman", "Courier New", "Verdana"]
        self.ruta = ""
        self.imagen = None
        self.draw = None
        self.texto = ""
        self.valor_fuente = self.fuente[0]

        columna_izquierda = [
            [sg.Text("Seleccionar fuente")],
            [
                sg.Combo(
                    self.fuente,
                    default_value=self.fuente[0],
                    size=(43, 1),
                    key="-COMBO-",
                    enable_events=True,
                )
            ],
            [sg.Text("Texto 1")],
            [
                sg.InputText(key="-TEXTOUNO-", enable_events=True, disabled=False)
            ],  # ANTES disabled=True
        ]
        columna_derecha = [
            [sg.Text("Imagen Seleccionada")],
            [sg.Image(key="-IMAGEN-", filename=self.ruta_imagen)],
        ]
        self.layout = [
            [
                sg.Text("Generar Meme", font="Any 15"),
                sg.Push(),
                sg.Button("< Volver", font="Any 10", key="-VOLVER-"),
            ],
            [sg.Column(columna_izquierda), sg.Column(columna_derecha)],
            [sg.Push(), sg.Button("Guardar", disabled=True, key="-GENERAR-")],
        ]

        self.window = sg.Window("", self.layout)

    def iniciar(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "-VOLVER-":
                self.window.close()
                break
            elif event == "-COMBO-":
                self.valor_fuente = values["-COMBO-"]
            elif event == "-TEXTOUNO-":
                if values["-TEXTOUNO-"] != "":
                    self.window["-GENERAR-"].update(disabled=False)
                else:
                    self.window["-GENERAR-"].update(disabled=True)
                self.texto = values["-TEXTOUNO-"]
                self.escribir_texto_uno()
            elif event == "-GENERAR-":
                self.evento_guardar()
                self.generar_log()
                sg.SystemTray.notify(
                    "Meme Guardado", "El meme se ha guardado con éxito."
                )

    def fuentes_conversion(self):
        """Esta funcion retorna un objeto que contiene
         la fuente y el tamaño del texto
        seleccionado por el usuario
        """
        diccionario_fuentes = {
            "Arial": "/arial.ttf",
            "Times New Roman": "/times.ttf",
            "Courier New": "/cour.ttf",
            "Verdana": "/verdana.ttf",
        }
        valor_fuente = diccionario_fuentes[self.valor_fuente]
        with open(
            os.path.normpath(PATH_FUENTES + valor_fuente), "rb"
        ) as archivo_fuente:
            return ImageFont.truetype(archivo_fuente, 30)

    def escribir_texto_uno(self):
        """Esta funcion escribe sobre la imagen un texto"""
        try:
            text_boxes = obtener_text_boxes(
                self.nombre_imagen_png
            )  # retorna lista de coordenadas
        except FileNotFoundError:
            sg.popup_error("No se pudo encontrar el archivo para crear el meme")
            self.window.close()
        except PermissionError:
            sg.popup_error(
                "No se tienen los derechos adecuados para abrir el archivo para crear memes"
            )
            self.window.close()

        fuente = self.fuentes_conversion()
        self.imagen = Image.open(self.ruta_imagen)
        self.draw = ImageDraw.Draw(self.imagen)
        ancho_texto, alto_texto = self.draw.textsize(self.texto, font=fuente)
        if text_boxes:
            box = text_boxes[0]
            top_left = (box["top_left_x"], box["top_left_y"])
            bottom_right = (box["bottom_right_x"], box["bottom_right_y"])
            posicion_x = (
                top_left[0] + (bottom_right[0] - top_left[0]) // 2 - ancho_texto // 2
            )
            posicion_y = (
                top_left[1] + (bottom_right[1] - top_left[1]) // 2 - alto_texto // 2
            )
            self.draw.text(
                (posicion_x, posicion_y), self.texto, font=fuente, fill=(255, 255, 255)
            )
        imagen_bytes = io.BytesIO()
        self.imagen.save(imagen_bytes, format="PNG")
        self.window["-IMAGEN-"].update(data=imagen_bytes.getvalue())

    def evento_guardar(self):
        """Esta funcion guarda en el archivo json las imagenes
        modificadas con texto y emite una ventana en el caso
        de la carga fuera exitosa."""

        contador_nueva_imagen = 1
        while True:
            nuevo_nombre = f"meme({contador_nueva_imagen}).png"
            if archivo_mismo_nombre(ruta_nuevos_memes, nuevo_nombre):
                self.imagen.save(os.path.join(ruta_nuevos_memes, nuevo_nombre))
                break
            else:
                contador_nueva_imagen += 1
        self.window.close()

    def generar_log(self):
        """Esta funcion genera los logs cada vez que el usuario
        genera un meme"""

        usuario = traer_usuario_logueado()
        usuario = usuario["alias"]
        registrar_accion_de_usuario(
            usuario, MENSAJE_MEME, self.nombre_imagen_png, self.texto
        )


if __name__ == "__main__":
    pantalla = PantallaTresMeme()
    pantalla.iniciar()
