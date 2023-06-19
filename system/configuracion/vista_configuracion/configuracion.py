import PySimpleGUI as sg

from compartidos.acceso_a_datos import (
    cargar_rutas_directorio_imagenes,
    registrar_accion_de_usuario,
    traer_usuario_logueado,
)

from .. import acceso_a_datos_configuracion as adc
from .. import settings_config as sconf

sg.theme('Black')

sg.set_options(font=('Helvetica', 12))


def crear_layout(ruta_repositorio, ruta_collages, ruta_memes):
    '''
    Crea el layout para la pantalla

    Parametros:
    Parametros:
    ruta_repositorio (string): ruta de directorio donde se guardan las imágenes
    del repositorio
    ruta_collages (string): ruta de directorio donde se guardan los collages generados
    ruta_memes (string): ruta de directorio donde se guardan los memes generados
    '''

    titulo = [
        sg.Text(
            'Configuracion',
            font=('Arial Bold', sconf.TITULO_TAMANIO),
            text_color='blue',
        ),
        sg.Push(),
    ]

    datos_imagenes = [
        sg.Text('Ubicacion actual = '),
        sg.Text(ruta_repositorio, size=(100, 1), key='-TEXTO_REPO-'),
        sg.In(enable_events=True, key='-REPOSITORIO-', visible=False),
        sg.FolderBrowse('Cambiar'),
    ]

    datos_collages = [
        sg.Text('Ubicacion actual = '),
        sg.Text(ruta_collages, size=(100, 1), key='-TEXTO_COLLAGES-'),
        sg.In(enable_events=True, key='-COLLAGES-', visible=False),
        sg.FolderBrowse('Cambiar'),
    ]

    datos_memes = [
        sg.Text('Ubicacion actual = '),
        sg.Text(ruta_memes, size=(100, 1), key='-TEXTO_MEMES-'),
        sg.In(enable_events=True, key='-MEMES-', visible=False),
        sg.FolderBrowse('Cambiar'),
    ]

    datos = [
        [
            sg.Frame(
                'Repositorio de imágenes',
                [datos_imagenes],
                title_color=sconf.COLOR_TEXTO,
            )
        ],
        [
            sg.Frame(
                'Almacenamiento de collages',
                [datos_collages],
                title_color=sconf.COLOR_TEXTO,
            )
        ],
        [
            sg.Frame(
                'Almacenamiento de memes', [datos_memes], title_color=sconf.COLOR_TEXTO
            )
        ],
    ]

    botones = [
        sg.Push(),
        sg.Button('Guardar ubicaciones modificadas', key='-GUARDAR-'),
        sg.Button('Restaurar ubicaciones por defecto', key='-POR_DEFECTO-'),
        sg.Button('Salir'),
        sg.Push(),
    ]

    return [[titulo], [datos], [botones]]


def ejecutar():
    ruta_repositorio, ruta_collages, ruta_memes = cargar_rutas_directorio_imagenes()

    usuario_logueado = traer_usuario_logueado()

    window = sg.Window(
        'unlpimage', crear_layout(ruta_repositorio, ruta_collages, ruta_memes)
    )

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
            adc.guardar_rutas_directorio_imagenes(
                ruta_repositorio, ruta_collages, ruta_memes
            )
            registrar_accion_de_usuario(
                usuario_logueado['alias'], sconf.MENSAJE_MODIFICACION
            )
            sg.popup('Se guardan las ubicaciones del usuario')

        if event == '-POR_DEFECTO-':
            (
                ruta_repositorio,
                ruta_collages,
                ruta_memes,
            ) = adc.restaurar_rutas_por_defecto()
            window['-TEXTO_REPO-'].update(ruta_repositorio)
            window['-TEXTO_COLLAGES-'].update(ruta_collages)
            window['-TEXTO_MEMES-'].update(ruta_memes)
            registrar_accion_de_usuario(
                usuario_logueado['alias'], sconf.MENSAJE_MODIFICACION
            )
            sg.popup('Se restauran las ubicaciones por defecto')

    window.close()


if __name__ == '__main__':
    ejecutar()
