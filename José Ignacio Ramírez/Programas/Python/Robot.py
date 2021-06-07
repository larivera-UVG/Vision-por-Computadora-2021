#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 18:49:30 2020

@author: Jose Pablo Guerra

Codigo para la toma de poses de robots en la mesa de pruebas.


15/07/2020: Version 0.0.0 -- Creacion del archivo inicial.
15/07/2020: Version 0.1.0 -- Se crean los primeros metodos iniciales y las clases de robot y vector_robot
16/07/2020: Version 0.2.0 -- Se agregan funciones adicionales para su funcionamiento. 
19/07/2020: Version 0.2.1 -- Se eliminan funciones, se dejan solo los metodos y clases de Robot. Cambio nombre archivo.


Basado en el codigo escrito por André Rodas
"""
#Importando las librerias necesarias
import cv2 as cv #importando libreria para opencv 
import numpy as np #para la creacion de arrays
import math as mt #para el uso de herramientas matematicas como raiz cuadrada
#Robot = []


class Robot():
    """
    """
        
    def set_robot(self, _id, _ip, _pos):
        """
        

        Parameters
        ----------
        _id : TYPE
            DESCRIPTION.
        _ip : TYPE
            DESCRIPTION.
        _pos : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self.id_robot = _id
        self.ip = _ip
        self.x = _pos[0]
        self.y = _pos[1]
        self.theta = _pos[2]
        self.vel_left = 0
        self.vel_right = self.vel_left
        self.robot = [self.id_robot,self.ip,self.x,self.y,self.theta,self.vel_right,self.vel_left]
        return self.robot
        
    def set_IP(self,ip):
        """
        

        Parameters
        ----------
        ip : TYPE
            DESCRIPTION.

        Returns
        -------
        ip : TYPE
            DESCRIPTION.

        """
        self.ip = ip
        return ip
    
    def set_pos(self, pos):
        """
        

        Parameters
        ----------
        pos : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.x = pos[0]
        self.y = pos[1]
        self.theta = pos[2]
        
    def get_pos(self):
        """
        

        Returns
        -------
        Pos : TYPE
            DESCRIPTION.

        """
        Pos = []
        Pos.append(self.x)
        Pos.append(self.y)
        Pos.append(self.theta)
        return Pos
        
    def get_IP (self):
        """
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.ip
    
    def set_speed(self, vel):
        """
        

        Parameters
        ----------
        vel : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.vel_right = vel[0]
        self.vel_left = vel[1]
        
    def get_speed(self):
        """
        

        Returns
        -------
        speed : TYPE
            DESCRIPTION.

        """
        speed = []
        speed.append(self.vel_right)
        speed.append(self.vel_left)
        return speed
    
    
class vector_robot():
    """
    """
    #robot_vector_u = Robot()
    def __init__(self):
        self.Robot_vector = []
        
    
    def agregar_robot(self,vector_robot):
        """
        

        Parameters
        ----------
        vector_robot : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        #self.class_robot = class_robot
        #class_robot.id_robot = self
        #global _Robot
        self.Robot_vector.append(vector_robot)
        return self.Robot_vector
    
    def search_id_robot(self, _id):
        """
        

        Parameters
        ----------
        _id : TYPE
            DESCRIPTION.

        Returns
        -------
        final_ID : TYPE
            DESCRIPTION.

        """
        final_ID = -1
        for i in range (0, len(self.Robot_vector)):
            temp_Robot = self.Robot_vector[i]
            if (temp_Robot[0] == _id):
                final_ID = i 
                break
        return final_ID
    
    def get_robot(self, _id):
        """
        

        Parameters
        ----------
        _id : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        if _id == 0:
            return print("No hay robot")
        else:
            return self.Robot_vector[_id]
        


