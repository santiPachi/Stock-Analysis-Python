from FuenteDatos import FuenteDatos
class VistaControlador:
    def __init__(self,datos):
        self.datos = datos
        self.cambios = self.datos.getCambios()
        self.fechas = self.datos.getFechas()
    def getStock(self,nombreStock):

        if nombreStock == "Apple":
            return self.datos.apple
        elif nombreStock =="Google":
            return self.datos.google
        elif nombreStock =="Microsoft":
            return self.datos.microsoft
        return None
    
    