#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore, Qt
import pilas
import socket
import thread
from threading import Thread
import time
from pilas.interfaz.base_interfaz import BaseInterfaz
archivo = "no"
class Cliente(Thread):
    
    def __init__(self, destino, host):
        Thread.__init__(self)
        self.destino = destino
        self._socket = socket.socket()
        self._socket.connect((host, 6963))
        self.jugador1 = 0
        self.jugador2 = 0
        
    def entrada(self, dato):

        self._socket.send(str(dato))

            
    def salida(self, msj):
        mensaje = msj
        divisor = 34
        try:
            longitud = divisor - 1
            if mensaje[4]:

                parte1 = mensaje[:4]
                parte2 = mensaje[4:]
                divisible = len(mensaje) / divisor
                if divisible*divisor < len(mensaje):

                    divisible = divisible + 1 #es para lo que sobre del string
                acu = 1
                despedazado = []
                cuenta = 1
                for i in range(divisible):

                    parte = mensaje[:divisor*acu] + "\n"
                    acuant = acu -1
                    if acuant >= 0:
                        parte = mensaje[divisor*acuant:divisor*acu] + "\n"
                    self.item = QtGui.QListWidgetItem(parte)
                    self.destino.addItem(self.item)
                    self.destino.setCurrentItem(self.item)
                    acu = acu + 1
        except:
            self.item = QtGui.QListWidgetItem(mensaje)
            self.destino.addItem(self.item)
            self.destino.setCurrentItem(self.item)





#//////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                         Probar convinaciones
    def probarconvinaciones(self, msj):
        jugador = 0
        # --------Reparte   ///////////////////////////////////////////////////////////////////////
        a = msj
      
        try:

            a = a[16:]
            b = a.split(",")
            #carta 1
            distancia0 = len(b[0])
            final0 = distancia0 - 3
            b[0] = b[0][:final0]
            archivo = "cartas/" + b[0] + ".jpg"
            try:
                cartadeltipo0 = pilas.actores.Actor(archivo)
                cartadeltipo0.y = -280
                cartadeltipo0.x = -300  
   
            except:
                #print "no se pudo cargar el archivo para repartir: " + str(archivo)
                archivo = "no"
                        #carta 2
            distancia1 = len(b[1])
            final1 = distancia1 - 3
            b[1] = b[1][:final1]
            archivo = "cartas/" + b[1] + ".jpg"
            try:
                cartadeltipo1 = pilas.actores.Actor(archivo)
                cartadeltipo1.y = -280
                cartadeltipo1.x = 0          
   
            except:
                #print "no se pudo cargar el archivo del tipo: " + str(archivo)
                archivo = "no"
                        #carta 3
            distancia2 = len(b[2])
            final2 = distancia2 - 3
            b[2] = b[2][:final2]
            archivo = "cartas/" + b[2] + ".jpg"
            try:
                cartadeltipo2 = pilas.actores.Actor(archivo)
                cartadeltipo2.y = -280
                cartadeltipo2.x = 300   
           
            except:
                #print "no se pudo cargar el archivo del tipo: " + str(archivo)
                archivo = "no"
        except:
            archivo = "no"
 #Tirar y demas //////////////////////////////////////////////////////////////////////////           
 # //////////////////////////////////////////////////////////////////////////////////// 
        try:
            hecho = msj
            hatirado = hecho[18:]
            hatirado = hatirado[:9]

                        #jugador //////////////////////////////////////////
            if hatirado == "ha tirado":
                
                jugador = hecho[16]
                print "el jugador es: " + jugador
#/////////////////coordenada
                coordenada = 0
                if int(jugador) == 1:
                    self.jugador1 = self.jugador1 + 1
                    print "se le sumo 1 al jugador 1 "
                    if self.jugador1 == 1:
                        coordenada = -470
                        print coordenada
                    if self.jugador1 == 2:
                        coordenada = -340
                        print coordenada
                    if self.jugador1 == 3:
                        coordenada = -200
                        print coordenada
                if int(jugador) == 2:
                    self.jugador2 = self.jugador2 + 1
                    print "se le sumo 1 al jugador 2 "
                    if self.jugador2 == 1:
                        coordenada = 470
                        print coordenada
                    if self.jugador2 == 2:
                        coordenada = 340
                        print coordenada
                    if self.jugador2 == 3:
                        coordenada = 200
                print "la coordenada es: " + str(coordenada)
#/////////////////archivo
                cartasinproc = hecho[42:]
                longitud = len(cartasinproc)
                longitud = longitud - 6
                carta = cartasinproc[:longitud]
                archivo = "cartas/" + carta + ".jpg"
                print "Exito sabiendo la carta: " + archivo
#/////////////////subir imagen
                cartatirada = pilas.actores.Actor(imagen=archivo, x=coordenada)
        except:
            print "Por lo menos anda.." 
#Cantar //////////////////////////////////////////////////////////////////////////           
 # //////////////////////////////////////////////////////////////////////////////////// 
        try:
            comp1 = "Server: jugador_1 ha cantado :"
            comp2 = "Server: jugador_2 ha cantado :"
            #print str(comp2) + "\n" + str(comp1) + "\n" + str(msj[:30])
            if msj[:30] == comp1 or msj[:30] == comp2:
                texto = pilas.actores.Texto(msj)
                texto.y = -150
                #texto.color = (0, 0, 0)
                time.sleep(3)
                texto.eliminar()
        except:
            archivo = "no"
            print "No se pudo cantar :("

                

        
    def run(self):
        # hilo es para poder leer el teclado y el socket
        # al mismo tiempo, ya que los dos métodos se bloquean.
        self.salida("Conectado.")
        while 1:
            try:
                dato = self._socket.recv(2048) ## Esta linea
                self.probarconvinaciones(dato)
            except:
                break
            # Si dato es una cadena vacía seguro es porque el
            # server se desconectó, entonces termina el bucle.
            # (Porque se produciría un bucle infinito).
            if dato == "":
                self.salida("El server se ha desconectado.")
                break
            self.salida(dato)
            
        self.salida("Cerrando...")
        self._socket.close()
        self.salida("Cerrado.")

       
class Ventana(QtGui.QMainWindow):

    def __init__(self, canvas):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Truco-Chat")
        self.canvas = canvas
        self.resize(930, 500)
        self.move(0, 0)

        self.cwidget = QtGui.QWidget(self)
        self.layout = QtGui.QHBoxLayout()

        self.cwidget.setLayout(self.layout)
        self.setCentralWidget(self.cwidget)

        self.layout.addWidget(self.canvas, 1)

        # Creando el panel lateral
        self.layout_panel = QtGui.QVBoxLayout()
        self.layout.addLayout(self.layout_panel)

        self.CampoConectar = QtGui.QLineEdit()
        self.CampoConectar.setText("localhost")
        self.layout_panel.addWidget(self.CampoConectar)
        
        self.BotonConectar = QtGui.QPushButton("Conectar") 
        self.layout_panel.addWidget(self.BotonConectar)
        
        self.CampoEnviar = QtGui.QLineEdit()    
        self.CampoEnviar.setText("jugador_")
        self.layout_panel.addWidget(self.CampoEnviar)
        
        self.BotonEnviar = QtGui.QPushButton("Enviar")
        self.layout_panel.addWidget(self.BotonEnviar)

        

        self.lista = QtGui.QListWidget()
        #self.lista = QtGui.QTextEdit()
        self.layout_panel.addWidget(self.lista)
        #self.lista.setText("Bienvenido a Truco-Chat")

        
        #self.lista.setReadOnly(True)

        # Creando el primer mensaje
        self.item = QtGui.QListWidgetItem("Bienvenido a Truco-Chat")
        self.lista.addItem(self.item)

        #Funciones*-*-*-*
    def Conectar(self):
        
        host =  self.CampoConectar.text()
        self.ObjetoRun = Cliente(self.lista, host)
        self.ObjetoRun.start()


    
    def Enviar(self):
        mensaje =  ventana.CampoEnviar.text()
        try:
            self.ObjetoRun.entrada(str(mensaje))
            self.CampoEnviar.setText("")
        except:
            #self.lista.setText("Bienvenido a Truco-Chat\nEstas desconectado(no puedes enviar mensajes!)")
  
        #self.lista = QtGui.QTextEdit()
            #self.layout_panel.addWidget(self.lista)
        #self.lista.setText("Bienvenido a Truco-Chat")

        
        #self.lista.setReadOnly(True)

        # Creando el primer mensaje
            self.lista.clear()
            self.item = QtGui.QListWidgetItem("Bienvenido a Truco-Chat\nEstas desconectado(no puedes enviar mensajes!)")
            self.lista.addItem(self.item)
            



app = QtGui.QApplication(sys.argv[1:])





pilas.iniciar(usar_motor="qtsugar", ancho=1058, alto=725)


canvas = pilas.mundo.motor.canvas
ventana = Ventana(canvas)
aceituna = pilas.actores.Actor("aceituna.png")
aceituna.radio_de_colision = 17
aceituna.aprender(pilas.habilidades.RebotarComoPelota)
aceituna.aprender(pilas.habilidades.Arrastrable)
boton = pilas.interfaz.Boton("Desconectar")
boton.y = 100
boton.x = -390
boton2 = pilas.interfaz.Boton("nick:")
boton2.y = 100
boton2.x = -310
boton3 = pilas.interfaz.Boton("cantar:")
boton3.y = 100
boton3.x = -250
boton4 = pilas.interfaz.Boton("tirar:")
boton4.y = 100
boton4.x = -190
boton5 = pilas.interfaz.Boton("nueva_partida")
boton5.y = 100
boton5.x = -100
boton6 = pilas.interfaz.Boton("comandos")
boton6.y = 100
boton6.x = 0
boton7 = pilas.interfaz.Boton("puntaje")
boton7.y = 100
boton7.x = 90
boton8 = pilas.interfaz.Boton("pedir:")
boton8.y = 100
boton8.x = 160
def puntaje():
    try:
        ventana.ObjetoRun.entrada("puntaje")
    except:

        ventana.lista.clear()
        ventana.item = QtGui.QListWidgetItem("Bienvenido a Truco-Chat\nEstas desconectado(no puedes enviar mensajes!)")
        ventana.lista.addItem(ventana.item)
def comandos():
    try:
        ventana.ObjetoRun.entrada("comandos")
    except:

        ventana.lista.clear()
        ventana.item = QtGui.QListWidgetItem("Bienvenido a Truco-Chat\nEstas desconectado(no puedes enviar mensajes!)")
        ventana.lista.addItem(ventana.item)  
def cuando_desconectan():
    try:
        ventana.ObjetoRun.entrada("desconectar")
    except:

        ventana.lista.clear()
        ventana.item = QtGui.QListWidgetItem("Bienvenido a Truco-Chat\nEstas desconectado(no puedes enviar mensajes!)")
        ventana.lista.addItem(ventana.item)              
def nueva_partida():
    try:
        ventana.ObjetoRun.entrada("nueva_partida")
    except:

        ventana.lista.clear()
        ventana.item = QtGui.QListWidgetItem("Bienvenido a Truco-Chat\nEstas desconectado(no puedes enviar mensajes!)")
        ventana.lista.addItem(ventana.item)


def nick():
    try:
        parte2 = ventana.CampoEnviar.text()
        ventana.CampoEnviar.setText("")
        todo = str("nick:") + str(parte2)
        ventana.ObjetoRun.entrada(str(todo))
    except:

        ventana.lista.clear()
        ventana.item = QtGui.QListWidgetItem("Bienvenido a Truco-Chat\nEstas desconectado(no puedes enviar mensajes!)")
        ventana.lista.addItem(ventana.item)
def pedir():
    try:
        parte2 = ventana.CampoEnviar.text()
        ventana.CampoEnviar.setText("")
        todo = str("pedir:") + str(parte2)
        ventana.ObjetoRun.entrada(str(todo))
    except:

        ventana.lista.clear()
        ventana.item = QtGui.QListWidgetItem("Bienvenido a Truco-Chat\nEstas desconectado(no puedes enviar mensajes!)")
        ventana.lista.addItem(ventana.item)

def cantar():
    try:
        parte2 = ventana.CampoEnviar.text()
        ventana.CampoEnviar.setText("")
        todo = str("cantar:") + str(parte2)
        ventana.ObjetoRun.entrada(str(todo))
    except:

        ventana.lista.clear()
        ventana.item = QtGui.QListWidgetItem("Bienvenido a Truco-Chat\nEstas desconectado(no puedes enviar mensajes!)")
        ventana.lista.addItem(ventana.item)
def tirar():
    try:
        parte2 = ventana.CampoEnviar.text()
        ventana.CampoEnviar.setText("")
        todo = str("tirar:") + str(parte2)
        ventana.ObjetoRun.entrada(str(todo))
    except:

        ventana.lista.clear()
        ventana.item = QtGui.QListWidgetItem("Bienvenido a Truco-Chat\nEstas desconectado(no puedes enviar mensajes!)")
        ventana.lista.addItem(ventana.item)


boton.conectar(cuando_desconectan)
boton2.conectar(nick)
boton3.conectar(cantar)
boton4.conectar(tirar)
boton5.conectar(nueva_partida)
boton6.conectar(comandos)
boton7.conectar(puntaje)
boton8.conectar(pedir)
app.connect(ventana.BotonConectar, Qt.SIGNAL("clicked()"), ventana.Conectar)
app.connect(ventana.BotonEnviar, Qt.SIGNAL("clicked()"), ventana.Enviar)
ventana.show()
sys.exit(app.exec_())


