import PySimpleGUI as sg
from menu_principal import acceso_a_datos as ad, menu, inicio_ver_mas as vm
from menu_principal.nuevo_perfil import NuevoPerfil
from menu_principal.settings import PATH

sg.theme('Black')

PERFILES_POR_PANTALLA = 5

TITULO_TAMANIO = 18

PERFILES_TAMANIO_FUENTE = 17


def crear_boton_e_imagen(usuario, imagen):
    boton = [sg.Text(f'{usuario}', size=(20,1), enable_events= True, font=('Arial', PERFILES_TAMANIO_FUENTE),
                    text_color= 'red',justification='center', tooltip='Seleccionar'),
                    sg.Image(imagen, size=(70,70), subsample=3)]

    return boton


def crear_layout(perfiles_disponibles):
    # partes del layout
    titulo = [sg.Text('Inicio', font=('Helvetica', TITULO_TAMANIO), text_color='blue'), sg.Push()]

    botones_e_imagenes_perfiles = [crear_boton_e_imagen(usuario, imagen)
              for usuario, imagen
              in perfiles_disponibles.items()
              ]
    
    columna_perfiles = [
        [sg.VPush()],
        [sg.Push(),sg.Column(botones_e_imagenes_perfiles), sg.Push()],
        [sg.VPush()]
        ]

    if (ad.calcular_cantidad_de_usuarios()) > PERFILES_POR_PANTALLA:
        botones_inferiores = [[sg.Push(), sg.Button('Agregar Usuario', key='-AGREGAR-'),
        sg.Button('Ver más perfiles', key='-VER_MAS-'), sg.Push()],
        [sg.VPush()]
        ]
    else:
        botones_inferiores = [
            [sg.Push(), sg.Button('Agregar Usuario', key='-AGREGAR-'), sg.Push()],
            [sg.VPush()]
            ]
    
    return [
        [titulo],
        [columna_perfiles],
        [botones_inferiores]
    ]


def ejecutar():
    
    perfiles_disponibles = ad.cargar_varios_perfiles(PERFILES_POR_PANTALLA, 0)

    alias_y_avatars =  ad.cargar_alias_y_avatars(perfiles_disponibles)

    window = sg.Window('unlpimage', crear_layout(alias_y_avatars), size=(800,600))

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
            datos_de_usuario = next((usuario for usuario in perfiles_disponibles if usuario["alias"] == perfil_elegido))
            ad.guardar_usuario_logueado(datos_de_usuario)
            window.close()
            menu.MenuPrincipal().iniciar()
            break
    
    window.close()    
    

if __name__ == '__main__':
    ejecutar()