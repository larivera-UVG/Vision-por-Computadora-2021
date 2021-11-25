#Prueba de cliente con comunicación a traves de sockets.
#!/usr/bin/env python3

import socket

HOST = '192.168.1.14'  # Nombre del servidor o dirección IP
PORT = 65432        # Puerto para realizar la conexión

sendData = input('> ')
while(sendData != ''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # Declaración de socket. De esta manera, no hay necesidad de cerrarla con .close()
        s.connect((HOST, PORT))                                     # Conectar al servidor a través del puerto de arriba
        s.sendall(bytes(sendData, 'utf-8'))                         # Enviar la data en formato de bytes
        data = s.recv(1024)                                         # Recibir los bytes siguientes

    print('Received', data.decode("utf-8"))                         # Desplegar lo recivido
    sendData = input('> ')
