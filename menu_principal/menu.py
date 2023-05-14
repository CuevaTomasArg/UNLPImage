import PySimpleGUI as sg
import os
from menu_principal.mostrar_pantalla import mostrar_pantalla
from menu_principal.acceso_a_datos import traer_usuario_logueado,traer_ruta_imagen
from menu_principal import etiquetar_imagenes,ayuda,configuracion,generador_memes,generador_collage
from menu_principal.editar_perfil import EditarPerfil


sg.theme('Black')

class MenuPrincipal:
    def __init__(self):
        """
        Esta interfaz es la principal de la aplicación. Desde aquí se puede acceder a todas las funcionalidades de la aplicación.
        La navegación es posible gracias al diccionario "events" el cual contiene todos los eventos posibles de la interfaz.
        """
        user =traer_usuario_logueado() 
        imagen_path = traer_ruta_imagen(user)
        nick = [
            [sg.Image(filename=imagen_path,pad=(0,0),enable_events=True, key="-EDITAR PERFIL-")],
            [sg.Text(user["alias"],font=("Helvetica", 20),pad=(0,0))]
        ]
        
        menu = [
            [sg.Button("Etiquetar imagenes",key="-ETIQUETAR IMAGENES-")],
            [sg.Button("Generar meme",key="-GENERAR MEME-")],
            [sg.Button("Generar collage",key="-GENERAR COLLAGE-")],   
            [ sg.Button("Salir",key="-SALIR-",size=(15, 2), font=("Helvetica", 14))],
        ]
        configuracion_ayuda = [
            [sg.Button("Configuración", key="-CONFIGURACION-", font=("Helvetica", 10)),sg.Button("Ayuda", key="-AYUDA-", font=("Helvetica", 10))]
        ]

        
        layout = [
            [sg.Column(nick, element_justification="center",vertical_alignment="top", pad=(0, 0)),sg.Column(menu, element_justification="center", vertical_alignment="center", pad=((180, 180), (128, 128))),sg.Column(configuracion_ayuda, element_justification="center", vertical_alignment="top", pad=(0, 0))]
        ]

        

        self.window = sg.Window("Menú principal", layout,size=(1024,768),margins=(64,72), resizable=True, finalize=True)





        self.events = {
            "-AYUDA-": lambda values: ayuda.Ayuda().iniciar(),
            "-ETIQUETAR IMAGENES-":lambda values: etiquetar_imagenes.EtiquetarImagenes().iniciar(),
            "-CONFIGURACION-":lambda values: configuracion.ejecutar(),
            "-GENERAR MEME-": lambda values: generador_memes.GeneradorMemes().iniciar(),
            "-GENERAR COLLAGE-": lambda values: generador_collage.GeneradorCollage().iniciar() ,
            "-EDITAR PERFIL-": lambda values: self.actualizar_imagen(),
        }  
    def actualizar_imagen(self):
        """
        Esta funcion actualiza la imagen de perfil del usuario. al momento de editar el perfil.
        """
        EditarPerfil().iniciar()
        user =traer_usuario_logueado() 
        imagen_path = traer_ruta_imagen(user)
        self.window["-EDITAR PERFIL-"].update(filename=imagen_path)
        
    def iniciar(self):
        mostrar_pantalla(self.window,self.events)


