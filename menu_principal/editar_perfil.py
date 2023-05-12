import PySimpleGUI as sg
#import json
import os
from menu_principal import settings
from menu_principal import acceso_a_datos as ad

sg.theme("Black")

ruta_perfiles=settings.PERFILES_AVATARS

class EditarPerfil:
    #CONSTRUCTOR 
    def __init__(self):

        self.diccionario=ad.traer_usuario_logueado() #devuelve una lista con un solo usuario

        self.alias = self.diccionario["alias"]   
        self.nombre = self.diccionario['nombre']
        self.edad = self.diccionario['edad']
        self.imagen = self.diccionario['imagen']
        
        self.ruta_imagen = ad.traer_ruta_imagen(self.diccionario)

        self.lista = ["Femenino", "Masculino"]

        columna_izquierda =[
            [sg.Text("Nick o Alias")],
            [sg.InputText(key="-ALIAS-",default_text=self.alias,disabled=True,text_color="black",)], 
            [sg.Text("Nombre")],
            [sg.InputText(key="-NOMBRE-",default_text=self.nombre,enable_events=True)],
            [sg.Text("Edad")],
            [sg.InputText(key="-EDAD-",default_text=self.edad,enable_events=True)],
            [sg.Text('')],
            [sg.Combo(self.lista, default_value="Selecciona una opcion", size=(43, 1),key="-COMBO-",enable_events=True)],
            [sg.Radio("Otro","radio1", key="-RADIO-", size=(10,1))],
            [sg.InputText(default_text="Complete el género", key="-OTRO GENERO-",enable_events=True)],
        ]

        columna_derecha =[   
            [sg.Image(key="-IMAGEN-", filename=self.ruta_imagen)],#self.diccionario["imagen"])],  
            [sg.Input(key="-ELEGIR ARCHIVO-", enable_events=True, visible=False,default_text=self.diccionario["imagen"]), 
            sg.FileBrowse("Seleccionar avatar", target="-ELEGIR ARCHIVO-",file_types=(("Archivos PNG", "*.png"),("JPEG", "*.jpg")),initial_folder=ruta_perfiles)]                      
        ]

        self.layout =[ 
            [sg.Text("Editar Perfil",font='Any 15'),sg.Push(),sg.Button("< Volver",key="-VOLVER-",font="Any 10")],
            [sg.Column(columna_izquierda),sg.Column(columna_derecha)],
            [sg.Push(),sg.Button("Guardar",key="-GUARDAR-", disabled=True)]                   
        ]


        self.window=sg.Window('',self.layout,finalize=True)


        if self.diccionario["genero"] == "Femenino" or self.diccionario["genero"] == "Masculino":
            self.window["-COMBO-"].update(value=self.diccionario["genero"])
        else:
            self.window["-OTRO GENERO-"].update(value=self.diccionario["genero"])
            self.window["-RADIO-"].update(True)

        self.diccionario={} 

        self.genero=None


    #METODO
    def iniciar(self):    
        while True:
            event,values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                self.window.close()
                break
            elif event == "-VOLVER-":
                 self.window.close()
            elif event == "-ELEGIR ARCHIVO-":
                self.evento_avatar(values)
            elif (event == "-NOMBRE-" or event == "-EDAD-" 
                or event == "-COMBO-" or event == "-OTRO GENERO-"):     
                self.evento_chequear(values)                   
            elif event == "-GUARDAR-":
                self.eventos_guardar_datos(values)
                self.window.close()
    

    #METODO
    def evento_avatar(self,values):
        """Esta funcion actualiza la imagen seleccionada como avatar """

        self.window["-GUARDAR-"].update(disabled=False)
        if values["-ELEGIR ARCHIVO-"]:
            self.window["-IMAGEN-"].update(filename=values["-ELEGIR ARCHIVO-"])
        

    #METODO
    def evento_chequear(self,values):
        """Esta funcion verifica que todos los campos obligatorios esten llenos.
           En caso de que se cumpla dicha condicion se activa el boton Guardar"""

        if (values['-NOMBRE-'].strip() != "" and values['-EDAD-'].strip() != ""):
            self.window["-GUARDAR-"].update(disabled=False)
            if values["-COMBO-"] != "Selecciona una opcion":
                self.genero = values["-COMBO-"]
                self.window["-GUARDAR-"].update(disabled=False) 
            else:
                if values["-RADIO-"] == True and values["-OTRO GENERO-"] != "Complete el género": 
                    self.genero = values["-OTRO GENERO-"]
                    self.window["-GUARDAR-"].update(disabled=False)    
        else:
           self.window["-GUARDAR-"].update(disabled=True) 


    #METODO
    def eventos_guardar_datos(self,values):
        """Esta funcion guarda los datos en el archivo json"""

        # with open(settings.PATH_PERFILES) as archivo:
        #     datos=json.load(archivo)
        datos = ad.info_de_todos_los_perfiles()
        for usuario in datos:
            if usuario["alias"] == self.alias:
                usuario["nombre"] = values ["-NOMBRE-"]
                usuario["edad"] = values ["-EDAD-"]
                usuario["genero"]= self.genero
                usuario["imagen"] = values ["-ELEGIR ARCHIVO-"]
                break
        valor_imagen=usuario["imagen"]
        # nombre_archivo=valor_imagen.replace(settings.PERFILES_AVATARS,"")
        # nombre_archivo=nombre_archivo.replace(nombre_archivo[0],"")
        nombre_archivo = os.path.basename(valor_imagen)
        usuario["imagen"]=nombre_archivo  
        ad.guardar_usuario_logueado(usuario)

        # with open(settings.PATH_PERFILES,"w") as archivo:
        #     json.dump(datos,archivo)
        ad.actualizar_perfiles(datos)
        sg.popup("Se edito el perfil con exito.")

            
if __name__ =="__main__":
  pantalla = EditarPerfil() 
  pantalla.iniciar() 



      