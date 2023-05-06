import PySimpleGUI as sg
import os
from etiquetar_imagenes import EtiquetarImagenes
from ayuda import Ayuda
from mostrar_pantalla import mostrar_pantalla
sg.theme('Black')


layout = [
    [sg.Text("nick",key="-PERFIL SELECCIONADO-", font=("Helvetica", 20)),sg.Button("Configuración",key="-CONFIGURACION-", font=("Helvetica", 14)),sg.Button("Ayuda",key="-AYUDA-", font=("Helvetica", 14))],
    [sg.Button("Etiquetar imagenes",key="-ETIQUETAR IMAGENES-")],
    [sg.Button("Generar meme",key="-GENERAR MEME-")],
    [sg.Button("Generar collage",key="-GENERAR COLLAGE-")],   
    [ sg.Button("Salir",key="-SALIR-",size=(15, 2), font=("Helvetica", 14))],
    
]

window = sg.Window("Menú principal", layout,size=(1400,992), resizable=True, element_padding=((128,128),(64,64)),margins=(0,0),element_justification="center", finalize=True)


def mostrar_perfil_seleccionado():
    pass
def mostrar_ventana_configuracion():
    pass
def mostrar_generar_meme():
    pass
def mostrar_generar_collage():
    pass


events = {
    "-PERFIL SELECCIONADO-": lambda values:mostrar_perfil_seleccionado(),
    "-CONFIGURACION-": lambda values: mostrar_ventana_configuracion(),
    "-AYUDA-": lambda values: Ayuda().iniciar(),
    "-ETIQUETAR IMAGENES-":lambda values: EtiquetarImagenes().iniciar(),
    "-GENERAR MEME-":lambda values: mostrar_generar_meme(),
    "-GENERAR COLLAGE-":lambda values: mostrar_generar_collage(),
}



mostrar_pantalla(window,events)


