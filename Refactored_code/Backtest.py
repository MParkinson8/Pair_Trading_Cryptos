import numpy as np
import math

class Backtest:

    def __init__(self, commission_per_trade):
        self.commission_per_trade = commission_per_trade;

###################################################################################

    def run_backtest(self, trader, strategy, data, tester,window_ols):
        #backtest the trading strategy given by the if statements in 68 72 76-80

        offset = window_ols

        beta=0
#we loop over all time steps, this simulates the arrival of new information when trading live
        for i in range(0,len(data.currencies[data.name1])-window_ols):

            # Current time idx in the currencies, since beta is shorter than the currencies need to move idx accordingly
            idx = offset + i
#we compute the net open position in the coins
            sum_2 = np.sum(trader.position2)
            sum_1 = np.sum(trader.position1)
#we read the current prices with offset
            price_curr_1 = data.currencies[data.name1][idx]
            price_curr_2 = data.currencies[data.name2][idx]
            hprice1=data.currencies[data.name1][(idx-window_ols):idx]
            hprice2=data.currencies[data.name2][(idx-window_ols):idx]
            
            #rebalance when the test for stationarity with current beta fails, if position is not open it does not have effect
            if not math.isnan(beta):
                rebalancing=not tester.test_stationarity(hprice1,hprice2,beta)
            else:
                rebalancing=False

#if we are not trading we use the zscore to read the trading signal provided the coins are cointegrated
            if sum_2==0  and tester.test_cointegration(hprice1,hprice2):#and data.beta[i]>0:
                beta = tester.calculate_beta(hprice1,hprice2)
                zscore = tester.calculate_Zscore(hprice1,hprice2,beta)
                trader.openZ.append(np.nan)
                trader.Zscore.append(zscore)
                trader.beta.append(beta)
                #check if convenient to open position 
                value, position_curr_1, position_curr_2 = strategy.generate_signal \
                                                        (zscore, beta, price_curr_1, price_curr_2, 
                                                         sum_1, sum_2, self.commission_per_trade,
                                                         sum(trader.value)/price_curr_2*0.1)
#if the position is already open we have to manage it
            elif sum_2!=0 :
                #if we do not rebalance we use the same beta we used to open the position
                if not rebalancing:
                    #we compute the value of the trading signal using old beta
                    temp = hprice2-beta*hprice1
                    zscore = (price_curr_2-beta*price_curr_1-temp.mean())/temp.std()
                    trader.openZ.append(zscore)# we save it separately for visualisation purposes 
                    trader.Zscore.append(np.nan)
                    trader.beta.append(beta)
                    #check whether to close position
                    value, position_curr_1, position_curr_2 = strategy.generate_signal \
                                                            (zscore, beta, price_curr_1, price_curr_2, 
                                                             sum_1, sum_2, self.commission_per_trade,
                                                             sum(trader.value)/price_curr_2*0.1)
#if we rebalance, and the coins are cointegrated
                elif rebalancing and tester.test_cointegration(hprice1,hprice2):#and data.beta[i]>0:
                    #load the trading signal corresponding to the new beta
                    betanew = tester.calculate_beta(hprice1,hprice2)
                    zscore = tester.calculate_Zscore(hprice1,hprice2,betanew)
                    trader.openZ.append(zscore)
                    trader.Zscore.append(np.nan)
                    trader.beta.append(betanew)
                    #rebalance
                    value, position_curr_1, position_curr_2 = strategy.rebalance \
                                                            (beta,betanew, price_curr_1, price_curr_2, 
                                                             sum_1, sum_2, self.commission_per_trade,
                                                             sum(trader.value)/price_curr_2*0.1)
                    beta=betanew #update the value of beta for future management of the position
                else:#the currencies are no longer cointegrated, close the position
                    value=sum_2*price_curr_2+sum_1*price_curr_1 - self.commission_per_trade*(
                                            abs(sum_2*price_curr_2) +abs( sum_1*beta * price_curr_1))
                    position_curr_1=-sum_1
                    position_curr_2=-sum_2
                    trader.Zscore.append(np.nan)
                    trader.openZ.append(np.nan)
                    trader.beta.append(np.nan)
            else: 
                    value=0
                    position_curr_1=0
                    position_curr_2=0
                    trader.Zscore.append(np.nan)
                    trader.openZ.append(np.nan)
                    trader.beta.append(np.nan)

            if i == 0:
                trader.value[0]+value
            else:
                trader.value.append(value)

            trader.position1.append(position_curr_1)
            trader.position2.append(position_curr_2)

###################################################################################




