import numpy as np

class Backtest:

    def __init__(self, commission_per_trade):
        self.commission_per_trade = commission_per_trade;

###################################################################################

    def run_backtest(self, trader, strategy, data, tester,window_ols):

#we loop over all time steps, this simulates the arrival of new information when trading live
        for i in range(window_ols,len(data.currencies[data.name1])-window_ols):

#we compute the net open position in the coins
            sum_2 = np.sum(trader.position2)
            sum_1 = np.sum(trader.position1)
#we read the data and save separately the current price and the window of past prices
            price_curr_1 = data.currencies[data.name1][i]
            price_curr_2 = data.currencies[data.name2][i]
            hprice1=data.currencies[data.name1][(i-window_ols):i]
            hprice2=data.currencies[data.name2][(i-window_ols):i]

#we decide now what to do with the position depending whether it is open or not
#if we are not trading we use the zscore to read the trading signal provided the coins are cointegrated
            if sum_2==0 and sum_1==0 and tester.test_cointegration(hprice1,hprice2):
#compute the cointegration parameter
                beta = tester.calculate_beta(hprice1,hprice2)
#compute the z score
                zscore = tester.calculate_Zscore(hprice1,hprice2,beta)
#save data for future visulisation
                trader.openZ.append(np.nan)
                trader.Zscore.append(zscore)
                trader.beta.append(beta)
                #check if convenient to open position 
                value, position_curr_1, position_curr_2 = strategy.generate_signal \
                                                        (zscore, beta, price_curr_1, price_curr_2, 
                                                         sum_1, sum_2, self.commission_per_trade,
                                                         sum(trader.value)*trader.riskad)
#if the position is already open we have to manage it
            elif abs(sum_2)+abs(sum_1)>0:
                #if we do not rebalance we use the same beta we used to open the position
                if tester.test_stationarity(hprice1,hprice2,beta):
                    #we compute the value of the trading signal using old beta
                    temp = hprice2-beta*hprice1
                    zscore = (price_curr_2-beta*price_curr_1-temp.mean())/temp.std()
# we save it separately for visualisation purposes 
                    trader.openZ.append(zscore)
                    trader.Zscore.append(np.nan)
                    trader.beta.append(beta)
#check whether to close position
                    value, position_curr_1, position_curr_2 = strategy.generate_signal \
                                                            (zscore, beta, price_curr_1, price_curr_2, 
                                                             sum_1, sum_2, self.commission_per_trade,
                                                             sum(trader.value)*trader.riskad)
#if we rebalance, and the coins are cointegrated
                elif tester.test_cointegration(hprice1,hprice2):
#compute the new cointegration parameter and z score
                    betanew = tester.calculate_beta(hprice1,hprice2)
                    zscore = tester.calculate_Zscore(hprice1,hprice2,betanew)
#save it separately for visualisation purposes
                    trader.openZ.append(zscore)
                    trader.Zscore.append(np.nan)
                    trader.beta.append(betanew)
#rebalance
                    value, position_curr_1, position_curr_2 = strategy.rebalance \
                                                            (zscore,beta,betanew, price_curr_1, price_curr_2, 
                                                             sum_1, sum_2, self.commission_per_trade,
                                                             sum(trader.value)*trader.riskad)
#update the value of beta for future management of the position
                    beta=betanew 
                else:#the currencies are no longer cointegrated, close the position
                    value=sum_2*price_curr_2+sum_1*price_curr_1 - self.commission_per_trade*(
                                            abs(sum_2*price_curr_2) +abs( sum_1*beta * price_curr_1))
                    position_curr_1=-sum_1
                    position_curr_2=-sum_2
                    trader.Zscore.append(np.nan)
                    trader.openZ.append(np.nan)
                    trader.beta.append(np.nan)
            else: #position is closed but there is no cointegration -> do nothing
                    value=0
                    position_curr_1=0
                    position_curr_2=0
                    trader.Zscore.append(np.nan)
                    trader.openZ.append(np.nan)
                    trader.beta.append(np.nan)
#update the portfolio value
            if i == 0:
                trader.value[0]+value
            else:
                trader.value.append(value)
#save current position
            trader.position1.append(position_curr_1)
            trader.position2.append(position_curr_2)

###################################################################################




