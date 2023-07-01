import PySimpleGUI as sg

def entero_positivo(values): 
    """Chequea si que la edad sea un valor entero positivo
    mayor a cero"""

    cumple=False
    if values["-EDAD-"].isdigit() and int(values["-EDAD-"]) > 0:
        cumple=True
    else:
        sg.popup("En edad se espera un valor entero positivo.")
    return cumple

def validar_usuario(values):
    """Chequea que los campos no esten vacios y que
    la edad sea un numero entero positivo mayor a cero"""
  
    cumple=False
    if (values["-ALIAS-"].strip() != "" and 
        values["-NOMBRE-"].strip() != "" and
        values["-EDAD-"].strip() != "" and entero_positivo(values)):
        cumple=True
    return cumple
        
def validar_usuario_sin_alias(values):
    """Chequea que los campos no esten vacios y que
    la edad sea un numero entero positivo mayor a cero"""

    cumple=False
    if (values['-NOMBRE-'].strip() != ""
        and values['-EDAD-'].strip() != "" 
        and entero_positivo(values)):
        cumple=True
    return cumple
