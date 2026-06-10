from dataclasses import dataclass

import pandas as pd

from trading_system.config import TradingConfig
from trading_system.portfolio import Portfolio
from trading_system.risk import RiskManager
from trading_system.strategies import Signal, Strategy


@dataclass(frozen=True)
class BacktestResult:
    trades: pd.DataFrame
    equity_curve: pd.DataFrame
    final_equity: float
    total_return_fraction: float


def run_backtest(data: pd.DataFrame, strategy: Strategy, config: TradingConfig) -> BacktestResult:
    portfolio = Portfolio(cash=config.initial_cash)
    risk = RiskManager(config)
    signals = strategy.generate(data)
    trades: list[dict[str, object]] = []
    equity_rows: list[dict[str, object]] = []
    peak_equity = config.initial_cash

    for row, signal in zip(data.itertuples(index=False), signals, strict=True):
        price = float(row.close)
        timestamp = row.timestamp
        current_equity = portfolio.equity(price)
        peak_equity = max(peak_equity, current_equity)

        if signal == Signal.BUY.value and portfolio.position == 0:
            if risk.allows_new_entry(current_equity, peak_equity):
                quantity = risk.quantity_for_entry(portfolio.cash, price)
                portfolio.buy(price, quantity, config.commission_rate)
                trades.append({"timestamp": timestamp, "side": "buy", "price": price, "quantity": quantity})
        elif signal == Signal.SELL.value and portfolio.position > 0:
            quantity = portfolio.position
            portfolio.sell_all(price, config.commission_rate)
            trades.append({"timestamp": timestamp, "side": "sell", "price": price, "quantity": quantity})

        equity_rows.append({"timestamp": timestamp, "equity": portfolio.equity(price), "cash": portfolio.cash, "position": portfolio.position})

    final_price = float(data.iloc[-1]["close"])
    final_equity = portfolio.equity(final_price)
    return BacktestResult(
        trades=pd.DataFrame(trades),
        equity_curve=pd.DataFrame(equity_rows),
        final_equity=final_equity,
        total_return_fraction=(final_equity / config.initial_cash) - 1,
    )
