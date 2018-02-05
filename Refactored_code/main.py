from DataHolder import DataHolder
from Strategy import Strategy
from Backtest import Backtest
from Trader import Trader
from Plotter import Plotter
import matplotlib.pyplot as plt


def plot(trader,data):
    Plotter.plot_zscore(data.Zscore, data.name1, data.name2)
    Plotter.plot_openZ(trader.openZ, data.name1, data.name2)
    Plotter.plot_beta(data.beta)
    Plotter.plot_currencies(data.currencies, data.name1, data.name2)
    Plotter.plot_pnl(data.currencies,trader.value, data.name1, data.name2)
    #Plotter.plot_returns(trader.value, data.name1, data.name2)
    #Plotter.plot_logsc(data.currencies, data.beta, data.name1, data.name2)
    Plotter.plot_open_position(trader.position1, trader.position2, data.name1, data.name2)
    Plotter.plot_units_bought_and_sold(trader.position1, trader.position2, data.name1, data.name2)

    plt.show()


if __name__=="__main__":

#Available coins: BTC LTC ETH ETC DASH XMR BCH

    coins = ['DASH', 'XMR']
    window_ols = 48*7
    window_ma = 48*28
    
    # How many standard deviations from the mean are entry and exit points
    buy_sell_zscore = 2.0
    close_zscore = 0.2
    starting_capital = 1000.0
    comission_per_trade = 0.5/100 #this is variable commission 


    # DataHolder reads coins and computes beta and zscore
    data = DataHolder(coins,window_ols,window_ma)

    # Set the strategy, parameters are the entry and exit points of the model
    strategy = Strategy(buy_sell_zscore, close_zscore)
    
    # Trader holds capital
    trader = Trader(starting_capital)

    # Backtest iterates over the days.
    backtest = Backtest(comission_per_trade)

    # Read coins prices, compute z-srore and beta
    data.get_data()


    # Run the backtest
    backtest.run_backtest(trader,strategy,data)


    # Plot results of the backtest
    plot(trader,data)
