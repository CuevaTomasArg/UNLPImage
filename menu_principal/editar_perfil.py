import PySimpleGUI as sg
import os
from menu_principal.settings import PERFILES_AVATARS
from menu_principal.acceso_a_datos import traer_usuario_logueado,traer_ruta_imagen,info_de_todos_los_perfiles,guardar_usuario_logueado,actualizar_perfiles

sg.theme("Black")

ruta_perfiles=PERFILES_AVATARS

class EditarPerfil:
    #CONSTRUCTOR 
    def __init__(self):

        self.diccionario=traer_usuario_logueado() 

        self.alias = self.diccionario["alias"]   
        self.nombre = self.diccionario["nombre"]
        self.edad = self.diccionario["edad"]
        self.imagen = self.diccionario["imagen"]
        
        self.ruta_imagen = traer_ruta_imagen(self.diccionario)

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
            [sg.Image(key="-IMAGEN-", filename=self.ruta_imagen)], 
            [sg.Input(key="-ELEGIR ARCHIVO-", enable_events=True, visible=False,default_text=self.diccionario["imagen"]),
            sg.FileBrowse("Seleccionar avatar", tooltip="Extensión valida .png", target="-ELEGIR ARCHIVO-",file_types=[("Archivos PNG", "*.png")],initial_folder=ruta_perfiles)]                      
        ]

        self.layout =[ 
            [sg.Text("Editar Perfil",font="Any 15"),sg.Push(),sg.Button("< Volver",key="-VOLVER-",font="Any 10")],
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
    def evento_edad(self,values):
        ok=False
        if values["-EDAD-"].isdigit() and int(values["-EDAD-"]) > 0:
             ok=True
        else:
            sg.popup("En edad se espera un valor entero positivo.")
        return ok
        

    #METODO
    def evento_chequear(self,values):
        """Esta funcion verifica que todos los campos obligatorios esten llenos.
           En caso de que se cumpla dicha condicion se activa el boton Guardar"""

        if (values['-NOMBRE-'].strip() != "" and values['-EDAD-'].strip() != "" and self.evento_edad(values)):
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

        datos = info_de_todos_los_perfiles()
        for usuario in datos:
            if usuario["alias"] == self.alias:
                usuario["nombre"] = values ["-NOMBRE-"]
                usuario["edad"] = values ["-EDAD-"]
                usuario["genero"]= self.genero
                usuario["imagen"] = values ["-ELEGIR ARCHIVO-"]
                break
        valor_imagen=usuario["imagen"]
        nombre_archivo = os.path.basename(valor_imagen)
        usuario["imagen"]=nombre_archivo  
        guardar_usuario_logueado(usuario)
        actualizar_perfiles(datos)
        sg.popup("Se edito el perfil con exito.")

           
if __name__ =="__main__":
  pantalla = EditarPerfil() 
  pantalla.iniciar() 



      