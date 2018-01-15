import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import csv
from DataHolder import DataHolder
from Plotter import Plotter



class Backtest:

    def __init__(self):
        self.coins = ['Dash','Litecoin']
        self.Q= [0]
        self.trades = [[0,0]]
        self.budget= [1000]
        self.value = [1000]
        self.m=0

        #coins=['Dash','Litecoin']
        #coins=['PIVX','Litecoin']
        #coins=['GameCredits','StellarLumens']


    def get_data(self):

        self.Zscore = DataHolder.get_zscore(self.coins)
        self.beta = DataHolder.get_beta(self.coins)
        self.currencies, self.name1, self.name2 = DataHolder.get_currencies(self.coins)


    def run_backtest(self):
            #backtest the trading strategy given by the if statements in 68 72 76-80
        trade=0
        for i in range(1,len(self.Zscore)):
            P1=self.currencies[self.name1][i]
            P2=self.currencies[self.name2][i]
            if trade==0:
                if self.Zscore[i]<-2: #sell beta coins of first currency buy one coin of the second --> the spread will narrow
                    trade=1
                    self.Q.append(np.abs(self.budget[i-1]/(P1-self.m*self.beta[i]*P2)))
                elif self.Zscore[i]>2:
                    trade=1
                    self.Q.append(-np.abs(self.budget[i-1]/(P1-self.m*self.beta[i]*P2)))
                else:
                    self.Q.append(self.Q[i-1])
            else:
                if -0.5<self.Zscore[i]<0.5:
                    self.Q.append(0)
                    trade=0
                else:
                    self.Q.append(self.Q[i-1])
            self.trades.append([(self.Q[i]-self.Q[i-1])*P1,(self.Q[i]-self.Q[i-1])*self.beta[i]*P2])
            self.value.append(self.budget[i-1]+self.Q[i]*(P1-self.beta[i]*P2)+self.trades[i][0]+self.trades[i][1])
            self.budget.append(self.budget[i-1]-self.trades[i][0]-self.trades[i][1])

        
    def plot(self):
        Plotter.plot_zscore(self.Zscore, self.name1, self.name2)
        Plotter.plot_currencies(self.currencies,self.name1, self.name2)
        Plotter.plot_logsc(self.currencies, self.beta, self.name1, self.name2)
        Plotter.plot_pnl(self.value, self.name1, self.name2)
        
        plt.figure()
        plt.plot(self.Q)
        
        #len_c=len(self.currencies[self.name2])
        #len_p=len(self.position1)
        #Plotter.plot_open_position(self.position1*self.currencies[self.name1][len_c-len_p:len_c], self.position2*self.currencies[self.name2][len_c-len_p:len_c], self.name1, self.name2)
        #Plotter.plot_units_bought_and_sold(self.position1, self.position2, self.name1, self.name2)
        #plt.show()



if __name__=="__main__":
    backtest = Backtest()
    #plotter = Plotter()
    #dataHolder = DataHolder()
    backtest.get_data()
    backtest.run_backtest()
    backtest.plot()

