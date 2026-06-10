import pandas as pd

from trading_system.config import TradingConfig
from trading_system.portfolio import Portfolio
from trading_system.risk import RiskManager
from trading_system.strategies import Signal, Strategy


def run_paper_session(data: pd.DataFrame, strategy: Strategy, config: TradingConfig) -> list[dict[str, object]]:
    portfolio = Portfolio(cash=config.initial_cash)
    risk = RiskManager(config)
    signals = strategy.generate(data)
    events: list[dict[str, object]] = []
    peak_equity = config.initial_cash

    for row, signal in zip(data.itertuples(index=False), signals, strict=True):
        price = float(row.close)
        equity = portfolio.equity(price)
        peak_equity = max(peak_equity, equity)
        event = {"timestamp": row.timestamp, "signal": signal, "equity": equity, "action": "none"}

        if signal == Signal.BUY.value and portfolio.position == 0 and risk.allows_new_entry(equity, peak_equity):
            quantity = risk.quantity_for_entry(portfolio.cash, price)
            portfolio.buy(price, quantity, config.commission_rate)
            event["action"] = "paper_buy"
            event["quantity"] = quantity
        elif signal == Signal.SELL.value and portfolio.position > 0:
            portfolio.sell_all(price, config.commission_rate)
            event["action"] = "paper_sell"

        events.append(event)

    return events
