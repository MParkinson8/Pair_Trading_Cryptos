from DataHolder import DataHolder
from Strategy import Strategy
from Backtest import Backtest
from Trader import Trader
from Tester import Tester
from Plotter import Plotter


##################################################################################
if __name__=="__main__":

#Available coins: BTC LTC ETH ETC DASH XMR BCH

    coins = ['BCH', 'BTC']
    window_ols = 48*30
    window_ma = 48*30
    
    # How many standard deviations from the mean are entry and exit points
    buy_sell_zscore = 2.0
    close_zscore = 0.2
    starting_capital = 1000.0
    comission_per_trade = 0.5/100 #this is variable commission 
    significance= 0.1
    #significance= 1.1

##################################################################################

    data = DataHolder(coins,window_ols,window_ma)
    tester=Tester(significance)
    # Set the strategy, parameters are the entry and exit points of the model
    strategy = Strategy(buy_sell_zscore, close_zscore)
    # Trader holds capital
    trader = Trader(starting_capital)
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