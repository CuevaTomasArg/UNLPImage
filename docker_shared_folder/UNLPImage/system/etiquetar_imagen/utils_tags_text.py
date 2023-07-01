from PySimpleGUI import popup

def delete_tag(image_info, values, window):
    """
    Elimina una etiqueta de la lista de etiquetas de la imagen.

    Parameters:
        image_info (dict): Información de la imagen.
        values (dict): Valores de los elementos de la interfaz.
        window (sg.Window): Ventana de la interfaz.

    Raises:
        None

    Returns:
        None
    """
    if isinstance(image_info['lista de tags'], str):
        tags = eval(image_info['lista de tags'])
    else:
        tags = image_info['lista de tags']

    for tag in tags:
        if tag.lower().strip() == values['-TAG DROP-'].lower().strip():
            tags.remove(tag)
            popup('Etiqueta eliminada con éxito')
            break
    else:
        popup('No se encuentra la etiqueta a eliminar')

    window['-VIEW TAGS-'].update(' '.join(tags))
    window.metadata['lista de tags'] = tags


def append_text(values, agree, window):
    """
    Agrega texto (etiqueta o descripción) a la imagen.

    Parameters:
        values (dict): Valores de los elementos de la interfaz.
        agree (str): Elección del usuario ("-TAG-" para agregar etiqueta, "-TEXT-" para agregar descripción).
        window (sg.Window): Ventana de la interfaz.

    Raises:
        None

    Returns:
        None
    """
    image_info = window.metadata
    if agree == "-TAG-":
        if isinstance(image_info['lista de tags'], str):
            tags = eval(image_info['lista de tags'])
            tags.append(values['-TAG-'])
            window.metadata['lista de tags'] = tags
            window['-VIEW TAGS-'].update(' '.join(window.metadata['lista de tags']))
        else:
            image_info['lista de tags'].append(values['-TAG-'])
            window.metadata['lista de tags'] = image_info['lista de tags']
            window['-VIEW TAGS-'].update(' '.join(window.metadata['lista de tags']))
    elif agree == "-TEXT-":
        window.metadata['texto descriptivo'] = values['-TEXT-']
        window['-DESCRIPTION-'].update(values['-TEXT-'])
