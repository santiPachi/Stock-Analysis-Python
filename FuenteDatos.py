import pandas as pd
import quandl
import datetime
import pandas_datareader.data as web    # Going to get SPY from Yahoo! (I know I said you shouldn't but I didn't have a choice)
import numpy as np

class FuenteDatos:
    def __init__(self):
        start = datetime.datetime(2011,1,1)
        end = datetime.date.today()
       
        (self.microsoft, self.google, self.facebook, self.twitter, self.netflix,
        self.amazon, self.yahoo, self.ge, self.qualcomm, self.ibm, self.hp,self.apple)= (quandl.get("WIKI/" + s, start_date=start, end_date=end) for s in ["MSFT", "GOOG", "FB", "TWTR","NFLX", "AMZN", "YHOO", "GE","QCOM", "IBM", "HPQ","AAPL"])
 
        # Below I create a DataFrame consisting of the adjusted closing price of these stocks, first by making a list of these objects and using the join method
        self.stocks = pd.DataFrame({"AAPL": self.apple["Adj. Close"],
                            "MSFT": self.microsoft["Adj. Close"],
                            "GOOG": self.google["Adj. Close"],
                            "FB": self.facebook["Adj. Close"],
                            "TWTR": self.twitter["Adj. Close"],
                            "NFLX": self.netflix["Adj. Close"],
                            "AMZN": self.amazon["Adj. Close"],
                            "YHOO": self.yahoo["Adj. Close"],
                            "GE": self.ge["Adj. Close"],
                            "QCOM": self.qualcomm["Adj. Close"],
                            "IBM": self.ibm["Adj. Close"],
                            "HPQ": self.hp["Adj. Close"]})

        spyder = web.DataReader("SPY", "yahoo", start, end)    # Didn't work
        self.stocks = self.stocks.join(spyder.loc[:, "Adj Close"]).rename(columns={"Adj Close": "SPY"})

        ##rff
        tbill = quandl.get("FRED/TB3MS", start_date=start, end_date=end)
        self.rrf = tbill.iloc[-1, 0]    # Get the most recent Treasury Bill rate

 
    def getCambios(self):
        cambio = self.stocks.apply(lambda x: np.log(x) - np.log(x.shift(1)))
        return cambio 

    def getFechas(self):
        
        #La parte del grafico 

        # Let's get Apple stock data; Apple's ticker symbol is AAPL
        # First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date
        

        fechas  = []
        fechasCorto = []
        fechasNum = []
        cont = 1
        cont2 = 0
        for x in self.stocks.index:
            fechasNum.append(cont2)
            cont2 += 1
            fechas.append(x._date_repr)
            if cont < 30:
                fechasCorto.append("")
            else:
                fechasCorto.append(x._date_repr)
                cont = 0
            cont += 1
       


        
        return [fechas,fechasCorto,fechasNum]

    def getPrecios(self,stocks):
        precios = list()
        for s in ["MSFT", "GOOG","AAPL","SPY"]:
            precios.append(stocks[s].data.obj)
        return precios

