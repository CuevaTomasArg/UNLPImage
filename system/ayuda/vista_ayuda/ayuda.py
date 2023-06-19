import PySimpleGUI as sg

from compartidos.mostrar_pantalla import mostrar_pantalla


class Ayuda:
    def __init__(self):
        self.layout = [
            [sg.Text("Bienvenido a UNLPImage", auto_size_text=True,font=("Arial", 24), justification="left", pad=((0, 0), (0, 30)))],
            [sg.Text("Editar perfil", auto_size_text=True,font=("Arial", 21), pad=((0, 0), (0, 20)))],
            [sg.Text("""
            En la esquina superior izquierda encontrarás la foto de perfil de tu avatar.
            Al hacer click en la foto, se abrirá una interfaz para que puedas editar tu perfil actual. 
            Puedes cambiar el nombre de tu nick, la foto de tu avatar y cualquier otra cosa que desees.
                     """, auto_size_text=True,font=("Arial", 18), pad=((0, 0), (0, 20)))],
            [sg.Text("Configuración", auto_size_text=True,font=("Arial", 21), pad=((0, 0), (0, 20)))],
            [sg.Text("""
                     Al hacer click en este botón, se abrirá una interfaz donde podrás configurar tus repositorios.
                     """, auto_size_text=True,font=("Arial", 18), pad=((0, 0), (0, 20)))],
            [sg.Text("¿Qué son los repositorios?", auto_size_text=True,font=("Arial", 18), pad=((0, 0), (0, 10)))],
            [sg.Text("""Los repositorios son las carpetas donde se encontrarán las imágenes que crearás o donde se 
                     almacenarán las imágenes que utilizarás para crear tus collages o memes. 
                     Puedes usar cualquier repositorio de tu computadora o utilizar los que vienen predeterminados para ti.""", auto_size_text=True,font=("Arial", 18), pad=((0, 0), (0, 20)))],
            [sg.Text("Etiquetar imágenes", auto_size_text=True,font=("Arial", 18), pad=((0, 0), (0, 10)))],
            [sg.Text("""Esta sección es la más divertida de la aplicación y la mejor desarrollada. 
                     Aquí podrás visualizar las imágenes dentro de tu repositorio de imágenes y ver sus características. 
                     También podrás etiquetar las imágenes o agregarles alguna descripción adicional.""", auto_size_text=True,font=("Arial", 18), pad=((0, 0), (0, 20)))],
            [sg.Text("Generador de memes y generador de collages", auto_size_text=True,font=("Arial", 18), pad=((0, 0), (0, 10)))],
            [sg.Text("En esta interfaz podrás generar memes o collages utilizando las imágenes de tu repositorio.", auto_size_text=True,font=("Arial", 18), pad=((0, 0), (0, 20)))],
            [sg.Text("Ayuda", auto_size_text=True,font=("Arial", 18), pad=((0, 0), (0, 10)))],
            [sg.Text("Ya estás en ayuda", auto_size_text=True,font=("Arial", 18), pad=((0, 0), (0, 20)))]
        ]
        self.window = sg.Window("Ayuda", self.layout,size=(1400,992), resizable=True, element_padding=((128,128),(64,64)),margins=(32,32),element_justification="left", finalize=True)

    def iniciar(self):
        mostrar_pantalla(self.window)