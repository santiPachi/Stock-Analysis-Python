import tkinter as tk
from tkinter import ttk
from VistaControlador import VistaControlador
from Grafico import Grafico
class Gui:
    def __init__(self,controlador):
        self.win =  tk.Tk()
        self.win.title("Invest & Grow")
        self.tabControl = ttk.Notebook(self.win) 
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Cambios Porcentuales')
        self.tab2 = ttk.Frame(self.tabControl)            
        self.tabControl.add(self.tab2, text='Stocks')      
        self.tab3 = ttk.Frame(self.tabControl)            
        self.tabControl.add(self.tab3, text='Portafolio')      
        self.tab4 = ttk.Frame(self.tabControl)            
        self.tabControl.add(self.tab4, text='Totales')     
        self.tabControl.pack(expand=1, fill="both")  

        self.result = tk.StringVar()
        self.text = tk.Label(self.tab3,text = "",textvariable=self.result)
        self.text.pack()

        #comboBox
        self.combo = ttk.Combobox(self.tab2, state="readonly")
        self.combo["values"] = ["Apple", "Google", "Microsoft"]
        self.combo.pack()

        #boton graficar
        self.btnGraficar = ttk.Button(self.tab2, text="Graficar", command=self.graficar)   
        self.btnGraficar.pack()
        self.grillaDatos()

        self.vistaControlador = controlador
        self.grafico =  Grafico()
        self.grafico.graficar(self.vistaControlador.cambios,self.tab1)
        self.grafico.pandas_candlestick_ohlc(self.vistaControlador.getStock("Microsoft"),self.vistaControlador.fechas[2],self.tab2)

    def setResultados(self,trades):
        self.result.set(str(trades))
    def iniciar(self):
        self.win.mainloop()
    def setGraficaResultados(self,datos):
        self.grafico.graficarResultados(self.tab4,datos)

    def grillaDatos(self):
        self.tree= ttk.Treeview(self.tab3, column=("column1", "column2", "column3", "column4", "column5"), show='headings')
        self.tree.heading("#1", text="Fecha")
        self.tree.heading("#2", text="Simbolo")
        self.tree.heading("#3", text="Efectivo")
        self.tree.heading("#4", text="Valor Portafolio")
        self.tree.heading("#5", text="Ganacia por Share")
        self.tree.pack()
    def setDatosGrilla(self,datos):
        i = 0
        for fila in datos['Shares'].index.values:
            fila = [fila[0],fila[1],datos.values[i][1],datos.values[i][0],datos.values[i][7]]
            self.tree.insert("", tk.END, values=fila)
            i += 1
    def graficar(self):
        self.grafico.pandas_candlestick_ohlc(self.vistaControlador.getStock(self.combo.get()),self.vistaControlador.fechas[2],self.tab2)

