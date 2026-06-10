from trading_system.backtest import run_backtest
from trading_system.config import TradingConfig
from trading_system.market_data import load_price_data
from trading_system.strategies import MovingAverageCrossover


def test_backtest_runs_on_sample_data():
    data = load_price_data("examples/sample_prices.csv")
    strategy = MovingAverageCrossover(fast_window=3, slow_window=5)
    result = run_backtest(data, strategy, TradingConfig())

    assert result.final_equity > 0
    assert len(result.equity_curve) == len(data)
    assert "equity" in result.equity_curve.columns
