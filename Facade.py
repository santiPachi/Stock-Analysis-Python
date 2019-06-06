from Grafico import Grafico
from FuenteDatos import FuenteDatos
from Gui import Gui
from Analisis import Analisis
from VistaControlador import VistaControlador
class Facade:
    def __init__(self):
        self.analisis = Analisis()
        self.generarDatos = FuenteDatos()
        self.vistaControlador = VistaControlador(self.generarDatos)
        self.mainWindow = Gui(self.vistaControlador)

    def iniciarBot(self):
        seniales = self.analisis.analisisMediasMoviles([("AAPL", self.generarDatos.apple),
                                    ("MSFT",  self.generarDatos.microsoft),
                                    ("GOOG",  self.generarDatos.google),
                                    ("FB",    self.generarDatos.facebook),
                                    ("TWTR",  self.generarDatos.twitter),
                                    ("NFLX",  self.generarDatos.netflix),
                                    ("AMZN",  self.generarDatos.amazon),
                                    ("YHOO",  self.generarDatos.yahoo),
                                    ("GE",    self.generarDatos.ge),
                                    ("QCOM",  self.generarDatos.qualcomm),
                                    ("IBM",   self.generarDatos.ibm),
                                    ("HPQ",   self.generarDatos.hp)],
                            fast = 20, slow = 50)

        bk = self.analisis.backtest(seniales, 1000000)

        
        self.mainWindow.setDatosGrilla(bk)
        self.mainWindow.setGraficaPortafolio(bk)
      
        #self.mainWindow.setResultados(bk)
        self.mainWindow.iniciar()
