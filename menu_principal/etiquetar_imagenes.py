import PySimpleGUI as sg
import datetime
from PIL import Image
import csv
import os
import os.path
from mostrar_pantalla import mostrar_pantalla
from settings import METADATA_DIR


class EtiquetarImagenes:
    def __init__(self):
        self.ruta_repositorio = os.path.normpath(os.getcwd() + "/" +"multimedia")
        archivos = os.listdir(self.ruta_repositorio)
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
        with open(METADATA_DIR,mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            data = [tuple(row) for row in csv_reader]
            data_cleaned = [tupla for tupla in data if tupla]
            for row in data_cleaned:
                if row[0] == values["-LIST-"][0]:
                    info_image = {
                        'nombre del archivo': row[0],
                        'ruta relativa a la imagen': row[1],
                        'texto descriptivo': row[2],
                        'resolucion': row[3],
                        'tamanio': row[4],
                        'tipo': row[5],
                        'lista de tags': row[6],
                        'ultimo perfil que actualizo': row[7],
                        'fecha de última actualizacion': row[8]
                    }
                    break
                
        

        with open(METADATA_DIR,mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            head = next(csv_reader)
            data = [tuple(row) for row in csv_reader]
        data_cleaned = [tupla for tupla in data if tupla]
        tuple_found = None
        for row in data_cleaned:
            
            if row[0] == info_image['nombre del archivo']:
                tuple_found = row
                break
        if tuple_found is None:
            print('not found image')
        else:
            if agree == "-TAG-":
                tag = values['-TAG-']
                current_tags =eval(tuple_found[6]) 
                current_tags.append(tag)
                update_tuple = (tuple_found[0],tuple_found[1],tuple_found[2],tuple_found[3],tuple_found[4],tuple_found[5],current_tags,tuple_found[7],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                index = data_cleaned.index(tuple_found)
                data_cleaned[index] = update_tuple
            elif agree == "-TEXT-":
                description = values['-TEXT-']
                update_tuple = (tuple_found[0],tuple_found[1],description,tuple_found[3],tuple_found[4],tuple_found[5],tuple_found[6],tuple_found[7],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                index = data_cleaned.index(tuple_found)
                data_cleaned[index] = update_tuple
        
        with open(METADATA_DIR,mode="w") as csv_file:
            csv_writer = csv.writer(csv_file,delimiter = ',')
            csv_writer.writerow(head)
            csv_writer.writerows(data_cleaned)
            csv_file.truncate()
            
        self.set_window(values)
    
    def get_imagen_info(self,value_path):
        file_path = os.path.normpath(self.ruta_repositorio + "/" + value_path)

        img = Image.open(file_path)
        width, height = img.size
        size = os.path.getsize(file_path)
        mimetype = Image.MIME[img.format]

        info = {
            'nombre del archivo': value_path,
            'ruta relativa a la imagen': file_path,
            'texto descriptivo': '',
            'resolucion': f'{width}x{height}',
            'tamanio': size,
            'tipo': mimetype,
            'lista de tags': [],
            'ultimo perfil que actualizo': '',
            'fecha de última actualizacion': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.guardar_info(info)
        
        
    
    
    def set_window(self,values):
        
        self.get_imagen_info(values["-LIST-"][0])
        with open(METADATA_DIR,mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            data = [tuple(row) for row in csv_reader]
            data_cleaned = [tupla for tupla in data if tupla]
            for row in data_cleaned:
                if row[0] == values["-LIST-"][0]:
                    info_imagen = {
                        'nombre del archivo': row[0],
                        'ruta relativa a la imagen': row[1],
                        'texto descriptivo': row[2],
                        'resolucion': row[3],
                        'tamanio': row[4],
                        'tipo': row[5],
                        'lista de tags': row[6],
                        'ultimo perfil que actualizo': row[7],
                        'fecha de última actualizacion': row[8]
                    }
                    break
            
        # It is necessary to add the functionality of the last user that updates the image
        self.window['-LAST DATE UPDATE-'].update(info_imagen['fecha de última actualizacion'])
        self.window['-NOMBRE ARCHIVO-'].update(info_imagen['nombre del archivo'])
        self.window['-DESCRIPTION-'].update(info_imagen['texto descriptivo'])
        self.window['-RESOLUCION-'].update(info_imagen['resolucion'])
        self.window['-TAMANIO-'].update(info_imagen['tamanio'])
        print(f"los tags que voy a mostrar son: {info_imagen['lista de tags']}")
        self.window['-VIEW TAGS-'].update(info_imagen['lista de tags'])
        
        
    def guardar_info(self,info):
       
        exist = False
        
        if os.path.exists(METADATA_DIR):
            
            with open(METADATA_DIR, 'r') as archivo_csv:

                
                lector_csv = csv.reader(archivo_csv)

               
                for fila in lector_csv:
                    if info['nombre del archivo'] in fila:
                       
                        exist = True
                        break
            if not exist:
                with open(METADATA_DIR, mode="a", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=info.keys())

                  
                    if os.stat(METADATA_DIR).st_size == 0:
                        
                        writer.writeheader()

                    writer.writerow(info)
        else:
           
            with open(METADATA_DIR, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=info.keys())
                writer.writeheader()
                writer.writerow(info)
                
    def iniciar(self):
        mostrar_pantalla(self.window,self.events)

