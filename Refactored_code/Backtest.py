
import numpy as np

class Backtest:

    def __init__(self, commission_per_trade):
        self.commission_per_trade = commission_per_trade;

    def run_backtest(self, trader, strategy, data):
        #backtest the trading strategy given by the if statements in 68 72 76-80

        offset = len(data.currencies) - len(data.beta)
        counter=0
#we loop over all time steps, this simulates the arrival of new information when trading live
        for i in range(0,len(data.Zscore)):

            # Current time idx in the currencies, since beta is shorter than the currencies need to move idx accordingly
            idx = offset + i
#we compute the net open position in the coins
            sum_2 = np.sum(trader.position2)
            sum_1 = np.sum(trader.position1)
#we read the current prices with offset
            price_curr_1 = data.currencies[data.name1][idx]
            price_curr_2 = data.currencies[data.name2][idx]
            
            #temporarely we set rebalance after a position has been open for x days 
            x=7
            rebalancing=not counter%(24*x)

#if we are not trading we use the zscore to read the trading signal (only when beta>0, what would the opposite mean?)
            if sum_2==0 :#and data.beta[i]>0:
                counter=0 #set counter to zero
                zscore = data.Zscore[i]
                trader.openZ.append(0)
                beta = data.beta[i]#read the time dependent beta
                #check if convenient to open position 
                value, position_curr_1, position_curr_2 = strategy.generate_signal \
                                                        (zscore, beta, price_curr_1, price_curr_2, 
                                                         sum_1, sum_2, self.commission_per_trade,
                                                         sum(trader.value)/price_curr_2*0.1)
#if the position is already open we have to manage it
            elif sum_2!=0:
                counter=counter+1 #the counter increases and counts how many periods the position has been open
                #if we do not rebalance we use the same beta we used to open the position
                if not rebalancing:
                    #we compute the value of the trading signal using old beta
                    zscore = (price_curr_2-beta*price_curr_1-data.spread_mavg[i])/data.spread_std[i]
                    trader.openZ.append(zscore)# we save it separately for visualisation purposes 
                    #check whether to close position
                    value, position_curr_1, position_curr_2 = strategy.generate_signal \
                                                            (zscore, beta, price_curr_1, price_curr_2, 
                                                             sum_1, sum_2, self.commission_per_trade,
                                                             sum(trader.value)/price_curr_2*0.1)
#if we rebalance, and the time dependent beta is positive
                elif rebalancing :#and data.beta[i]>0:
                    #load the trading signal corresponding to the new beta
                    zscore = data.Zscore[i]
                    trader.openZ.append(zscore)
                    betanew = data.beta[i] #read the new beta 
                    #rebalance
                    value, position_curr_1, position_curr_2 = strategy.rebalance \
                                                            (beta,betanew, price_curr_1, price_curr_2, 
                                                             sum_1, sum_2, self.commission_per_trade,
                                                             sum(trader.value)/price_curr_2*0.1)
                    beta=betanew #update the value of beta for future management of the position
                else: #if the new beta is negative TEMP we do nothing
                    value=0
                    position_curr_1=0
                    position_curr_2=0
            else: #if the new beta is negative TEMP we do nothing
                    value=0
                    position_curr_1=0
                    position_curr_2=0

            if i == 0:
                trader.value[0]+value
            else:
                trader.value.append(value)

            trader.position1.append(position_curr_1)
            trader.position2.append(position_curr_2)


        




