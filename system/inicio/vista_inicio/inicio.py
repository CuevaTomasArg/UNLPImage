import PySimpleGUI as sg

from compartidos.acceso_a_datos import guardar_usuario_logueado

from ...menu_principal.vista_menu_principal.menu import MenuPrincipal
from ...perfil.vista_perfil.nuevo_perfil import NuevoPerfil
from .. import acceso_a_datos_inicio as adi
from .. import settings_inicio as sini
from . import inicio_ver_mas as vm

sg.theme(sini.COLOR_PYSIMPLEGUI)

def crear_boton_e_imagen(usuario, imagen):
    '''
    Crea un boton con el nombre del usuario y un boton con la imagen de su avatar

    Parametros:
    usuario (string): el alias del usuario
    imagen (string): la ubicacion donde se almacena la imagen del avatar

    Retorna:
    boton usuario y boton imagen
    '''
    boton = [
        sg.Text(
            f'{usuario}',
            size=(20, 1),
            enable_events=True,
            font=('Arial', 17),
            text_color='red',
            justification='center',
            tooltip='Seleccionar',
        ),
        sg.Image(imagen, size=(70, 70), subsample=3),
    ]

    return boton


def crear_layout(perfiles_disponibles):
    '''
    Crea el layout para la pantalla a partir de los perfiles disponibles

    Parametros:
    perfiles_disponibles = {
        un_alias (string): una ruta a su avatar,
        otro_alias (string): otra ruta a su avatar,
        otro_alias (string): otra ruta a su avatar
        }

    Retorna:
    layout para la pantalla
    '''
    # partes del layout
    titulo = [sg.Text('Inicio', font=('Helvetica', 18), text_color='blue'), sg.Push()]

    botones_e_imagenes_perfiles = [
        crear_boton_e_imagen(usuario, imagen)
        for usuario, imagen in perfiles_disponibles.items()
    ]

    columna_perfiles = [
        [sg.VPush()],
        [sg.Push(), sg.Column(botones_e_imagenes_perfiles), sg.Push()],
        [sg.VPush()],
    ]

    if (adi.calcular_cantidad_de_usuarios()) > sini.PERFILES_POR_PANTALLA:
        botones_inferiores = [
            [
                sg.Push(),
                sg.Button('Agregar Usuario', key='-AGREGAR-'),
                sg.Button('Ver más perfiles', key='-VER_MAS-'),
                sg.Push(),
            ],
            [sg.VPush()],
        ]
    else:
        botones_inferiores = [
            [sg.Push(), sg.Button('Agregar Usuario', key='-AGREGAR-'), sg.Push()],
            [sg.VPush()],
        ]

    return [[titulo], [columna_perfiles], [botones_inferiores]]


def ejecutar():
    perfiles_disponibles = adi.cargar_varios_perfiles(sini.PERFILES_POR_PANTALLA, 0)

    alias_y_avatars = adi.cargar_alias_y_avatars(perfiles_disponibles)

    window = sg.Window('unlpimage', crear_layout(alias_y_avatars), size=(800, 600))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
            break
        if '-AGREGAR-' in event:
            window.close()
            NuevoPerfil().iniciar()
            break
        if '-VER_MAS-' in event:
            window.close()
            vm.ejecutar()
            break
        if event in alias_y_avatars:
            perfil_elegido = event
            datos_de_usuario = next(
                (
                    usuario
                    for usuario in perfiles_disponibles
                    if usuario["alias"] == perfil_elegido
                )
            )
            guardar_usuario_logueado(datos_de_usuario)
            window.close()
            MenuPrincipal().iniciar()
            break

    window.close()


if __name__ == '__main__':
    ejecutar()