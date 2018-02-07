import pandas as pd

class DataHolder:

    def __init__(self,coins,window_ols,window_ma):

        self.coins = coins

        # choose the width of the window for the estimation of beta (the wider the smoother)
        self.window_ols = window_ols

        # choose the lookback period for the moving average to build the Zscore (more robust for slower ma)
        self.window_ma = window_ma

        self.currencies = []

        self.currencies=[]

###################################################################################

#    def read_zscore(self):
#
#        #upload .csv produced by trading_signal.py
#        Zscore=pd.read_csv('./data/Z_'+str(self.coins[0])+'-'+str(self.coins[1])+'.csv')
#        Zscore = Zscore.dropna(axis = 0)
#        Zscore=Zscore['Unnamed: 1'].tolist()
#
#        return Zscore
#
##---------------------------------------------------------------------------------
#
#    def read_beta(self):
#        beta=pd.read_csv('./data/b_'+str(self.coins[0])+'-'+str(self.coins[1])+'.csv')
#        beta=beta['beta'].tolist()
#    
#        return beta


###################################################################################

    def read_currencies(self):

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

#---------------------------------------------------------------------------------

    def get_data(self):

        self.read_currencies()

##################################################################################

    def printer(self):

        self.Zscore.to_csv('./data/Z_'+str(self.name1)+'-'+str(self.name2)+'.csv')
        self.beta = pd.DataFrame(self.beta, columns=["beta"])
        self.beta.to_csv('./data/b_'+str(self.name1)+'-'+str(self.name2)+'.csv', index=False)