import PySimpleGUI as sg

from system.collage.settings_collage import (
    FORMATO_COLLAGE_CINCO,
    FORMATO_COLLAGE_CUATRO,
    FORMATO_COLLAGE_DOS,
    FORMATO_COLLAGE_OCHO,
    FORMATO_COLLAGE_SEIS,
    FORMATO_COLLAGE_SIETE,
    FORMATO_COLLAGE_TRES,
    FORMATO_COLLAGE_UNO,
)
from system.collage.vista_collage.collage_cuatro_imagenes import CuatroImagenesCollage
from system.collage.vista_collage.collage_dos_imagenes import DosImagenesCollage
from system.collage.vista_collage.collage_seis_imagenes import SeisImagenesCollage
from system.collage.vista_collage.collage_tres_imagenes import TresImagenesCollage

sg.theme("Black")


class GeneradorCollage:
    def __init__(self):
        self.nombre_formato = ""
        fila_uno = [
            sg.Button(
                image_filename=FORMATO_COLLAGE_UNO,
                key="-FORMATOUNO-",
                enable_events=True,
                border_width=4,
            ),
            sg.Button(
                image_filename=FORMATO_COLLAGE_DOS,
                key="-FORMATODOS-",
                enable_events=True,
                border_width=4,
            ),
            sg.Button(
                image_filename=FORMATO_COLLAGE_TRES,
                key="-FORMATOTRES-",
                enable_events=True,
                border_width=4,
            ),
            sg.Button(
                image_filename=FORMATO_COLLAGE_CUATRO,
                key="-FORMATOCUATRO-",
                enable_events=True,
                border_width=4,
            ),
        ]
        fila_dos = [
            sg.Button(
                image_filename=FORMATO_COLLAGE_CINCO,
                key="-FORMATOCINCO-",
                enable_events=True,
                border_width=4,
            ),
            sg.Button(
                image_filename=FORMATO_COLLAGE_SEIS,
                key="-FORMATOSEIS-",
                enable_events=True,
                border_width=4,
            ),
            sg.Button(
                image_filename=FORMATO_COLLAGE_SIETE,
                key="-FORMATOSIETE-",
                enable_events=True,
                border_width=4,
            ),
            sg.Button(
                image_filename=FORMATO_COLLAGE_OCHO,
                key="-FORMATOOCHO-",
                enable_events=True,
                border_width=4,
            ),
        ]
        fila_uno_texto = [
            sg.Text("Formato 1", font=("Any", 10, "italic")),
            sg.Text(
                "Formato 2",
                justification="center",
                font=("Any", 10, "italic"),
                pad=(20, 0, 0, 0),
            ),
            sg.Text(
                "Formato 3",
                justification="center",
                font=("Any", 10, "italic"),
                pad=(10, 0, 0, 0),
            ),
            sg.Text(
                "Formato 4",
                justification="center",
                font=("Any", 10, "italic"),
                pad=(10, 0, 0, 0),
            ),
        ]
        fila_dos_texto = [
            sg.Text("Formato 5", font=("Any", 10)),
            sg.Text(
                "Formato 6",
                justification="center",
                font=("Any", 10, "italic"),
                pad=(20, 0, 0, 0),
            ),
            sg.Text(
                "Formato 7",
                justification="center",
                font=("Any", 10, "italic"),
                pad=(10, 0, 0, 0),
            ),
            sg.Text(
                "Formato 8",
                justification="center",
                font=("Any", 10, "italic"),
                pad=(10, 0, 0, 0),
            ),
        ]
        self.layout = [
            [
                sg.Text("Seleccionar diseño de collage", font="Any 15"),
                sg.Push(),
                sg.Push(),
                sg.Push(),
                sg.Push(),
                sg.Push(),
                sg.Button("< Volver", font="Any 10", key="-VOLVER-"),
            ],
            [sg.VPush()],
            [sg.VPush()],
            [sg.VPush()],
            fila_uno,
            fila_uno_texto,
            [sg.VPush()],
            fila_dos,
            fila_dos_texto,
        ]
        self.window = sg.Window("", self.layout)

    def iniciar(self):
        formatos = {
            "-FORMATOUNO-": ("Formato 1", DosImagenesCollage),
            "-FORMATODOS-": ("Formato 2", DosImagenesCollage),
            "-FORMATOOCHO-": ("Formato 8", DosImagenesCollage),
            "-FORMATOTRES-": ("Formato 3", CuatroImagenesCollage),
            "-FORMATOCUATRO-": ("Formato 4", TresImagenesCollage),
            "-FORMATOSEIS-": ("Formato 6", TresImagenesCollage),
            "-FORMATOSIETE-": ("Formato 7", TresImagenesCollage),
            "-FORMATOCINCO-": ("Formato 5", SeisImagenesCollage),
        }

        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "-VOLVER-":
                self.window.close()
                break
            elif event in formatos:
                formato, collage_clase = formatos[event]
                sg.popup(f"Seleccionaste: {formato}")
                self.window.close()
                self.nombre_formato = event
                collage_clase(self.nombre_formato).iniciar()


if __name__ == "__main__":
    pantalla = GeneradorCollage()
    pantalla.iniciar()
