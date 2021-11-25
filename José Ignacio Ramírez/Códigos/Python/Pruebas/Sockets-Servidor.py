#Prueba de servidor con comunicación a través de sockets.
#!/usr/bin/env python3

import socket

HOST = '172.16.32.159'  # Dirrección del dispositivo que servirá como servidor
PORT = 65432        # Puerto a traves del cual se estara escuchando (Puertos sin privilegios son > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # Declaración de socket. De esta manera, no hay necesidad de cerrarla con .close()
    s.bind((HOST, PORT))                                        # Vincular el socket con la ip y puerto definidos
    while(True):                                                # Repetir siempre
        try:                                                    # En caso de error, no terminar la ejecución
            s.listen()                                          # Escuchar el socket hasta recibir un mensaje
            conn, addr = s.accept()                             # Obtener datos de connexión
            with conn:
                print('Connected by', addr)                     # Mostrar ip que realiza la connexión
                while True:
                    data = conn.recv(1024)                      # Recibir todos los datos siguientes
                    print(type(data))                           # Mostrar información de la data recibida
                    print(len(data))
                    print(data.decode("utf-8"))
                    if not data:                                # Hasta que el dato sea un byte vacío
                        break
                    conn.sendall(data)                          # Enviar de vuelta la misma data
        except:
            pass
