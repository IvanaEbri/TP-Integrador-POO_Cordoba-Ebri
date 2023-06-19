from peewee import *
from datetime import *

sqlite_db = SqliteDatabase('./TPIntegradorPOO_Cordoba-Ebri/obras_urbanas.db', pragmas={'journal_mode': 'wal'})
try:
    """Intento de conexion a la base de datos"""
    sqlite_db.connect()
except OperationalError as e:
    print("Error al conectar con la BD.", e)
    exit()

class BaseModel(Model):
    """Clase base para las entidades de la base"""
    class Meta:
        database = sqlite_db

class Entorno(BaseModel):
    """Entidad Entorno de obra"""
    id_entorno = AutoField(primary_key = True)
    entorno = TextField(unique = True, null = False)
    
    def __str__(self):
        return self.entorno

    class Meta:
        db_table='entornos'

class Etapa(BaseModel):
    """Entidad Etapa de ejecucion"""
    id_etapa = AutoField(primary_key = True)
    etapa = TextField(unique = True, null = False)
    
    def __str__(self):
        return self.etapa

    class Meta:
        db_table='etapas'

class Tipo(BaseModel):
    """Entidad de Tipo de obra a ejecutar/ejecutada"""
    id_tipo = AutoField(primary_key = True)
    tipo = TextField(unique = True, null = False)

    def __str__(self):
        return self.tipo

    class Meta:
        db_table = 'tipos'

class AreaResponsable(BaseModel):
    """Entidad de Area responsable de la gestion"""
    id_area = AutoField(primary_key = True)
    area_responsable = TextField(unique = True, null = False)

    def __str__(self):
        return self.area_responsable

    class Meta:
        db_table = 'areas_responsables'

class Barrio(BaseModel):
    """Validacion e ingreso de barrio segun la comuna establecida"""
    id_barrio = AutoField(primary_key = True)
    comuna = IntegerField(null= False)
    barrio = TextField(unique = True, null = False)

    def __str__(self):
        return (f"Comuna {self.comuna} - Barrio {self.barrio}")
    
    class Meta:
        db_table = 'barrios'

class Contratacion(BaseModel):
    """Entidad tipo de contratacion de la obra"""
    id_contratacion = AutoField (primary_key = True)
    contratacion = TextField(unique = True)

    def __str__(self):
        return self.contratacion

    class Meta:
        db_table = 'contrataciones'

class Financiamiento(BaseModel):
    """Entidad tipo de financiamiento de la obra"""
    id_financiamiento = AutoField (primary_key = True)
    financiamiento = TextField(unique = True)

    def __str__(self):
        return self.financiamiento

    class Meta:
        db_table = 'financiamientos'

class Obra (BaseModel):
    """Entidad que recopila las obras realizadas por GCBA"""
    id_obra = AutoField(primary_key = True)
    entorno =ForeignKeyField(Entorno, backref= 'obras_ciudad')
    nombre = TextField(null= False)
    etapa_obra = ForeignKeyField(Etapa, backref= 'obras_ciudad')
    tipo_obra = ForeignKeyField(Tipo, backref= 'obras_ciudad')
    area_responsable_obra = ForeignKeyField(AreaResponsable, backref= 'obras_ciudad')
    descripcion = TextField(null = False)
    monto_contratado = FloatField(null= True,default=0)#si no se contrató no tendra monto por ello 0
    #la comuna se obtiene de un join con la tabla barrio
    barrio_obra = ForeignKeyField(Barrio, backref= 'obras_ciudad')
    direccion = TextField(null=True)
    latitud = FloatField(null= False)
    longitud = FloatField(null= False)
    fecha_inicio = DateField(null=True)
    fecha_fin_inicias = DateField(null=True)
    plazo_meses = IntegerField(null=True)
    porcentaje = IntegerField(null=True)
    licitacion_oferta_empresa = TextField(null=True)
    licitacion_anio = IntegerField(null=True)
    contratacion_obra = ForeignKeyField(Contratacion, backref= 'obras_ciudad')
    nro_contratacion = TextField(null=True)
    cuit_contratista = TextField(null=True)
    beneficiarios = TextField(null=True)
    mano_obra = IntegerField(null=True)
    compromiso = BooleanField(default= False)
    destacada = BooleanField(default= False)
    ba_elige = BooleanField(default= False)
    expediente_nro = TextField(null=True)
    financiamiento_obra = ForeignKeyField(Financiamiento, backref= 'obras_ciudad')


    def __str__(self):
        return(f"{self.nombre}: obra {self.etapa_obra.etapa} en {self.barrio_obra.barrio} (Comuna {self.barrio_obra.comuna}) por ${self.monto_contratado}")

    class Meta:
        db_table = 'obras_ciudad'

    
    def nuevo_proyecto(self):
        try:
            self.etapa_obra = Etapa.select().where(Etapa.etapa == 'En  proyecto ')
            self.porcentaje = 0
            print("A continuacion seleccionará e ingresará los parametros de la obra a registrar")
            
            #Seleccion del entorno de obra
            while True:
                query= Entorno.select()
                max_id = Entorno.select(fn.Max(Entorno.id_entorno)).scalar()
                for entorno in query:
                    print(f"   -{entorno.id_entorno}_{entorno.entorno}")
                try:
                    entorno_no = int(input("Ingrese el número correspondiente al entorno de la obra "))
                    if entorno_no >= 0 and entorno_no<= max_id:
                        self.entorno= Entorno.select().where(Entorno.id_entorno== entorno_no)
                        break
                    else:
                        print("Debe ingresar un número valido")
                except:
                    print("Debe ingresar el número que corresponda a la opción elegida")

            self.nombre = input("A continuacion escriba el nombre de la obra ")
            
            #Seleccion del tipo de obra
            while True:
                query= Tipo.select()
                max_id = Tipo.select(fn.Max(Tipo.id_tipo)).scalar()
                for tipo in query:
                    print(f"   -{tipo.id_tipo}_{tipo.tipo}")
                try:
                    tipo_no = int(input("Ingrese el número correspondiente al tipo de obra "))
                    if tipo_no >= 0 and tipo_no<= max_id:
                        self.tipo_obra = Tipo.select().where(Tipo.id_tipo== tipo_no)
                        break
                    else:
                        print("Debe ingresar un número valido")
                except:
                    print("Debe ingresar el número que corresponda a la opción elegida")

            #Seleccion del area responsable de la obra
            while True:
                query= AreaResponsable.select()
                max_id = AreaResponsable.select(fn.Max(AreaResponsable.id_area)).scalar()
                for area in query:
                    print(f"   -{area.id_area}_{area.area_responsable}")
                try:
                    area_no = int(input("Ingrese el número correspondiente al área responsable de la obra "))
                    if area_no >= 0 and area_no<= max_id:
                        self.area_responsable_obra = AreaResponsable.select().where(AreaResponsable.id_area==area_no)
                        break
                    else:
                        print("Debe ingresar un número valido")
                except:
                    print("Debe ingresar el número que corresponda a la opción elegida")

            self.descripcion = input("A continuacion escriba la descripción de la obra ")

            #Seleccion del barrio de la obra
            while True:
                query= Barrio.select()
                max_id = Barrio.select(fn.Max(Barrio.id_barrio)).scalar()
                for barrio in query:
                    print(f"   -{barrio.id_barrio}_{barrio.barrio}: Comuna {barrio.comuna}")
                try:
                    barrio_no = int(input("Ingrese el número correspondiente al barrio donde se localiza la obra "))
                    if barrio_no >= 0 and barrio_no<= max_id:
                        self.barrio_obra = Barrio.select().where(Barrio.id_barrio==barrio_no)
                        break
                    else:
                        print("Debe ingresar un número valido")
                except:
                    print("Debe ingresar el número que corresponda a la opción elegida")

            self.direccion = input("A continuacion escriba la dirección de la obra ")
            
            #asignacion de latitud y longitud
            while True:
                print("Se le solicitará la latitud y longitud, recuerde los caracteres permitidos son '-', números y como separador de decimales '.'")
                lat_no = input("A continuacion escriba la latitud de la obra ")
                lng_no = input("A continuacion escriba la longitud de la obra ")
                try:
                    self.latitud= float(lat_no)
                    self.longitud= float(lng_no)
                    break
                except:
                    print("Debe cumplir con los caracteres permitidos")

            #Seleccion del compromiso de la obra
            while True:
                print("""Ingrese si la obra conlleva COMPROMISO desde el GCBA:
                    -1_ SI
                    -2_ NO""")
                try:
                    compromiso_no = int(input("Ingrese el número que corresponda para esta obra "))
                    if compromiso_no== 1:
                        self.compromiso= True
                        break
                    elif compromiso_no ==2:
                        self.compromiso=False
                        break
                    else:
                        print("Debe ingresar un número valido")
                except:
                    print("Debe ingresar el número que corresponda a la opción elegida")

            #Seleccion de caracter de destacada de la obra
            while True:
                print("""Ingrese si la obra se considera DESTACADA por el GCBA:
                    -1_ SI
                    -2_ NO""")
                try:
                    destacada_no = int(input("Ingrese el número que corresponda para esta obra "))
                    if destacada_no== 1:
                        self.destacada= True
                        break
                    elif destacada_no ==2:
                        self.destacada=False
                        break
                    else:
                        print("Debe ingresar un número valido")
                except:
                    print("Debe ingresar el número que corresponda a la opción elegida")

            #Pertenece al programa BA_elige de la obra
            while True:
                print("""Ingrese si la obra se se encuentra dentro de BA Elige del GCBA:
                    -1_ SI
                    -2_ NO""")
                try:
                    ba_elige_no = int(input("Ingrese el número que corresponda para esta obra "))
                    if ba_elige_no== 1:
                        self.ba_elige= True
                        break
                    elif ba_elige_no ==2:
                        self.ba_elige=False
                        break
                    else:
                        print("Debe ingresar un número valido")
                except:
                    print("Debe ingresar el número que corresponda a la opción elegida")

        except Exception as e:
            print("No se pudieron seleccionar los parametros de la obra", e)

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

