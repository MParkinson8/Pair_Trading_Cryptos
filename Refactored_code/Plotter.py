import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Plotter:

###################################################################################

    def plot_zscore(self,Zscore, name1, name2):

        plt.figure()
        plt.plot(Zscore)
        plt.title(name1+" "+name2+" normalised spread")
        plt.axhline(0, color='black')
        plt.axhline(2.0, color='red', linestyle='--');
        plt.axhline(-2.0, color='green', linestyle='--');

#----------------------------------------------------------------------------------

    def plot_openZ(self,Zscore, name1, name2):

        plt.figure()
        plt.plot(Zscore)
        plt.title(name1+" "+name2+" normalised spread for open positions")
        plt.axhline(0, color='black')
        plt.axhline(2.0, color='red', linestyle='--');
        plt.axhline(-2.0, color='green', linestyle='--');

#----------------------------------------------------------------------------------

    def plot_beta(self,beta):

        plt.figure()
        plt.plot(beta)

#----------------------------------------------------------------------------------

    def plot_currencies(self,currencies,name1,name2):

        plt.figure()
        plt.semilogy(currencies[str(name1)])
        plt.semilogy(currencies[str(name2)])
        plt.legend([str(name1), str(name2)])
        plt.title(name1+" "+name2)
        plt.ylabel('$ (log-scale)');

#----------------------------------------------------------------------------------

    def plot_returns(self,value, name1, name2):
        #returns = pd.Series((np.cumsum(value)-value[0])/value[0]*100.0)#this is not the metric we want
        #now it plots monthly returns
        tt=48*20
        returns=[]
        for i in range(tt,len(value)-tt):
            returns.append((np.sum(value[0:tt+i])-np.sum(value[0:i]))/np.sum(value[0:i])*100.0)
        return_s = pd.Series(returns)
    
        plt.figure()
        plt.plot(return_s)
        plt.title(name1+" "+name2+" returns %")
        plt.ylabel('Returns %');

#----------------------------------------------------------------------------------

    def plot_pnl(self,currencies,value, name1, name2):

        plt.figure()
        plt.plot(np.cumsum(value))
        plt.title(name1+" "+name2+" P&L")
        plt.ylabel('Portfolio value $');

#----------------------------------------------------------------------------------

    def plot_logsc(self,currencies, beta, name1, name2):

        plt.figure()
        plt.plot(currencies[name1].index[len(currencies)-len(beta):len(currencies)],-np.min(beta*currencies[name1].values[len(currencies)-len(beta):len(currencies)])+ beta*currencies[name1].values[len(currencies)-len(beta):len(currencies)])
        plt.plot(currencies[name2].index[len(currencies)-len(beta):len(currencies)], -np.min(beta*currencies[name1].values[len(currencies)-len(beta):len(currencies)])+currencies[name2].values[len(currencies)-len(beta):len(currencies)])
        plt.legend([str(name1)+' rescaled', str(name2)])
        plt.title(name1+" "+name2+" scaled prices")
        plt.ylabel('$ (log-scale)');

#----------------------------------------------------------------------------------

    def plot_open_position(self,position1,position2, name1, name2):

        plt.figure()
        plt.plot(np.cumsum(position1))
        plt.plot(np.cumsum(position2))
        plt.legend([str(name1), str(name2)])
        plt.title(name1+" "+name2+" portfolio positions")
        plt.ylabel('coins-holding (# of coins)');

#----------------------------------------------------------------------------------

    def plot_units_bought_and_sold(self,position1, position2, name1, name2):

        plt.figure()
        plt.plot(position1)
        plt.plot(position2)
        plt.legend([str(name1), str(name2)])
        plt.title(name1+" "+name2+" trades")
        plt.ylabel('units bought and sold');

###################################################################################

    def plot(self,trader,data):
        self.plot_zscore(trader.Zscore, data.name1, data.name2)
        self.plot_openZ(trader.openZ, data.name1, data.name2)
        self.plot_beta(trader.beta)
        self.plot_currencies(data.currencies, data.name1, data.name2)
        self.plot_pnl(data.currencies,trader.value, data.name1, data.name2)
        #self.plot_returns(trader.value, data.name1, data.name2)
        #self.Plotter.plot_logsc(data.currencies, data.beta, data.name1, data.name2)
        self.plot_open_position(trader.position1, trader.position2, data.name1, data.name2)
        self.plot_units_bought_and_sold(trader.position1, trader.position2, data.name1, data.name2)
       
        plt.show()
###################################################################################