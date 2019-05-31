from tkinter import *
import matplotlib
import matplotlib.dates
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


import matplotlib.pyplot as plt 
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from mpl_finance import candlestick_ohlc
import pandas as pd
from matplotlib.dates import date2num

from Analisis import Analisis
class Grafico():
    def __init__(self):
        self.grafico = False
    def graficaCambioDiario(self,dataMercado,window):
        pass
    def graficarResultados(self,window,data):
        fig = Figure(figsize=(12,6))

        a = fig.add_subplot(111)
        data["Portfolio Value"].groupby(level = 0).apply(lambda x: x[-1]).plot(ax=a)     
        a.set_title ("Resultados", fontsize=16)
        a.set_ylabel("Precio", fontsize=11)
        a.set_xlabel("Tiempo", fontsize=11)
        a.legend()
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().pack()
        canvas.draw()

        #navigation tool
        toolBar = NavigationToolbar2Tk(canvas,window)
        canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)
    def graficar(self,stocks,window):
        fig = Figure(figsize=(12,6))
        a = fig.add_subplot(111)
    
        stocks.plot(ax=a)
    
       
        
        a.set_title ("Estimation Grid", fontsize=16)
        a.set_ylabel("Precio", fontsize=11)
        a.set_xlabel("Tiempo", fontsize=11)
        a.legend()
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().pack()
        canvas.draw()

        #navigation tool
        toolBar = NavigationToolbar2Tk(canvas,window)
        canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)
    

    def pandas_candlestick_ohlc(self,share,fechasNum,window, stick = "day",  otherseries = ["20d", "50d"], adj=False):
        """
        :param share: pandas DataFrame object with datetime64 index, and float columns "Open", "High", "Low", and "Close", likely created via DataReader from "yahoo"
        :param stick: A string or number indicating the period of time covered by a single candlestick. Valid string inputs include "day", "week", "month", and "year", ("day" default), and any numeric input indicates the number of trading days included in a period
        :param adj: A boolean indicating whether to use adjusted prices
        :param otherseries: An iterable that will be coerced into a list, containing the columns of share that hold other series to be plotted as lines
    
        This will show a Japanese candlestick plot for stock data stored in share, also plotting other series if passed.
        """
        share["20d"] = np.round(share["Adj. Close"].rolling(window = 20, center = False).mean(), 2)
        share["50d"] = np.round(share["Adj. Close"].rolling(window = 50, center = False).mean(), 2)
       


        mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
        alldays = DayLocator()              # minor ticks on the days
        dayFormatter = DateFormatter('%d')      # e.g., 12
        
        # Create a new DataFrame which includes OHLC data for each period specified by stick input
        fields = ["Open", "High", "Low", "Close"]
        if adj:
            fields = ["Adj. " + s for s in fields]
        transdat = share.loc[:,fields]
        transdat.columns = pd.Index(["Open", "High", "Low", "Close"])
        if (type(stick) == str):
            if stick == "day":
                plotdat = transdat
                stick = 1 # Used for plotting
            elif stick in ["week", "month", "year"]:
                if stick == "week":
                    transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1]) # Identify weeks
                elif stick == "month":
                    transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month) # Identify months
                transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0]) # Identify years
                grouped = transdat.groupby(list(set(["year",stick]))) # Group by year and other appropriate variable
                plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
                for name, group in grouped:
                    plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                                "High": max(group.High),
                                                "Low": min(group.Low),
                                                "Close": group.iloc[-1,3]},
                                            index = [group.index[0]]))
                if stick == "week": stick = 5
                elif stick == "month": stick = 30
                elif stick == "year": stick = 365
    
        elif (type(stick) == int and stick >= 1):
            transdat["stick"] = [np.floor(i / stick) for i in range(len(transdat.index))]
            grouped = transdat.groupby("stick")
            plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                            "High": max(group.High),
                                            "Low": min(group.Low),
                                            "Close": group.iloc[-1,3]},
                                        index = [group.index[0]]))
    
        else:
            raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')
    
    
        # Set plot parameters, including the axis object ax used for plotting
        fig = Figure(figsize = (7.5, 4.5), dpi = 100)
        self.ax = fig.add_subplot(111)
        self.ax.clear()
        
    
        self.ax.grid(True)
    
        # Create the candelstick chart

        candlestick_ohlc(self.ax,list(zip(list(date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
                        plotdat["Low"].tolist(), plotdat["Close"].tolist())),
                        colorup = "black", colordown = "red", width = stick * .4)
    
        # Plot other series (such as moving averages) as lines
        if otherseries != None:
            if type(otherseries) != list:
                otherseries = [otherseries]
            share.loc[:,otherseries].plot(ax = self.ax, lw = 1.3, grid = True)
    
        self.ax.xaxis_date()
        self.ax.autoscale_view()
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    

        # estadis = Estadisticas()
        # desviEstandar = estadis.desviacionEstadar(share["Adj. Close"].data.obj)
        
        # media = estadis.regresionLineal(share,fechasNum)

        # mediaMasDE = estadis.cambiarValorPrecios(media.copy(),desviEstandar*2)
        # mediaMenosDE = estadis.cambiarValorPrecios(media.copy(),-desviEstandar*2)

        # ax.plot(plotdat.index.tolist(),media,"r",label = "regression")
        # ax.plot(plotdat.index.tolist(),mediaMasDE,"b",label = "+DE")
        # ax.plot(plotdat.index.tolist(),mediaMenosDE,"b",label = "-DE")
        
        
        
        
        #navigation tool
        if self.grafico:
            self.canvas.get_tk_widget().destroy()

        if ~self.grafico:
            self.canvas = FigureCanvasTkAgg(fig, master=window)
            self.canvas.get_tk_widget().pack()
            

            self.toolbar = NavigationToolbar2Tk(self.canvas,window)
            self.canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)
        
        
            
        self.canvas.draw()
        self.grafico = True