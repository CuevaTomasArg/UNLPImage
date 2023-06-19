import PySimpleGUI as sg

def mostrar_pantalla(window,events = dict()):
    """
    Esta funcion permite ejecutar la vista de la ventana que se pasa por parametro como 'window'
    """
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == '-SALIR-': 
            break
        else:
            
            events[event](values)
    window.close()



 