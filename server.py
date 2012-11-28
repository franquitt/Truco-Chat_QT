#!/usr/bin/env python
# -*- coding: utf-8 -*-

# diguito69 : chat con nick
# Agresta corp. : Truco Chat V2.3


import socket
import threading
import os
import select
import random
import time
def repartidor():
    """Funcion general.. reparte las cartas"""
    cartas_posibles=["1_de_espada", "2_de_espada", "3_de_espada", "4_de_espada", "5_de_espada", "6_de_espada", "7_de_espada", "10_de_espada", "11_de_espada", "12_de_espada", "1_de_copa", "2_de_copa", "3_de_copa", "4_de_copa", "5_de_copa", "6_de_copa", "7_de_copa", "10_de_copa", "11_de_copa", "12_de_copa", "1_de_oro", "2_de_oro", "3_de_oro", "4_de_oro", "5_de_oro", "6_de_oro", "7_de_oro", "10_de_oro", "11_de_oro", "12_de_oro", "1_de_basto", "2_de_basto", "3_de_basto", "4_de_basto", "5_de_basto", "6_de_basto", "7_de_basto", "10_de_basto", "11_de_basto", "12_de_basto"]
    pack_1 = []
    pack_2 = []
    for i in range(3): #el truco necesita 3 cartas por jugador
        carta_elegida = random.choice(cartas_posibles) # elegimos una carta al azar
        pack_1.append(carta_elegida) #la agregamos a la lista personal del jugador
        cartas_posibles.remove(carta_elegida) # la removemos_de_la lista general para que no salga_de_vuelta

    for i in range(3): #Identico a los puntos anteriores, pero manejando la lista del otro jugador
        carta_elegida = random.choice(cartas_posibles)
        pack_2.append(carta_elegida)
        cartas_posibles.remove(carta_elegida)
    for i in range(3):
        pack_1[i] = pack_1[i] + "(" + str(i) + ")"
        pack_2[i] = pack_2[i] + "(" + str(i) + ")"
    return pack_1, pack_2

def esperar(tiempo):
    time.sleep(int(tiempo))


class Server(threading.Thread):

    def __init__(self, socket_server): #el constructor DEBE recibir un objeto socket como parametro
        threading.Thread.__init__(self)
        self.socket_server = socket_server
        self._read_fd, self._write_fd = os.pipe()
        self.clientes = [self._read_fd]
        self.nick = {}
        self.cartas1=[]
        self.cartas2=[]
        self.cartaq1=[]
        self.cartaq2=[]
        self.puntaje1 = 0
        self.puntaje2 = 0

               
    def run(self):
        salir = False
        jugador1 = False
        jugador2 = False
        pedidodejug1 = False #pedidos_de_puntos(una variable por jugador)
        pedidodejug2 = False #
        termjug1 = False #pedidos_de_terminar la ronda(una variable por jugador)
        termjug2 = False #
        comenzar_partida = False
        apedir = 0 #puntaje que se pide        
        finjugador1 = False
        finjugador2 = False



        while not salir:
            clientes, b, c = select.select(self.clientes, [], [])
            for cliente in clientes:
                if (cliente == self._read_fd):
                    if os.read(self._read_fd, 1) == '0':
                        salir = True
                        break

                elif pedidodejug1 == True and self.nick[cliente] == "jugador_2":
                        cliente.send("jugador_1 ha pedido " + apedir + " puntos. Aceptar ? s/n") #(revisado)
                        msj = cliente.recv(2048)
                        esperar(1)
                        if msj == "n": # -------------------sub COMANDO-----(revisado)------

                            self.enviar("server", self.nick[cliente] + " ha denegado la peticion_de_puntos. ")
                            pedidodejug1 = False
                        elif msj == "s": # -------------------sub COMANDO -----(revisado)-------
                            self.puntaje1 = self.puntaje1 + int(apedir)
                            self.enviar("server", self.nick[cliente] + " ha aceptado la peticion_de_puntos. ")
                            pedidodejug1 = False

                elif pedidodejug2 == True and self.nick[cliente] == "jugador_1":
                        cliente.send("jugador_2 ha pedido " + apedir + " puntos. Aceptar ? s/n")
                        msj = cliente.recv(2048)
                        esperar(1)
                        if msj == "n": # -------------------sub COMANDO----(revisado)----------------

                            self.enviar("server", self.nick[cliente] + " ha denegado la peticion_de_puntos. ")
                            pedidodejug2 = False
                        elif msj == "s": # -------------------sub COMANDO ------(revisado)--------------
                            self.puntaje2 = self.puntaje2 + int(apedir)
                            self.enviar("server", self.nick[cliente] + " ha aceptado la peticion_de_puntos. ")
                            pedidodejug2 = False
                        esperar(1)

                elif termjug1 == True and self.nick[cliente] == "jugador_2":
                        cliente.send("jugador_1 ha pedido terminar. Aceptar ? s/n\n")
                        msj = cliente.recv(2048)
                        esperar(1)
                        if msj == "n": # -------------------SUB COMANDO--------------------

                            self.enviar("server", self.nick[cliente] + " ha denegado la peticion_de_terminar. \n")
                            termjug1 = False
                        elif msj == "s": # -------------------SUB COMANDO --------------------

                            self.enviar("server", self.nick[cliente] + " ha aceptado la peticion_de_terminar. \n")
                            self.puntaje()
                            comenzar_partida = False
                            termjug1 = False

                elif termjug2 == True and self.nick[cliente] == "jugador_1":
                        cliente.send("jugador_2 ha pedido terminar. Aceptar ? s/n\n")
                        msj = cliente.recv(2048)
                        esperar(1)
                        if msj == "n": # -------------------SUB COMANDO--------------------

                            self.enviar("server", self.nick[cliente] + " ha denegado la peticion_de_terminar. \n")

                            termjug2 = False
                        elif msj == "s": # -------------------SUB COMANDO --------------------

                            self.enviar("server", self.nick[cliente] + " ha aceptado la peticion_de_terminar. \n")
                            self.puntaje()
                            comenzar_partida = False
                            termjug2 = False
                        esperar(1)
                        
                        
   

                else: # -----------------------Termina el caso_de_pedidos ------------------------

                    
                    msj = cliente.recv(2048) ## Esta linea recibe
                    if msj == "desconectar": # -------------------COMANDO 1------(revisado)--------------

                        # Un cliente se desconect�.
                        self.enviar("server", self.nick[cliente] + " se a desconectado. ")
                        if self.nick[cliente] == "jugador_1":
                            jugador1 = False
                            pedidodejug1 = False
                            termjug1 = False
                            comenzar_partida = False
                            apedir = 0 #puntaje que se pide
                            self.cartas1=[]
                            self.cartaq1=[]
                            self.puntaje1 = 0
                            finjugador1 = True

                        elif self.nick[cliente] == "jugador_2":
                            jugador2 = False
                            pedidodejug2 = False
                            termjug2 = False
                            comenzar_partida = False
                            apedir = 0 #puntaje que se pide
                            self.cartas2=[]
                            self.cartaq2=[]
                            self.puntaje2 = 0
                            finjugador2 = True
                        if finjugador2 == True:
                            if finjugador1 == True:
                                finjugador2 = False  
                                finjugador1 = False
                                print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nJugadores desconectados, se limpiaron  las variables.\n\n\n\n\n\n\n" 
                        cliente.close()
                        self.clientes.remove(cliente)
                        del self.nick[cliente]
                        



                    elif msj.startswith("Server:"): # -------------------COMANDO FALSO------(revisado)------
                        cliente.send("Tu no puedes hacer eso!\n")
                    elif msj.startswith(" Server:"): # -------------------COMANDO FALSO------(revisado)------
                        cliente.send("Tu no puedes hacer eso!\n")



                    elif msj.startswith("cantar:") and comenzar_partida == True: # COMANDO2---(revisado)-----
                        self.enviar("server", self.nick[cliente] + " ha cantado " + msj[6:] + ". \n")



                    elif msj == "puntaje" and comenzar_partida == True: # --------COMANDO3--(revisado)------
                        self.puntaje()



                    elif msj == "terminar" and comenzar_partida == True: # -------COMANDO4-------------------(revisado)------
                        self.enviar("server", self.nick[cliente] + " ha pedido terminar la ronda. s/n\n")
                        if self.nick[cliente] == "jugador_1":
                            termjug1 = True
                        elif self.nick[cliente] == "jugador_2":
                            termjug2 = True



                    elif msj.startswith("pedir:") and comenzar_partida == True: #COMANDO 5(revisado)
                        apedir = msj[6:]
                        self.enviar("server", self.nick[cliente] + " ha pedido " + apedir + " puntos.\n")
                        if self.nick[cliente] == "jugador_1":
                            pedidodejug1 = True
                        elif self.nick[cliente] == "jugador_2":
                            pedidodejug2 = True



                    elif msj.startswith("tirar:") and comenzar_partida == True: # COMANDO 6(revisado)----
                        numerodecarta = msj[6]
                        usar = True
                        
                        if self.nick[cliente] == "jugador_1":
                            for i in self.cartaq1:
                                print i
                                if numerodecarta == i:
                                    usar=False
                            if usar != False:
                        
                                carta = self.cartas1[int(numerodecarta)]
                                self.cartaq1.append(numerodecarta)
                                self.enviar("server", self.nick[cliente] + " ha tirado en la mesa el " + carta + ". \n")
                            else:
                                self.enviar("server", self.nick[cliente] + " intento tirar en la mesa una carta ya usada.. \n")
                        else:
                            for i in self.cartaq2:
                                print i
                                if numerodecarta == i:
                                    usar=False
                                    print numerodecarta
                                    print 'usar=false'
                            if usar != False:
                                carta = self.cartas2[int(numerodecarta)]
                                self.cartaq2.append(numerodecarta)
                                self.enviar("server", self.nick[cliente] + " ha tirado en la mesa el " + carta + ". \n")
                            else:
                                self.enviar("server", self.nick[cliente] + " intento tirar en la mesa una carta ya usada.. \n")



                    elif msj.startswith("nick:") and comenzar_partida == False: # COMANDO 7(revisado)---
                        # Un cliente se cambia el nick.
                        nick = self.nick[cliente]
                        if msj[5]:
                            self.nick[cliente] = msj[5:]
                        else:
                            datos_cliente = cliente.getpeername()
                            self.nick[cliente] = datos_cliente[0] + ":" + str(datos_cliente[1])
                        self.enviar("server", nick + " se a cambiado el nombre a " + self.nick[cliente])

                        if self.nick[cliente] == "jugador_1": # -----SUB COMANDO(revisado)-----
                            jugador1 = True
                            esperar(1)
                            self.enviar("server", " jugador 1 activado")
                        if self.nick[cliente] == "jugador_2": # -------SUB COMANDO(revisado)-----
                            jugador2 = True
                            esperar(1)
                            self.enviar("server", " jugador 2 activado")



                    elif msj == "decir_cartas" and comenzar_partida == True: # ----COMANDO 8(revisado)-----
                        self.decircartas()
                        


                    elif msj == "nueva_partida" and comenzar_partida == False: #COMANDO 9(revisado)--
                        if jugador1 == True and jugador2 == True:
                            comenzar_partida = True

                            self.enviar("server", " --La partida ha comenzado-- ")
                            esperar(1)
                            self.enviar("server", " Espere por favor...")
                            esperar(2)
                            self.repartir_y_decir()
                        else:
                            self.enviar("server", " Error, jugadores no definidos...(jugador_1 y jugador_2)")
                    
                    elif msj == "comandos": # --------COMANDO9--(revisado)------
                        mensaje = "desconectar\ncantar\npuntaje\npedir\nterminar\ntirar\nnick\nnueva_partida\n"
                        self.enviar("server", mensaje)


                    else:
                        # Un cliente envia un mensaje.(revisado)
                        self.enviar(cliente, msj)
    


    def enviar(self, emisor, msj):
        """Env�a un mensaje a todos los clientes_de_la lista."""
        if emisor == "server":
            mensaje = "Server: " + msj
        elif emisor == "nada": # -------------------Mensaje "Sin Emisor"--------------------
            mensaje = msj
        else:
            mensaje = self.nick[emisor] + " dijo: " + msj
        print mensaje
        for cliente in self.clientes:
            if cliente != self._read_fd:
                cliente.send(mensaje)

    def puntaje(self):
        """Dice el puntaje"""
        msj = "El puntaje es:\nJugador_1: " + str(self.puntaje1) + "\nJugador_2: " + str(self.puntaje2)
        mensaje = "Server: " + msj
        print mensaje
        for cliente in self.clientes:
            if cliente != self._read_fd:
                cliente.send(mensaje)
    

    def repartir_y_decir(self):
        """Reparte y dice las cartas"""
        self.cartas1, self.cartas2 = repartidor()
        for cliente in self.clientes:
            if cliente != self._read_fd:


                if self.nick[cliente] == "jugador_1":
                    cliente.send("Tus cartas son: " + self.cartas1[0] + "," + self.cartas1[1] + "," + self.cartas1[2])

                if self.nick[cliente] == "jugador_2":
                    cliente.send("Tus cartas son: " + self.cartas2[0] + "," + self.cartas2[1] + "," + self.cartas2[2] )

  
    def decircartas(self):
        """Dice las cartas"""
        for cliente in self.clientes:
            if cliente != self._read_fd:


                if self.nick[cliente] == "jugador_1":
                    cliente.send("Tus cartas son: " + self.cartas1[0] + "," + self.cartas1[1] + "," + self.cartas1[2] )

                if self.nick[cliente] == "jugador_2":
                    cliente.send("Tus cartas son: " + self.cartas2[0] + "," + self.cartas2[1] + "," + self.cartas2[2])


       
    def agregar_cliente(self, socket_cliente):
        """Agrega un cliente a la lista_de_clientes conectados."""
        self.clientes.append(socket_cliente)
        datos_cliente = socket_cliente.getpeername()
        self.nick[socket_cliente] = datos_cliente[0] + ":" + str(datos_cliente[1])
        os.write(self._write_fd, '1')
    
    def cerrar(self):
        """Libera el select e indica que termine el thread."""
        os.write(self._write_fd, '0')
        
                              
def main():
    socket_server = socket.socket() #creamos un objeto socket
    socket_server.bind(("", 6963)) #con el objeto socket creamos un server
    socket_server.listen(1) #definimos la Cola maxima_de_clientes esperando para conectarse
    chat_server = Server(socket_server) #creamos un objeto server y le pasamos como parametro el objeto socket
    chat_server.start() #corremos la funcion run del objeto server( se va a ejecutar en un hilo distinto y podremos obtener nuevos clintes mientras la corremos)
    print "Server listo, esperando conexiones.\n\n--> Para apagar el server o cerarlo, por favor apriete ctrl + c <--"
    while 1:
        try:
            socket_cliente, datos_cliente = socket_server.accept() #Aceptamos conecciones y obtenemos un objeto socket(del cliente) y la direccion

        except KeyboardInterrupt:
            chat_server.cerrar()
            break
        chat_server.enviar("server", datos_cliente[0] + ":" + str(datos_cliente[1]) + " se a conectado.")
        chat_server.agregar_cliente(socket_cliente)
    print "\nCerrando..."
    socket_server.close()
    
if __name__ == "__main__":
    main()
