from modelo_orm import *
import pandas as pd
from abc import ABCMeta
import csv
from correccion_csv import correccion_dataset

#obras_csv = "./TPIntegradorPOO_Cordoba-Ebri/observatorio-de-obras-urbanas.csv"
#las comillas doble que tiene el archivo original hacen que no se pueda separar por la ',' cada linea por lo que se corrige por funcion y se genera el segundo archivo
obras_csv ='./TPIntegradorPOO_Cordoba-Ebri/observatorio-de-obras-urbanas_correccion.csv'

class GesionarObra (metaclass = ABCMeta):

    def extraer_datos(self):
        """Lectura del dataset mediante modulo 'pandas'"""
        try:
            #Funcion que reemplaza las '""""' por "'", '""' por '"' y elimina la primer y ultima comilla doble en caso que la hubiese
            correccion_dataset()
            # Separa los datos por las ',', mantiene las citas que se encuentran entre '"'
            df = pd.read_csv(obras_csv, sep=',', skipinitialspace=True, quotechar='"', on_bad_lines='skip')
            return df
        except FileNotFoundError as e:
            print("Error al conectar con el dataset.", e)
            exit()

    def conectar_db(self):
        """sentencias necesarias para realizar la conexión a la base de datos “obras_urbanas.db” """
        try:
            """Intento de conexion a la base de datos"""
            sqlite_db.connect()
        except OperationalError as e:
            print("Error al conectar con la BD.", e)
            exit()

    def mapear_orm(self):
        """sentencias necesarias para realizar la creación de la
        estructura de la base de datos (tablas y relaciones) utilizando el método de instancia
        “create_tables(list)” del módulo peewee"""
        pass

    def limpiar_datos(self):
        """sentencias necesarias para realizar la “limpieza” de
        los datos nulos y no accesibles del Dataframe"""
        pass

    def cargar_datos(self):
        """sentencias necesarias para persistir los datos de las obras (ya transformados y 
        “limpios”) que contiene el objeto Dataframe en la base de datos relacional SQLite. 
        Para ello se debe utilizar el método de clase Model create() en cada una 
        de las clase del modelo ORM definido"""
        pass

    def nueva_obra(self):
        pass

    def obtener_indicadores(self):
        """sentencias necesarias para obtener información de las obras existentes en la 
        base de datos SQLite a través de sentencias ORM"""
        pass

class Obra():
    #metodos requeridos en la clase
    #sus atributos serian los definidos en el orm por cada registro de obra
    #será cada registro de obra extraido del data set y orm, quiza deberia heredar la clase del orm
    def nuevo_proyecto(self):
        pass

    def iniciar_contratacion(self):
        pass

    def adjudicar_obra(self):
        pass

    def iniciar_obra(self):
        pass

    def actualizar_porcentaje_avance(self):
        pass

    def incrementar_plazo(self):
        #paso opcional
        pass

    def incrementar_mano_obra(self):
        #paso opcional
        pass

    def finalizar_obra(self):
        pass

    def rescindir_obra(self):
        pass