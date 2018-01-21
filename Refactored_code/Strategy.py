


class Strategy:

    def __init__ (self, buy_sell_zscore, close_zscore):
        self.buy_sell_zscore = buy_sell_zscore
        self.close_zscore = close_zscore

    def generate_signal(self, zscore, beta, price_curr_1, price_curr_2, sum_1, sum_2):

        # sell beta coins of first currency buy one coin of the second --> the spread will narrow
        if zscore<-self.buy_sell_zscore:

            value = -price_curr_2 + beta * price_curr_1
            position_curr_1 = -beta
            position_curr_2 = 1.0

        # buy beta coins of first currency sell one coin of the second --> the spread will narrow
        elif zscore>self.close_zscore:
            value = +price_curr_2 - beta * price_curr_1
            position_curr_1 = beta
            position_curr_2 = -1.0

        # the spread is narrow-->close all positions (avoid currency 1 coins leftovers)
        elif -self.close_zscore<zscore<self.close_zscore:

            value = (-sum_2*price_curr_2-sum_1*price_curr_1)
            position_curr_1 = -sum_1
            position_curr_2 = -sum_2

        # spread does not have a statistically significant value, wait.
        else:
            value = 0.0
            position_curr_1 = 0.0
            position_curr_2 = 0.0

        return value, position_curr_1, position_curr_2

