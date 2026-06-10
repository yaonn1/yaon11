from dataclasses import dataclass
from enum import Enum

import pandas as pd


class Signal(str, Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class Strategy:
    name = "base"

    def generate(self, data: pd.DataFrame) -> pd.Series:
        raise NotImplementedError


@dataclass(frozen=True)
class MovingAverageCrossover(Strategy):
    fast_window: int = 3
    slow_window: int = 5
    name: str = "moving_average_crossover"

    def generate(self, data: pd.DataFrame) -> pd.Series:
        if self.fast_window >= self.slow_window:
            raise ValueError("fast_window must be smaller than slow_window")

        prices = data["close"]
        fast = prices.rolling(self.fast_window).mean()
        slow = prices.rolling(self.slow_window).mean()

        previous_fast = fast.shift(1)
        previous_slow = slow.shift(1)
        buy = (previous_fast <= previous_slow) & (fast > slow)
        sell = (previous_fast >= previous_slow) & (fast < slow)

        signals = pd.Series(Signal.HOLD.value, index=data.index)
        signals.loc[buy] = Signal.BUY.value
        signals.loc[sell] = Signal.SELL.value
        return signals
