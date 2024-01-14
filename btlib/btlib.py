from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Type, Hashable, Optional
from math import nan, isnan
import pandas as pd

@dataclass
class Position:
    symbol: Optional[str] = None
    open_date: Optional[datetime] = None
    last_date: Optional[datetime] = None
    open_price: float = nan
    last_price: float = nan
    position_size: float = nan
    profit_loss: float = nan
    change_pct: float = nan
    current_value: float = nan

    def update(self, last_date: datetime, last_price: float):
        self.last_date = last_date
        self.last_price = last_price
        self.profit_loss = (self.last_price - self.open_price) * self.position_size
        self.change_pct = (self.last_price / self.open_price - 1) * 100
        self.current_value = self.open_price * self.position_size + self.profit_loss

@dataclass
class Trade:
    symbol: Optional[str] = None
    open_date: Optional[datetime] = None
    close_date: Optional[datetime] = None
    open_price: float = nan
    close_price: float = nan
    position_size: float = nan
    profit_loss: float = nan
    change_pct: float = nan
    trade_commission: float = nan
    cumulative_return: float = nan

@dataclass
class Result:
    returns: pd.Series
    trades: List[Trade]
    open_positions: List[Position]

class Strategy(ABC):

    @abstractmethod
    def init(self):
        """ Abstract method for initializing resources for the strategy """

    @abstractmethod
    def next(self, i: int, record: Dict[Hashable, Any]):
        """ Abstract method defining the core functionality of the strategy """

    def __init__(self):
        self.data = pd.DataFrame()
        self.date = None
        self.cash = .0
        self.commission = .0

        self.symbols: List[str] = []

        self.records: List[Dict[Hashable, Any]] = []
        self.index: List[datetime] = []

        self.returns: List[float] = []
        self.trades: List[Trade] = []
        self.open_positions: List[Position] = []

        self.cumulative_return = self.cash
        self.cash_stock_value = .0

    def open(self, price: float, size: Optional[float] = None, symbol: Optional[str] = None):
        if isnan(price) or price <= 0 or (size is not None and (isnan(size) or size <= .0)):
            return False

        if size is None:
            size = self.cash / (price * (1 + self.commission))
            open_cost = self.cash
        else:
            open_cost = size * price * (1 + self.commission)

        if isnan(size) or size <= .0 or self.cash < open_cost:
            return False

        position = Position(symbol=symbol, open_date=self.date, open_price=price, position_size=size)
        position.update(last_date=self.date, last_price=price)

        self.cash_stock_value += position.current_value
        self.cash -= open_cost

        self.open_positions.extend([position])
        return True

    def close(self, price: float, symbol: Optional[str] = None, position: Optional[Position] = None):
        if isnan(price) or price <= 0:
            return False

        if position is None:
            for position in self.open_positions[:]:
                if position.symbol == symbol:
                    self.close(position=position, price=price)
        else:
            self.cash_stock_value -= position.current_value
            position.update(last_date=self.date, last_price=price)

            trade_commission = (position.open_price + position.last_price) * position.position_size * self.commission
            self.cumulative_return += position.profit_loss - trade_commission

            trade = Trade(position.symbol, position.open_date, position.last_date, position.open_price,
                position.last_price, position.position_size, position.profit_loss, position.change_pct,
                trade_commission, self.cumulative_return)

            self.trades.extend([trade])
            self.open_positions.remove(position)

            close_cost = position.last_price * position.position_size * self.commission
            self.cash += position.current_value - close_cost

        return True

    def _eval(self, *args, **kwargs):
        self.cumulative_return = self.cash
        self.cash_stock_value = .0

        self.init(*args, **kwargs)

        for i, record in enumerate(self.records):
            self.date = self.index[i]

            self.next(i, record)

            for position in self.open_positions:
                last_price = record[(position.symbol, 'Close')] if (position.symbol, 'Close') in record else record['Close']
                if last_price > 0:
                    position.update(last_date=self.date, last_price=last_price)

            self.cash_stock_value = sum(position.current_value for position in self.open_positions)
            self.returns.append(self.cash + self.cash_stock_value)

        return Result(
            returns=pd.Series(index=self.index, data=self.returns, dtype=float),
            trades=self.trades,
            open_positions=self.open_positions
        )

class Backtest:

    def __init__(self,
                 strategy: Type[Strategy],
                 data: pd.DataFrame,
                 cash: float = 10_000,
                 commission: float = .0
                 ):

        self.strategy = strategy
        self.data = data
        self.cash = cash
        self.commission = commission

        columns = data.columns
        self.symbols = columns.get_level_values(0).unique().tolist() if isinstance(columns, pd.MultiIndex) else []

        self.records = data.to_dict('records')
        self.index = data.index.tolist()

    def run(self, *args, **kwargs):
        strategy = self.strategy()
        strategy.data = self.data
        strategy.cash = self.cash
        strategy.commission = self.commission

        strategy.symbols = self.symbols
        strategy.records = self.records
        strategy.index = self.index

        return strategy._eval(*args, **kwargs)