from btester import Trade, Position, Strategy, Backtest
import pandas as pd

import unittest

SINGLE_ASSET_DATA = pd.DataFrame(
    index=['2023-10-18', '2023-10-19', '2023-10-20'],
    data={
        'Open': [100.0, 200.0, 300.0],
        'High': [100.0, 200.0, 300.0],
        'Low': [100.0, 200.0, 300.0],
        'Close': [100.0, 200.0, 300.0],
        'Volume': [2000000, 2500000, 3000000]
    }
)

MULTIPLE_ASSETS_DATA = pd.DataFrame(
    index=['2023-10-18', '2023-10-19', '2023-10-20'],
    data={
        ('AAA','Open'): [100.0, 200.0, 300.0],
        ('AAA','High'): [100.0, 200.0, 300.0],
        ('AAA','Low'): [100.0, 200.0, 300.0],
        ('AAA','Close'): [100.0, 200.0, 300.0],
        ('AAA','Volume'): [2000000, 2500000, 3000000],
        ('BBB','Open'): [2850.0, 2835.0, 2820.0],
        ('BBB','High'): [2860.0, 2835.0, 2825.0],
        ('BBB','Low'): [2840.0, 2805.0, 2800.0],
        ('BBB','Close'): [2840.0, 2815.0, 2810.0],
        ('BBB','Volume'): [1500000, 1700000, 1600000]
    }
)

class SingleAssetStrategy(Strategy):
    def init(self):
        pass

    def next(self, i, record):
        if i == 0:
            self.open(price=record['Open'])
        if i == 2:
            self.close(price=record['Open'])

class MultipleAssetsStrategy(Strategy):
    def init(self):
        pass

    def next(self, i, record):
        if i == 0:
            self.open(symbol='AAA', price=record[('AAA','Open')], size=10)
        if i == 1:
            self.open(symbol='BBB', price=record[('BBB','Open')], size=1)
        if i == 2:
            self.close(symbol='AAA', price=record[('AAA','Open')])

class TestBacktest(unittest.TestCase):

    def test_backtest_single_asset(self):
        bt = Backtest(strategy=SingleAssetStrategy, data=SINGLE_ASSET_DATA, cash=10000.0, commission=0.01)
        result = bt.run()

        returns = pd.Series(index=SINGLE_ASSET_DATA.index, data=[9900.990099009901, 19801.980198019803, 29405.940594059408])

        trades = [Trade(symbol=None, open_date='2023-10-18', close_date='2023-10-20', open_price=100.0,
            close_price=300.0, position_size=99.00990099009901, profit_loss=19801.980198019803, change_pct=200.0,
            trade_commission=396.03960396039605, cumulative_return=29405.940594059408)]

        open_positions = []

        pd.testing.assert_series_equal(result.returns, returns)
        self.assertEqual(result.trades, trades)
        self.assertEqual(result.open_positions, open_positions)


    def test_backtest_multiple_assets(self):
        bt = Backtest(strategy=MultipleAssetsStrategy, data=MULTIPLE_ASSETS_DATA, cash=10000.0, commission=0.01)
        result = bt.run()

        returns = pd.Series(index=MULTIPLE_ASSETS_DATA.index, data=[9990.0, 10941.65, 11906.65])

        trades = [Trade(symbol='AAA', open_date='2023-10-18', close_date='2023-10-20', open_price=100.0,
            close_price=300.0, position_size=10, profit_loss=2000.0, change_pct=200.0,
            trade_commission=40.0, cumulative_return=11960.0)]

        open_positions = [Position(symbol='BBB', open_date='2023-10-19', last_date='2023-10-20', open_price=2835.0,
            last_price=2810.0, position_size=1, profit_loss=-25.0, change_pct=-0.881834215167554,
            current_value=2810.0)]

        pd.testing.assert_series_equal(result.returns, returns)
        self.assertEqual(result.trades, trades)
        self.assertEqual(result.open_positions, open_positions)
