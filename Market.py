from Distributions import Distribution
from Firm import Firm
from numpy import mean
from Curves import Curve


class Market:
    def __init__(self,
                 N_firms: int,
                 tau: int,
                 price_dist: Distribution,
                 demand_curve: Curve,
                 obfuscation_dist: Distribution):
        self.price_dist = price_dist
        self.obfuscation_dist = obfuscation_dist
        self.demand_curve = demand_curve
        self.tau = tau
        self.firms = [Firm(
            price=price_dist.sample(),
            obfuscation_level=obfuscation_dist.sample())
            for _ in range(N_firms)]

    def compute_mean_obfuscation_level(self):
        return mean([f.obfuscation_level
                     for f in self.firms])
