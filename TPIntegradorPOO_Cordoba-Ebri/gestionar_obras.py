from modelo_orm import *
from pandas import *
from abc import ABCMeta


class GesionarObra (metaclass = ABCMeta):
    def extraer_datos():
        pass

    def conectar_db():
        pass

    def mapear_orm():
        pass

    def limpiar_datos():
        pass

    def cargar_datos():
        pass

    def nueva_obra():
        pass

    def obtener_indicadores():
        pass

class Obra():
    #metodos requeridos en la clase
    #sus atributos serian los definidos en el orm por cada registro de obra
    #será cada registro de obra extraido del data set y orm, quiza deberia heredar la clase del orm
    def nuevo_proyecto():
        pass

    def iniciar_contratacion():
        pass

    def adjudicar_obra():
        pass

    def iniciar_obra():
        pass

    def actualizar_porcentaje_avance():
        pass

    def incrementar_plazo():
        #paso opcional
        pass

    def incrementar_mano_obra():
        #paso opcional
        pass

    def finalizar_obra():
        pass

    def rescindir_obra():
        pass