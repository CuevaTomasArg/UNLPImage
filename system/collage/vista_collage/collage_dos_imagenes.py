import io
import os

import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont

from compartidos.acceso_a_datos import (
    cargar_rutas_directorio_imagenes,
    registrar_accion_de_usuario,
    traer_usuario_logueado,
)
from system.collage.acceso_a_datos_collage import chequear_campo_lista_tags
from system.collage.settings_collage import MENSAJE_COLLAGE
from system.collage.validacion_imagen import archivo_mismo_nombre

sg.theme("Black")
tipo_de_archivo = [("PNG (*.png)", "*.png")]
ruta_imagenes_collage_gral = cargar_rutas_directorio_imagenes()
ruta_imagenes_collage = ruta_imagenes_collage_gral[0]
ruta_nuevo_collage = ruta_imagenes_collage_gral[1]


class DosImagenesCollage:
    def __init__(self, numero_formato):
        self.formato = numero_formato
        self.archivo = ["-ELEGIR ARCHIVO 1-", "-ELEGIR ARCHIVO 2-"]
        self.imagen = None
        self.texto = ""
        self.imagenes = []
        self.imagen_bytes = io.BytesIO()
        self.collage = None
        self.filename = ""
        self.log_usuario = []

        columna_izquierda = [
            [
                sg.Input(
                    key="-ELEGIR ARCHIVO 1-",
                    enable_events=True,
                    visible=False,
                    default_text=ruta_imagenes_collage,
                ),
                sg.FileBrowse(
                    "Seleccionar imagen 1",
                    tooltip="Extensión valida .png",
                    target="-ELEGIR ARCHIVO 1-",
                    file_types=tipo_de_archivo,
                    initial_folder=ruta_imagenes_collage,
                ),
            ],
            [
                sg.Input(
                    key="-ELEGIR ARCHIVO 2-",
                    enable_events=True,
                    visible=False,
                    default_text=ruta_imagenes_collage,
                ),
                sg.FileBrowse(
                    "Seleccionar imagen 2",
                    tooltip="Extensión valida .png",
                    target="-ELEGIR ARCHIVO 2-",
                    file_types=tipo_de_archivo,
                    initial_folder=ruta_imagenes_collage,
                ),
            ],
            [sg.Text("Titulo")],
            [
                sg.InputText(
                    key="-TITULO-", enable_events=True, size=(20, 1), disabled=True
                )
            ],
        ]
        columna_derecha = [
            [sg.Text("Previsualización del collage", font="Any 12")],
            [sg.Image(key="-PREVIEW-", size=(200, 200))],
            [sg.Push(), sg.Button("Guardar", disabled=True, key="-GUARDAR-")],
        ]

        self.layout = [
            [
                sg.Text("Generar Collage", font="Any 15"),
                sg.Push(),
                sg.Push(),
                sg.Push(),
                sg.Push(),
                sg.Push(),
                sg.Button("< Volver", font="Any 10", key="-VOLVER-"),
            ],
            [sg.Column(columna_izquierda), sg.Column(columna_derecha)],
        ]

        self.window = sg.Window("", self.layout)

    def iniciar(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "-VOLVER-":
                self.window.close()
                break
            elif event in self.archivo:
                self.manejo_archivo(event, values)
            elif event == "-TITULO-":
                self.texto = values["-TITULO-"]
            elif event == "-GUARDAR-":
                self.texto_sobre_collage()
                self.guardar_collage()
                self.generar_log()
                self.window.close()
                sg.SystemTray.notify(
                    "Collage Guardado", "El Collage se ha guardado con éxito."
                )

    def chequear_etiqueta_imagen(self):
        """Esta funcion llama a otra funcion, pasandole
         por parametro el nombre de la imagen para verificar si dicha imagen
         esta etiquetada.
        Advierte al usuario de etiquetar la imagen en caso de no estarlo
        """

        nombre_imagen = os.path.basename(self.filename)
        try:
            resultado = chequear_campo_lista_tags(nombre_imagen)
            if resultado:
                sg.popup("¡ADVERTENCIA, ETIQUERAR IMAGEN!: ", nombre_imagen)
        except FileNotFoundError:
            sg.popup_error(
                "ERROR CONTACTAR CON SISTEMA: No se puede abrir el archivo de metadatos."
            )
        except PermissionError:
            sg.popup_error(
                "ERROR CONTACTAR CON SISTEMA: No se tienen los permisos adecuados para abrir el archivo."
            )

    def insertar_img_segun_formato(self):
        """Esta función genera el collage según el formato
        seleccionado por el usuario.
        Llama a otras funciones para generar el collage
        en función del tipo de formato elegido."""

        if self.formato == "-FORMATOUNO-":
            self.generar_collage_formato_uno()
        if self.formato == "-FORMATODOS-":
            self.generar_collage_formato_dos()
        if self.formato == "-FORMATOOCHO-":
            self.generar_collage_formato_ocho()

    def evento_elegir_archivo(self, num):
        """Esta función guarda la imagen seleccionada
        por el usuario en una lista, según su posicion.
        También actualiza el boton "Guardar" y habilita el campo "Titulo"
        para que el usuario pueda escribir.
        """

        if len(self.imagenes) > num:
            self.imagenes[num] = self.filename
        else:
            self.imagenes.insert(num, self.filename)
        if len(self.imagenes) == 2:
            self.window["-GUARDAR-"].update(disabled=False)
            self.window["-TITULO-"].update(disabled=False)
        self.insertar_img_segun_formato()

    def manejo_archivo(self, event, values):
        """Esta función maneja el evento de selección de archivo.
        Según el evento realizado, llama a otras funciones
        para guardar la imagen seleccionada en una lista
        y verificar si la imagen seleccionada por el usuario está etiquetada.
        """

        indice = self.archivo.index(event)
        self.filename = values[event]
        self.evento_elegir_archivo(indice)
        self.chequear_etiqueta_imagen()

    def generar_collage_formato_uno(self):
        """ "Esta funcion itera sobre la lista de imagenes para
        ir pegandolas en el collage y luego las imagenes PNG las
        transforma en Bytes
        Divide la pantalla en en dos,
        una imagen en el margen derecho
        y la otra en el margen izquierdo"""

        width, height = 400, 200
        self.collage = Image.new("RGB", (width, height))
        coords = [(0, 0, width // 2, height), (width // 2, 0, width, height)]
        for i in range(len(self.imagenes)):
            img = Image.open(self.imagenes[i])
            img = img.resize((width // 2, height))
            self.collage.paste(img, coords[i])
        self.imagen_bytes = io.BytesIO()
        self.collage.save(self.imagen_bytes, format="PNG")
        self.window["-PREVIEW-"].update(data=self.imagen_bytes.getvalue())

    def generar_collage_formato_dos(self):
        """ "Esta funcion itera sobre la lista de imagenes para
        ir pegandolas en el collage y luego las imagenes PNG las
        transforma en Bytes
        Divide la pantalla en en dos,
        una imagen en el margen superior
        y la otra en el margen inferior"""

        width, height = 200, 300
        self.collage = Image.new("RGB", (width, height))
        coords = [(0, 0, width, height // 2), (0, height // 2, width, height)]
        for i in range(len(self.imagenes)):
            img = Image.open(self.imagenes[i])
            img = img.resize((width, height // 2))
            self.collage.paste(img, coords[i])
        self.imagen_bytes = io.BytesIO()
        self.collage.save(self.imagen_bytes, format="PNG")
        self.window["-PREVIEW-"].update(data=self.imagen_bytes.getvalue())

    def generar_collage_formato_ocho(self):
        """ "Esta funcion itera sobre la lista de imagenes para
        ir pegandolas en el collage y luego las imagenes PNG las
        transforma en Bytes
        Divide la pantalla en en dos,
        una imagen en el margen derecho, mas pequeña
        y la otra en el margen izquierdo, mas grande"""

        width, height = 400, 600
        self.collage = Image.new("RGB", (width, height))
        coords = [(0, 0, width, height // 3), (0, height // 3, width, height)]
        for i in range(len(self.imagenes)):
            img = Image.open(self.imagenes[i])
            if i == 0:
                img = img.resize((width, height // 3))
            else:
                img = img.resize((width, 2 * (height // 3)))
            self.collage.paste(img, coords[i])
        self.imagen_bytes = io.BytesIO()
        self.collage.save(self.imagen_bytes, format="PNG")
        self.window["-PREVIEW-"].update(data=self.imagen_bytes.getvalue())

    def texto_sobre_collage(self):
        """Esta funcion edita el collage ya generado.
        Escribe texto sobre la imagen
        """

        imagen = self.collage
        editor_img = ImageDraw.Draw(imagen)
        fuente = ImageFont.truetype("arial.ttf", 20)
        image_width, image_height = imagen.size
        text_width, text_height = fuente.getsize(self.texto)
        texto_x = 10
        texto_y = image_height - text_height - 10
        editor_img.text(
            (texto_x, texto_y), self.texto, font=fuente, fill=(255, 255, 255, 255)
        )
        self.imagen_bytes = io.BytesIO()
        imagen.save(self.imagen_bytes, format="PNG")
        self.window["-PREVIEW-"].update(data=self.imagen_bytes.getvalue())

    def guardar_collage(self):
        """ "Esta funcion guarda en el archivo json las imagenes
        transformadas en Bytes"""

        contador_nuevo_collage = 1
        self.collage.save(self.imagen_bytes, format="PNG")
        while True:
            nuevo_nombre = f"collage({contador_nuevo_collage}).png"
            if archivo_mismo_nombre(ruta_nuevo_collage, nuevo_nombre):
                self.collage.save(os.path.join(ruta_nuevo_collage, nuevo_nombre))
                break
            else:
                contador_nuevo_collage += 1

    def generar_log(self):
        """Esta funcion genera los logs cada vez que el usuario
        genera un collage
        """
        usuario = traer_usuario_logueado()
        usuario = usuario["alias"]
        for elemento in self.imagenes:
            nombre_img = os.path.basename(elemento)
            self.log_usuario.append(nombre_img)
        registrar_accion_de_usuario(
            usuario, MENSAJE_COLLAGE, self.log_usuario, self.texto
        )


if __name__ == "__main__":
    pantalla = DosImagenesCollage()
    pantalla.iniciar()
