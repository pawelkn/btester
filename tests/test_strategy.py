
from btester import Strategy, Position, Trade
from math import nan
import pandas as pd
import unittest

class CustomStrategy(Strategy):
    def init(self):
        """ Implementation for initialization """

    def next(self, i, record):
        """ Implementation for the core strategy logic """

class TestStrategy(unittest.TestCase):

    def test_initial_states(self):
        strategy = CustomStrategy()
        pd.testing.assert_frame_equal(strategy.data, pd.DataFrame())
        self.assertIsNone(strategy.date)
        self.assertEqual(strategy.cash, 0)
        self.assertEqual(strategy.commission, 0)
        self.assertEqual(strategy.symbols, [])
        self.assertEqual(strategy.records, [])
        self.assertEqual(strategy.index, [])
        self.assertEqual(strategy.returns, [])
        self.assertEqual(strategy.trades, [])
        self.assertEqual(strategy.open_positions, [])
        self.assertEqual(strategy.cumulative_return, 0)
        self.assertEqual(strategy.assets_value, 0)

    # The init() method can be overridden by a subclass of Strategy
    def test_init_method_overridden(self):
        strategy = CustomStrategy()
        self.assertTrue(callable(strategy.init))

    # The next() method can be overridden by a subclass of Strategy
    def test_next_method_overridden(self):
        strategy = CustomStrategy()
        self.assertTrue(callable(strategy.next))

    # The open() method returns False if price or size is NaN or less than or equal to zero
    def test_open_returns_false_if_price_or_size_invalid(self):
        strategy = CustomStrategy()
        self.assertFalse(strategy.open(nan, 10))
        self.assertFalse(strategy.open(10, nan))
        self.assertFalse(strategy.open(0, 10))
        self.assertFalse(strategy.open(10, 0))
        self.assertEqual(strategy.open_positions, [])

    # The open() method returns False if there is not enough cash to cover the cost of the trade
    def test_open_returns_false_if_not_enough_cash(self):
        strategy = CustomStrategy()
        strategy.cash = 100
        self.assertFalse(strategy.open(10, 20))
        self.assertEqual(strategy.open_positions, [])

    # The open() method sets size to cash / price if size is none
    def test_open_sets_size_to_cash_divided_by_price_if_size_is_none(self):
        strategy = CustomStrategy()
        strategy.cash = 100

        self.assertTrue(strategy.open(10)) # open a new position
        self.assertEqual(strategy.cash, 0)
        self.assertEqual(strategy.trades, [])
        self.assertEqual(strategy.open_positions, [
            Position(symbol=None, open_date=None, last_date=None, open_price=10, last_price=10,
                     position_size=10.0, profit_loss=0.0, change_pct=0.0, current_value=100.0)
        ])
        self.assertEqual(strategy.assets_value, 100)

        self.assertTrue(strategy.close(20)) # close the position
        self.assertEqual(strategy.cash, 200)
        self.assertEqual(strategy.trades, [
            Trade(symbol=None, open_date=None, close_date=None, open_price=10, close_price=20,
                  position_size=10.0, profit_loss=100.0, change_pct=100.0, trade_commission=0.0,
                  cumulative_return=100.0)
        ])
        self.assertEqual(strategy.open_positions, [])
        self.assertEqual(strategy.assets_value, 0)

    # The close() method returns False if price is NaN or less than or equal to zero
    def test_close_returns_false_if_price_or_size_invalid(self):
        strategy = CustomStrategy()
        self.assertFalse(strategy.close(nan))
        self.assertFalse(strategy.close(0))
