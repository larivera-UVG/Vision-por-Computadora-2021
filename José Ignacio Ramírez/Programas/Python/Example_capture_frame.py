#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 16:11:59 2020

@author: joseguerra
"""
import cv2 as cv #importando libreria para opencv
import threading as th
import time

# In[Defnieno funciones multi-hilos]
videoCaptureObject = cv.VideoCapture(0)
frame_buffer_capture = []
processing_buffer = []
actual_frame = []
lock = th.Lock() #Funciona como el semaphore en C. Aunque python tiene una funcion 'semaphore' se tiene un 
                        #mejor control en cuanto a sincronizacion usando este recurso de Lock()
lock2 = th.RLock()


# The duration in seconds of the video captured
capture_duration = 1

#cap = cv2.VideoCapture(0)

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))


#cap, frame = videoCaptureObject.read()
def capturar_frame():
    print("entre a capturar")
    ret, frame = videoCaptureObject.read()
    return frame

"""
def image_process():
    global frame_buffer
    
    while(1):
        lock2.acquire() #Analogo a semaphore. Bloquea el recurso hasta que se envie la orden de liberarlo.
        actual_frame = frame_buffer_capture[0]
        frame_buffer_capture.pop(0)
        cv.imshow('Capturing Video',actual_frame)
        cv.waitKey(0)
        lock2.release() #libera el recurso para alguien mas 
    
        
def getting_pose_from_frame():
    global actual_frame
    lock.acquire() #Analogo a semaphore. Bloquea el recurso hasta que se envie la orden de liberarlo.
    

    lock2.release() #libera el recurso para alguien mas 
"""
#global frame
#capturar = th.Thread(target = Capturar) #asignacion de los hilos a una variable
#procesar = th.Thread(target = image_process) #asignacion de los hilos a una variable
#mostrar = th.Thread(target = getting_pose_from_frame) #asignacion de los hilos a una variable
#escribiendo = threading.Thread(target = Escritura) #asignacion de los hilos a una variable
#capturar.start() #inicializa el hilo.
#procesar.start() #inicializa el hilo.
#mostrar.start() #inicializa el hilo.

while(True):
    if cv.waitKey(1000):
        frame2 = capturar_frame()
        cv.imshow("frame", frame2)
        #k = cv.waitKey(1) #k = 1 es para espacio
        k = cv.waitKey(1) & 0xFF
        if k == ord('q'):
            break


#procesar.join()
#mostrar.join()