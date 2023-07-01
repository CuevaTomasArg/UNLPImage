from compartidos.acceso_a_datos import (
    info_de_todos_los_perfiles,
    traer_ruta_imagen_avatar,
)


def cargar_varios_perfiles(cantidad_a_cargar, desde_posicion):
    """
    Devuelve una lista de diccionarios con la informacion de la cantidad
    de usuarios solicitados, o los que haya si no se llega a esa cantidad de usuarios.

    Parametros:
    cantidad_a_cargar: cantidad de usuarios solicitados
    desde_posicion: posición de usuario en el archivo de perfiles desde
    la que se solicita informacion

    Retorno:
    varios_perfiles = [
        {
            alias (string): un alias,
            nombre (string): un nombre,
            edad (int): una edad,
            genero (string): un genero,
            imagen (string): nombre del archivo de imagen avatar del perfil
        }
    ]
    """
    perfiles = info_de_todos_los_perfiles()
    hasta_posicion = desde_posicion + cantidad_a_cargar
    varios_perfiles = perfiles[desde_posicion:hasta_posicion]
    return varios_perfiles


def cargar_alias_y_avatars(varios_perfiles):
    """Recibe una lista de diccionarios de usuarios y retorna un diccionario,
    donde sus claves son los nombres usuarios y sus valores la ruta donde se almacena
    la imagen de ese perfil de usuario:

    Parametro:
    varios_perfiles = [
        {
            alias (string): un alias,
            nombre (string): un nombre,
            edad (int): una edad,
            genero (string): un genero,
            imagen (string): nombre del archivo de imagen avatar del perfil
        }
    ]

    Retorno:
    alias_y_avatars = {
        un_alias (string): una ruta a su avatar,
        otro_alias (string): otra ruta a su avatar,
        }"""
    alias = [
        perfil["alias"]
        for perfil
        in varios_perfiles
        ]

    rutas_imagenes_avatars = list(map(traer_ruta_imagen_avatar, varios_perfiles))

    alias_y_avatars = {
        alias: ruta_a_su_avatar
        for alias, ruta_a_su_avatar
        in zip(alias, rutas_imagenes_avatars)
    }

    return alias_y_avatars


def calcular_cantidad_de_usuarios():
    """Retorna la cantidad de perfiles almacenados por la aplicacion"""
    return len(info_de_todos_los_perfiles())
