from Grafico import Grafico
from FuenteDatos import FuenteDatos
from MainWindow import MainWindow
from Estadisticas import Estadisticas
from ViewController import ViewController
class Facade:
    def __init__(self):
        self.esta = Estadisticas()
        self.generarDatos = FuenteDatos()
        self.viewController = ViewController(self.generarDatos)
        self.mainWindow = MainWindow(self.viewController)
    def iniciarGui(self):
        signals = self.esta.ma_crossover_orders([("AAPL", self.generarDatos.apple),
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
        bk = self.esta.backtest(signals, 1000000)

        
        self.mainWindow.setDatosGrilla(bk)
        self.mainWindow.setGraficaResultados(bk)
      
        #self.mainWindow.setResultados(bk)
        self.mainWindow.iniciar()
