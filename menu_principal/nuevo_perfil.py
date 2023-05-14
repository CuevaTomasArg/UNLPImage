import PySimpleGUI as sg
import os 
import json
from menu_principal import inicio as ini
from menu_principal.settings import PERFILES_AVATARS,AVATAR_PREDEFINIDO,PATH_PERFILES
from menu_principal.acceso_a_datos import guardar_perfil_en_base_de_perfiles

sg.theme("Black")

ruta_perfiles=PERFILES_AVATARS
ruta_predefinida=AVATAR_PREDEFINIDO 
tipo_de_archivo = [("PNG (*.png)","*.png")]


class NuevoPerfil:
    def __init__(self):      
        self.usuarios=[]
        self.dicci={}
        self.genero= None
        self.imagen= None
        self.lista = ["Femenino", "Masculino"] 
        
        columna_izquierda = [
            [sg.Text("Nick o Alias")],
            [sg.InputText(key="-ALIAS-",enable_events=True)],
            [sg.Text("Nombre")],
            [sg.InputText(key="-NOMBRE-",enable_events=True)],
            [sg.Text("Edad")],
            [sg.InputText(key="-EDAD-",enable_events=True)],
            [sg.Text("Genero autopercibido")],
            [sg.Combo(self.lista, default_value="Selecciona una opcion", size=(43, 1), key="-COMBO-",enable_events=True)],
            [sg.Radio("Otro", "radio1", key="-OTRO-", size=(10,1))],
            [sg.InputText(default_text="Complete el género", key="-OTROGENERO-",enable_events=True)]
         ]            

        columna_derecha= [
            [sg.Image(key="-IMAGEN-",filename=ruta_predefinida )],                       
            [sg.Input(key="-ELEGIR ARCHIVO-", enable_events=True, visible=False,default_text=ruta_predefinida ),
            sg.FileBrowse("Seleccionar avatar", tooltip="Extensión valida .png", target="-ELEGIR ARCHIVO-", file_types=tipo_de_archivo,initial_folder= ruta_perfiles)]
        ]

        self.layout= [
            [sg.Text("Nuevo Perfil",font="Any 15"),sg.Push(), sg.Button("< Volver",font="Any 10",key="-VOLVER-")],
            [sg.Column(columna_izquierda), 
            sg.Column(columna_derecha)],
            [sg.Push(),sg.Button("Guardar",disabled=True,key="-GUARDAR-")]
        ]

        self.window = sg.Window("",self.layout)
        

    #FUNCION
    def iniciar(self):
        while True:
            event, values = self.window.read()                
            if event == sg.WIN_CLOSED:
                self.window.close()
                ini.ejecutar()
                break
            elif event == "-VOLVER-":
                self.window.close()
                ini.ejecutar()
                break 
            elif event == "-ELEGIR ARCHIVO-":
                self.evento_avatar(values,event)
            elif (event == "-NOMBRE-" or event == "-EDAD-" 
                        or event == "-COMBO-" or event == "-OTRO-" or event == "-OTROGENERO-" 
                        or event =="-ALIAS-"):    
                        if self.evento_alias(values):
                            self.evento_chequear(values)
            elif event == "-GUARDAR-":
                guardar_perfil_en_base_de_perfiles(self.genero, values)
                sg.popup("El usuario fue creado con éxito")
                self.window.close()
                ini.ejecutar()
                break
        self.window.close()
         
      
    #Funcion
    def evento_avatar(self,values,event):
        """Esta funcion actualiza la imagen seleccionada como avatar"""
        
        if values['-ELEGIR ARCHIVO-']:
            self.window['-IMAGEN-'].update(filename=values['-ELEGIR ARCHIVO-'])

    #Funcion
    def evento_edad(self,values):
        ok=False
        if values["-EDAD-"].isdigit() and int(values["-EDAD-"]) > 0:
             ok=True
        else:
            sg.popup("En edad se espera un valor entero positivo.")
        return ok
        

    #Funcion
    def evento_alias(self,values):
        """Esta funcion busca si el alias ya existe en el sistema.
        Si existe, envia un cartel del que usuario ya existe y no permite duplicar alias.
        Retorna true en caso de que exista. Si no existe retorna False"""

        ok=True
        #Si el archivo existe, guardo los datos del archivo json a usuarios, luego le agrego los nuevos datos del dicci
        if os.path.isfile(PATH_PERFILES):
            with open (PATH_PERFILES,"r") as archivo:
                self.usuarios=json.load(archivo)
                valores=[d[list(d.keys())[0]] for d in self.usuarios]    #Guardo en una lista los valores de key
                if values["-ALIAS-"] in valores:                                #Verifico que no exista el alias
                    sg.popup("El alias ya existe en el sistema.")
                    ok:False
        return ok


    #Funcion
    def evento_chequear(self,values):        
        """Esta funcion verifica que todos los campos obligatorios esten llenos.
           En caso de que se cumpla dicha condicion se activa el boton Guardar"""
        
        # Codigo a ejecutar si el campo de entrada no esta vacio o solo contiene espacios en blanco
        if (values["-ALIAS-"].strip() != "" and values["-NOMBRE-"].strip() != "" and values["-EDAD-"].strip() != "" and self.evento_edad(values)):
            if values["-COMBO-"] != "Selecciona una opcion":
                self.genero=values["-COMBO-"]
                self.window["-GUARDAR-"].update(disabled=False)
            else:
                if values["-OTRO-"] == True and values["-OTROGENERO-"] != "Complete el género":
                        self.genero=values["-OTROGENERO-"]
                        self.window["-GUARDAR-"].update(disabled=False)

        #Si no se llenaron los campos (escribi y borre), se inhabilita el boton
        else:
            self.window["-GUARDAR-"].update(disabled=True)
            
 
if __name__ =="__main__":
  pantalla = NuevoPerfil()  
  pantalla.iniciar() 