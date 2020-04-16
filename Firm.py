class Firm:
    def __init__(self, price, obfuscation_level, cost=0.0):
        self.price = price
        self.obfuscation_level = obfuscation_level
        self.cost = cost
        self.sales = 0

    def get_profit(self) -> float:
        return self.sales * (self.price - self.cost)

    def sell(self) -> float:
        self.sales += 1
        return self.price
