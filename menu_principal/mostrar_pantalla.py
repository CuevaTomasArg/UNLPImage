import PySimpleGUI as sg


def mostrar_pantalla(window,events = dict()):
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == '-SALIR-': 
            break
        else:
            
            events[event](values)
    window.close()



 