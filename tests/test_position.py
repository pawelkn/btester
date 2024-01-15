from btester import Position
from datetime import datetime
import math

import unittest

class TestPosition(unittest.TestCase):

    # Creating a Position object with default values
    def test_create_position_with_default_values(self):
        position = Position()
        self.assertIsNone(position.symbol)
        self.assertIsNone(position.open_date)
        self.assertIsNone(position.last_date)
        self.assertTrue(math.isnan(position.open_price))
        self.assertTrue(math.isnan(position.last_price))
        self.assertTrue(math.isnan(position.position_size))
        self.assertTrue(math.isnan(position.profit_loss))
        self.assertTrue(math.isnan(position.change_pct))
        self.assertTrue(math.isnan(position.current_value))

    # Creating a Position object with all values set
    def test_create_position_with_all_values_set(self):
        symbol = 'AAPL'
        open_date = datetime(2021, 1, 1)
        last_date = datetime(2021, 1, 2)
        open_price = 100.0
        last_price = 110.0
        position_size = 10.0
        profit_loss = 100.0
        change_pct = 10.0
        current_value = 1100.0

        position = Position(symbol=symbol, open_date=open_date, last_date=last_date, open_price=open_price,
                            last_price=last_price, position_size=position_size, profit_loss=profit_loss,
                            change_pct=change_pct, current_value=current_value)

        self.assertEqual(position.symbol, symbol)
        self.assertEqual(position.open_date, open_date)
        self.assertEqual(position.last_date, last_date)
        self.assertEqual(position.open_price, open_price)
        self.assertEqual(position.last_price, last_price)
        self.assertEqual(position.position_size, position_size)
        self.assertEqual(position.profit_loss, profit_loss)
        self.assertEqual(position.change_pct, change_pct)
        self.assertEqual(position.current_value, current_value)

    # Updating a Position object with valid values
    def test_update_position_with_valid_values(self):
        symbol = 'AAPL'
        open_date = datetime(2021, 1, 1)
        open_price = 100.0
        position_size = 10.0

        position = Position(symbol=symbol, open_date=open_date, open_price=open_price, position_size=position_size)

        last_date = datetime(2021, 1, 2)
        last_price = 150.0

        position.update(last_date=last_date, last_price=last_price)

        self.assertEqual(position.last_date, last_date)
        self.assertEqual(position.last_price, last_price)
        self.assertAlmostEqual(position.profit_loss, 500.0)
        self.assertAlmostEqual(position.change_pct, 50.0)
        self.assertAlmostEqual(position.current_value, 1500.0)
