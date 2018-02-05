import pandas as pd
import numpy as np
import statsmodels.api as sm



class DataHolder:

    def __init__(self,coins,window_ols,window_ma):

        self.coins = coins

        # choose the width of the window for the estimation of beta (the wider the smoother)
        self.window_ols = window_ols

        # choose the lookback period for the moving average to build the Zscore (more robust for slower ma)
        self.window_ma = window_ma

        self.beta = []

        self.Zscore = []

        self.currencies = []
        
        self.spread_mavg=[]
        
        self.spread_std=[]

    def read_zscore(self):

        #upload .csv produced by trading_signal.py
        Zscore=pd.read_csv('./data/Z_'+str(self.coins[0])+'-'+str(self.coins[1])+'.csv')
        Zscore = Zscore.dropna(axis = 0)
        Zscore=Zscore['Unnamed: 1'].tolist()

        return Zscore

    def read_beta(self):
        beta=pd.read_csv('./data/b_'+str(self.coins[0])+'-'+str(self.coins[1])+'.csv')
        beta=beta['beta'].tolist()
    
        return beta


    def read_currencies(self):
        currencies=[]

        for i in range(0,2):

            tmp = pd.read_csv('./data/'+str(self.coins[i])+'.csv')
            tmp = tmp.drop(['date','close','high','low','since','volume','weightedAverage'], axis = 1)
            #tmp['date']= pd.to_datetime(tmp['date'], infer_datetime_format=True)
            #tmp = tmp.set_index('date')
            #tmp= tmp.resample('30T').mean()
            self.currencies.append(tmp)

        for i in range(0, 2):
            self.currencies[i] = self.currencies[i].rename(columns={'open':str(self.coins[i])})



        self.currencies = pd.concat(self.currencies,axis=1)
        self.currencies = self.currencies.dropna(axis = 0)

        keys=self.currencies.keys()
        self.name1=keys[0]
        self.name2=keys[1]


    def get_data(self):

        self.read_currencies()
        self.calculate_beta()
        self.calculate_Zscore()


    def calculate_beta(self):

        self.N=len(self.currencies[self.name1])
        self.beta = [np.nan] * self.N
        y_ = self.currencies[self.name2]
        x_ = sm.add_constant(self.currencies[self.name1])

        # we are using an rectangular window here
        for n in range(self.window_ols, self.N):
            Y = y_[(n - self.window_ols):n]
            X = x_[(n - self.window_ols):n]
            b = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
            self.beta[n] = b[1].tolist()

    def calculate_Zscore(self):

        spread = self.currencies[self.name2] - self.beta * self.currencies[self.name1]

        # Get the 1 day moving average of the price spread
        spread_mavg1 = spread.rolling(window=1).mean()

        # Get the longer moving average
        self.spread_mavg = spread.rolling(window=self.window_ma,win_type='hamming',center=False).mean()

        # Take a rolling standard deviation
        self.spread_std = spread.rolling(window=self.window_ma).std()

        # Compute the z score for each day
        self.Zscore = (spread_mavg1 - self.spread_mavg)/self.spread_std


    def printer(self):

        self.Zscore.to_csv('./data/Z_'+str(self.name1)+'-'+str(self.name2)+'.csv')
        self.beta = pd.DataFrame(self.beta, columns=["beta"])
        self.beta.to_csv('./data/b_'+str(self.name1)+'-'+str(self.name2)+'.csv', index=False)