import PySimpleGUI as sg
from . import menu, acceso_a_datos as ad, nuevo_perfil
from menu_principal import inicio as ini

sg.theme('Black')

PERFILES_POR_PANTALLA = 5
PERFILES_TAMANIO_FUENTE = 17


def crear_boton_e_imagen(usuario, imagen):
    boton = [sg.Text(f'{usuario}', size=(20,1), enable_events= True, font=('Helvetica', PERFILES_TAMANIO_FUENTE),
                    text_color= 'red',justification='center', tooltip='Seleccionar'),
                    sg.Image(imagen, size=(70,70), subsample=3)]

    return boton


def crear_layout(perfiles_disponibles):

    botones_superiores = [
        [sg.VPush()],
        [sg.Button('< Anterior', key='-ANTERIOR-'), sg.Push()]
        ]

    botones_e_imagenes_perfiles = [crear_boton_e_imagen(usuario, imagen)
              for usuario, imagen
              in perfiles_disponibles.items()
              ]
    
    columna_perfiles = [
        [sg.VPush()],
        [sg.Push(),sg.Column(botones_e_imagenes_perfiles), sg.Push()],
        [sg.VPush()]
        ]

    botones_inferiores = [
            [sg.Push(), sg.Button('Agregar Usuario', key='-AGREGAR-'), sg.Push()],
            [sg.VPush()]
            ]
    
    return [
        [botones_superiores],
        [columna_perfiles],
        [botones_inferiores]
    ]

def ejecutar():
    perfiles_disponibles = ad.cargar_varios_perfiles(PERFILES_POR_PANTALLA, 5)

    alias_y_avatars =  ad.cargar_alias_y_avatars(perfiles_disponibles)

    window = sg.Window('unlpimage', crear_layout(alias_y_avatars), size=(800,600))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if '-AGREGAR-' in event:
            window.close()
            nuevo_perfil.NuevoPerfil().iniciar() 
            break
        if '-ANTERIOR-' in event:
            window.close()
            ini.ejecutar()
            break
        if event in alias_y_avatars:
            perfil_elegido = event
            datos_de_usuario = next((usuario for usuario in perfiles_disponibles if usuario["alias"] == perfil_elegido))
            ad.guardar_usuario_logueado(datos_de_usuario)
            window.close()
            menu.MenuPrincipal().iniciar()
            break

    window.close()

if __name__ == '__main__':
    ejecutar()