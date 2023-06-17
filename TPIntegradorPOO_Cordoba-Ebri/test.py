from gestionar_obras import *

gestor = GesionarObra()
datos = gestor.extraer_datos()
print(datos.head())
print(datos.count())
print(datos.columns)

gestor.mapear_orm()