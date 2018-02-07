
class Trader:


    def __init__(self,initial_capital,risk_ad):

        self.initial_capital = initial_capital
        self.position1 = []
        self.position2 = []
        self.value = [initial_capital]
        self.openZ=[]
        self.Zscore=[]
        self.beta=[]
        self.riskad=risk_ad