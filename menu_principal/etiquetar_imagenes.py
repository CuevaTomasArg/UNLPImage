import PySimpleGUI as sg
import datetime
from PIL import Image
import json
import csv
import os
import os.path
from menu_principal import mostrar_pantalla, settings 
from menu_principal.acceso_a_datos import traer_usuario_logueado,traer_ruta_imagen,cargar_rutas_directorio_imagenes


class EtiquetarImagenes:
    
    def __init__(self):
        """
        Esta interfaz permite etiquetar imagenes. La navegación es posible gracias al diccionario "events" 
        el cual contiene todos los eventos posibles de la interfaz.
        "-LIST-": Permite seleccionar una imagen de la lista de imagenes disponibles.
        "-ADD-": Permite agregar una etiqueta a la imagen seleccionada.
        "-DROP-": Permite quitar una etiqueta a la imagen seleccionada.
        "-ADD TEXT-": Permite agregar una descripción a la imagen seleccionada.
        "-SALIR-": Permite volver al menú principal.
        """
        self.repositorio = cargar_rutas_directorio_imagenes()
        
        diccionario=traer_usuario_logueado() 

        self.alias = diccionario["alias"]   
        
        self.ruta_imagen = traer_ruta_imagen(diccionario)

        archivos = os.listdir(self.repositorio[0])
        selector = [
            [sg.Listbox(values=archivos,size=(30, 6),key='-LIST-',enable_events=True)],
            [sg.Text('Etiquetas:')],
            [sg.Input(key='-TAG-'),sg.Button('Agregar',key='-ADD-')],
            [sg.Input(key='-TAG DROP-'),sg.Button('Quitar',key='-DROP-')],
            [sg.Text('Añade un texto descriptivo')],
            [sg.Input(key='-TEXT-'),sg.Button('Modificar',key='-ADD TEXT-')],
        ]
        visor = [
            [sg.Text('', key='-NOMBRE ARCHIVO-')],
            [sg.Image(key='-IMAGE-')],
            [sg.Text('Descripción:')],
            [sg.Text(key='-DESCRIPTION-')],
            [sg.Text('', key='-TIPO-'),sg.Text(' | '),sg.Text('', key='-RESOLUCION-'),sg.Text(' | '), sg.Text('', key='-TAMANIO-')],
            [sg.Text('Etiquetas:'), sg.Text('', key='-VIEW TAGS-')],   
        ]
        layout = [
            [sg.Text('Etiquetar imagenes'),sg.Button('< Volver',key='-SALIR-')],
            [sg.Column(selector),sg.Column(visor)],
            [sg.Text(' '),sg.Button('Guardar',key='-SAVE-')]
        ]
        self.window =  sg.Window('Etiquetar imagenes', layout, finalize=True, metadata={})
        
        self.events = {
            '-LIST-': lambda values:self.set_window(values), 
            '-ADD-': lambda values:self.add_text(values,"-TAG-"),
            '-ADD TEXT-': lambda values:self.add_text(values,"-TEXT-"),
            '-SAVE-': lambda values:self.upload_metadata(),
            '-DROP-':lambda values:self.drop_tag(values),
        }
    
    def upload_metadata(self):
        """
        Esta función toma los datos de la metadata qu se va actualizando a medida que el usuario agrega
        o quita etiquetas y/o agrega texto descriptivo. Luego, recorre el archivo metadata.csv y busca la tupla
        que corresponde a la imagen seleccionada. Actualiza la tupla con la información ingresada por el usuario
        y guarda la tupla actualizada en el archivo metadata.csv.
        """
        image_save = {
            'ruta_relativa': self.window.metadata['ruta_relativa'],
            'texto descriptivo': self.window.metadata['texto descriptivo'],
            'resolucion': self.window.metadata['resolucion'],
            'tamanio': self.window.metadata['tamanio'],
            'tipo': self.window.metadata['tipo'],
            'lista de tags': self.window.metadata['lista de tags'],
            'ultimo perfil que actualizo': self.alias,
            'ultima aztualizacion': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        data_cleaned = []
        header = None

        with open(settings.METADATA_DIR, mode="r") as metadata_csv:
            csv_reader = csv.reader(metadata_csv)
            data = list(csv_reader)

            if len(data) > 0:
                header = data[0]
                data = data[1:]

            for tupla in data:
                if tupla and tupla[0] == image_save['ruta_relativa']:
                    tupla = tuple(image_save.values())
                data_cleaned.append(tupla)

        if image_save['ruta_relativa'] not in [tupla[0] for tupla in data_cleaned]:
            data_cleaned.append(tuple(image_save.values()))

        with open(settings.METADATA_DIR, mode="w", newline="") as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            if header:
                escritor_csv.writerow(header)
            for tupla in data_cleaned:
                escritor_csv.writerow(tupla)

    
    def drop_tag(self,values):
        """
        Esta función permite quitar una etiqueta a la imagen seleccionada.
        Recorre la lista de etiquetas de la imagen y elimina la etiqueta seleccionada.
        """
        
        image_info = self.window.metadata
        if type(image_info['lista de tags']) == str:
            tags = eval(image_info['lista de tags'])
        else:
            tags = image_info['lista de tags']
            
        for tag in tags:
            if tag.lower().strip() == values['-TAG DROP-'].lower().strip():
                tags.remove(tag)
                sg.popup('Etiqueta eliminada con éxito')
                break
        else:
            sg.popup('No se encuentra la etiqueta a eliminar')
        
        self.window['-VIEW TAGS-'].update(tags)
        self.window.metadata['lista de tags'] = tags
            
    def add_text(self,values,agree):
        """
        Este metodo permite agregar una etiqueta o un texto descriptivo a la imagen seleccionada.
        Estos cambios se guardan en la metadata de la imagen.
        """
        """
        :param values:                      diccionario con los valores de los elementos de la ventana
        :type agree:                        dict
        :param agree:                       "-TAG-","-TEXT-"
        :type agree:                        str
        """
        
        
        image_info = self.window.metadata
        if agree == "-TAG-":
            if type(image_info['lista de tags']) == str:
                tags = eval(image_info['lista de tags'])
                tags.append(values['-TAG-'])
                self.window.metadata['lista de tags'] = tags
                self.window['-VIEW TAGS-'].update(self.window.metadata['lista de tags'])
            else:
                image_info['lista de tags'].append(values['-TAG-'])
                self.window.metadata['lista de tags'] = image_info['lista de tags']
                self.window['-VIEW TAGS-'].update(self.window.metadata['lista de tags'])
        elif agree == "-TEXT-":
            self.window.metadata['texto descriptivo'] = values['-TEXT-']
            self.window['-DESCRIPTION-'].update(values['-TEXT-'])
            
    def get_imagen_info(self,value_path):
        """
        Este metodo toma la información de la imagen seleccionada del archivo "metadata.csv".
        si no encuentra la información de la imagen dentro del archivo, crea un diccionario con la información.
        """
        data = None
        try:
            metadata_csv = open(settings.METADATA_DIR,mode="r")    
        except FileNotFoundError:
            file_ = settings.METADATA_DIR
            metadata_csv = open(file_,mode="w")
            metadata_csv.write("ruta_relativa,texto descriptivo,resolucion,tamanio,tipo,lista de tags,ultimo perfil que actualizo,ultima aztualizacion\n")
            metadata_csv.close()
            metadata_csv = open(settings.METADATA_DIR,mode="r")    
        csv_reader = csv.reader(metadata_csv)
        data = [tuple(row) for row in csv_reader]
        data_cleaned = [tupla for tupla in data if tupla]
        exist = False
        for row in data_cleaned:
            if row[0] == value_path:
                exist = True
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
        if exist:
            return info_imagen
        else:
            file_path = os.path.normpath(self.repositorio[0] + "/" + value_path)
            img = Image.open(file_path)
            width, height = img.size
            size = os.path.getsize(file_path)
            size_kilobytes = size / 1024
            size_megabytes = size_kilobytes / 1024
            mimetype = Image.MIME[img.format]

            info = {
                'ruta_relativa': value_path,
                'texto descriptivo': '',
                'resolucion': f'{width} x {height}',
                'tamanio': f'{size_megabytes} MB',
                'tipo': mimetype,
                'lista de tags': [],
                'ultimo perfil que actualizo': '',             
                'ultima aztualizacion': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            return info

    
    def set_window(self,values):
        """
        Este metodo setea la ventana de la aplicación con la información de la imagen seleccionada.
        Si el archivo seleccionado no es una imagen, se muestra un mensaje de error.
        """
        if values["-LIST-"][0].endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")):
            self.window.metadata = self.get_imagen_info(values["-LIST-"][0])
            path_image = os.path.join(self.repositorio[0],self.window.metadata['ruta_relativa'])
            self.window['-IMAGE-'].update(filename=path_image)
            self.window['-TIPO-'].update(self.window.metadata['tipo'])
            self.window['-NOMBRE ARCHIVO-'].update(self.window.metadata['ruta_relativa'])
            self.window['-DESCRIPTION-'].update(self.window.metadata['texto descriptivo'])
            self.window['-RESOLUCION-'].update(self.window.metadata['resolucion'])
            self.window['-TAMANIO-'].update(self.window.metadata['tamanio'])
            self.window['-TEXT-'].update(self.window.metadata['texto descriptivo'])
            if type(self.window.metadata['lista de tags']) == str:
                tags = eval(self.window.metadata['lista de tags'])
                tags = " ".join(tags)
                self.window['-VIEW TAGS-'].update(tags)
            else:
                tags = " ".join(self.window.metadata['lista de tags'])
                self.window['-VIEW TAGS-'].update(tags)
        else:
            sg.popup('No se puede mostrar el archivo seleccionado porque tiene se ser una imagen')
                
    def iniciar(self):
        mostrar_pantalla.mostrar_pantalla(self.window,self.events)

