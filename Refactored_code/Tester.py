import pandas as pd
from statsmodels.tsa.stattools import coint
from statsmodels.tsa.stattools import adfuller as adf

class Tester:


    def __init__(self,s):
    #self.pairs = pd.read_csv('./data/pairs.csv')
        self.significance=s

    def choose_pairs_from_list(self):
        list = []



        for ii in range(0,len(self.pairs)):
            print(ii)
            coin_name_1 = self.pairs['coin1'][ii]
            coin_name_2 = self.pairs['coin2'][ii]

            coin_1 = pd.read_csv('./data/'+str(coin_name_1) + '.csv')
            coin_1 = coin_1.drop(['Open', 'High', 'Low', 'Volume', 'Market Cap'], axis=1)
            coin_1['Date'] = pd.to_datetime(coin_1['Date'], infer_datetime_format=True)
            coin_1 = coin_1.set_index('Date')
            coin_1 = coin_1.resample('D').mean()

            coin_2 = pd.read_csv('./data/'+str(coin_name_2) + '.csv')
            coin_2 = coin_2.drop(['Open', 'High', 'Low', 'Volume', 'Market Cap'], axis=1)
            coin_2['Date'] = pd.to_datetime(coin_2['Date'], infer_datetime_format=True)
            coin_2 = coin_2.set_index('Date')
            coin_2 = coin_2.resample('D').mean()
            if len(coin_1)>len(coin_2):
                coin_1=coin_1[0:len(coin_2)]

            else:
                coin_2=coin_2[0:len(coin_1)]

            result = coint(coin_1, coin_2)
            pvalue = result[1]
            print(pvalue)

            if pvalue<0.001:
                list.append([coin_name_1,coin_name_2])
        return list
    
    #the following tests cointegration and output either true of false, depending whether
    #the p value is smaller than the significance
    def test_cointegration(self, coin1, coin2):
        if coint(coin1, coin2)[1] < self.significance:
            return True
        else:
            return False
        
    #the following tests stationarity using aug dickey fuller and output either true of false,
    #depending whether the p value is smaller than the significance
    def test_stationarity(self, coin1, coin2, beta):
        temp=coin2-beta*coin1
        if adf(temp)[1] < self.significance:
            return True
        else:
            return False

