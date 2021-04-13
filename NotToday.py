#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Luis Javier Reyes Camacho"
__credits__ = []
__license__ = "AGPL3"
__version__ = "1.0.1"
__maintainer__ = "Luis Javier Reyes Camacho"
__email__ = "asnoru@disroot.org"
__status__ = "Pruebas"

from datetime import datetime
from os import mkdir, name, path, getcwd, listdir
from pathlib import Path
import pyodbc

# VARIABLES DEL SCRIPT

#Variables Fecha
TuplaDS=("Lunes", "Martes", "Miercoles", "Jueves","Viernes", "Sabado","Domingo")
Inicio=datetime.now()
PosDiaSemana=datetime.weekday(Inicio)
DiaSemana=TuplaDS[PosDiaSemana]

#Variables Rutas
RutaProgramar="Programacion"
RutaLog="LOGS"
RutaTemp="Temp"
RutaDiaria= path.join(getcwd(),RutaProgramar,DiaSemana)	
TuplaDNecesarios=(RutaLog,RutaTemp,RutaProgramar)

#Variables Ficheros

ListaFicheros=[""]
ArchivoLog=Inicio.strftime('NotToday_%d-%m-%Y.log')
ListaUnidades=[]
ListaFicherosDescartados=[]

### LAS FUNCIONES DEL SCRIPT ###

def EnviaPantalla(CLIENTE, RESULTADO, SERVIDOR, APLICACION, UNIDAD, DiaSemana, DESTINO):
	
	FechaAsunto=datetime.now().strftime('%d/%m/%Y')
	HoraAsunto=datetime.now().strftime('%H:%m')
	
	ASUNTO = CLIENTE + '*' + Resultado + '*' + SERVIDOR + '*' + APLICACION  + '*' +  '*' + UNIDAD + '*' + DiaSemana + '*' + DESTINO + '*'
	print (f'''
	Asunto enviado: {ASUNTO}
	Fecha: {FechaAsunto}	Hora: {HoraAsunto}''')	

def EnviaAccess(CLIENTE, RESULTADO, SERVIDOR, APLICACION, OTRO, UNIDAD, DiaSemana, DESTINO):
	# Nombre del controlador.
	DRIVER_NAME = "Microsoft Access Driver (*.mdb, *.accdb)"
	# Ruta completa del archivo.
	DB_PATH = path.join(getcwd(),"NotToday.accdb")	
	# Establecer la conexión.
	conn = pyodbc.connect("Driver={%s};DBQ=%s;" % (DRIVER_NAME, DB_PATH))
	# Crear cursor para ejecutar consultas.
	cursor = conn.cursor()

	# Fecha y hora de las insercciones en la BD
	FechaAccess=datetime.now().strftime('%d/%m/%Y')
	HoraAccess=datetime.now().strftime('%H:%m')

	# Agregar algunos datos Manualmente.
	"""	
	CLIENTE = "Confuso"  # Cliente Propietario del Servidor
	RESULTADO = "NotToday"  # Mensaje predefinido
	SERVIDOR = "Servidor"  # Nombre del Servidor
	APLICACION = "SNAPSHOT"  # Aplicación de Backup
	Tipo = "NotToday"  # Campo Desconocido
	UNIDAD = "C"  # Unidad ahora
	DiaSemana = "DOMINGO"  # DiaSemana
	DESTINO = "Infierno"  # Ruta Destino
	FECHA = "03/10/2014"  # Fecha
	HORA = "08:30" # Hora
	"""
	# Ejecutar la consulta.
	cursor.execute(u"INSERT INTO Resultados (CLIENTE, RESULTADO, SERVIDOR, APLICACION, TIPO, UNIDAD, DiaSemana, DESTINO, FECHA, HORA) "
				"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
				CLIENTE, RESULTADO, SERVIDOR, APLICACION, TIPO, UNIDAD, DiaSemana, DESTINO, FechaAccess, HoraAccess)


	# Guardar los cambios.
	cursor.commit()
	cursor.close()
	conn.close()



### EL SCRIPT ####


print(f'INICIO: {Inicio}')

print (f'''
El Script se ejecuta desde:
{getcwd()}''')
Contenido = listdir(RutaDiaria)

print(f'''
La ruta actual es:
{RutaDiaria}
''')

for Archivo in Contenido:

	ListaUnidades.clear()

	if Archivo.endswith('.cnf'):
		print(f'''
		Se está procesando el Archivo: 
		*{Archivo}
		''')
		ArchivoActual=path.join(RutaDiaria,Archivo)

		with open(ArchivoActual,'r') as archivo_lectura:
			for linea in archivo_lectura:
				linea = linea.rstrip()
				if linea.startswith('CLIENTE')==True:
					separado = linea.split("=")
					CLIENTE=(separado[1])
					continue
	
				if linea.startswith('SERVIDOR')==True:
					separado = linea.split("=")
					SERVIDOR=(separado[1])
					continue
				
				if linea.startswith('DESTINO')==True:
					separado = linea.split("=")
					DESTINO=(separado[1])
					continue

				if linea.startswith('APLICACION')==True:
					separado = linea.split("=")
					APLICACION=(separado[1])
					continue
				
				if linea.startswith('UNIDAD')==True:
					separado = linea.split("=")
					ListaUnidades.append(separado[1])
					
					continue
		for UNIDAD in ListaUnidades:
			EnviaPantalla(CLIENTE, Resultado, SERVIDOR, APLICACION, UNIDAD, DiaSemana, DESTINO)

			EnviaAccess(CLIENTE, Resultado, SERVIDOR, APLICACION, OTRO, UNIDAD, DiaSemana, DESTINO)

			
		print(f'''
		CLIENTE = {CLIENTE}
		SERVIDOR = {SERVIDOR}
		DESTINO = {DESTINO}
		APLICACION = {APLICACION}
		UNIDADES = {ListaUnidades}
		''')
	else:
		ListaFicherosDescartados.append(Archivo)
print(f'WARNING :: NO se va a PROCESAR porque no tiene la extensión correcta (CNF) el archivo : {ListaFicherosDescartados}' )
		
