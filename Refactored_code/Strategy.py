


class Strategy:

    def __init__ (self, buy_sell_zscore, close_zscore):
        #here we will have to call a function to compute these points
        self.buy_sell_zscore = buy_sell_zscore
        self.close_zscore = close_zscore

###################################################################################

#the following uses the zscore to decide whether to enter long or short in a position 
# and to decide when to close. This function is called only when there is cointegration
    def generate_signal(self, zscore, beta, price_curr_1, price_curr_2, sum_1, sum_2,commission,bud):

#"bud" (budget) represent the maximum exposure on one side (the one with cointegration parameter 1)

        #if z score is deep negative and we are currently not trading
        if zscore<-self.buy_sell_zscore and sum_2==0:
            #then we buy currency 2 and sell currency 1
            #transaction cost is proportional to the size of the trade
            value = -bud + bud*beta*price_curr_1/price_curr_2 - commission*(abs(bud) +abs( bud*beta))
            position_curr_1 = -bud*beta/price_curr_2 #short beta unit of budget currency 1
            position_curr_2 = bud/price_curr_2 #long 1 unit of budget currency 2

        #if z score is positive and we are currently not trading
        elif zscore>self.buy_sell_zscore and sum_2==0:
            #then we buy currency 1 and sell currency 2
            #transaction cost is proportional to the size of the trade
            value = +bud - bud*beta*price_curr_1/price_curr_2 - commission*(abs(bud) +abs( bud*beta))
            position_curr_1 = bud*beta/price_curr_2 #long beta unit of budget currency 1
            position_curr_2 = -bud/price_curr_2 #short 1 unit of budget currency 2

        # the spread is narrow-->close all positions (avoid currency 1 coins leftovers)
        elif -self.close_zscore<zscore<self.close_zscore and sum_2 != 0:
            # the sum variable only contains the current position in the coins
            value = +sum_2*price_curr_2+sum_1*price_curr_1 - commission*(
                                                      abs(sum_2*price_curr_2) +abs( sum_1*beta * price_curr_1))
            #positions are closed by entering in opposite trades
            position_curr_1 = -sum_1
            position_curr_2 = -sum_2

        # spread does not have a statistically significant value, wait.
        else:
            value = 0.0
            position_curr_1 = 0.0
            position_curr_2 = 0.0

        return value, position_curr_1, position_curr_2


###################################################################################

#the following takes care of rebalancing. The function is called when coins are
#cointegrated with betanew parameter
    def rebalance(self,zscore, beta,betanew, price_curr_1, price_curr_2, sum_1, sum_2,commission,bud):
        #liquidate the position (on paper)
        value = sum_1*price_curr_1
        position_curr_1 = -sum_1
        position_curr_2 = 0.0
#rebalance the position according to the zscore or close it
        if zscore<-self.buy_sell_zscore:
            value =  bud*betanew *price_curr_1/price_curr_2 -commission*abs(bud*(betanew-beta))
            position_curr_1 = -bud*betanew/price_curr_2
        elif zscore>self.buy_sell_zscore:
            value = - bud*betanew*price_curr_1/price_curr_2 -commission*abs(bud*(betanew-beta))
            position_curr_1 = bud*betanew/price_curr_2
        else:
            value = +sum_2*price_curr_2+sum_1*price_curr_1 - commission*(
                           abs(sum_2*price_curr_2) +abs( sum_1*beta * price_curr_1)) 
            position_curr_1 = -sum_1
            position_curr_2 = -sum_2

        return value, position_curr_1, position_curr_2

###################################################################################
