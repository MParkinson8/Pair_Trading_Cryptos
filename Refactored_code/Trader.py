import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from DataHolder import DataHolder
from Plotter import Plotter

class Trader:


    def __init__(self,initial_capital):

        self.initial_capital = initial_capital
        self.position1 = []
        self.position2 = []
        self.value = []



