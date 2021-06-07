#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 19:21:56 2020

@author: joseguerra

09/08/2020: Version 0.1.0 -- Creacion inicial del archivo

09/08/2020: Version 0.2.0 -- Se toman las funciones de toma de pose de Swarm_robotic.py para usarlas en multi-hilos
                             o bien, para usarlo normal, sin embargo, separarlo en archivos ayuda a que no sea tan
                             cargado de codigo el archivo de Swarm_robotic.py (ver versionado del mencionado archivo
                             para entender que hacen estas funciones y cuando son agregadas y elminadas)

12/08/2020: Version 0.3.0 -- Version unificada de para usarse con multi-hilos. La version original no estaba pensado para implementarse
                             en multi-hilos, con estas modificaciones, esta planetado para su uso en ambos escenarios.
                             Favor referirse a toma_pose.py para las anotaciones completas del archivo original.

"""
import cv2 as cv #importando libreria para opencv
#from Swarm_robotic import Robot
#de momento no se usan
SQRTDE2 = 1.41421356
MyPI = 3.14159265

#revisar si es que se usan
anchoMesa = 14.5
largoMesa = 28.0

#de momento no se usan
#GlobalCodePixThreshold = 80
#GlobalColorDifThreshold = 10

#si se usan
MyGlobalCannyInf = 185
MyGlobalCannySup = 330
#Code_size = 1.0 #no se usa

#si se usan
MAX_IMAGE_SIZE = 75

#Para detectar los cuadros grises, normalmente con buena iluminacion pueden llegar a tener un valor de 130 (o mas)
#pero para condiciones de poca luz, el valor MIN puede variar.
TRESHOLD_DETECT_MIN = 65
TRESHOLD_DETECT_MAX = 130

"""
Definiendo las funciones para la toma de poses.
"""

def process_image(calib_snapshot, Canny_inf, Canny_sup):
    print("Entre a process_image")
    """
    Parameters
    ----------
    calib_snapshot : numpy Array
        El vector calibrado (recortado y aplicado la matriz obtenido de la clase ***camara***)
    Canny_inf : int
        Parameto inferior para el Canny detection (ver documentacion de OpenCV para mas informacion)
    Canny_sup : int
        Parametro superior para el Canny detection (ver documentacion de OpenCV para mas informacion)

    Returns
    -------
    contour : numpy Array
        Contiene los contornos detectados, esto sirve para identificar los codigos
    gray_blur_img : numpy Array
        Imagen luego de pasarle el filtro blanco y negro y una difuminacion, de aqui se extraen los codigos
    canny_img : numpy Array
        Imagen luego de aplicarle el Canny Detection Edge Function

    """
    #vector = vector_robot() #inicializa el objeto vector_robot para agregar los diferentes parametros de cada robot como vector
    blur_size = (3,3) #para la difuminacion, leer documentacion
    height_im, width_im = calib_snapshot.shape[:2] #obtiene los tama;os de la imagen capturada
    print(height_im, width_im)
    #PixCodeSize = Medida_cod * width_im / anchoMesa
    print("voy a prrocesar la imagen")
    print("Aplicare filtro de grises")
    gray_img = cv.cvtColor(calib_snapshot, cv.COLOR_BGR2GRAY) #se le aplica filtro de grises
    print("Aplicare blur")
    gray_blur_img = cv.blur(gray_img, blur_size) #difuminacion para elimiar detalles innecesarios
    print("Obtendre canny")
    canny_img = cv.Canny(gray_blur_img, Canny_inf, Canny_sup, apertureSize = 3) #a esto se le aplica Canny para la deteccion de bordes
    print("Termine de procesar")

    #para debug
    #muestra la imagen de canny para ver que contornos va a detectar.
    #cv.imshow("Canny_contour", canny_img)
    #cv.waitKey(0)

    #obtiene los contornos de la imagen de Canny
    image, contour, hierarchy = cv.findContours(canny_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #cv.drawContours(calib_snapshot, contour,  -1, (10,200,20), 2) #dibuja los contornos
    #cv.imshow("Canny_contour", calib_snapshot)
    #cv.waitKey(0)
    #para debug
    #dibuja los contornos detectados, descomentar estas lineas:

    #cv.drawContours(calib_snapshot, contour,  -1, (255,0,0), 2) #dibuja los contornos
    #cv.imshow("Contornos", calib_snapshot)
    #cv.waitKey(0)

    print("voy a retonar algo")
    return contour,gray_blur_img, canny_img

def getRobot_fromSnapshot(contour, snap, MyWiHe, codeSize = 3,mode = "CAPTURE"):
    """


    Parameters
    ----------
    contour : numpy Array
        Los contornos detectados en la foto capturada
    snap : numpy Array
        La imagen calibrada y procesada con el filtro blanco y negro asi como la difuminacion
    MyWiHe : TYPE array 2x2
        DESCRIPTION. El ancho y el alto (width y heigth) de la IMAGEN CALIBRADA. Al momento de calibrar
        se debe pasar las dimensiones que se retornan para esta funcion
    codeSize : TYPE, optional
        DESCRIPTION. The default is 3. El tama;o del codigo. Usado normalmente para detectar codigos mas peque;os
        de 3x3 cm, aunque la funcionalidad ha sido probado con resultados exitos de 3x3 cm en adelante.
    mode : TYPE, optional
        DESCRIPTION. The default is "CAPTURE".
        Si mode = "CAPTURE" entonces se obvian imagenes que sirven solamente para mostrar el codigo funcionando visualmente
        Si mode == "DEBUG" se muestran todas las figuras y otros elementos para ver el comportamiento completo del codigo
        en los diferentes pasos de esta funcion
        Si mode == "DEBUG_ON_CAPTURE" muestra ciertas figuras pero estas son retornadas (para usarse en multi-hilos)

    Raises
    ------
    Exception
        DESCRIPTION. si mode (mode de la funcion descrita en el versionado) no es adecuado tira un error.

    Returns
    -------
    TYPE
        DESCRIPTION. Dependiendo el modo retorna solo los parametros del robot u otros elementos para debugging.

    """

    if mode == "CAPTURE" or mode == "DEBUG" or mode == "DEBUG_ON_CAPTURE":
        pass
    else:
        raise Exception("Valor invalido de mode. Valores aceptados CAPTURE, DEBUG, DEBUG_ON_CAPTURE")

    parameter_robot = []
    for c in contour:
        #cv.drawContours(snap, c,  -1, (10,200,20), 2) #dibuja los contornos
        #cv.waitKey(0)
        #para debug, imprimi separadores de lo que se va realizando.

        print(" ")
        print("-----------------")
        #print("Este es el contador",a)
        RecCod = cv.minAreaRect(c)
        #cv.drawContours(calib_snapshot, c,  -1, (10*i + 100,15*i,20*i + 20), 2) #dibuja los contornos
        #cv.waitKey(0)
        #Rx, Ry = RecCod[0] #SingleRecCod.center
        #print("Contornos", RecCod[0])
        #print("Contornos", RecCod[0][0])

        center, size, theta = RecCod #SingleRecCod.size, del codigo de C++, obtiene el angulo, centro y tama;o del contorno
        center, size = tuple(map(int, center)), tuple(map(int, size)) #lo vuelve un int.

        #para debug, imprimi el valor del centro.
        #print(center)
        if theta < -45:
            theta += 90

        #separador
        print("-----------------")
        print(" ")


        """
        A continuacion se detalla el procedimiento:
            Se obtiene un factor de escala entre la medida real del marcador o identificador y el tama;o estandar
            con el cual se hizo este codigo, es decir, 3. Este rescale_factor sirve para evitar que contornos muy peque;os
            pasen, aunque igual, mas adelante, hay otro filtro que elimina eso.
        """
        rescale_factor_size = codeSize/3 #factor de escala

        #para debug, imprime el tama;o del contorno, se puede descomentar
        print("Size[0] y size[1]: ", size[0], size[1])

        #Compara si ambos tama;os estan por arriba del minimo para no tener imagenes o contornos muy peque;os
        #y nada relevantes para este programa.
        if (size[0] > (40 * rescale_factor_size) and size[1] > (40 * rescale_factor_size)):
            ctrl = 1
        else:
            ctrl = 0

        if ctrl == 1:

            GlobalWidth = MyWiHe[1]
            GlobalHeigth = MyWiHe[0]

            MyGlobalWidth = snap.shape[1]
            MyGlobalHeigth = snap.shape[0]

            #---------------------------------------------
            #separador
            print(" ")
            print("-----------------")
            print("Ingresando a getRobot_fromSnapshot")


            #Para obtener el snap recortado.
            #height_cont,width_cont = RecContorno[1] #height_cont

            #verificar si es usado --------
            """
            """
            tempWiMitad = SQRTDE2 * size[1] / 2
            tempHeMitad = SQRTDE2 * size[0] / 2


            Cx = center[0] #pasa los centros a variables para su identificacion, centro en X
            Cy = center[1] #Centro en Y


            EscalaColores = []

            rows = [int(Cy - tempHeMitad), int(Cy + tempHeMitad)]
            cols = [int(Cx - tempWiMitad), int(Cx + tempWiMitad)]
            #rows_1 = np.array([int(Cy - tempHeMitad), int(Cy + tempHeMitad)])
            #cols_1 = np.array([int(Cx - tempWiMitad), int(Cx + tempWiMitad)])


            #print(RecContorno)

            SemiCropCod = snap[rows[0]:rows[1], cols[0]:cols[1]] #hasta aqui todo bien al 19 de julio del 2020, variable no usada

            #Obtener matriz de rotacion de la imagen
            M = cv.getRotationMatrix2D(center, theta, 1)

            #se obtiene la perspectiva de la imagen basada en la matriz y las dimensiones de la imagen, esto es para recortar
            dst = cv.warpAffine(snap, M, (MyGlobalWidth, MyGlobalHeigth))
            #image_rotated = cv.warpAffine(SemiCropCod, temp_matRotated, (SemiCropCod_Heigth, SemiCropCod_Width), flags = cv.INTER_CUBIC)

            #Final_Crop_rotated = cv.getRectSubPix(image_rotated, (int(height_cont),int(width_cont)), (np.size(rows_1)/2.0, np.size(cols_1)/2.0))


            Final_Crop_rotated = cv.getRectSubPix(dst, size, center) #obtiene el recorte final.

            if mode == "DEBUG" or mode == "DEBUG_ON_CAPTURE":
                cv.imwrite("Imagen_Inicial.png", Final_Crop_rotated) #Guarda la foro
                initial_image = Final_Crop_rotated
            #cv.imshow("Init", SemiCropCod)



            #obtiene las nuevas dimensiones del recorte, esto servira para otro filtro y para el resize de las imagenes
            height_Final_Rotated, width_Final_Rotated = Final_Crop_rotated.shape[:2]

            #para debug, imprime las dimensiones actuales de la imagen
            print("Dimensiones actuales: ")
            print(height_Final_Rotated, width_Final_Rotated)


            scale_percent = (codeSize/3.0)  # percent of original size, factor de reescala que se utiliza basado en el codigo
            #la variable MIN_IMAGE_SIZE es para que las imagenes mas peque;as que hayan pasado el primer filtro, no se tomen en cuenta
            #aqui lo que se se busca eliminar son imagenes o cuadros (normalmente los blancos en cada identificador)
            #sean eliminados para evitar confusiones de identificacion

            """
            if (height_Final_Rotated < (MAX_IMAGE_SIZE * scale_percent) or width_Final_Rotated < (MAX_IMAGE_SIZE * scale_percent)):
                #para debug
                print("cumpli el if")
                ctrl = 0 #si la imagen es mas peque;a, entonces se lo salta
            else:
                ctrl = 1 #sino, entra a hacer todo el procesamiento de la imagen para la identificacion del ID.

            if ctrl == 1:
            """

            """
            Este codigo esta pensado para funcionar reconociendo imagenes entre 114 x 114 hasta 120 x 120,
            se define como medida 116x166.
            El objetivo de esto es llevar los codigos a estas medidas en caso de ser necesario (si son de 3x3 puede que no)
            Por lo tanto, se calcula un porcentaje diferente tanto para el width como para el heigth de la imagen.
            """

            #calculo del porcentaje de escala para las medidas
            height_percent = (116/height_Final_Rotated)
            width_percent = (116/width_Final_Rotated)

            #para debug, separador e imprime el factor de escala de la imagen.
            print("-----------------")
            print("% de escala", scale_percent)

            #para debug, muestra una de las medidas temporales de la imagen.
            print("Medida temporal: ", width_Final_Rotated * scale_percent)
            print("-----------------")

            #calcula las nuevas medidas
            width = int(width_Final_Rotated * width_percent)
            height = int(height_Final_Rotated* height_percent)

            #para debug, imprime como tupla las nuevas medidas.
            dim = (width, height)

            print("Dimensiones resized: ")
            print("-----------------")
            print(dim)

            # resize image
            resized = cv.resize(Final_Crop_rotated, dim, interpolation = cv.INTER_AREA)

            if mode == "DEBUG" or mode == "DEBUG_ON_CAPTURE":
                image_befor_rotate = resized
                cv.imwrite("Imagen_resized.png", resized) #Guarda la foro

            if (mode == "DEBUG"):
                #para debug muestra la imagen recortada
                cv.imshow("Final_crop_resized",resized)
                #para debug, muestra la imagen recortada y rotada
                cv.imshow("Rotated", dst)
                cv.imshow("Final_crop",Final_Crop_rotated)
                cv.waitKey(0)

            #obtiene las nuevas medidas para los calculos
            height_Final_Rotated, width_Final_Rotated = resized.shape[:2]


            #ppara debug, muestra las medidas, separador.
            print("height_Final_Rotated: ", height_Final_Rotated)
            print("width_Final_Rotated: ", width_Final_Rotated)
            print("-----------------")



            a = 0 #variable bandera, ya no se usa pero evita modificaciones sustanciales al codigo en cuanto a funcion e ifs



            if a == 0:

                """
                La mayoria de imshow() son para debug y mostrar las porciones recortadas.
                Lo que se hace aqui es buscar e identificar los cuadros dentro de cada identificador o codigo.
                Las medidas estan pensadas para imagenes con las medidas mencionadas, por eso se hace el resize.

                Estas lineas no se deben modificar a salvo este fallando la identifacion de los cuadros o se dese otro
                tipo de identificacion.

                Basicamente, por las caracteristicas del codigo/identificador utilizado, se tiene la siguiente figura:

                |-----------------------
                |   P  |    1  |   2   |
                |   -  |   -   |   -   |
                |   3  |   4   |   5   |
                |   -  |   -   |   -   |
                |   6  |   7   |   8   |
                |------------------------

                Donde P representa al pivote y cuadro blanco y los numeros del 1 al 8 son los bits a0 hasta a7 para un
                codigo de hasta 255.

                Este codigo identifica el pivote, y lo alinea siempre en la esquina superior izquierda (por eso se le
                aplica un filtro de blanco y negro para que los valores de igual forma queden entre 0 y 255).
                Luego, dependiendo donde este el pivote se rota hasta alinearlo. La rotacion inicial solo lo coloca con angulo 0.
                Finalmente, se ubican los diferentes cuadros y asi es como se identifica el codigo: 1 para gris, 0 para negro
                dependiendo los tresholds establecidos.
                """
                #print(height_Final_Rotated)
                temp_ColorSupIzq = resized[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]
                temp_ColorInfIzq = resized[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)]
                temp_ColorSupDer = resized[int(height_Final_Rotated*1/8):40, 65:100]
                temp_ColorInfDer = resized[62:90, 70:90]

                ColorSupIzq = temp_ColorSupIzq[int(temp_ColorSupIzq.shape[0]/2),int(temp_ColorSupIzq.shape[1]/2)]
                ColorSupDer = temp_ColorSupDer[int(temp_ColorSupDer.shape[0]/2),int(temp_ColorSupDer.shape[1]/2)]
                ColorInfDer = temp_ColorInfDer[int(temp_ColorInfDer.shape[0]/2),int(temp_ColorInfDer.shape[1]/2)]
                ColorInfIzq = temp_ColorInfIzq[int(temp_ColorInfIzq.shape[0]/2),int(temp_ColorInfIzq.shape[1]/2)]
                #print("temp_ColorSupIzq.shape", temp_ColorSupIzq.shape)
                #print("Midle array image gray sup izq: ", temp_ColorSupIzq[int(temp_ColorSupIzq.shape[0]/2),int(temp_ColorSupIzq.shape[1]/2)])
                #print("Midle array image gray inf izq: ", temp_ColorInfIzq[int(temp_ColorInfIzq.shape[0]/2),int(temp_ColorInfIzq.shape[1]/2)])
                #print("Midle array image gray sup der: ", temp_ColorSupDer[int(temp_ColorSupDer.shape[0]/2),int(temp_ColorSupDer.shape[1]/2)])
                #print("Midle array image gray inf der: ", temp_ColorInfDer[int(temp_ColorInfDer.shape[0]/2),int(temp_ColorInfDer.shape[1]/2)])

                #if Final_Crop_rotated.shape[0] > 14 and Final_Crop_rotated.shape[1] > 44:
                #print("int(height_Final_Rotated*1/8)", int(height_Final_Rotated*1/8 + 2))
                #print("Final_Crop_rotated: ", Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:35])
                #cv.imshow("Prueba gris", Final_Crop_rotated[10:20])
                #ColorSupIzq = sum(sum(Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]))
                    #print(Final_Crop_rotated[15:45, 15:42])
                    #ColorSupIzq = (ColorSupIzq_1[0] + ColorSupIzq_1[1] + ColorSupIzq_1[2])/3
                #print("Superior izquierdo")
                #print(ColorSupIzq)
                #print(" ")

                if (mode == "DEBUG"):
                    cv.imshow("ColorSupIzq_1",resized[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:35])

                    cv.imshow("supderecho",resized[int(height_Final_Rotated*1/8):40, 65:100])

                    cv.imshow("ColorInfDer1",resized[62:90, 70:90])

                    cv.imshow("ColorInfIzq1",resized[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)])
                #cv.imshow("ColorMiddleIzq",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2)+30:int(height_Final_Rotated*1/8 + 30)+30, 10:35])
                #cv.imshow("ColorMiddle",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2)+30:int(height_Final_Rotated*1/8 + 30)+30, 10+30:35+25])
                #cv.imshow("Color_a0",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10+30:35+30])
                #cv.imshow("Color_a4",Final_Crop_rotated[int(height_Final_Rotated*1/8)+30:40+30, 65:100])
                #cv.imshow("Color_a6",Final_Crop_rotated[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8)+30:int(height_Final_Rotated*1/8 + 23)+30])



            for i in range(0,3):
                EscalaColores.append(ColorSupIzq)


                #cv.imshow("El crop por partes", Final_Crop_rotated[15:45,70:105])

                #cuadro superior izquierdo: 15:45, 15:42
                                                #30 x 25

               #cuadro inferior izquierda: 70:105, 15:42

               #cuadro superior derecho: 15:45, 70:105
               #cuadro inferior derecho: 70:105, 70:105

            tempFloatTheta = theta #el angulo al que esta rotado el codigo.
            print("este es el angulo de mi robot al inicio", tempFloatTheta)

            #comparacion mencionada, detecta cual de las esquinas tiene el mayor color para hacer la rotacion.
            if ((ColorSupDer > ColorSupIzq) and (ColorSupDer > ColorInfDer) and (ColorSupDer > ColorInfIzq)):
                print("90 en contra del reloj")
                print(" ")
                resized = cv.rotate(resized, cv.ROTATE_90_COUNTERCLOCKWISE)
                tempFloatTheta = tempFloatTheta + 90
                EscalaColores[2] = ColorSupDer
            elif ((ColorInfDer > ColorSupIzq) and (ColorInfDer > ColorSupDer) and (ColorInfDer > ColorInfIzq)):
                print("rotado 180")
                print(" ")
                resized = cv.rotate(resized,cv.ROTATE_180);
                tempFloatTheta = tempFloatTheta + 180;
                EscalaColores[2] = ColorInfDer

            elif ((ColorInfIzq > ColorSupIzq) and (ColorInfIzq > ColorInfDer) and (ColorInfIzq > ColorSupDer)):
                print("90 a favor del reloj")
                print(" ")
                resized = cv.rotate(resized, cv.ROTATE_90_CLOCKWISE)
                tempFloatTheta = tempFloatTheta - 90
                EscalaColores[2] = ColorInfIzq
            print("este es el angulo de mi robot rotado", tempFloatTheta)
            #temp_ColorSupIzq = Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]
            #temp_a5 = Final_Crop_rotated[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)]
            #temp_a1 = Final_Crop_rotated[int(height_Final_Rotated*1/8):40, 65:100]
            #temp_a7 = Final_Crop_rotated[62:90, 70:90]

            #ColorSupIzq = temp_ColorSupIzq[int(temp_ColorSupIzq.shape[0]/2),int(temp_ColorSupIzq.shape[1]/2)]
            #ColorSupDer = temp_ColorSupDer[int(temp_ColorSupDer.shape[0]/2),int(temp_ColorSupDer.shape[1]/2)]
            #ColorInfDer = temp_ColorInfDer[int(temp_ColorInfDer.shape[0]/2),int(temp_ColorInfDer.shape[1]/2)]
            #ColorInfIzq = temp_ColorInfIzq[int(temp_ColorInfIzq.shape[0]/2),int(temp_ColorInfIzq.shape[1]/2)]


            #a partir de aqui, se localizan los otros 8 cuadros dentro de la imagen y se calcula su valor.

            #temp_ColorSupIzq = Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]
            temp_a1 = resized[int(height_Final_Rotated*1/8):40, 65:100]
            temp_a5 = resized[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)]
            temp_a7 = resized[int(height_Final_Rotated*1/2) + 15:int(height_Final_Rotated*1/2) + 45, int(width_Final_Rotated*1/2)+20 :int(width_Final_Rotated*1/2) + 45]


            #print(int(temp_a1.shape[1]/2))

            #calcula justo el centro del cuadro para evitar tomar otros colores que no son. Solo toma un valor
            #entre 0 y 255 (255 para blanco) aunque con buena iluminacion, el gris esta entre 100 y 130, con iluminacion media
            #puede estar entre 60 y 80.

            a1 = temp_a1[int(temp_a1.shape[0]/2),int(temp_a1.shape[1]/2)]
            a7 = temp_a7[int(temp_a7.shape[0]/2),int(temp_a7.shape[1]/2)]
            a5 = temp_a5[int(temp_a5.shape[0]/2),int(temp_a5.shape[1]/2)]


                #print("temp_ColorSupIzq.shape", temp_ColorSupIzq.shape)
                #print("Midle array image gray sup izq: ", temp_ColorSupIzq[int(temp_ColorSupIzq.shape[0]/2),int(temp_ColorSupIzq.shape[1]/2)])
                #print("Midle array image gray inf izq: ", temp_ColorInfIzq[int(temp_ColorInfIzq.shape[0]/2),int(temp_ColorInfIzq.shape[1]/2)])
                #print("Midle array image gray sup der: ", temp_ColorSupDer[int(temp_ColorSupDer.shape[0]/2),int(temp_ColorSupDer.shape[1]/2)])
                #print("Midle array image gray inf der: ", temp_ColorInfDer[int(temp_ColorInfDer.shape[0]/2),int(temp_ColorInfDer.shape[1]/2)])

                #if Final_Crop_rotated.shape[0] > 14 and Final_Crop_rotated.shape[1] > 44:
                #print("int(height_Final_Rotated*1/8)", int(height_Final_Rotated*1/8 + 2))
                #print("Final_Crop_rotated: ", Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:35])
                #cv.imshow("Prueba gris", Final_Crop_rotated[10:20])
                #ColorSupIzq = sum(sum(Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]))
                    #print(Final_Crop_rotated[15:45, 15:42])
                    #ColorSupIzq = (ColorSupIzq_1[0] + ColorSupIzq_1[1] + ColorSupIzq_1[2])/3
                #print("Superior izquierdo")
            #print(ColorSupIzq)
            #print(" ")
            #cv.imshow("Pivote",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:35])

                #ColorSupDer = sum(sum(Final_Crop_rotated[15:45, 70:105]))
                    #ColorSupDer = (ColorSupDer1[0] + ColorSupDer1[1] + ColorSupDer1[2])/3
            #print("Superior derecho")
            #print(ColorSupDer)
            #print(" ")
            #cv.imshow("Color_a1",Final_Crop_rotated[int(height_Final_Rotated*1/8):40, 65:100])

                #ColorInfDer = sum(sum(Final_Crop_rotated[62:90, 70:90]))
                    #ColorInfDer = (ColorInfDer1[0] + ColorInfDer1[1] + ColorInfDer1[2])/3
            #print("inferior derecho")
            #print(ColorInfDer)
            #print(" ")
            #cv.imshow("Color_a1",Final_Crop_rotated[int(height_Final_Rotated*1/8):40, 65:100])
            #cv.imshow("Color_a7",Final_Crop_rotated[int(height_Final_Rotated*1/2) + 15:int(height_Final_Rotated*1/2) + 45, int(height_Final_Rotated*1/2) :int(height_Final_Rotated*1/2) + 26])

            #print("int(height_Final_Rotated*1/4 + 2))",int(height_Final_Rotated*1/4 + 2))
                #ColorInfIzq = sum(sum(Final_Crop_rotated[int(height_Final_Rotated*1/4 + 50):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 25)]))
                    #ColorInfIzq = (ColorInfIzq1[0] + ColorInfIzq1[1] + ColorInfIzq1[2])/3
            #print("inferior izquierdo")
            #print(ColorInfIzq)
            #print(" ")

            if (mode == "DEBUG"):
                #para debug, muestra los cuadros detectados
                #--------------------------------
                #cv.imshow("Color_a0",resized[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), int(height_Final_Rotated*1/8)+25:int(height_Final_Rotated*1/8)+52])
                cv.imshow("Color_a0",resized[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), int(width_Final_Rotated*1/8)+25:int(width_Final_Rotated*1/8)+55])
                cv.imshow("Color_a1",resized[int(height_Final_Rotated*1/8):40, 65:100])
                cv.imshow("Color_a2",resized[int(height_Final_Rotated*1/8)+30:int(height_Final_Rotated*1/8 + 30)+22, 12:38])
                cv.imshow("Color_a3",resized[int(height_Final_Rotated*1/8 + 2)+23:int(height_Final_Rotated*1/8 + 25)+30, 10+30:35+30])
                cv.imshow("Color_a4",resized[int(height_Final_Rotated*1/8)+30:40+30, 65:95])
                cv.imshow("Color_a5",resized[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)])
                cv.imshow("Color_a6",resized[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8)+30:int(height_Final_Rotated*1/8 + 23)+30])
                cv.imshow("Color_a7",resized[int(height_Final_Rotated*1/2) + 15:int(height_Final_Rotated*1/2) + 45, int(width_Final_Rotated*1/2)+20 :int(width_Final_Rotated*1/2) + 45])


                #para debug, muestra como quedo el codigo al final
                cv.imshow("Codigo", resized)
                cv.waitKey(0)
                #--------------------------------
            if mode == "DEBUG" or mode == "DEBUG_ON_CAPTURE":
                cv.imwrite("codigo_resized.png", resized) #Guarda la foro
                #Generando los valores para detectar el codigo.
            temp_a3 = resized[int(height_Final_Rotated*1/8 + 2)+23:int(height_Final_Rotated*1/8 + 25)+30, 10+30:35+30]
            a3 = temp_a3[int(temp_a3.shape[0]/2),int(temp_a3.shape[1]/2)]

            #print("a3: ", a3)

            temp_a2 = resized[int(height_Final_Rotated*1/8)+30:int(height_Final_Rotated*1/8 + 30)+22, 12:38]
            a2 = temp_a2[int(temp_a2.shape[0]/2),int(temp_a2.shape[1]/2)]
            #print("a2: ", a2)

            #print("height_Final_Rotated*1/8: ",height_Final_Rotated*1/8)
            temp_a0 = resized[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), int(height_Final_Rotated*1/8)+25:int(height_Final_Rotated*1/8)+52]
            a0 = temp_a0[int(temp_a0.shape[0]/2),int(temp_a0.shape[1]/2)]
            #print("a0: ", a0)


            temp_a4 = resized[int(height_Final_Rotated*1/8)+30:40+30, 65:95]
            a4 = temp_a4[int(temp_a4.shape[0]/2),int(temp_a4.shape[1]/2)]
            #print("a4: ", a4)

            temp_a6 = resized[int(height_Final_Rotated*1/4 + 50):int(height_Final_Rotated*1/2 + 60), int(height_Final_Rotated*1/8)+20:int(height_Final_Rotated*1/8+30 + 23)+40]
            #cv.imshow("temp_a6", temp_a6)
            #cv.waitKey(0)
            #print(temp_a6)
            #print(int(temp_a6.shape[0]/2))
            #print(int(temp_a6.shape[1]/2))
            a6 = temp_a6[int(temp_a6.shape[0]/2),int(temp_a6.shape[1]/2)]
            #print("a6: ", a6)


            #guarda los valores en este vector para luego proceder a su identificacion
            code = [a7,a6,a5,a4,a3,a2,a1,a0]



            #NO SE USA, PERO DE MOMENTO, NO SE BORRARA HASTA VERIFICAR QUE NO INTERFIERA CON EL FUNCIONAMIENTO
            #DE ESTE CODIGO
            if ((ColorSupIzq <= ColorSupDer) and (ColorSupIzq <= ColorInfDer) and (ColorSupIzq <= ColorInfIzq)):
                EscalaColores[0] = ColorSupIzq
            elif ((ColorSupDer <= ColorSupIzq) and (ColorSupDer <= ColorInfDer) and (ColorSupDer <= ColorInfIzq)):
                EscalaColores[0] = ColorSupDer
            elif ((ColorInfDer <= ColorSupDer) and (ColorInfDer <= ColorSupIzq) and (ColorInfDer <= ColorInfIzq)):
                EscalaColores[0] = ColorInfDer
            else:
                EscalaColores[0] = ColorInfIzq



            #print(Matriz_color)
            #Extraemos el codigo binario

            #Variable que guardara el valor del codigo
            CodigoBinString = ""

            #para debug, imprime el valor del vector de bits.
            print(code)
            #print(len(code))

            i = 0 #para evitar alguna sobreescritura de esta variable.
            for i in range (0, len(code)):
                #print(i)
                #print("codigo en la posicion i: ", code[i] )

                #con los tresholds establecidos, busca que valores sean grises y los cataloga como 1,
                #sino, los catalaga como 0.
                if code[i] > TRESHOLD_DETECT_MIN and code[i]< TRESHOLD_DETECT_MAX:

                    CodigoBinString = CodigoBinString + "1"
                else:
                    CodigoBinString = CodigoBinString + "0"



            #Guardamos los valores
            if a == 0:

                #para debug, imprime el codigo binario en formato string
                print("Codibo binario: ",CodigoBinString)

                #esta funcion pasa el string de bits a formato de numero int.
                tempID =int(CodigoBinString, 2)

                #calcula las posiciones y demas parametros del robot.
                tempFloatX = (anchoMesa / GlobalWidth) * Cx;
                tempFloatY = (largoMesa / GlobalHeigth) * Cy;
                tempX = int(tempFloatX)
                tempY = int(tempFloatY)
                tempTheta = int(tempFloatTheta)
                pos = [tempX, tempY, tempTheta]

                #para debug y seperacion
                print("ID temporal",tempID)
                print("-------------------")
                print(" ")

            else:
                #en caso de falla, aunque por las modificaciones ya no se usa,
                #de igual forma se deja para evitar errores
                tempID = 0
                tempFloatX = (anchoMesa / GlobalWidth) * Cx;
                tempFloatY = (largoMesa / GlobalHeigth) * Cy;
                tempX = int(tempFloatX)
                tempY = int(tempFloatY)
                tempTheta = int(tempFloatTheta)
                pos = [0, 0, 0]



            #En ambos return, se manda a llamar a la clase Robot para pasar sus argumentos a la clase vector_robot
            parameter_robot.append([tempID, "", pos])
    if mode == "DEBUG_ON_CAPTURE":
        return parameter_robot, resized, initial_image, image_befor_rotate #Robot(tempID,"", pos) #si ctrl es 1, se retorna el valor correcto
        #return None
    elif mode == "CAPTURE" or mode == "DEBUG":
        return parameter_robot #Robot(tempID,"", pos) #si ctrl es 1, se retorna el valor correcto
        #return None
