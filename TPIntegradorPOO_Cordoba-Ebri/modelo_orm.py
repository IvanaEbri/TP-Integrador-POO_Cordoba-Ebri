from peewee import *

sqlite_db = SqliteDatabase('./TPIntegradorPOO_Cordoba-Ebri/Obras_CABA.db', pragmas={'journal_mode': 'wal'})
try:
    """Intento de conexion a la base de datos"""
    sqlite_db.connect()
except OperationalError as e:
    print("Error al conectar con la BD.", e)
    exit()

class BaseModel(Model):
    class Meta:
        database = sqlite_db
