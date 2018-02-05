
import numpy as np

class Backtest:

    def __init__(self, commission_per_trade):
        self.commission_per_trade = commission_per_trade;

    def run_backtest(self, trader, strategy, data):
        #backtest the trading strategy given by the if statements in 68 72 76-80

        offset = len(data.currencies) - len(data.beta)

        for i in range(0,len(data.Zscore)):

            # Current time idx in the currencies, since beta is shorter than the currencies need to move idx accordingly
            idx = offset + i

            sum_2 = np.sum(trader.position2)
            sum_1 = np.sum(trader.position1)
            price_curr_1 = data.currencies[data.name1][idx]
            price_curr_2 = data.currencies[data.name2][idx]
            zscore = data.Zscore[i]
            beta = data.beta[i]

            value, position_curr_1, position_curr_2 = strategy.generate_signal(zscore, beta, price_curr_1, price_curr_2, sum_1, sum_2, self.commission_per_trade,sum(trader.value)/price_curr_2*0.1)


            if i == 0:
                trader.value[0]+value
            else:
                trader.value.append(value)

            trader.position1.append(position_curr_1)
            trader.position2.append(position_curr_2)


        




