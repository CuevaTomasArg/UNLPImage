import PySimpleGUI as sg
from PIL import Image
import os
import io
from menu_principal.settings import FUENTE_IMAGENES_POR_DEFECTO,GUARDADO_COLLAGES_POR_DEFECTO

sg.theme("Black")
ruta_imagenes=FUENTE_IMAGENES_POR_DEFECTO
ruta_nuevo_collage=GUARDADO_COLLAGES_POR_DEFECTO


class GeneradorCollage:
    #CONSTRUCTOR 
    def __init__(self):   
        self.layout = [ 
                        [sg.Text("Generador de Collage",font='Any 15')],
                        [sg.Column([[sg.Text("Imágenes seleccionadas:")], [sg.Listbox(values=[], size=(40, 10), key='-LISTA-')]])],
                        [sg.Input(key="-ELEGIR ARCHIVO-", enable_events=True, visible=False),
                        sg.FileBrowse("Seleccionar Imagen", target="-ELEGIR ARCHIVO-",file_types=(("Archivos PNG", "*.png"),("JPEG", "*.jpg")),initial_folder=ruta_imagenes)], #ruta_memes)],
                        [sg.Button("Guardar", key="-GUARDAR-", disabled=True)],
                        [sg.Image(key="-IMAGEN-")]                      
                      ]

        self.window=sg.Window('',self.layout)

        self.imagenes=[]


    #METODO
    def iniciar(self):    
        while True:
            event,values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                self.window.close()
                break
            elif event =="-ELEGIR ARCHIVO-":
                self.evento_elegir_archivo(values)
            elif event == "-GUARDAR-":
                self.evento_guardar()
                self.window.close()

    #METODO
    def evento_elegir_archivo(self, values):   
        """"Esta funcion va guardando en una lista las imagenes seleccionadas por el usuario
        para a futuro formar un collage"""

        filename = values["-ELEGIR ARCHIVO-"]
        self.imagenes.append(filename)
        self.window['-LISTA-'].update(self.imagenes)
        self.window["-GUARDAR-"].update(disabled=False) # Habilitar el botón de guardar

    #METODO
    def evento_guardar(self): 
        """"Esta funcion itera sobre la lista de imagenes para ir pegandolas en 
        el collage y luego las imagenes PNG las transforma en Bytes"""

        width, height = 800, 600 # Define el tamaño del collage (en píxeles)
        collage = Image.new('RGB', (width, height)) # Crea una imagen en blanco para el collage
        #Define las coordenadas de la esquina superior izquierda de cada imagen en el collage
        coords = [(0, 0), (width//2, 0), (0, height//2), (width//2, height//2)]
        #Itera sobre cada imagen y pégala en el collage en la posición correspondiente
        for i in range(len(self.imagenes)):
            img = Image.open(self.imagenes[i])
            img = img.resize((width//2, height//2))  # Redimensiona la imagen para que encaje en el collage
            collage.paste(img, coords[i])
        imagen_bytes = io.BytesIO()
        self.guardar_collage(collage,imagen_bytes)


    #METODO
    def guardar_collage(self,collage,imagen_bytes):
        """"Esta funcion muestra en una segunda ventana como queda el collage y guarda 
        en el archivo json las imagenes transformadas en Bytes """

        contador_nuevo_collage=1

        collage.save(imagen_bytes,format="PNG")
        window2 = sg.Window("Collage generado", [[sg.Image(data=imagen_bytes.getvalue())]],keep_on_top=True)    
        event, values = window2.read()
        window2.close()

        while True:
            nuevo_nombre=f"collage({contador_nuevo_collage}).png"
            if not os.path.exists(os.path.join(ruta_nuevo_collage, nuevo_nombre)):
                collage.save(os.path.join(ruta_nuevo_collage, nuevo_nombre)) # Guarda el collage en un archivo
                break
            else:
                contador_nuevo_collage += 1


if __name__ =="__main__":
  pantalla = GeneradorCollage() 
  pantalla.iniciar() # llama al metodo iniciar de esta clase
        