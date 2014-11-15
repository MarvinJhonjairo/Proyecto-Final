#------------Proyecto------------
#para cargar: sudo python Proyecto.py

#Importamos las galerias de twitter, tiempo y GPIO
import tweepy
import time
import RPi.GPIO as GPIO
import datetime     # Libreria para la fecha y hora actual 

# Se crea y abre el archivo para que se pueda escribir
    archivo=open('datos.txt','w')
	
#Pines de entrada o salida
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(22,GPIO.OUT) #led cuarto 1
GPIO.setup(11,GPIO.OUT) #led cuarto 2
GPIO.setup(8,GPIO.OUT) #abrir porton
GPIO.setup(7,GPIO.OUT) #cerrar porton
GPIO.setup(14,GPIO.OUT) #Reset alarma
GPIO.setup(10,GPIO.IN)  #alarma

#claves de aplicacion de twitter creada
CONSUMER_KEY = 'dY10qQMsqvE7FdG7TNzW4RXkB'
CONSUMER_SECRET = 'hM1Zvy6OElIxZhipBZssZAamXeBd75m4SyJueCNLc7M590rkKR'
ACCESS_KEY = '2784664589-h6ZsEmz0vJpNgRO3moMr61CVABodWlDd7HjgerK'
ACCESS_SECRET = '4F0yNDxluHuKVctLY97mWfjMYHN3zzRArLE479CkLr7uC'

#En esta parte nos identifica para poder realizar operaciones en la cuenta de twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

#variables
control = "control" #esta variable de control
comando = "comando" #variable donde guardaremos el texto del twitter 
x = tweepy.API(auth)
y = tweepy.API(auth)
z=0 #contador para alarma
num=1 #contador para alarma

# Se inicializan los valores de nuestro grafo, se definen los valores iniciales y también las relaciones que tenemos
# entre las alarmas y nuestro grafo (casa)
archivo.write("CREATE (casa:Customer {id: 'Casa',name: 'Casa'})"+"\n")
archivo.write("CREATE (alarma1:Tipo {id: 'A1', date: 20130928})"+"\n")
archivo.write("CREATE (alarma1)-[:NEXT]->(alarma2:Tipo {id: 'A2', date: 20140129})"+"\n")
archivo.write("CREATE (alarma2)-[:NEXT]-> (alarma3:Tipo {id: 'A3', date: 20141010})"+"\n")
archivo.write("CREATE (casa)-[:SAVED]->(alarma1)"+"\n")
archivo.write("CREATE (casa)-[:SAVED]->(alarma2)"+"\n")
archivo.write("CREATE (casa)-[:SAVED]->(alarma3)"+"\n")

while True:#ciclo infinito
    for tweets in x.user_timeline(count=1): #nos permite leer solo el ultimo tweet
		now = datetime.datetime.now()
# Se hace este casteamiento para poder escribir en el archivo de texto
		valor = str(now)
		rpta = str(num)
                comando = tweets.text	
#----------------------------------------------------------alarma			
                if (GPIO.input(10) ):
                    print "Alarma activada"
                    z=z+1
# Se llama el método write utilizado para escribir en el archivo de texto el nodo y los valores que se activaron para la alarma global
					archivo.write("CREATE (Activada"+rpta+":Alerta {id: 'Activada"+rpta+"',name: '"valor"'})"+"\n")
					archivo.write("CREATE (Activada"+rpta+")-[:SAVED{hora:['Hora']}]->(alarma1)"+"\n")
					num = num +1
                    y.update_status('!!!ALERTA ALARMA ACTIVADA!!! @jhonajarro   '+str(z))#tweet de aviso de alarma activada
                    time.sleep(3)
#----------------------------------------------------------
					
                if control != comando: #este if nos ayuda que solo envié una vez por tweet la orden
#----------------------------------------------------------cuarto 1
				if comando in "Encender luz 1": #Enciende el led 1, si lee un tweet con (Encender luz 1)
                                print("led 1 prendido")
                                GPIO.output(22,GPIO.HIGH)
# Se escribe en el archivo de texto el siguiente nodo con la hora y fecha de la activación del cuarto uno
								archivo.write("CREATE (Activada"+rpta+":Alerta {id: 'Activada"+rpta+"',name: '"valor"'})"+"\n")
								archivo.write("CREATE (Activada"+rpta+")-[:SAVED{hora:['Hora']}]->(alarma2)"+"\n")
								num = num +1
                                control = comando #asignacion para no volver a entrar hasta que se escriba un nuevo tweet
  
				elif comando in "Apagar luz 1": #apaga el led 1 
                                print("led 1 apagado")
                                GPIO.output(22,GPIO.LOW)
                                control = comando

#----------------------------------------------------------cuarto 2                                
                        if comando in "Encender luz 2": #prende led 2 
                                print("led 2 prendido")
                                GPIO.output(11,GPIO.HIGH)
# Se escribe en el archivo de texto el siguiente nodo con la hora y fecha de la activación del cuarto dos
								archivo.write("CREATE (Activada"+rpta+":Alerta {id: 'Activada"+rpta+"',name: '"valor"'})"+"\n")
								archivo.write("CREATE (Activada"+rpta+")-[:SAVED{hora:['Hora']}]->(alarma3)"+"\n")
								num = num +1
                                control = comando
								
                        elif comando in "Apagar luz 2": #apaga led 2 
                                print("led 2 apagado")
                                GPIO.output(11,GPIO.LOW)
                                control = comando
#----------------------------------------------------------abrir
                                
                        if comando in "Abrir porton ": # Abre el porton
                                print("Motor activado")
                                GPIO.output(8,GPIO.HIGH)
                                time.sleep(6)
                                GPIO.output(8,GPIO.LOW)# Detiene la apertura del porton
# Se escribe en el archivo de texto el siguiente nodo con la hora y fecha en que se abre el porton para su control
								archivo.write("CREATE (Activada"+rpta+":Alerta {id: 'Activada"+rpta+"',name: '"valor"'})"+"\n")
								archivo.write("CREATE (Activada"+rpta+")-[:SAVED{hora:['Hora']}]->(alarma4)"+"\n")
								num = num +1
                                control = comando
								
                        elif comando in "Desactivar": 
                                print("Motor apagado")
                                GPIO.output(8,GPIO.LOW)
                                control = comando
#----------------------------------------------------------cerrar
                                
                        if comando in "Cerrar porton": #Cierra porton
                                print("Motor activado")
                                GPIO.output(7,GPIO.HIGH)
                                time.sleep(6)
                                GPIO.output(7,GPIO.LOW)# Detiene el cierre del porton
                                control = comando
                        elif comando in "Desactivado": 
                                print("Motor apagado")
                                GPIO.output(7,GPIO.LOW)		
                                control = comando
								
#----------------------------------------------------------apagar alarma								
				if comando in "Reset alarma": 
                                print("Reset alarma")
                                GPIO.output(14,GPIO.HIGH)
				time.sleep(1)
				GPIO.output(14,GPIO.LOW)
                                control = comando

                                elif comando in "Activado": #Encendido
                                print("Sistema activo")
                                control = comando

    time.sleep(5) #leera el ultimo tweet cada 5 segundos
