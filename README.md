# Trading System

A maintainable Python trading-system starter project focused on safe iteration:

- market data loading from CSV files
- simple strategy interface
- moving-average crossover example strategy
- risk controls for position sizing and drawdown limits
- backtesting engine
- paper-trading simulation loop
- CLI entry point
- basic tests

This project is intentionally built around backtesting and paper trading first. Real-money exchange integration should only be added after strategy behavior, logging, and risk controls are well tested.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
python -m trading_system.cli backtest --data examples/sample_prices.csv
pytest
```

## Project Structure

```text
trading_system/
  backtest.py        Backtesting engine
  cli.py             Command-line entry point
  config.py          Runtime configuration
  market_data.py     CSV market data loading
  paper.py           Paper-trading simulation
  portfolio.py       Cash, position, and equity accounting
  risk.py            Risk checks and position sizing
  strategies.py      Strategy interface and examples
examples/
  sample_prices.csv  Small sample data file
scripts/
  run_backtest.ps1   Convenience launcher
```

## Roadmap

1. Add more strategy examples.
2. Add richer performance reports.
3. Add persistent logs and trade journals.
4. Add exchange connectors only for paper trading first.
5. Add real trading only after explicit risk review.

## Safety Note

This software is for education, research, and simulation. It is not financial advice and does not guarantee profit.