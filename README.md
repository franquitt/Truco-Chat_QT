Truco-Chat
==========

Este juego es una versión del conocido juego de cartas "Truco", realizado en python a través del módulo pilas, el cual facilita la creación de juegos en 2 dimensiones.

La característica principal que ofrece esta opción de truco virtual es el chat. Esta implementación fue pensada para proporcionarle un mayor parecido al juego en la vida real.


Reglas - ¿Cómo se juega?
------------------------

Para aquel que no sabe cómo se juega al truco y quiere comenzar, le aconsejamos que consulte las reglas del juego en el siguiente <a href="http://es.wikipedia.org/wiki/Truco_argentino">link</a>.


Modo de uso
-----------

Sistema de puntajes
*******************

Una de las características de esta versión es el sistema de puntos, que no es llevado a cabo por el sistema, sino por los jugadores.

Cada jugador al terminar la ronda deberá reclamar sus correspondientes puntos al otro jugador, haciendo que se parezca más a la realidad.


Comandos
********

1. ``desconectar``: Este comando se usa para desconectarse del servidor.
2. ``cantar:``: Luego de este comando se escribe la proposicion (truco, envido, etc) para decirla de una manera formal.
3. ``terminar``: Hace que se termine la ronda. Cabe destacar que el otro jugador, luego de que se haya ejecutado el comando, debe escribir 'n'(para no terminar la ronda) o 's' (para terminar la ronda).
4. ``pedir:``: Luego de este comando se escribe los puntos (en numeros) que el jugador reclama. Cabe destacar que el otro jugador, luego de que se haya ejecutado el comando, debe escribir 'n'(para no entregar los puntos) o 's' (para entregar los puntos).
5. ``tirar:``: Luego de este comando se escribe el numero de carta que el jugador  usa en la 'mesa'(no podra usarla de nuevo).
6. ``nick:``: Luego de este comando se escribe el nick que el usuario quiere ponerse.
7. ``decir_cartas``: Le dice las respectivas cartas que posee a cada jugador.
8. ``nueva_partida``: Inicia una nueva ronda.
9. ``puntaje``: Les muestra los puntajes a los jugadores
10. ``comandos``: Muestra una lista de comandos disponibles.

Enviar mensaje
**************

Para enviar un mensaje a otro jugador simplemente habrá que ingresar el mensaje (o comando) en el cuadro de Enviar y presionar el botón enviar.


Conectarse con el host
**********************

Deberá ingresar la direccion de intranet (de la computadora que esta corriendo el archivo server) en el cuadro de arriba y luego presionar conectar. Si todo salió bien deberia decir en el cuadro de conversación "conectado".


Acerca de...
------------
Truco-Chat y Truco-Chat_QT esta creado y desarrollado por Franco Agresta(Argentina). Estas dos obras son libres de usarse, distribuirse y modificarse(software libre y open source).
En el caso de distribución y modificación: Se podrán llevar a cabo estas acciones solo con la condición que se reconozca a Franco Agresta como autor del software que se usó como base y que la nueva obra sea software libre y open source.
