from dataclasses import dataclass


@dataclass(frozen=True)
class TradingConfig:
    initial_cash: float = 10_000.0
    max_position_fraction: float = 0.25
    max_drawdown_fraction: float = 0.2
    commission_rate: float = 0.001
