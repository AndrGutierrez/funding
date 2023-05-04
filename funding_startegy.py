import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

def parse_funding_rate(x):
    return float(x.strip('%'))
class FundingRateStrategy(Strategy):
    funding_rate_low = -0.00075  # Define el límite inferior de Funding Rate para comprar
    funding_rate_high = 0.00075   # Define el límite superior de Funding Rate para vender

    def init(self):
        # Prepara el indicador de Funding Rate
        self.funding_rate = self.I(lambda x: x, self.data['Funding rate'])
    
    def next(self):
        if self.funding_rate[-1] < self.funding_rate_low:
            # Compra si el Funding Rate es menor al límite inferior y no hay una posición abierta
            self.buy()
        
        elif self.funding_rate[-1] > self.funding_rate_high:
            # Vende si el Funding Rate es mayor al límite superior y hay una posición abierta
            self.sell()

data = pd.read_csv('./data/merged_funding_binance.csv', parse_dates=['datetime'], index_col='datetime',  converters={'Funding Rate': parse_funding_rate})
data.columns= [column.capitalize() for column in data.columns]
bt = Backtest(data, FundingRateStrategy, cash=100000, commission=.002)
optimization_results = bt.optimize(
    funding_rate_low=(0.00005, 0.001, 0.00005),
    funding_rate_high=(0.005, 0.02, 0.001),
    maximize='Equity Final [$]',
    # constraint=lambda p: p.funding_rate_low < p.funding_rate_high,
    # n_jobs=-1
)
print(optimization_results)
bt.plot()
