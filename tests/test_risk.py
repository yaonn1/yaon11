from trading_system.config import TradingConfig
from trading_system.risk import RiskManager


def test_position_size_uses_configured_fraction():
    risk = RiskManager(TradingConfig(max_position_fraction=0.25))

    assert risk.quantity_for_entry(cash=1_000, price=100) == 2.5


def test_drawdown_limit_blocks_new_entries():
    risk = RiskManager(TradingConfig(max_drawdown_fraction=0.1))

    assert risk.allows_new_entry(current_equity=950, peak_equity=1_000)
    assert not risk.allows_new_entry(current_equity=850, peak_equity=1_000)
