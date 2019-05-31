from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import math
class Analisis:
   
    def cambiarValorPrecios(self,shares,valor):
        cambios = list()
        for share in shares:
            share += valor
            cambios.append(share)
        return cambios
    def desviacionEstadar(self,shares):
        media = 0
        n = 1
        for share in shares:
            media += share
            n += 1
        media = media / n
        suma = 0
        for share in shares:
            suma = suma + pow((share - media),2)
        de = math.sqrt(suma/n)
        return de

    def regresionLineal(self,shares,fechas):
        prices = shares['Close'].tolist()
      
        #Convert to 1d Vector
        fechas = np.reshape(fechas, (len(fechas), 1))
        prices = np.reshape(prices, (len(prices), 1))
        regressor = LinearRegression()
        regressor.fit(fechas, prices)
        yvec = []
        predic = regressor.predict(fechas)
        for y in predic:
            yvec.append(y[0])

        return yvec

    def analisisMediasMoviles(self,stocks, fast, slow):
        
        oso = str(fast) + 'd'
        toro = str(slow) + 'd'
        diff = oso + '-' + toro

        trades = pd.DataFrame({"Price": [], "Regime": [], "Signal": []})
        for s in stocks:
            # Get the moving averages, both fast and slow, along with the difference in the moving averages
            s[1][oso] = np.round(s[1]["Close"].rolling(window = fast, center = False).mean(), 2)
            s[1][toro] = np.round(s[1]["Close"].rolling(window = slow, center = False).mean(), 2)
            s[1][diff] = s[1][oso] - s[1][toro]

            # np.where() is a vectorized if-else function, where a condition is checked for each component of a vector, and the first argument passed is used when the condition holds, and the other passed if it does not
            s[1]["Regime"] = np.where(s[1][diff] > 0, 1, 0)
            # We have 1's for bullish regimes and 0's for everything else. Below I replace bearish regimes's values with -1, and to maintain the rest of the vector, the second argument is apple["Regime"]
            s[1]["Regime"] = np.where(s[1][diff] < 0, -1, s[1]["Regime"])
            # To ensure that all trades close out, I temporarily change the regime of the last row to 0
            regime_orig = s[1].loc[:, "Regime"].iloc[-1]
            s[1].loc[:, "Regime"].iloc[-1] = 0
            s[1]["Signal"] = np.sign(s[1]["Regime"] - s[1]["Regime"].shift(1))
            # Restore original regime data
            s[1].loc[:, "Regime"].iloc[-1] = regime_orig

            # Get signals
            signals = pd.concat([
                pd.DataFrame({"Price": s[1].loc[s[1]["Signal"] == 1, "Adj. Close"],
                            "Regime": s[1].loc[s[1]["Signal"] == 1, "Regime"],
                            "Signal": "Buy"}),
                pd.DataFrame({"Price": s[1].loc[s[1]["Signal"] == -1, "Adj. Close"],
                            "Regime": s[1].loc[s[1]["Signal"] == -1, "Regime"],
                            "Signal": "Sell"}),
            ])
            signals.index = pd.MultiIndex.from_product([signals.index, [s[0]]], names = ["Date", "Symbol"])
            trades = trades.append(signals)

        trades.sort_index(inplace = True)
        trades.index = pd.MultiIndex.from_tuples(trades.index, names = ["Date", "Symbol"])

        return trades


    def backtest(self,signals, cash, port_value = .1, batch = 100):
        
        SYMBOL = 1 # Constant for which element in index represents symbol
        portfolio = dict()    # Will contain how many stocks are in the portfolio for a given symbol
        port_prices = dict()  # Tracks old trade prices for determining profits
        # Dataframe that will contain backtesting report
        results = pd.DataFrame({"Start Cash": [],
                                "End Cash": [],
                                "Portfolio Value": [],
                                "Type": [],
                                "Shares": [],
                                "Share Price": [],
                                "Trade Value": [],
                                "Profit per Share": [],
                                "Total Profit": []})

        for index, row in signals.iterrows():
            # These first few lines are done for any trade
            shares = portfolio.setdefault(index[SYMBOL], 0)
            trade_val = 0
            batches = 0
            cash_change = row["Price"] * shares   # Shares could potentially be a positive or negative number (cash_change will be added in the end; negative shares indicate a short)
            portfolio[index[SYMBOL]] = 0  # For a given symbol, a position is effectively cleared

            old_price = port_prices.setdefault(index[SYMBOL], row["Price"])
            portfolio_val = 0
            for key, val in portfolio.items():
                portfolio_val += val * port_prices[key]

            if row["Signal"] == "Buy" and row["Regime"] == 1:  # Entering a long position
                batches = np.floor((portfolio_val + cash) * port_value) // np.ceil(batch * row["Price"]) # Maximum number of batches of stocks invested in
                trade_val = batches * batch * row["Price"] # How much money is put on the line with each trade
                cash_change -= trade_val  # We are buying shares so cash will go down
                portfolio[index[SYMBOL]] = batches * batch  # Recording how many shares are currently invested in the stock
                port_prices[index[SYMBOL]] = row["Price"]   # Record price
                old_price = row["Price"]
            elif row["Signal"] == "Sell" and row["Regime"] == -1: # Entering a short
                pass
                # Do nothing; can we provide a method for shorting the market?
            #else:
                #raise ValueError("I don't know what to do with signal " + row["Signal"])

            pprofit = row["Price"] - old_price   # Compute profit per share; old_price is set in such a way that entering a position results in a profit of zero

            # Update report
            results = results.append(pd.DataFrame({
                    "Start Cash": cash,
                    "End Cash": cash + cash_change,
                    "Portfolio Value": cash + cash_change + portfolio_val + trade_val,
                    "Type": row["Signal"],
                    "Shares": batch * batches,
                    "Share Price": row["Price"],
                    "Trade Value": abs(cash_change),
                    "Profit per Share": pprofit,
                    "Total Profit": batches * batch * pprofit
                }, index = [index]))
            cash += cash_change  # Final change to cash balance

        results.sort_index(inplace = True)
        results.index = pd.MultiIndex.from_tuples(results.index, names = ["Date", "Symbol"])

        return results

