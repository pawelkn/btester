
from btester import Strategy
from math import nan, inf

import unittest

class CustomStrategy(Strategy):
    def init(self):
        """ Implementation for initialization """

    def next(self, i, record):
        """ Implementation for the core strategy logic """

class TestStrategy(unittest.TestCase):

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

    # The open() method returns False if there is not enough cash to cover the cost of the trade
    def test_open_returns_false_if_not_enough_cash(self):
        strategy = CustomStrategy()
        strategy.cash = 100
        self.assertFalse(strategy.open(10, 20))

    # The open() method sets size to cash / price if size is none
    def test_open_sets_size_to_cash_divided_by_price_if_size_is_none(self):
        strategy = CustomStrategy()
        strategy.cash = 100
        self.assertTrue(strategy.open(10, None))
        self.assertEqual(strategy.open_positions[0].position_size, 10)

    # The close() method returns False if price is NaN or less than or equal to zero
    def test_close_returns_false_if_price_or_size_invalid(self):
        strategy = CustomStrategy()
        self.assertFalse(strategy.close(nan))
        self.assertFalse(strategy.close(0))
