from DataHolder import DataHolder
from Strategy import Strategy
from Backtest import Backtest
from Trader import Trader
from Plotter import Plotter
import matplotlib.pyplot as plt


def plot(trader,data):
    Plotter.plot_zscore(data.Zscore, data.name1, data.name2)
    Plotter.plot_currencies(data.currencies, data.name1, data.name2)
    Plotter.plot_pnl(data.currencies,trader.value, data.name1, data.name2)
    Plotter.plot_returns(trader.value, data.name1, data.name2)
    #Plotter.plot_logsc(data.currencies, data.beta, data.name1, data.name2)
    Plotter.plot_open_position(trader.position1, trader.position2, data.name1, data.name2)
    Plotter.plot_units_bought_and_sold(trader.position1, trader.position2, data.name1, data.name2)

    plt.show()


if __name__=="__main__":

#Available coins: BTC LTC ETH ETC DASH XMR BCH

    coins = ['BTC', 'BCH']
    window_ols = 48*7
    window_ma = 48*28
    buy_sell_zscore = 2.0
    close_zscore = 0.1
    starting_capital = 1000.0  #the capital does not affect the size of the positions
    comission_per_trade = 2.0

    data = DataHolder(coins,window_ols,window_ma)
    strategy = Strategy(buy_sell_zscore, close_zscore)
    trader = Trader(starting_capital)
    backtest = Backtest(comission_per_trade)

    data.get_data()

    backtest.run_backtest(trader,strategy,data)

    plot(trader,data)
