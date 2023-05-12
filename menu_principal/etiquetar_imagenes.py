import PySimpleGUI as sg
import datetime
from PIL import Image
import json
import csv
import os
import os.path
from menu_principal import mostrar_pantalla, settings 
from menu_principal.acceso_a_datos import traer_usuario_logueado,traer_ruta_imagen


class EtiquetarImagenes:
    
    def __init__(self):
        with open(settings.PATH_CONFIGURACION) as file:
            data = json.load(file)
            
        diccionario=traer_usuario_logueado() #devuelve una lista con un solo usuario

        self.alias = diccionario["alias"]   
        
        self.ruta_imagen = traer_ruta_imagen(diccionario)

        archivos = os.listdir(data['ubicaciones_usuario']["ubicacion_repositorio"])
        selector = [
            [sg.Listbox(values=archivos,size=(30, 6),key='-LIST-',enable_events=True)],
            [sg.Text('Etiquetas:')],
            [sg.Input(key='-TAG-'),sg.Button('Agregar',key='-ADD-')],
            [sg.Text('Añade un texto descriptivo')],
            [sg.Input(key='-TEXT-'),sg.Button('Agregar',key='-ADD TEXT-')],
        ]
        visor = [
            [sg.Text('Ultima fecha de actualización'),sg.Text('', key='-LAST DATE UPDATE-')],
            [sg.Text('', key='-NOMBRE ARCHIVO-')],
            [sg.Text(key='-DESCRIPTION-')],
            [sg.Text('', key='-RESOLUCION-'),sg.Text(' | '), sg.Text('', key='-TAMANIO-')],
            [sg.Text('Etiquetas:'), sg.Text('', key='-VIEW TAGS-')],   
        ]
        layout = [
            [sg.Text('Etiquetar imagenes'),sg.Button('Salir',key='-SALIR-')],
            [sg.Column(selector),sg.Column(visor)],
        ]
        self.window =  sg.Window('Etiquetar imagenes', layout, finalize=True)
        
        self.events = {
            '-LIST-': lambda values:self.set_window(values), 
            '-ADD-': lambda values:self.add_text(values,"-TAG-"),
            '-ADD TEXT-': lambda values:self.add_text(values,"-TEXT-"),
        }
    

    def add_text(self,values,agree):
        self.get_imagen_info(values['-LIST-'][0])
        with open(settings.METADATA_DIR,mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            data = [tuple(row) for row in csv_reader]
            data_cleaned = [tupla for tupla in data if tupla]
            for row in data_cleaned:
                if row[0] == values["-LIST-"][0]:
                    info_image = {
                        'ruta_relativa': row[0],
                        'texto descriptivo': row[1],
                        'resolucion': row[2],
                        'tamanio': row[3],
                        'tipo': row[4],
                        'lista de tags': row[5],
                        'ultimo perfil que actualizo': row[6],
                        'ultima aztualizacion': row[7]
                    }
                    break
                
        

        with open(settings.METADATA_DIR,mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            head = next(csv_reader)
            data = [tuple(row) for row in csv_reader]
        data_cleaned = [tupla for tupla in data if tupla]
        tuple_found = None
        for row in data_cleaned:
            
            if row[0] == info_image['ruta_relativa']:
                tuple_found = row
                break
        if tuple_found is None:
            pass
        else:
            if agree == "-TAG-":
                tag = values['-TAG-']
                current_tags =eval(tuple_found[5]) 
                current_tags.append(tag)
                update_tuple = (tuple_found[0],tuple_found[1],tuple_found[2],tuple_found[3],tuple_found[4],current_tags,self.alias,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                index = data_cleaned.index(tuple_found)
                data_cleaned[index] = update_tuple
            elif agree == "-TEXT-":
                description = values['-TEXT-']
                update_tuple = (tuple_found[0],description,tuple_found[2],tuple_found[3],tuple_found[4],tuple_found[5],self.alias,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                index = data_cleaned.index(tuple_found)
                data_cleaned[index] = update_tuple
        
        with open(settings.METADATA_DIR,mode="w") as csv_file:
            csv_writer = csv.writer(csv_file,delimiter = ',')
            csv_writer.writerow(head)
            csv_writer.writerows(data_cleaned)
            csv_file.truncate()
            
        self.set_window(values)
    
    def get_imagen_info(self,value_path):
        with open(settings.PATH_CONFIGURACION) as file:
            data = json.load(file)
        file_path = os.path.normpath(data['ubicaciones_usuario']["ubicacion_repositorio"] + "/" + value_path)
        try:
            img = Image.open(file_path)
            width, height = img.size
            size = os.path.getsize(file_path)
            mimetype = Image.MIME[img.format]

            info = {
                'ruta_relativa': value_path,
                'texto descriptivo': '',
                'resolucion': f'{width}x{height}',
                'tamanio': size,
                'tipo': mimetype,
                'lista de tags': [],
                'ultimo perfil que actualizo': '',             
                'ultima aztualizacion': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.guardar_info(info)
        except:
            pass
        
        
    
    
    def set_window(self,values):
        info_imagen = None
        try:
            self.get_imagen_info(values["-LIST-"][0])    
            with open(settings.METADATA_DIR,mode="r") as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                data = [tuple(row) for row in csv_reader]
                data_cleaned = [tupla for tupla in data if tupla]
                for row in data_cleaned:
                    if row[0] == values["-LIST-"][0]:
                        info_imagen = {
                            'ruta_relativa': row[0],
                            'texto descriptivo': row[1],
                            'resolucion': row[2],
                            'tamanio': row[3],
                            'tipo': row[4],
                            'lista de tags': row[5],
                            'ultimo perfil que actualizo': row[6],
                            'ultima aztualizacion': row[7]
                        }
                        break
            
        except:
            pass
        if info_imagen is not None:
            self.window['-LAST DATE UPDATE-'].update(info_imagen['ultima aztualizacion'])
            self.window['-NOMBRE ARCHIVO-'].update(info_imagen['ruta_relativa'])
            self.window['-DESCRIPTION-'].update(info_imagen['texto descriptivo'])
            self.window['-RESOLUCION-'].update(info_imagen['resolucion'])
            self.window['-TAMANIO-'].update(info_imagen['tamanio'])
            self.window['-VIEW TAGS-'].update(info_imagen['lista de tags'])
        
    def guardar_info(self,info):
       
        exist = False
        
        if os.path.exists(settings.METADATA_DIR):
            
            with open(settings.METADATA_DIR, 'r') as archivo_csv:

                
                lector_csv = csv.reader(archivo_csv)

               
                for fila in lector_csv:
                    if info['ruta_relativa'] in fila:
                       
                        exist = True
                        break
            if not exist:
                with open(settings.METADATA_DIR, mode="a") as file:
                    writer = csv.DictWriter(file, fieldnames=info.keys())

                  
                    if os.stat(settings.METADATA_DIR).st_size == 0:
                        
                        writer.writeheader()

                    writer.writerow(info)
        else:
           
            with open(settings.METADATA_DIR, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=info.keys())
                writer.writeheader()
                writer.writerow(info)
                
    def iniciar(self):
        mostrar_pantalla.mostrar_pantalla(self.window,self.events)

