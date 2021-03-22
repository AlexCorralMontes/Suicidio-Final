import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import date, timedelta, datetime
import serial  # comunicador de arduino
import pyowm  # tiempo por localidad 
from Keys import OPENWEATHER 
import operator  # matematicas
import random  
import os  #Interactuar con el directorio del pc 

reconocedor = sr.Recognizer()#reconocedor clase recognizer
micro = sr.Microphone()#variable micro

engine = pyttsx3.init()
engine.setProperty('volume', 1.0) #volumen del lector de texto

despertar = "COPON"#nombre con el que despierta 

conversacion = "conversacion.txt"#archivo donde se guardan las conversaciones
#algunas palabras con la que solemos empezar una pregunta
palabras = {"quien":"quien", "que":"que", "donde":"donde","cuando":"cuando", "porque":"porque","como":"como"}

'''
#conexion con arduino
try:
		ser = serial.Serial('com3', 9600)
		LED = True
except serial.SerialException:#si el parametro "LED" no se encuentra o no esta disponible
	print("Los LEDS no estan encendidos")
	LED = False
	pass
'''
class COPON:
	def __init__(self):#clase con la que se empieza a ejecutar
		self.reconocedor = sr.Recognizer()#inicializamos la variable rec
		self.micro = sr.Microphone()
	
	def escucha(self, reconocedor, micro, respuesta):
		try:
			with micro as source:
				print("Esperando el comando...")
				reconocedor.adjust_for_ambient_noise(source)#ajutar el sonido del ambiente
				reconocedor.dynamic_energy_threshold = 3000
				audio = reconocedor.listen(source, timeout=2.0)#escucha el reconocedor y lo guarda en audio
				comando = reconocedor.recognize_google(audio)#usa google para reconocer el comando
				s.remember(comando)#recordar el comando 
			return comando.lower() #devuelve el comando en minusculas

		except sr.WaitTimeoutError:#si pasa tiempo sin escuchar nada
			print("Ha pasado mucho tiempo...")
		except sr.UnknownValueError:#si no se reconoce el comando
			print("No se que es eso")
		except sr.RequestError:#si falla el internet
			print("No tienes internet")

	def hablar(self, text):#hablador
		engine.say(text)
		engine.runAndWait()

	def abrir_paginas(self, comando):

		if comando == "abre youtube":
			s.hablar("abriendo youtube")
			webbrowser.open("https://www.youtube.com/")
			pass

		elif comando == "abre whatsapp":
			s.hablar("abriendo el wasap")
			webbrowser.open("https://web.whatsapp.com/")
			pass

		elif comando == "abre netflix":
			s.hablar("abriendo nesflis")
			webbrowser("https://www.netflix.com/browse")
			pass

		elif comando == "abre instagram":
			s.hablar("abriendo intagrang")
			webbrowser("https://www.instagram.com/explore/")
			pass
		elif comando == "abre explorador de archivos":
			s.hablar("abriendo explorador de archivos")
			os.startfile("C:/Usuarios/Aleix/Documentos")
			pass
		
		else:
			s.hablar("Dile a mi programador que me enseñe a hacer eso")
			pass
			
	def conversacion(self):
		hoy = str(date.today())
		hoy = hoy

		with open(conversacion, "a") as f:
			f.write("La conversacion empezó en:" +hoy+"\n")

	def recuerdo(self, comando):
		with open(conversacion, "a") as f:
			f.write("Usuario: "+comando+"\n")

	def tiempo_fecha(self, comando):
		hoy = date.today()#dia de hoy
		ahora = datetime.now()#hora 

		if "hoy" in comando:
			s.hablar("Hoy es "+hoy.strftime("%B")+" "+hoy.strftime("%d")+", "+hoy.strftime("%Y"))#formato de fecha 
		elif comando == "que hora es":
			s.hablar("Son las "+ahora.strftime("%I")+ahora.strftime("%M")+ahora.strftime("%p")+".")#formato de hora
		elif "ayer" in comando:
			date_intent = hoy - timedelta(days=1)#resto un dia a la fecha de ahora 
			return date_intent

		elif "este momento el año pasado" in comando:
			current_year = hoy.year
			if current_year % 4 == 0:
				days_in_current_year = 366
			else:
				days_in_current_year = 365	
			date_intent = hoy - timedelta(days=days_in_current_year)	
			return date_intent
		elif "semana pasada" in comando:
			date_intent = hoy - timedelta(days=7)	
			return date_intent
		else: 
			pass

	def tiempo(self, comando):
		casa = "Barcelona, Montcada i Reixach"#localidad 
		owm = pyowm.OUM(OPENWEATHER)
		mgr = owm.weather_manager()

		if "ahora" in comando:
			tiempo = mgr.weather_manager(home)
			w = tiempo.weather
			temp = w.temperature('celsius')#formato salida temperatura 
			estado = w.detailed_status
			s.hablar("Ahora mismo hace "+str(int(temp['temp']))+ " grados y "+estado)

		else:	
			print("No tengo esta funcion ahora mismo. ")

	def calculadora(self, operador):
		return{
			'x':operador.add,
			'-':operador.sub,
			'x':operador.mul,
			'dividir':operador.__truediv__,
			'Mod':operador.Mod,
			'mod':operador.mod,
			'^':operador.xor,
		}[operador]

	def hacer_mates(self, lista):
    	#cojemos el segundo item en nuestra lista para saber la operacion
		operador = self.calculadora(lista[1])
    	#cojemos los numero de la operacion
		int1, int2 = int(lista[0]), int(lista[2])
		resultado = operador(int1, int2)
		s.hablar(str(int1)+" "+ li[1]+" "+str(int2)+" igual "+str(resultado))

	def cheker(self, comando):
		lista_numero = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}#lista con los numeros 

		lista = list(comando.split(" "))#de la lista hacemos un separador

		del lista[0:2]

		if lista[0] in lista_numero:#llamo a la calculadora
			self.hacer_mates()
		elif "que dia es hoy" in comando:#que dia es hoy 
			self.tiempo_fecha()
		else:
    		#sino del comando no encuetra nada, se va al buscador de google 
			self.buscador_palabras(comando)
	#buscador de palabras
	def buscador_palabras(self, comando):
		s.hablar("Esto es lo que he buscado en Google")
		webbrowser.open("https://www.google.com/search?q={}".format(command))

	def analizador_comando(self, comando):
		try:

			if comando.startswith('abre'):
				self.abrir_paginas(comando)
			elif comando == "que hora es":
				self.tiempo_fecha(comando)

			elif comando == "como estas":
				sentimientos = ["estoy bien", "podria estar mejor con mas dinero", "ahi voy", "vivo, gracias por preguntar"]
				random_sentimientos = random.choice(sentimientos)
				s.hablar(random_sentimientos)
			elif comando == "quien eres":
				s.hablar("Soy COPON, un placer")
			elif "tiempo" in comando:
				self.tiempo(comando)
			elif "que es" in comando:
				self.cheker(comando)
			elif palabras.get(comando.split(' ')[0] == comando.split(' ')[0]):
				self.buscador_palabras(comando)
			else:
				s.hablar("No se hacer esto todavia")
		except TypeError:
			print("Tienes un error tipografico, cuidado")
			pass
		except AttributeError:
			print("Tienes un AttributeError")
			pass
    
	def escuhar(self, reconocedor, micro):
		while True:#se va a ejecutar siempre
			try:
				with micro as entrada:
					print("Te estoy escuchando")
					reconocedor.adjust_for_ambient_noise(entrada)#se ajusta al ruido del ambiente
					reconocedor.dynamic_energy_threshold = 3000
					audio = reconocedor.listen(entrada, timeout=3.0)
					respuesta = reconocedor.recognize_google(audio)
				if respuesta == despertar:
    					s.hablar("Dime")
    					return respuesta.lower()
				else:
					pass

			except sr.WaitTimeoutError:
				pass
			except sr.UnknownValueError:
				pass
			except sr.RequestError:
				print("No tienes conexion a internet")

s = COPON()
s.conversacion()
respuesta_previa = ""
while True:
	respuesta = s.escucha(reconocedor, micro)
	comando = s.escucha(reconocedor, micro, respuesta)

	if comando == respuesta_previa:
		s.hablar("Eso ya me lo has preguntado antes. Vuelve a decirmelo")
		comando_previo = ""
		respuesta = s.listen(reconocedor, micro)
		comando = s.escucha(reconocedor, micro, respuesta)
	s.analizador_comando(comando)
	respuesta_previa = comando