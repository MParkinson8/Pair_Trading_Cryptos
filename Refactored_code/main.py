from DataHolder import DataHolder
from Strategy import Strategy
from Backtest import Backtest
from Trader import Trader
from Tester import Tester
from Plotter import Plotter


##################################################################################
if __name__=="__main__":

#Available coins: BTC LTC ETH ETC DASH XMR BCH

#select the two coins to analyse
    coins = ['ETC', 'ETH']
#set windows for use of past data 
    window_ols = 48*1 #estimation of beta
    window_ma = 48*7#normalisation of the z score
    
#TEMP: levels to close position
    buy_sell_zscore = 2.0
    close_zscore = 0.5
#trading data
    starting_capital = 1000.0
#provide risk adversion in [0,1] where it represets the percentage of 
#portfolio value invested in one trade
    risk_adversion = 0.1  #(exposure)
    comission_per_trade = 0.5/100 #this is variable commission 
    #significance= 0.1 #for statistical test acceptance
    significance= 0.1

##################################################################################

    data = DataHolder(coins,window_ols,window_ma)
    #initialise cointegration and stationarity test
    tester=Tester(significance)
    # Set the strategy, parameters are the entry and exit points of the model
    strategy = Strategy(buy_sell_zscore, close_zscore)
    # Trader holds capital
    trader = Trader(starting_capital,risk_adversion)
    # Backtest iterates over the days.
    backtest = Backtest(comission_per_trade)
    plotter=Plotter()
    
#---------------------------------------------------------------------------------

    # Read coins prices, compute z-srore and beta
    data.get_data()

    # Run the backtest
    backtest.run_backtest(trader,strategy,data,tester,window_ols)

    # Plot results of the backtest
    plotter.plot(trader,data)

#--------------------------------------------------------------------------------