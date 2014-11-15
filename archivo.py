# *****************************************************************
# Lectura de archivos de texto y grabación de la fecha y hora en un
# ciclo con contador
# Marvin Najarro - 13
# Max de León - 13012
# Rony Ajtún - 13
# Henry Orellana
# 9/11/2014
# *****************************************************************

# *****************************************************************
# Literatura citada para el programa 
# http://docs.python.org.ar/tutorial/2/inputoutput.html
# http://pythonya.appspot.com/detalleconcepto?deta=Creaci%C3%B3n,%20carga%20y%20lectura%20de%20archivos%20de%20texto
# http://misnotaslinux.blogspot.com/2013/08/python-fecha-y-hora-actual.html
# http://stackoverflow.com/questions/510348/how-can-i-make-a-time-delay-in-python
# *****************************************************************

# Librerias importadas para la fecha y hora y también para el delay
import datetime     # Libreria para la fecha y hora actual 
import time         # Libreria para el delay

def grabartxt():

# Se crea y abre el archivo para que se pueda escribir
    archivo=open('datos.txt','w')
# Contador para entrar al ciclo 
    num = 1
    while num <= 10:
# Se obtniene la fecha y hora del ordenador
        now = datetime.datetime.now()
# Se castean las variables del contador y la fecha y hora
        rpta = str(num)
        valor = str(now)
# Se escribe en el archivo de texto el contador y fecha y hora
        archivo.write(rpta+" ---> "+valor+"\n")
        num+=1          # Se aumenta en uno el contador 
        time.sleep(10)  # Delay para el la hora y fecha
    archivo.close()     # Se cierra el archivo de texto
    print "Proceso terminado"    
	
grabartxt()             # Se cierra el programa en general 
