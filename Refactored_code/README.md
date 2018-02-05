
To compile in python 3 run in the terminal:

python3 main.py

or if python 2 is installed: 

python main.py


note that it is quite slow now that we use 30mins data, if you plot returns in addition (due to a badly written for loop) it becomes terribly slow!

#TODO:

I found a major error in Strategy.py, when closing the position the value was counted with the wrong sign. I corrected it and introduced two features: when a position is opened we read the signal on the true process, if we do so we need to rebalance otherwise we end up never closing the position.

0. Check whether we have lookahead bias (it seems that we indeed have it...)
    ab{why? you talking about current code or the strategy outlined in report?}
    am{We are trading based on the current close prices i.e. at day k, though we do not know close price on the day and thus should use close of previous day, i.e. day k-1}
ab{we are using open prices now so it should be fine...}

2. Specify the range of the backtest (Starting and ending days of the simulation)

4. Different entry and exit points, i.e. enter when 2 sigmas away and exit when 1 standard deviation (need to think about it)ab{this is provided by the optimal strategy file}

6. Add support for tracking open positions, i.e. support for multiple pairs of coins. (should be added in trader and backtest classes I.e. trader has infomation about portfolio and in backtest we go through all pairs in the portfolio)

8. Add support for itterative computation of zscore and beta, i.e. assume real life scenario when we connect to the brocker and we need to update everything sequentially - should be added in the backtest class. We also need another class, say "Market" which we will ask from the backtest class to give more data.{in this way we could load only most recent data rather than the whole time series}
9. Add computation of strategy performance, i.e. sharp ratio. ab{tricky business, but I have aready introduced monthly returns rather than compute them based on initial capital} 

10. Margin account for short position, i.e when opening short this should not offset the cost of going long in the computation of value. However when the position is closed we need to consider the margin account too. (should not change anything, however might be worth it to add an extra fee for shorting)

11. Check the resampling in data holder, should not be needed but it was there before and now does not work on 30 mins data---> we have no dates to use for item 2.

12 check the updates listed below. The performance are terrible now so I hope there is still stuff to correct

------DONE----
1. Percent of the position is commission per trade (not fixed, but depends on the amount traded)DONE

3. Position sizes - percent of total capital DONE

7. Try with open, not close prices (i.e. leave open and drop close prices in the data holder){I have done this already at previous commit} DONE

5. Update beta after entering position (i.e. adjust open position sizes with the time) DONE
--------------


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








