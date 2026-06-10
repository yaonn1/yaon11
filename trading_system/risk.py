from dataclasses import dataclass

from trading_system.config import TradingConfig


@dataclass(frozen=True)
class RiskManager:
    config: TradingConfig

    def quantity_for_entry(self, cash: float, price: float) -> float:
        budget = cash * self.config.max_position_fraction
        if price <= 0:
            raise ValueError("price must be positive")
        return budget / price

    def allows_new_entry(self, current_equity: float, peak_equity: float) -> bool:
        if peak_equity <= 0:
            return True
        drawdown = (peak_equity - current_equity) / peak_equity
        return drawdown <= self.config.max_drawdown_fraction
