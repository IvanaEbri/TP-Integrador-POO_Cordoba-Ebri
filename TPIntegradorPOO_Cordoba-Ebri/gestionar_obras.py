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
        #self.conectar_db()
        try:
            sqlite_db.create_tables([Entorno, Etapa, Tipo, AreaResponsable, Barrio, Contratacion, Financiamiento, ObraCiudad])
        except Exception as e:
            print("Error al crear las tablas.", e)
            exit()

    def limpiar_datos(self):
        """Limpieza del dataset, se requiere latitud y longitud (ubicacion de obra), monto contratado y el barrio en el que se realiza por lo que se deshechan los NaN"""
        try:
            df = self.extraer_datos()
            df.dropna(subset = ["lat"], axis = 0, inplace = True)
            df.dropna(subset = ["lng"], axis = 0, inplace = True)
            df.dropna(subset = ["barrio"], axis = 0, inplace = True)
            return df
        except Exception as e:
            print("Error al limpier el dataset.", e)
            exit()

    def cargar_datos(self):
        """sentencias necesarias para persistir los datos de las obras (ya transformados y 
        “limpios”) que contiene el objeto Dataframe en la base de datos relacional SQLite. 
        Para ello se debe utilizar el método de clase Model create() en cada una 
        de las clase del modelo ORM definido"""
        self.mapear_orm()
        df = self.limpiar_datos()
        #Carga de datos en la tabla 'entorno'
        ntornos_unique = list(df['entorno'].unique())
        for elem in entornos_unique:
            try:
                Entorno.create(entorno = elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Entornos de Obra.", e)

        #Carga de datos en la tabla 'etapa'
        etapas_unique = list(df['etapa'].unique())
        for elem in etapas_unique:
            try:
                Etapa.create(etapa = elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Etapas de Obra.", e)
        #Carga de datos en la tabla 'tipo'
            tipos_unique = list(df['tipo'].unique())
        for elem in tipos_unique:
            try:
                Tipo.create(tipo = elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Tipos de Obra.", e)
        #Carga de datos en la tabla 'areas_responsables'
        areas_unique = list(df['area_responsable'].unique())
        for elem in areas_unique:
            try:
                AreaResponsable.create(area_responsable = elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Areas Responsables de Obra.", e)
        #Carga de datos en la tabla 'barrios'
        barrios_unique = df.drop_duplicates(subset= 'barrio')
        dic_barrio_comuna = {}
        for index, row in barrios_unique.iterrows():
            try:
                barrio = row['barrio']
                comuna = row['comuna']
                dic_barrio_comuna[barrio] = comuna
            except Exception as e:
                print("Error en la lectura del dataset.", e)
        for key in dic_barrio_comuna.keys():
            try:
                Barrio.create(barrio=key, comuna = dic_barrio_comuna[key])
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Barrios de Obra.", e)
        #Carga de datos en la tabla 'contrataciones'
        contrataciones_unique = list(df['contratacion_tipo'].unique())
        for elem in contrataciones_unique:
            try:
                Contratacion.create(contratacion = elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Contrataciones de Obra.", e)
        #Carga de datos en la tabla 'financiamientos'
            financiamientos_unique = list(df['financiamiento'].unique())
        for elem in financiamientos_unique:
            try:
                Financiamiento.create(financiamiento = elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Financiamientos de Obra.", e)
        #Carga de datos en la tabla 'obras_ciudad'
        try:
            for elem in df.values:
                entorno_obra = Entorno.get(Entorno.entorno == elem[1])
                etapa_obra = Etapa.get(Etapa.etapa == elem[3])
                tipo_obra = Tipo.get(Tipo.tipo == elem[4])
                area_responsable_obra = AreaResponsable.get( AreaResponsable.area_responsable == elem[5])
                barrio_obra = Barrio.get( Barrio.barrio == elem[9])
                contratacion_obra = Contratacion.get( Contratacion.contratacion == elem[23])
                compromiso_bool = self.valor_booleano(elem, 28)
                destacada_bool = self.valor_booleano(elem, 29)
                ba_elige_bool = self.valor_booleano(elem, 30)
                financiamiento_obra =  Financiamiento.get( Financiamiento.financiamiento == elem[35])
                ObraCiudad.create(entorno= entorno_obra, nombre= elem[2], etapa_obra=etapa_obra, tipo_obra=tipo_obra, area_responsable_obra=area_responsable_obra, descripcion= elem[6], monto_contratado= elem[7], barrio_obra=barrio_obra, direccion= elem[10], latitud= elem[11], longitud= elem[12], fecha_inicio= elem[13], fecha_fin_inicias= elem[14],plazo_meses= elem[15],porcentaje= elem[16],licitacion_oferta_empresa= elem[21], licitacion_anio= elem[22], contratacion_obra=contratacion_obra, nro_contratacion= elem[24], cuit_contratista= elem[25], beneficiarios= elem[26], mano_obra= elem[27], compromiso=compromiso_bool, destacada=destacada_bool, ba_elige=ba_elige_bool, expediente_nro= elem[33], financiamiento_obra= financiamiento_obra)
        except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla Obras de la Ciudad.", e)

    def valor_booleano(self,fila, indice):
        if fila[indice] == "SI":
            return True
        else:
            return False

    def nueva_obra(self):
        etapa_no = Etapa.select().where(Etapa.etapa == 'En  proyecto ')
        porcentaje_no = 0
        while True:
            query= 
            for 
        entorno_no = n
        nombre_no = n
        tipo_no = n 
        area_no = n
        descripcion_no =n
        barrio_no =n 
        comuna_no =n  #se autocompleta de acuerdo al barrio
        dieccion_no =n 
        lat_no =n 
        lng_no =n 
        compromiso_no =n 
        destacada_no =n 
        ba_elige_no =n 
        obra_nueva = ObraCiudad(entorno= entorno_no, nombre= nombre_no, etapa_obra=etapa_no, tipo_obra= tipo_no, area_responsable_obra= area_no, descripcion= descripcion_no, barrio_obra= barrio_no, direccion= dieccion_no, latitud= lat_no, longitud= lng_no, porcentaje= porcentaje_no, compromiso=compromiso_no, destacada=destacada_no, ba_elige=ba_elige_no)
        while True:
            guardar = input(f"¿Desea guardar la obra {obra_nueva.nombre}? (S/N)")
            if guardar == "S" or guardar == "s":
                try:
                    obra_nueva.save()
                    obra_nueva.__str__()
                    print("Se ha cargado de manera correcta la obra.")
                except Exception as e:
                    print("Ha fallado el guardado de la obra",e)
                break
            elif guardar == "N" or guardar == "n":
                print("No se guardará la informacion de la obra")
                break
            else:
                pass

    def obtener_indicadores(self):
        """sentencias necesarias para obtener información de las obras existentes en la 
        base de datos SQLite a través de sentencias ORM"""
        #Listado de todas las áreas responsables.
        try:
            print("Áreas responsables de las obras:")
            for area in AreaResponsable.select():
                print(f"    -{area.area_responsable}")
            print("_"*50)
            # Listado de todos los tipos de obra.
            print("Tipos de obra:")
            for tipo in Tipo.select():
                print(f"    -{tipo.tipo}")
            print("_"*50)
            # Cantidad de obras que se encuentran en cada etapa.
            print("Obras por etapa de avance:")
            query = (Etapa.select(Etapa, fn.count(ObraCiudad.id_obra).alias('cant_etapa')).join(ObraCiudad).group_by(Etapa.id_etapa))
            etapa_y_obras = query.dicts()
            for result in etapa_y_obras:
                print(f"    -Etapa: {result['etapa']}- Obras: {result['cant_etapa']}")
            print("_"*50)
            # Cantidad de obras por tipo de obra.
            print("Obras por tipo:")
            query = (Tipo.select(Tipo, fn.count(ObraCiudad.id_obra).alias('cant_tipo')).join(ObraCiudad).group_by(Tipo.id_tipo))
            tipo_y_obras = query.dicts()
            for result in tipo_y_obras:
                print(f"    -Tipo: {result['tipo']}- Obras: {result['cant_tipo']}")
            print("_"*50)
            # Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3.
            print("Barrios de las comunas 1, 2 y 3")
            query = Barrio.select().where(Barrio.comuna.in_(["1","2","3"])).order_by(Barrio.comuna)
            barrio_y_comunas = query.dicts()
            for result in barrio_y_comunas:
                print(f"    -Comuna: {result['comuna']} - Barrio: {result['barrio']}")
            print("_"*50)
            # Cantidad de obras “Finalizadas” en la comuna 1.
            query = ObraCiudad.select().join(Etapa, on=(Etapa.id_etapa==ObraCiudad.etapa_obra)).join(Barrio, on=(Barrio.id_barrio==ObraCiudad.barrio_obra)).where(Etapa.etapa == "Finalizada ").where(Barrio.comuna == "1")
            obras_fin1 = query.count()
            print(f"Obras Finalizadas en la Comuna 1: {obras_fin1}")
            print("_"*50)
            # Cantidad de obras “Finalizadas” en un plazo menor o igual a 24 meses.
            query = ObraCiudad.select().join(Etapa, on=(Etapa.id_etapa==ObraCiudad.etapa_obra)).where(Etapa.etapa == "Finalizada ").where(ObraCiudad.plazo_meses <= 24 )
            obras_cortas = query.count() 
            print(f"Obras Finalizadas en un plazo de 24 meses o menos: {obras_cortas}")
            print("_"*50)
        except Exception as e:
            print("Error al obtener los indicadores de las Obras en la ciudad",e)

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