from dataclasses import dataclass


@dataclass
class Portfolio:
    cash: float
    position: float = 0.0
    realized_pnl: float = 0.0

    def equity(self, price: float) -> float:
        return self.cash + self.position * price

    def buy(self, price: float, quantity: float, commission_rate: float) -> None:
        cost = price * quantity
        fee = cost * commission_rate
        total = cost + fee
        if total > self.cash:
            raise ValueError("Not enough cash to buy requested quantity")
        self.cash -= total
        self.position += quantity

    def sell_all(self, price: float, commission_rate: float) -> None:
        if self.position <= 0:
            return
        proceeds = price * self.position
        fee = proceeds * commission_rate
        self.cash += proceeds - fee
        self.position = 0.0
