import argparse

from trading_system.backtest import run_backtest
from trading_system.config import TradingConfig
from trading_system.market_data import load_price_data
from trading_system.strategies import MovingAverageCrossover


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trading system command line")
    subparsers = parser.add_subparsers(dest="command", required=True)

    backtest = subparsers.add_parser("backtest", help="Run a backtest from CSV price data")
    backtest.add_argument("--data", required=True, help="CSV file with timestamp and close columns")
    backtest.add_argument("--initial-cash", type=float, default=10_000.0)
    backtest.add_argument("--fast-window", type=int, default=3)
    backtest.add_argument("--slow-window", type=int, default=5)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "backtest":
        data = load_price_data(args.data)
        config = TradingConfig(initial_cash=args.initial_cash)
        strategy = MovingAverageCrossover(fast_window=args.fast_window, slow_window=args.slow_window)
        result = run_backtest(data, strategy, config)
        print(f"Final equity: {result.final_equity:.2f}")
        print(f"Total return: {result.total_return_fraction:.2%}")
        print(f"Trades: {len(result.trades)}")


if __name__ == "__main__":
    main()
