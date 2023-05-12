import PySimpleGUI as sg
from menu_principal import acceso_a_datos as ad

sg.theme('Black')

TITULO_TAMANIO = 15

sg.set_options(font=("Helvetica", 12))


def crear_layout(ruta_repositorio, ruta_collages, ruta_memes):

    titulo = [sg.Text('Configuracion', font=('Arial Bold', TITULO_TAMANIO), text_color='blue'), sg.Push()]

    datos_imagenes = [sg.Text('Ubicacion actual = '), sg.Text(ruta_repositorio, size=(100,1), key='-TEXTO_REPO-'),
    sg.In(enable_events=True, key='-REPOSITORIO-', visible=False), sg.FolderBrowse('Cambiar')]

    datos_collages = [sg.Text('Ubicacion actual = '), sg.Text(ruta_collages, size=(100,1), key='-TEXTO_COLLAGES-'),
    sg.In(enable_events=True, key='-COLLAGES-', visible=False), sg.FolderBrowse('Cambiar')]

    datos_memes = [sg.Text('Ubicacion actual = '), sg.Text(ruta_memes, size=(100,1), key='-TEXTO_MEMES-'),
    sg.In(enable_events=True, key='-MEMES-', visible=False), sg.FolderBrowse('Cambiar')]

    datos = [
    [sg.Frame('Repositorio de imágenes', [datos_imagenes], title_color='grey')],
    [sg.Frame('Almacenamiento de collages', [datos_collages], title_color='grey')],
    [sg.Frame('Almacenamiento de memes', [datos_memes], title_color='grey')]
    ]

    botones = [sg.Push(),
    sg.Button('Guardar cambios', key='-GUARDAR-'),
    sg.Button('Valores por defecto', key='-POR_DEFECTO-'), sg.Button('Salir'),
    sg.Push()
    ]

    return [
        [titulo],
        [datos],
        [botones]
    ]

def ejecutar():

    ruta_repositorio, ruta_collages, ruta_memes = ad.cargar_rutas_directorio_imagenes()

    usuario_logueado = ad.traer_usuario_logueado()

    window = sg.Window('unlpimage', crear_layout(ruta_repositorio, ruta_collages, ruta_memes))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break
    
        if event == '-REPOSITORIO-':
            ruta_repositorio = values['-REPOSITORIO-']
            window['-TEXTO_REPO-'].update(ruta_repositorio)

        if event == '-COLLAGES-':
            ruta_collages = values['-COLLAGES-']
            window['-TEXTO_COLLAGES-'].update(ruta_collages)
        if event == '-MEMES-':
            ruta_memes = values['-MEMES-']
            window['-TEXTO_MEMES-'].update(ruta_memes)

        if event == '-GUARDAR-':
            ad.guardar_rutas_directorio_imagenes(ruta_repositorio, ruta_collages, ruta_memes)
            ad.registrar_accion_de_usuario(usuario_logueado['alias'], "Cambio en rutas de imagenes")

        if event == '-POR_DEFECTO-':
            ruta_repositorio, ruta_collages, ruta_memes = ad.restaurar_rutas_por_defecto()
            window['-TEXTO_REPO-'].update(ruta_repositorio)
            window['-TEXTO_COLLAGES-'].update(ruta_collages)
            window['-TEXTO_MEMES-'].update(ruta_memes)
            ad.registrar_accion_de_usuario(usuario_logueado['alias'], "Valores por defecto en rutas de imagenes")

    window.close()


if __name__ == '__main__':
    ejecutar()