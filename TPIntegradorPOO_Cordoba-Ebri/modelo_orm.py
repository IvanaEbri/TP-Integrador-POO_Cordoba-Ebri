from peewee import *
from datetime import *

sqlite_db = SqliteDatabase('./TPIntegradorPOO_Cordoba-Ebri/Obras_CABA.db', pragmas={'journal_mode': 'wal'})
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

class Etapa(BaseModel):
    """Entidad Etapa de ejecucio"""
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

class ObraCiudad (BaseModel):
    """Entidad que recopila las obras realizadas por GCBA"""
    id_obra = AutoField(primary_key = True)
    entorno = TextField(null= False)
    nombre = TextField(null= False)
    etapa_obra = ForeignKeyField(Etapa, backref= 'obras_ciudad')
    tipo_obra = ForeignKeyField(Tipo, backref= 'obras_ciudad')
    area_responsable_obra = ForeignKeyField(AreaResponsable, backref= 'obras_ciudad')
    descripcion = TextField(null = False)
    monto_contratado = FloatField(null= False)
    comuna_obra = IntegerField(null= False) #deberia estar entre 1 y 15
    barrio_obra = ForeignKeyField(Barrio, backref= 'obras_ciudad')
    direccion = TextField()
    latitud = FloatField(null= False)
    longitud = FloatField(null= False)
    fecha_inicio = DateField(default= datetime.now)
    fecha_fin_inicias = DateField(default= datetime.now)
    plazo_meses = IntegerField()
    porcentaje = IntegerField(default= 0)
    licitacion_oferta_empresa = TextField()
    licitacion_anio = IntegerField()
    contratacion_obra = ForeignKeyField(Contratacion, backref= 'obras_ciudad')
    nro_contratacion = TextField()
    cuit_contratista = TextField()
    beneficiarios = TextField()
    mano_obra = IntegerField()
    compromiso = BooleanField(null = False, default= False)
    destacada = BooleanField(null = False, default= False)
    ba_elige = BooleanField(null = False, default= False)
    expediente_nro = TextField()
    financiamiento_obra = ForeignKeyField(Financiamiento, backref= 'obras_ciudad')


    def __str__(self):
        return(f"{self.nombre}: obra {self.etapa_obra.etapa} en {self.barrio_obra.__str__} por ${self.monto_costo}")

    class Meta:
        db_table = 'obras_ciudad'