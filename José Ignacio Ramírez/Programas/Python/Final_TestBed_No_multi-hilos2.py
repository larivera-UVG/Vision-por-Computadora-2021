#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:26:33 2020
@author: Jose Pablo Guerra
Codigo que implementa Calibracion y generacion de codigos para la mesa de pruebas y la deteccion de pose de robots
asi como la identifacion de sus codigos o marcadores.

7/07/2020: Version 0.1.0 -- Se incluye la GUI con el boton de calibrar y generacion de codigos
                            Se agrega el boton de limpiar pantallas generadas por OpenCV.
                            
7/07/2020: Vesion 0.1.1 -- Se agrega un textbox para el numero del generador de codigo, 
                           ademas de corregir su posicion en la GUI.
                           
12/07/2020: Version 0.2.0 -- Se agrega el boton para la toma de pose de datos, ademas de las funciones 
                            para reconocer la posicion de los robots. Fallas aun en la deteccion del codigo.
                            
12/07/2020: Version 0.2.1 -- Pruebas preeliminares de rotacion del codigo correctas. Se realizaran mas pruebas
                            para verificar que funcione. Proximo pasos: mejorar la deteccion del codigo.   
                            
21/07/2020: Version 0.3.0 -- Se arregla la parte del pivote, gira exitosamente siempre para dejar al pivote en la esquina superior izquierda.
                            Se arregla la identificacion de codigo.
                            
                            Para un mejor resultado, iluminar bien los codigos para que pueda detectar el pixel correctamente, sino, puede fallar.
26/07/2020: Version 0.4.0 -- Se arregla la identifcacion de codigo, ahora detecta codigos entre 3x3 y hasta 7x7 (pruebas realizadas)
                             Se agrega en la GUI el boton de toma de pose para unificar los 3 programas en uno solo.
                             
30/07/2020: Version 0.4.1 -- Se agrega un cuadro de texto para el tama;o de los marcadores o codigos, esto con el fin de
                            facilitar al usuario ingresar el tama;o del codigo desde la GUI y no tener que compilar el 
                            programa nuevamente cada vez que se desea cambiar de tama;o.
                            Detecta tama;os desde 3x3 hasta 10x10 (siempre cuidando la ilumacion)
                            Se agrega un if para evitar que otros objetos sean detectados, este if se maneja con las
                            variables gloables MIN_IMAGE_SIZE  y TRESHOLD_IMAGE_SIZE. La primera controla el tama;o 
                            de la imagen (en promedio es una imagen de 115x115) y el segundo controla el treshold
                            de tama;o porque puede variar minimamente.
                            
31/07/2020: Version 0.4.2 -- Arreglos menores a la deteccion de tama;o de imagen, se agrega las siguientes variables:
                            TRESHOLD_DETECT_MIN y TRESHOLD_DETECT_MAX. Por la forma en como se identifican los IDs se 
                            necesita detectar los cuadros grises, según sea la iluminación, este parametro puede variar
                            entre los 70 (o hasta 65) hasta un maximo de 130 (mas o menos). Con estas variables se 
                            controlan esos tresholds para detectar rangos de gris adecuados. 
                            
02/08/2020: Version 0.5.0 -- Se elimina la funcion reescalar por tama;o de codigo o marcador, ahora, reescala 
                            por tama;o de de imagen (lo lleva una imagen de 116x116)
                            Se agregan mas funciones a la GUI, en este caso una funcion de seteo de camara de la clase
                            robot (que hace lo mismo que la clase camara), y abre una nueva ventana para tomar una nueva
                            foto pero se calibra utilizando los parametros ya encontrados. 
                            Esta version esta lista para los multi-hilos.
                            
03/08/2020: Version 0.5.0 -- Se agregan comentarios para enteder el codigo y su funcionamiento, esto no sube el conteo del versionado.

03/08/2020: Version 0.6.0 -- Se eliminan funciones de toma de pose y se agregan a la libreria Swarm_robotic.py

03/08/2020: Version 0.6.1 -- Se agrega el metodo get_code de la clase Robot

09/08/2020: Version 0.7.0 -- Cambio en los metodos de calibracion y en la deteccion de pose por las modificaciones 
                             realizadas a la clase ***camara** y la clase ***vector_robot*** de la libreria
                             Swarm_robotic.py
                             
09/08/2020: Version 0.8.0 -- Cambio en la tome de pose, se importan las funciones (ya no forma parte de la clase ***vector_robot***)
                             con el objetivo de usarlo en multi-hilos (aunque a esta version funciona normal, sin hilos).

10/08/2020: Version 0.9.0 -- Se agregan funciones multi-hilos utilizando las libreria threading (se probo con 
                             multiprocessing pero por problemas del uso de GLI (consultar) no funciona algunas 
                             funciones de OpenCV).
                             hasta el momento se procesa la imagen, se obtiene el codigo y se actualiza el vector
                             en 3 hilos diferentes con captura manual del usuario. Se planea agregar la funcion de
                             captura continua como un 4 hilo. 
        
12/08/2020: Version 0.10.0 -- Se agregan ciertas ventanas en el hilo principal que muestra las imagenes para debug.
                              Esto depende del modo que se escoja en la funcion. Finalmente, se arreglan ciertos 
                              delay en los hilos para acelerar el procesamiento pero evitar colisiones y ayudar
                              a la sincronizacion.
                              
12/08/2020: Version 0.11.0 -- Se agrega un espacio para visualizar la imagen calibrada y la imagen de los robots a 
                              identificar dentro de la GUI con el metodo *set_label_image* que recibe como argumentos
                              la imagen y el nombre que se le pondra a la label de titulo. 
                              
12/08/2020: Version 0.12.0 -- Se agrega el boton para detener a los hilos y poder volver a iniciarlos con el boton
                              de "Tomar Pose"

18/08/2020: Version 0.12.1 -- Mejoras a la GUI para organizar mejor los botones. Se agrega el boton de Reiniciar calibracion
                              y otros elementos visuales.
                              
31/08/2020: Version 0.12.2 -- Actualizacion a uno de los hilos eliminando lineas innecesarias. 

16/09/2020: Version 0.12.3 -- Eliminacion del ciclo while en los hilos, se ejecutan cada vez que se toma
                              una nueva foto, para captura continua se puede agregar un hilo mas (pendiente)

18/09/2020: Version 0.13.0 -- Eliminacion de un hilo (el hilo de update de posicion) para compactar el codigo.                              

"""


from Swarm_robotic import camara, vector_robot, Robot #libreria swarm para la deteccion de la pose de agentes
from toma_pose import getRobot_fromSnapshot, process_image #para la deteccion de pose de los robots. 
import cv2 as cv #importando libreria para opencv 
import threading #para los hilos
#from time import time
import time

#importando la librerias para la GUI, en teoria se puede usar PyQt por que las funciones son las mismas
#aunque algunos metodos cambian, aunque se recomienda instalar PySide2 para compatibilidad con esta version
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QApplication, QWidget, QPushButton,QLineEdit
import sys
from PySide2.QtGui import QImage, QPixmap


n = 35 #para el boton1 de capturar
n2 = 300 #para el boton3 del codigo
n3 = 35

Canny_Factor = 2.5 #factor de multiplicacion para el limite superior de Canny
Calib_param = 80 #Factor de calibracion para Canny, este factor se puede variar
               #para una mejor deteccion de los bordes circulares.
Treshold = 1

#Tama;o del frame de la camara, de preferencia ajustarlo para que no capture cosas innecesarias
WIDTH = 960
HEIGTH = 720

#Inicializacion del objeto de la camara para el uso en la GUI
NUM_CAM = 0

camara = camara(NUM_CAM) #Inicializa el objeto camara para sus funciones respectivas
#robot = Robot(NUM_CAM) #Inicializa el objeto robot para la toma de poses y captura de imagen.
vector_robot = vector_robot()
#----------------------------------
#Para la toma de poses de los robots

MyGlobalCannyInf = 185
MyGlobalCannySup = 330

time_vector = []


"""
Para los hilos se definen las siguientes variables globales
"""
snapshot_robot = [] #para la foto de donde se calibrara 
RecCod = [] #los contornos obtenidos al momento de analizar cada foto
gray_blur_img = [] #la imagen de donde se extraera la informacion 
canny_img = [] #el contorno de canny 
parameters = [] #los parametros de los robots detectados. 
activate = 0 #para activar alguna funcion
a = 0 #para verificar el hilo que se esta usando, solo como debug.

#otras
Final_Crop_rotated = []
resized = []

flag_detener = False #detiene los hilos ejecutados. 

#MyWiHe = []
# In[Definiendo hilos]:

#read_lock = Lock()
lock = threading.Lock() #recurso para adquirir y bloquear el hilo mientras usa los recursos compartidos.
    
def image_processing():
    """
    Procesa la imagen y obtiene los contornos de donde se obtendran las pose de los robots

    Returns
    -------
    None. Pero utiliza las variables globales RecCod, gray_blur_img, canny_img para enviar info a otros hilos

    """
    global gray_blur_img, RecCod, canny_img, snapshot_robot
    #print("Soy el hilo de procesamiento")
    #while(1):
    lock.acquire()
    #print("Estoy procesando...")
    #read_lock.acquire()
    """
    while not q.empty():
        snapshot_robot = q.get()
        
    if q.empty():
        pass
    else:
    """
    a = 1
    print("Soy el hilo: ",a)
    #print("El procesamiento va a empezar")
    RecCod, gray_blur_img, canny_img = process_image(snapshot_robot, MyGlobalCannyInf, MyGlobalCannySup)
    #q.put(contour)
    #q.put(gray_blur_img)
    lock.release()
    #print("Libere")
    #time.sleep(1.5)
    #if flag_detener:
    #    break

def getting_robot_code(numCod, MyWiHe):
    vector = []
    vector_robot.clear_vector()
    """
    Una vez se obtiene los contornos de RecCod, se procesa y se obtiene los parametros de cada robot
    (posicion e ID)

    Parameters
    ----------
    numCod : TYPE int 
        DESCRIPTION. El tama;o del codigo (normalmente solo se usa si hay codigos menores a 2 x 2 cm)
    MyWiHe : TYPE array 
        DESCRIPTION. Las dimensiones de la calibracion, en este caso, se devuelve de la funcion calibrar_imagen()
        metodo de la clase vector_robot

    Returns
    -------
    None, pero usa la variable global parameters que es la informacion de todos los robots identificados.

    """
    global RecCod, gray_blur_img, parameters, activate, resized, Final_Crop_rotated
    #print(RecCod)
    #print("Soy el hilo de obtener pose")
    parameters = []
    #while(1):
    lock.acquire() #adquiere erl recurso
    activate = 1 #para activar el tercer hilo
    #print("adquiri el recurso")
    """
    n = 0
    while not q.empty():
        if n == 0:
            RecCod = q.get()
            n+=1
        if n == 1:
            gray_blur_img = q.get()
            n+=1
    """

    a = 2 #identificador del hilo, solo para ver el orden
    print("Soy el hilo: ",a)
    #print(n)
    #if n == 2:
    #print("La obtencion de pose va empezar")
    #cv.imshow("CapturaPoseRobot", snapshot_robot)
    #cv.waitKey(0)
    #parameters,resized,Final_Crop_rotated, _ = getRobot_fromSnapshot(RecCod, gray_blur_img,MyWiHe,numCod,"DEBUG_ON_CAPTURE")
    """
    Esta funcion lee la pose de robots y devuelve un vector de arrays con las posiciones de cada uno
    de los robots identificados. Ver a fondo la documentacion o la descripcion de toma_pose.py para ver 
    los otros parametros de esta fucnion
    """
    parameters = getRobot_fromSnapshot(RecCod, gray_blur_img,MyWiHe,numCod,"CAPTURE") 
    
    size = len(parameters)
    #print("El tama;o de los parametros: ", size)
    for i in range (0, size):
        temp_param = parameters[i]
        vector = vector_robot.agregar_robot(Robot(temp_param[0],temp_param[1],temp_param[2]))
         
        
       
    size_vector = len(vector)
    print("Este es el tama;o del vector en el while: ",size_vector)
    for v in range (0, size_vector):
        print("Este es el vector retornado: ",vector[v].id_robot)
        print("La posicione de ese vector es: ",vector[v].get_pos())
    

    lock.release()
    #time.sleep(1)
    #if flag_detener:
    #    break
        
def capturar_foto():
    pass


# In[Definiendo la interfaz grafica]
"""
Definiendo a la interfaz grafica. 
"""

class Window(QWidget):
    #global q
    #new_thread = 0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Swarm - Mesa Robotat")
        self.setGeometry(380,210,605,580)
        #self.setIcon()
        self.image_frame = QLabel()
        self.capturar_button()
        self.Reiniciar_calibracion()
        self.detener_procesamiento_button()
        self.Num_ID()
        self.ingresar_codigo()
        self.codigo_button()
        self.new_thread = 0
        self.Toma_pose()
        self.bToma_pose.setEnabled(False)
        self.size_codigo.setEnabled(False)
        self.detener.setEnabled(False)
        #self.mostrar_imagen = QLabel()
        
        #Muestra el titulo de la imagen en la GUI
        self.label_img_text = QLabel(self)
        self.label_img_text.move(220,220)
        self.label_img_text.setText("Visualizar Imagen")
        self.label_img_text.setFixedWidth(125)
        self.label_img_text.show()
        
        #Para mostrar la imagen en la GUI
        self.label_img = QLabel(self)
        #self.label_img.setText()
        self.label_img.setGeometry(320, 220,450, 300)
        self.label_img.move(70,220)
        self.label_img.show()
        #self.mostrar_imagen.addWidget(self.image_frame)
        #self.setLayout(self.mostrar_imagen)
        
        #Etiquetas para ordenar la GUI
        
        #Para mostrar etiqueta de calibracion
        self.label_calib = QLabel(self)
        self.label_calib.move(n+60,50-20)
        self.label_calib.setText("Calibracion*")
        self.label_calib.setFixedWidth(125)
        self.label_calib.show()
        
        #Para mostrar etiqueta de generar codigo/marcador/identificador
        self.label_code = QLabel(self)
        self.label_code.move(n+330,50-20)
        self.label_code.setText("Generacion Identificador")
        self.label_code.setFixedWidth(170)
        self.label_code.show()
        
        #Para mostrar etiqueta de obtencion de pose
        self.label_Pose = QLabel(self)
        self.label_Pose.move(n3+75,105)
        self.label_Pose.setText("Obtencion de Pose**")
        self.label_Pose.setFixedWidth(170)
        self.label_Pose.show()
        
        #Para mostrar etiqueta de notas
        self.label_note1 = QLabel(self)
        self.label_note1.move(n3-5,505)
        self.label_note1.setText("NOTA 1(*): Calibrar hasta ver las 4 esquinas del tablero (Presionar Reiniciar Calibracion)")
        self.label_note1.setFixedWidth(600)
        self.label_note1.show()
        
        #Para mostrar etiqueta de notas
        self.label_note2 = QLabel(self)
        self.label_note2.move(n3-5,525)
        self.label_note2.setText("NOTA 2(**): Mejores resultados se obtienen con ilumacion directa sobre la mesa")
        self.label_note2.setFixedWidth(600)
        self.label_note2.show()

    def capturar_button(self):
        self.bcapturar = QPushButton("Calibrar", self)
        self.bcapturar.move(n,50)
        self.bcapturar.clicked.connect(self.capturar)
    
    def Reiniciar_calibracion(self):
        self.bre_calib = QPushButton("Reiniciar calibracion", self)
        self.bre_calib.move(n+90,50)
        self.bre_calib.clicked.connect(self.Calibracion_reinit)
    
        
    def codigo_button(self):
        self.btn3 = QPushButton("Generar Codigo", self)
        self.btn3.move(n2,50)
        self.btn3.clicked.connect(self.codigo)
        
    
    def Toma_pose(self):
        self.bToma_pose = QPushButton("Tomar Pose", self)
        self.bToma_pose.move(n3,120)
        #self.Init_pose()
        self.bToma_pose.clicked.connect(self.pose)
        
    def detener_procesamiento_button(self):
        self.detener = QPushButton("Detener Procesamiento", self)
        self.detener.move(n3,150)
        self.detener.clicked.connect(self.detener_procesamiento)
    
    def Calibracion_reinit(self):
        self.bcapturar.setEnabled(True)
        self.bToma_pose.setEnabled(False)
        self.size_codigo.setEnabled(False)
        
        
    def pose(self):
        global gray_blur_img, canny_img, snapshot_robot, resized, Final_Crop_rotated
        text = self.size_codigo.text()
        vector = []
        vector_robot.clear_vector()
        if text == '':
            text = '3'
        numCod = int(text)
        #read_lock.acquire()
        start_time = time.time()
        foto = camara.get_frame("SINGLE")
        snapshot_robot,MyWiHe = vector_robot.calibrar_imagen(foto)

        self.set_label_image(snapshot_robot,"Robots a identificar")
        
        a = 1
        print("Soy el hilo: ",a)
        RecCod, gray_blur_img, canny_img = process_image(snapshot_robot, MyGlobalCannyInf, MyGlobalCannySup)
        
        a = 2 #identificador del hilo, solo para ver el orden
        print("Soy el hilo: ",a)
        parameters = []

        parameters = getRobot_fromSnapshot(RecCod, gray_blur_img,MyWiHe,numCod,"CAPTURE") 
        
        size = len(parameters)

        for i in range (0, size):
            temp_param = parameters[i]
            vector = vector_robot.agregar_robot(Robot(temp_param[0],temp_param[1],temp_param[2]))
             
        elapsed_time = time.time() - start_time
        elapsed_time = round(elapsed_time,3)
        print("Elapsed time: %.10f seconds." % elapsed_time)
        time_vector.append(elapsed_time)
        print(time_vector)    
           
        size_vector = len(vector)
        print("Este es el tama;o del vector en el while: ",size_vector)
        for v in range (0, size_vector):
            print("Este es el vector retornado: ",vector[v].id_robot)
            print("La posicione de ese vector es: ",vector[v].get_pos())
        
        #cv.imshow("CapturaPoseRobot", snapshot_robot)
        
        """
        #cv.waitKey(0)
        #time.sleep(1)
        if self.new_thread == 0:
            self.detener.setEnabled(True)
            #capturar = threading.Thread(target = capturar_foto, args=(numCod,)) #asignacion de los hilos a una variable
            self.procesar = threading.Thread(target = image_processing) #asignacion de los hilos a una variable
            self.obtener_pose = threading.Thread(target = getting_robot_code, args=(numCod,MyWiHe,))
            #self.vector_update = threading.Thread(target = actualizar_robots)
            self.procesar.start() #inicializa el hilo.
            time.sleep(0.1)
            self.obtener_pose.start() #inicializa el hilo.
            time.sleep(0.1)
            #self.vector_update.start()
            #self.new_thread = 1
            
            self.procesar.join()
            self.obtener_pose.join()
            #self.vector_update.join()
            elapsed_time = time.time() - start_time
            elapsed_time = round(elapsed_time,3)
            print("Elapsed time: %.10f seconds." % elapsed_time)
            time_vector.append(elapsed_time)
            print(time_vector)
        """
        """   
        if resized == [] or Final_Crop_rotated ==[]:
            pass
        else:
            #gray_blur_img
            cv.imshow("gray_blur_img",gray_blur_img)
            cv.imshow("resized",resized)
            cv.imshow("Final_Crop_rotated", Final_Crop_rotated)
            cv.imshow("canny_img",canny_img)
            cv.waitKey(0)
        """
        #cv.waitKey(100)
        #cv.imshow("canny_img", canny_img)
        #cv.waitKey(0)
        #cv.imshow("Imagen blur", gray_blur_img)
        #cv.waitKey(0)
        
        #procesar.join()
        #obtener_pose.join()
        #actualizar = threading.Thread(target = read_2)
        
        """
        #Version sin hilos
        #Snapshot = cv.imread("opencv_CalibSnapshot_0.png")
        RecCod, gray_blur_img, canny_img = getRobot_Code(snapshot_robot, MyGlobalCannyInf, MyGlobalCannySup, numCod)
        parameters = getRobot_fromSnapshot(RecCod,gray_blur_img,numCod)
        
        size = len(parameters)
        for i in range (0, size):
            temp_param = parameters[i]
            if vector_robot.update_robot_byID(temp_param[0], temp_param[1], temp_param[2]):
                pass
            else:
                vector = vector_robot.agregar_robot(Robot(temp_param[0],temp_param[1],temp_param[2]))
        print("Este es el vector retornado: ",vector[0].id_robot)
        print("Este es el vector retornado: ",vector[1].id_robot)
        """
    
    def Num_ID(self):
        self.lineEdit = QLineEdit(self,placeholderText="Ingrese número")
        self.lineEdit.setFixedWidth(120)
        self.lineEdit.move(n2+140,55)
        #vbox = QVBoxLayout(self)
        #vbox.addWidget(self.lineEdit)
    
    def ingresar_codigo(self):
        self.size_codigo = QLineEdit(self,placeholderText="Tamaño del código")
        self.size_codigo.setFixedWidth(125)
        self.size_codigo.move(n3+120,123)
        #vbox = QVBoxLayout(self)
        #vbox.addWidget(self.lineEdit)
        
    def detener_procesamiento(self):
        global flag_detener
        flag_detener = True
        self.procesar.join()
        self.obtener_pose.join()
        self.vector_update.join()
        self.new_thread = 0
        flag_detener = False
        self.detener.setEnabled(False)
        
    def codigo(self):
        text = self.lineEdit.text()
        if text == '':
            text = '0'
        num = int(text)
        camara.Generar_codigo(num)
        
    def set_label_image(self, snap, text):
        self.image = snap
        height, width, channels = self.image.shape
        bytesPerLine = channels * width
        self.image_show = QImage(self.image.data, width, height,bytesPerLine, QImage.Format_RGB888)
        self.image = QPixmap.fromImage(self.image_show)
        self.pixmap_resized = self.image.scaled(self.label_img.width(), self.label_img.height(), Qt.KeepAspectRatio)
        self.label_img.setPixmap(self.pixmap_resized)
        self.label_img_text.setText(text)
        
        
    def capturar(self):
        foto = camara.get_frame()
        CaliSnapshot = camara.Calibrar(foto,Calib_param,Treshold)
        self.set_label_image(CaliSnapshot, "Imagen Calibrada")
        #self.label_img.show()
        #self.image = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888).rgbSwapped()
        #self.image_frame.setPixmap(QPixmap.fromImage(self.image))

        #cv.imshow("Output Image", CaliSnapshot)
        #cv.waitKey(2000)
        #camara.destroy_window()
        self.bToma_pose.setEnabled(True)
        self.size_codigo.setEnabled(True)
        self.bcapturar.setEnabled(False)
        

            
myapp = QApplication.instance()
if myapp is None: 
    myapp = QApplication(sys.argv)
#myapp = QApplication(sys.argv)
window = Window()
window.show() 

sys.exit(myapp.exec_())

myapp.quit()