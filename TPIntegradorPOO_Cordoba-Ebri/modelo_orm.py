from peewee import *
from datetime import *
from dateutil.relativedelta import relativedelta

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

class Empresa(BaseModel):
    """Entidad tipo de contratacion de la obra"""
    id_empresa = AutoField (primary_key = True)
    empresa = TextField(unique = True)

    def __str__(self):
        return self.empresa

    class Meta:
        db_table = 'empresas'

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
    licitacion_oferta_empresa = ForeignKeyField(Empresa, backref= 'obras_ciudad') #accedo al cuit desde la empresa
    licitacion_anio = IntegerField(null=True)
    contratacion_obra = ForeignKeyField(Contratacion, backref= 'obras_ciudad')
    nro_contratacion = TextField(null=True)
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
            
            self.compromiso=False
            self.destacada=False
            self.ba_elige=False
            
        except Exception as e:
            print("No se pudieron seleccionar los parametros de la obra", e)

    def iniciar_contratacion(self):
        #contratacion_tipo por clave for y nro_contratacion, etapa a en licitacion
        #Seleccion forma de contratacion
        while True:
            query= Contratacion.select()
            max_id = Contratacion.select(fn.Max(Contratacion.id_contratacion)).scalar()
            for contratacion in query:
                print(f"   -{contratacion.id_contratacion}_{contratacion.contratacion}")
            try:
                contratacion_no = int(input("Ingrese el número correspondiente al tipo de contratacion de la obra "))
                if contratacion_no >= 0 and contratacion_no<= max_id:
                    self.contratacion_obra= Contratacion.select().where(Contratacion.id_contratacion== contratacion_no)
                    break
                else:
                    print("Debe ingresar un número valido")
            except:
                print("Debe ingresar el número que corresponda a la opción elegida") 
        #Input de nro de contratacion
        while True:
            nro_contratacion = input("Ingrese el numero de contratación ")
            try:
                self.nro_contratacion = nro_contratacion
                break
            except:
                print("Ocurrio un error en la carga de datos")
        #Etapa a en licitacion
        try:
            self.etapa_obra= Etapa.select().where(Etapa.id_etapa==10)
        except IntegrityError as e:
                print("Error al modificar la etapa de obra.", e)

    def adjudicar_obra(self):
        #Se establece la empresa que realizará la obra, el numero de expediente y etapa a "sin iniciar"
        #Seleccion de la empresa que llevará a cabo la obra
        while True:
            query= Empresa.select()
            max_id = Empresa.select(fn.Max(Empresa.id_empresa)).scalar()
            for empr in query:
                print(f"   -{empr.id_empresa}_{empr.empresa}")
            try:
                empresa_no = int(input("Ingrese el número correspondiente a la empresa que realizará la obra "))
                if empresa_no >= 0 and empresa_no<= max_id:
                    self.licitacion_oferta_empresa= Empresa.select().where(Empresa.id_empresa== empresa_no)
                    break
                else:
                    print("Debe ingresar un número valido")
            except:
                print("Debe ingresar el número que corresponda a la opción elegida") 
        #Input de nro de expediente
        while True:
            nro_expediente = input("Ingrese el numero de expediente ")
            try:
                self.expediente_nro = nro_expediente
                break
            except:
                print("Ocurrio un error en la carga de datos")
        #Etapa a sin iniciar
        try:
            self.etapa_obra= Etapa.select().where(Etapa.id_etapa==15)
        except IntegrityError as e:
                print("Error al modificar la etapa de obra.", e)

    def iniciar_obra(self):
        #Se coloca si la obra es destacada, de compromiso o parte de BA elige
        #Se asigna fecha de inicio y finalizacion (y el plazo en meses)
        #Se determica mano de obra, fuente de financiamiento y se establece la etapa de obra a en ejecucion
        # destacada, fecha inicio y fin (asigna plazo en meses), mano de obra y fianciamiento por foreign key, etapa a en ejecucion
        print("Se seleccionará si la obra conlleva Compromiso, es Destacada o forma parte de BA Elige")
        try:
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
            print("No se pudieron asignar las caracteristicas de la obra", e)
        #Fechas de inicio y fin programados
            fecha_inicio_input = 0
            fecha_fin_inicial_input = 0
        try:
            while True:
                fecha_inicio_input = input("Ingrese la fecha de inicio de obra, en formato AAAA-MM-DD ")
                try:
                    fecha_inicio = datetime.strptime(fecha_inicio_input, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("Formato de fecha incorrecto. Intente nuevamente.")
            while True:
                fecha_fin_inicial_input = input("Ingrese la fecha de fin de obra programada, en formato AAAA-MM-DD: ")
                try:
                    fecha_fin = datetime.strptime(fecha_inicio_input, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("Formato de fecha incorrecto. Intente nuevamente.")
            self.fecha_inicio= fecha_inicio
            self.fecha_fin_inicias= fecha_fin
            self.plazo_meses()
        except Exception as e:
            print("No se pudieron asignar las fechas de obra", e)
        #Mano de obra
        while True:
            try:
                mano_obra= int(input("Ingrese la cantidad de personas que seran necesarias para la obra "))
                if mano_obra>0:
                    self.mano_obra= mano_obra
                else:
                    print("El numero debe ser mayor a 0")
            except ValueError:
                print("Se debe ingresar un numero valido")
        #Financiamiento de obra
        while True:
            query= Financiamiento.select()
            max_id = Financiamiento.select(fn.Max(Financiamiento.id_financiamiento)).scalar()
            for finan in query:
                print(f"   -{finan.id_financiamiento}_{finan.financiamiento}")
            try:
                fianciamiento_no = int(input("Ingrese el número correspondiente al método de financiamiento de la obra "))
                if fianciamiento_no >= 0 and fianciamiento_no<= max_id:
                    self.financiamiento_obra= Financiamiento.select().where(Financiamiento.id_financiamiento== fianciamiento_no)
                    break
                else:
                    print("Debe ingresar un número valido")
            except:
                print("Debe ingresar el número que corresponda a la opción elegida") 
        #Etapa a en ejecucion
        try:
            self.etapa_obra= Etapa.select().where(Etapa.id_etapa==2)
        except IntegrityError as e:
                print("Error al modificar la etapa de obra.", e)

    def actualizar_porcentaje_avance(self):
        #Actualizacion del porcentaje de avance
        while True:
            try:
                ingreso= int(input("Ingrese el porcentaje de avance de obra actual (solo numeros)"))
                if ingreso>=0:
                    if ingreso > self.porcentaje:
                        try:
                            self.porcentaje = nuevo_porcentaje
                        except:
                            print("Ocurrio un error al cargar la actualizacion")
                        break
                    else:
                        a=input("Ingreso un valor menor al porcentaje de avance existente ¿Desea intentarlo nuevamente? (S/N) ")
                        if a == "S" or a=="s":
                            pass
                        else:
                            break
                else:
                    print("Debe ingresar un valor mayor a 0")
            except ValueError:
                print("Debe ingresar un valor numérico")
        
    def incrementar_plazo(self):
        #modifica plazo
        #paso opcional
        pass

    def incrementar_mano_obra(self):
        #modifica mao
        #paso opcional
        pass

    def finalizar_obra(self):
        #Etapa a finalizada y porcentaje 100%
        try:
            self.etapa_obra= Etapa.select().where(Etapa.id_etapa==1)
            self.porcentaje=100
            print("Se ha finalizado la obra")
        except IntegrityError as e:
                print("Error al modificar la etapa de obra.", e)

    def rescindir_obra(self):
        #Etapa a rescindida
        try:
            self.etapa_obra= Etapa.select().where(Etapa.id_etapa==3)
            print("Se ha rescindido la obra")
        except IntegrityError as e:
                print("Error al modificar la etapa de obra.", e)

    def plazo_meses(self):
        delta = relativedelta(self.fecha_inicio, self.fecha_fin_inicias)
        meses = delta.months + 12 * delta.years
        self.plazo_meses= meses