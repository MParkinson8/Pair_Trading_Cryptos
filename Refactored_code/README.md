
To compile in python 3 run in the terminal:

python3 main.py

or if python 2 is installed: 

python main.py



#TODO:



0. Check whether we have lookahead bias (it seems that we indeed have it...)
    ab{why? you talking about current code or the strategy outlined in report?}

1. Percent of the position is commission per trade (not fixed, but depends on the amount traded)
2. Specify the range of the backtest (Starting and ending days of the simulation)
3. Position sizes - percent of total capital
4. Different entry and exit points, i.e. enter when 2 sigmas away and exit when 1 standard deviation (need to think about it)ab{this is porvided by the optimal strategy file}
5. Update beta after entering position (i.e. adjust open position sizes with the time)
6. Add support for tracking open positions, i.e. support for multiple pairs of coins. (should be added in trader and backtest classes I.e. trader has infomation about portfolio and in backtest we go through all pairs in the portfolio)
7. Try with open, not close prices (i.e. leave open and drop close prices in the data holder){I have done this already at previous commit}
8. Add support for itterative computation of zscore and beta, i.e. assume real life scenario when we connect to the brocker and we need to update everything sequentially - should be added in the backtest class. We also need another class, say "Market" which we will ask from the backtest class to give more data.
9. Add computation of strategy performance, i.e. sharp ratio. ab{tricky business, but I have aready introduced monthly returns rather than compute them based on initial capital} 


#Files:

=====================================================================

main.py

Starting point of the function.
Here parameters are set and constructors of all classes are called.

=====================================================================

DataHolder.py


Holds the coins prices and zscore and beta

=====================================================================

Backtest.py

Iterates over the days and calls the strategy

=====================================================================

Strategy.py

Pairs trading heart 

=====================================================================

Plotter.py

Contains functionality to plot

=====================================================================

Tester.py

Tests for coins cointegration, ideally should be the starting point
for a program - to select pairs to trade. Should also support
cointegration check on the fly. I.e. check whether coins are still
cointegrated and if yes continue trading them

=====================================================================

Trader.py

Holds information about portfolio and capital








