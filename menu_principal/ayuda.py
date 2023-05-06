import PySimpleGUI as sg
from mostrar_pantalla import mostrar_pantalla

class Ayuda:
    def __init__(self):
        self.layout = [[sg.Text("Bienvenido a la aplicación de etiquetado, collage y memes", font=("Arial", 16), justification="center", pad=((0,0),(0,30)))],
          [sg.Text("A continuación, le explicaremos el funcionamiento de cada uno de los botones del menu principal", font=("Arial", 14), pad=((0,0),(0,20)))],
          [sg.Text("Etiquetar imágenes", font=("Arial", 12), pad=((0,0),(0,10)))],
          [sg.Text("Esta opción abrirá una ventana en la cual podrás agregar etiquetas a tus imágenes para poder diferenciarlas y generar collages o memes más rápido.", font=("Arial", 10), pad=((0,0),(0,20)))],
          [sg.Text("Generar memes", font=("Arial", 12), pad=((0,0),(0,10)))],
          [sg.Text("Esta opción abrirá una ventana para que puedas generar memes.", font=("Arial", 10), pad=((0,0),(0,20)))],
          [sg.Text("Generar collage", font=("Arial", 12), pad=((0,0),(0,10)))],
          [sg.Text("Esta opción abrirá una ventana para que puedas generar collages.", font=("Arial", 10), pad=((0,0),(0,20)))],
          [sg.Text("Hecho con PySimpleGUI", font=("Arial", 8), justification="right", pad=((0,0),(40,0)))],
          [sg.Text("Configuración", font=("Arial", 12), pad=((0,0),(0,10)))],
          [sg.Text("Esta opción abrirá una ventana para que puedas configurar la aplicación,podrá:", font=("Arial", 10), pad=((0,0),(0,20)))],
          [sg.Text("• Elegir el lugar donde estarán las imagenes para etiquetarlas.", font=("Arial", 12), pad=((0,0),(0,10)))],
          [sg.Text("• Elegir el lugar donde se guardarán los memes generados.", font=("Arial", 12), pad=((0,0),(0,10)))],
          [sg.Text("• Elegir el lugar donde se guardarán los collages generados.", font=("Arial", 12), pad=((0,0),(0,10)))],
          ]
        self.window = sg.Window("Ayuda", self.layout,size=(1400,992), resizable=True, element_padding=((128,128),(64,64)),margins=(0,0),element_justification="center", finalize=True)

    def iniciar(self):
        mostrar_pantalla(self.window)