import PySimpleGUI as sg
import os
import io
from PIL import Image, ImageDraw, ImageFont
from menu_principal import settings

sg.theme("Black")

ruta_imagenes=settings.FUENTE_IMAGENES_POR_DEFECTO
ruta_nuevos_memes=settings.GUARDADO_MEMES_POR_DEFECTO

class GeneradorMemes:
    #CONSTRUCTOR 
    def __init__(self):    
        self.layout = [  
            [sg.Text( "Generador de Memes",font="Any 15")],
            [sg.Input( key="-ELEGIR ARCHIVO-", enable_events=True, visible=False),
            sg.FileBrowse( "Seleccionar Imagen", target="-ELEGIR ARCHIVO-",file_types=(("Archivos PNG", "*.png"),("JPEG", "*.jpg")),initial_folder=ruta_imagenes)],
            [sg.Text( "Texto a añadir:")],
            [sg.Input( key="-TEXTO-", enable_events=True, size=(30,1))],
            [sg.Button( "Guardar", key="-GUARDAR-", disabled=True)],
            [sg.Image(key="-IMAGEN-")]                       
        ]
        
        self.window=sg.Window('',self.layout)

        self.imagen = None 

        self.texto=""


    #METODO
    def iniciar(self):    
        while True:
            event,values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                self.window.close()
                break
            elif event == "-TEXTO-":
                self.evento_editar_imagen_con_texto(values)
            elif event =="-ELEGIR ARCHIVO-":
                self.evento_elegir_archivo(values)
            elif event == "-GUARDAR-":
                self.evento_guardar()


    #METODO
    def evento_elegir_archivo(self, values ):
        """"Esta funcion guarda en la variable filename el valor del archivo de imagen seleccionado.
        Calcula el tamaño de la imagen para colocar el texto abajo y al medio """

        filename = values["-ELEGIR ARCHIVO-"]
        self.imagen = Image.open(filename) # Cargar la imagen seleccionada
        editor_img = ImageDraw.Draw(self.imagen) #edita imagen
        fuente = ImageFont.truetype("arial.ttf", 36) # Seleccionar la fuente y el tamaño del texto
       
        image_width, image_height = self.imagen.size #obtenemos la dimension de la imagen
        text_width, text_height = fuente.getsize(self.texto)  #obtenemos la dimension del texto
        #calculamos la posicion del texto
        texto_x = (image_width - text_width) // 2
        texto_y = image_height - text_height - 10
        editor_img.text((texto_x, texto_y), self.texto, font=fuente, fill=(255,255,255,255))   #dibujamos el texto en la posicion calculada

        # Mostrar la imagen resultante en ventana
        imagen_bytes = io.BytesIO()
        self.imagen.save(imagen_bytes, format="PNG")
        self.window["-IMAGEN-"].update(data=imagen_bytes.getvalue())
        self.window["-GUARDAR-"].update(disabled=False) # Habilita botón guardar

        
    #METODO
    def evento_guardar(self): 
        """Esta funcion guarda en el archivo json las imagenes modificadas con texto y
         emite una ventana en el caso de la carga fuera exitosa."""
        
        contador_nueva_imagen = 1 
        while True:
            nuevo_nombre = f"meme({contador_nueva_imagen}).png"
            if not os.path.exists(os.path.join(ruta_nuevos_memes, nuevo_nombre)):
                self.imagen.save(os.path.join(ruta_nuevos_memes, nuevo_nombre))
                break
            else:
                contador_nueva_imagen += 1     
        sg.popup("Imagen Guardada Con Exito")

    #METODO
    def evento_editar_imagen_con_texto(self,values):
        """Esta funcion permite esxribir texto para luego y si se selecciona una imagen se llama
        a la funcion evento_elegir_archivo para que la imagen sea editada con el texto ingresado"""

        self.texto= values["-TEXTO-"]
        if values["-ELEGIR ARCHIVO-"]:
            self.evento_elegir_archivo(values)

  
if __name__ =="__main__":
  pantalla = GeneradorMemes()  
  pantalla.iniciar() 
