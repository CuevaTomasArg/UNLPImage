# UNLPimage
-----------------
El presente proyecto es parte de la metodología de evaluacion de la catedra Seminario de lenguajes opción Python.
Al día de la fecha está siendo desarrollado por 4 estudiantes, incluido yo. A continuación detallaré mis tareas correspondientes hasta el día de la fecha:

## Descripción del proyecto
-----------------------------
El proyecto consiste en la creacion de una aplicacion de escritorio utilizando Python como lenguaje de programación junto con los frameworks PySimpleGUI y Pillow.

## Responsabilidades
----------------------------------
* Desarrollo de la interfaz "Menu principal" la cual tiene el objetivo de ser la interfaz principal, el rol principal de la interfaz está en ser el medio por el cual los usuarios serán capaces de navegarentre las siguientes interfaces:
  * Ayuda
  * Etiquetar imagenes
  * Configuración
  * Editar Perfil
  * Generar collage
  * Generar meme
* Desarrollo de la interfaz "Etiquetar imagen", en la cual, a través de un repositorio de imagenes dado por el usuario, se podrá visualizar las caracteristicas de las imagenes, como resolución, tamaño de bytes, nombre, ruta relativa, etc, y además el usuario podrá agregarle etiquetas a las imagenes para poder clasificarlas, como así también agregarle una descripción a la imagen.

## frameworks y librerias utilizadas hasta el momento
------------------------------------
* Datetime
* Pillow
* PySimpleGUI
* csv
* os
* json
* Pandas
* Numpy
* Wordcloud
* Matplotlib

## Aportes al proyecto
---------------------------------
* Organización: logre aportar una metodología para organizar al grupo que al día de la fecha nos viene ayudando para un desarrollo agil del proyecto
* Desarrollo de código es escalable: Tube la oportunidad de poder tomar desiciones globales dentro del proyecto para que tenga un codigo escalable y correctamente modularizado
* 
## Cómo instalar y ejecutar el proyecto
-------------
El proyecto aprobecha la posibilidad de la creacion de entornos virtuales de Python
```bash
python -m venv venv
```
Luego activaremos dicho entorno:
* En Windows:
```bash
.\venv\Scripts\activate
```
* en macOS y Linux:
```bash
source venv/bin/activate
```
Estando ahí procederemos a intalar los requerimienots necesarios:PySimleGUI==4.60.4 Pillow==9.5.0

## Requerimentos
-----------------------
Para instalar los requerimientos procederemos de la siguiente forma:
```bash
pip install -r requirements.txt
```
Ya estamos listos para correr nuestro entorno.

