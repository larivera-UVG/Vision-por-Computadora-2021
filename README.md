# Vision-por-Computadora-2021
Algoritmos y sistemas de visión por computadora para aplicaciones de robótica de enjambre. (*Versión únicamente de Matlab y pruebas en Python.*)

![](José%20Ignacio%20Ramírez/Códigos/Matlab/logo002.png)

### Features

- Permite generar imágenes de identificadores utilizados para marcar a los agentes.
- Permite calibrar la cámara automática o manualmente para tener únicamente el área de trabajo en la imagen.
- Permite obtener la pose de los agentes * **on demand** * o en tiempo real.

**Tabla de Contenidos**

[TOCM]

[TOC]

#Matlab

Aquí se mostrará toda la información de la herramienta desarrollada en Matlab.

##Dependencias
Para la funcionalidad de estos programas, se necesita de las siguientes *toolboxes* instaladas en Matlab:
- [MATLAB Support Package for USB Webcams](https://www.mathworks.com/matlabcentral/fileexchange/45182-matlab-support-package-for-usb-webcams "MATLAB Support Package for USB Webcams")*
- [ROBOTICS TOOLBOX](https://petercorke.com/toolboxes/robotics-toolbox/ "ROBOTICS TOOLBOX")
- [MACHINE VISION TOOLBOX](https://petercorke.com/toolboxes/machine-vision-toolbox/ "MACHINE VISION TOOLBOX")

*Nota, este sitio pedirá crear o ingresar en una cuenta de MathWorks para permitir la descarga.

Cabe mencionar que el único código que no depende de ninguna librería es el [creador de códigos](José%20Ignacio%20Ramírez/Códigos/Matlab/CreadorCodigos.m "creador de códigos"). Se mantuvo en un archivo *.m* separado con el fin que no se necesitara instalar paquetes extra para este primer paso de creación de códigos. Sin embargo, hay funciones en este repositorio que son necesarias para el funcionamiento, por lo que se debe descargar la carpeta completa de códigos.

Por último, mencionar que la interfaz se desarolló en Matlab 2020b, por lo que únicamente podrá ser utilizada en dicha versión o superiores.

###Instalación
Los enlaces de arriba redirigen al sitio de descarga de los paquetes. En cada uno se descargará un archivo *.mltbx*. Luego de descargar los archivos, se debe ingresar a Matlab. Utilizar el navegador de archivos de Matlab para ir a la carpeta en la que se descargaron los archivos. Una vez ahí, ejecutar los programas dando doble clic en el navegador. Al instalar un nuevo paquete, el programa pide ingresar a una cuenta de MathWorks para poder realizar la instalación (si ya ha ingresado a su cuenta, no se lo pedirá).

###Verificación
Para verificar que los paquetes se encuentran correctamente instalados, se puede utilizar el comando **ver** en el que se listarán todos los paquetes instalados en la línea de comandos. Otra alternativa es utilizar el botón 
**"Add-Ons" -> "Manage Add-Ons"**
Este abrirá un menú en el que se pueden ver todos los paquetes instalados. En cualquiera de las dos maneras se puede verificar que se encuentran instalados los paquetes.

Si se desea verificar que la instalación sea correcta, se pueden ejecutar los siguientes commandos para cada librería:
1. cams = webcamlist;
2. rtbdemo;
3. kcircle(2); (alternativamente existe [esta](https://github.com/petercorke/machinevision-toolbox-matlab/blob/master/mvtbdemo.m "esta") función mvtbdemo pero se debe descargar de github)

##Uso de herramienta
Se tiene la opción de utilizar los programas en los *scripts* por separado, o utilizar la interfaz gráfica. Si se cuenta con una versión inferior a la 2020b, se puede utilizar los archivos *.m* para hacer uso de la herramienta o crear una interfaz gráfica nueva en la versión que se necesite.

###Scripts 
En la carpeta de códigos de [Matlab](José%20Ignacio%20Ramírez/Códigos/Matlab "Matlab"), se el archivo [CreadorCodigos.m](José%20Ignacio%20Ramírez/Códigos/Matlab/CreadorCodigos.m "CreadorCodigos.m") para generar los identificadores para los agentes. Aparte, se tiene el script [Computer_Vision_swarm_UVG.m](José%20Ignacio%20Ramírez/Códigos/Matlab/Computer_Vision_swarm_UVG.m "Computer_Vision_swarm_UVG.m") en el que se tiene separado por secciones los códigos de calibración, detección de obstáculos y toma de pose. Se puede utilizar el botón de **Run Section** para ejecutar únicamente el código requerido. Por ejemplo, luego de una calibración, ya no es necesario recalibrar a menos que se modifique el área de trabajo, por lo que se puede ejecutar únicamente el código de toma de pose.

De momento, no se tiene tanta personalización en los parámetros de manera accesible como en la interfaz.

###Interfaz Gráfica
El archivo de la interfaz gráfica es [Final_TestBed.mlapp](José%20Ignacio%20Ramírez/Códigos/Matlab/Final_TestBed.mlapp "Final_TestBed.mlapp") que se encuentra en la carpeta de códigos de Matlab. 

###Ejecución
Este se abre dando doble clic al archivo desde el navegador de archivos de Matlab. Este abrirá *App Designer* con la aplicación. Esta tiene una ventana para editar la interfaz gráfica y otra ventana para editar el código, de desear modificar algo. De lo contrario, se puede ejecutar con el botón *Run* del menú superior.

###Pestañas
Una vez en la interfaz, se tienen 5 pestañas:
1. Calibración
2. Toma de Pose
3. Creación de Códigos
4. Comunicación
5. Debug

A continuación se detalla con más profundidad sobre cada una.

####Calibración
Al inicar el programa, se tienen únicamente dos* opciones: cargar una calibración anterior de no haber cambiando nada en la mesa de trabajo, o conectarse a una cámara web. 

Para la primera únicamente, se presiona el botón "Cargar última calibración" y se retribuye la información del archivo [Datos.mat](José%20Ignacio%20Ramírez/Códigos/Matlab/Datos.mat "Datos.mat"). Luego despliega una imagen con calibración. Esta sirve para verificar que las esquinas y objetos sigan en el mismo lugar. De no estarlo, se puede volver a calibrar.

La segunda opción es seleccionar la cámara web con la que se quiere trabajar y conectarse a la misma. Luego se puede presionar el botón "Calibrar" para realizar una calibración automática. Si no se logra la detección de las esquinas deseadas, se puede hacer una selección manual.

Para esto, se presiona "Selección Manual". Esto abre la herramienta *Crop Selection Tool*. Aquí del lado izquierdo se debe de hacer clic sobre las esquinas siendo lo más preciso posibles (se puede aumentar el zoom de necesitarlo). Es importante que luego de seleccionar una esquina, se seleccione un punto en la imagen de la derecha también. Este no se utilizará, por lo que puede ser en cualquier lugar, pero es necesario ya que la herramienta necesita hacer esta vinculación de puntos.

Si se comete un error, se puede seleccionar un punto y moverlo o eliminarlo. Una vez seleccionadas las cuatro esquinas, se puede cerrar la herramienta ya sea con la **X** de la parte superior derecha o en **File->Close Crop Selection Tool** o presionando **Ctrl + W**

Por último, se puede presionar el botón de "Calibrar" de nuevo y este tomará las esquinas seleccionadas manualmente.

Y como último paso, se debe dar las dimensiones de la longitud y ancho de la mesa. Esto servirá para la conversión de las coordenadas en los resultados. Estas no necesitan ser de alguna dimensional específica, por lo que se puede ingresar la dimensional en que se deseen los resultados. Esto será principalmente la interpretación del usuario. Es decir, si se ingresan datos en centímetros, los resultados serán en centímetros; si se ingresan datos en pulgadas, los resultados serán en pulgadas. Pero ya que no se despliegua la dimensional en los resultados, es tarea del usuario interpretarlas.

####Toma de Pose
Por defecto, únicamente la casilla de "Bucle" se encuentra activa. Una vez se tiene una calibración (ya sea tomada o cargada de sesiones anteriores), el botón de "Toma de Pose" es activado.

La casilla de "Guardar Tiempos" habilita la función para guardar los tiempos de ejecucción en el archivo [Tiempos.mat](José%20Ignacio%20Ramírez/Códigos/Matlab/Tiempos.mat "Tiempos.mat") en la variable "tiempos" de cada iteración. La casilla de "Desplegar Imagen con Resultados" hace que al final de cada iteración, se despliegue una Figura con la imagen de la mesa con los centroides identificados y textos a la par mostrando el número de identificador, posición (x,y) y orientación θ.

Si no se tiene el funcionamiento en bucle, al precionar "Toma de pose" se ejecutará el código una única vez y la aplicación se mantendrá en espera del siguiente comando. De estar en bucle, una vez se termina una iteración, inmediatamente comienza la siguiente. Debido a esto, cuando se presiona el botó de "Parar Toma de Pose", el programa tarda un tiempo en parar. Cuando lo hace, muestra un mensaje en la interfaz para alertar que se ha detenido.

####Generación de Códigos
Para utilizar esta pestaña, únicamente se debe de ingresar el número de indentificador que se desea crear y presionar "Generar Código". Si se ingresó el número equivocado, únicamente cambiar el número en la interfaz y volver a generar el código.

Una vez se tiene el código deseado, se ingresa el nombre del archivo con el que se desea guardar la imagen y se presiona "Guardar Código". Este guardará el código con el nombre dado y formato *.jpg* en el folder activo en Matlab.

Si se desea guardar en otro formato, se puede guardar desde la figura en la que se despliega el identificador. Se puede navegar a **File->Save As...** y guardarlo con el nombre y formato deseado.

####Comunicación
En esta pestaña se tiene habilitada por defecto la comunicación UDP, pero todos los demás parámetros se encuentran vacíos o en 0. Es importante que no se intente habilitar la comunicación TCP y UDP simultáneamente, porque como se utiliza la misma entrada del puerto en la interfaz, esto puede generar conflictos en los *sockets* de comunicación.

Con esto en consideración, se debe llenar el puerto (preferiblemente con un valor entre 1,001 y 65,535 ya que estos son los puertos sin restricciones, pero que también coincida con el puerto que el otro dispositivo está utilizando). Luego, se puede ingresar una dirección IP y el número de identificador que se desee esté asociado con dicha IP. Y se presiona "Agregar IP"

Si se llega a confundir de identificador o dirección, se puede presionar "Eliminar IP" para eliminar dicha IP e identificador del registro. Con cada set agregado o eliminado, se actualizará el listado en la esquina inferior derecha. Esta no es editable directamente, por lo que se tiene que hacer con los botones de agregar y eliminar.

####Debug
Esta pestaña fue agregada por necesidad de fácil acceso modificación de ciertos parámetros o visualización de ciertos procesos sin necesidad de modificar el código y volver a ejecutar la interfaz.

Por ejemplo, se tiene la opción de modificar los umbrales con los que distingue el pivote del identificador y el valor en el que distingue entre negro y gris. Por inconsistencias de iluminación que se dan ocasionalmente, esto es muy útil pode modificarlo sin necesidad de modificar el código.

Luego, se tienen dos casillas una para mostrar ciertas imágenes del proceso de calibración y otra para mostrar imágenes del proceso de toma de pose. Estos se utilizan principalmente cuando se tiene alguna calibración erronea o toma de pose. El segundo es el más útil, ya que sirve para reajustar los umbrales si las condiciones de iluminación varían.

Por último, pero no menos importante, se tiene la casilla de "Debug con Imagenes". Antes de habilitar esta, se debe llenar la entrada de "Extensión" con la extensión de la imagen que se desea utilizar. Luego, se habilita la casilla. Esto lee todas las imágenes en el folder activo con la extensión seleccionada y crea un listado en el *dropdown menu* de la derecha.

Se puede seleccionar la imagen con la que se desea trabajar y mientras se mantenga la casilla de "Debug con Imagenes" activa, tanto la calibración como la toma de pose funcionarán con esa imagen. Es importante notar que la imagen de trabajo se puede cambiar cuando se desee. Por lo que se puede utilizar una imagen para la calibración y otra para la toma de pose, o realizar varias toma de pose a una secuencia de imágenes.

Esto fue de gran utilidad al principio cuando se tuvo que desarrollar los programas desde casa y no se tenía acceso a la mesa de prueba todo el tiempo. Por lo que se tomaban fotografías con la cámara que se consideraban necesarias y se podía trabajar con ellas desde casa para validad los códigos.

#Python
En la carpeta de [pruebas](José%20Ignacio%20Ramírez/Códigos/Python/Pruebas "pruebas") de Python se encuentran códigos experimentales de comunicación UDP y TCP tanto de cliente como de servidor. En el archivo [ReadMe.md](José%20Ignacio%20Ramírez/Códigos/Python/Pruebas/ReadMe.md "ReadMe.md") se encuentran listados los archivos y lo que hace cada uno. De igual manera, cada uno se encuentra debidamente comentado.

#Documentos
En la carpeta de [documentos](José%20Ignacio%20Ramírez/Documentos "documentos") se tiene diversos documentos del trabajo. En el archivo [ReadMe.md](José%20Ignacio%20Ramírez/Documentos/ReadMe.md "ReadMe.md") de dicho folder se encuentran listados los archivos y que es cada uno.
