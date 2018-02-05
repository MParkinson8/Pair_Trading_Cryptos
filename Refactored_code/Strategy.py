


class Strategy:

    def __init__ (self, buy_sell_zscore, close_zscore):
        self.buy_sell_zscore = buy_sell_zscore
        self.close_zscore = close_zscore

    def generate_signal(self, zscore, beta, price_curr_1, price_curr_2, sum_1, sum_2,commission,bud):

        #if z score is deep negative and we are currently not trading
        if zscore<-self.buy_sell_zscore and sum_2==0:
            #then we buy currency 2 and sell currency 1
            #transaction cost is proportional to the size of the trade
            value = -bud*price_curr_2 + bud*beta * price_curr_1 - commission*(abs(bud*price_curr_2) +abs( bud*beta * price_curr_1))
            position_curr_1 = -bud*beta #short beta unit of budget currency 1
            position_curr_2 = bud*1.0 #long 1 unit of budget currency 2

        #if z score is positive and we are currently not trading
        elif zscore>self.buy_sell_zscore and sum_2==0:
            #then we buy currency 1 and sell currency 2
            #transaction cost is proportional to the size of the trade
            value = +bud*price_curr_2 - bud*beta * price_curr_1 - commission*(abs(bud*price_curr_2) +abs( bud*beta * price_curr_1))
            position_curr_1 = bud*beta #long beta unit of budget currency 1
            position_curr_2 = -bud*1.0 #short 1 unit of budget currency 2

        # the spread is narrow-->close all positions (avoid currency 1 coins leftovers)
        elif -self.close_zscore<zscore<self.close_zscore and sum_2 != 0:
            # the sum variable only contains the current position in the coins
            value = +sum_2*price_curr_2+sum_1*price_curr_1 - commission*(abs(sum_2*price_curr_2) +abs( sum_1*beta * price_curr_1))
            #positions are closed by entering in opposite trades
            position_curr_1 = -sum_1
            position_curr_2 = -sum_2

        # spread does not have a statistically significant value, wait.
        else:
            value = 0.0
            position_curr_1 = 0.0
            position_curr_2 = 0.0

        return value, position_curr_1, position_curr_2





#here we rebalance the position 
    def rebalance(self, beta,betanew, price_curr_1, price_curr_2, sum_1, sum_2,commission,bud):
        #if we are long on c1 we liquidate the current position and open a new long position of size betanew
        if sum_2<0:
            value = (-bud*betanew+sum_1) * price_curr_1 - 0*commission*abs( bud*(betanew-beta) * price_curr_1)
            position_curr_1 = bud*(betanew)-sum_1
            position_curr_2 = 0
        else:
            value = (bud*betanew+sum_1) * price_curr_1 - 0*commission*abs( bud*(betanew-beta) * price_curr_1)
            position_curr_1 = -bud*(betanew)-sum_1
            position_curr_2 = 0

        return value, position_curr_1, position_curr_2
    
    
    
    