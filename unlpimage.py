import PySimpleGUI as sg
from menu_principal import inicio as ini, settings

sg.theme('Black')

def crear_layout():
    # partes del layout
    logo_principal = [
        [sg.VPush()],
        [sg.Image(settings.LOGO_UNLPIMAGE , size=(800,210), subsample=2)],
        [sg.VPush()]
        ]

    boton_inferior = [sg.Push(), sg.Button('Empezar', key='-EMPEZAR-'), sg.Push()]

    logos_adicionales = [
        [sg.VPush()],
        [sg.Push(), sg.Image(settings.LOGO_INFORMATICA, size=(80,80), subsample=2),
         sg.Image(settings.LOGO_UNLP, size=(80,80), subsample=2), sg.Push()]
        ]
    
    return [
        [logo_principal],
        [boton_inferior],
        [logos_adicionales]
    ]

def ejecutar():
    
    window = sg.Window('unlpimage', crear_layout(), size=(800,600))
    
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-EMPEZAR-':
            window.close()
            ini.ejecutar()
            break
    
    window.close()

if __name__ == '__main__':
    ejecutar()