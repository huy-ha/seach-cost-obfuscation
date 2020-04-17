from __future__ import annotations
import numpy as np
from copy import copy
from Curves import Curve
from Market import Market
from scipy.integrate import quad


class Consumer:
    def __init__(self,
                 search_cost: Curve):
        self.p_0_firm = None  # Firm with lowest price so far
        self.t_0 = 0.0  # Total time searching so far
        self.search_cost = search_cost  # Search cost function g(t)
        self.search_count = 0  # Number of searches consumer does

    def compute_keep_search_benefit(self, market: Market):
        p_0 = self.get_lowest_price()
        demand_fn = market.demand_curve.get_fn()
        price_cfd = market.price_dist.get_cdf()
        def integrand(x): return demand_fn(x) * price_cfd(x)
        ans, err = quad(integrand,
                        market.price_dist.lower_bound,
                        p_0)
        return ans

    def compute_keep_search_cost(self,
                                 tau: float,
                                 t_mean: float):
        return self.search_cost(self.t_0 + tau + t_mean) \
            - self.search_cost(self.t_0)

    def get_final_search_cost(self):
        return self.search_cost(self.t_0)

    def get_lowest_price(self):
        return np.inf \
            if self.p_0_firm is None \
            else self.p_0_firm.price

    def should_keep_searching(self,
                              market: Market,
                              search_cost: float):
        return search_cost <\
            self.compute_keep_search_benefit(market=market)

    def play(self, market: Market):
        remaining_firms = copy(market.firms)
        # average obfuscation level
        t_mean = market.compute_mean_obfuscation_level()
        search_cost = self.compute_keep_search_cost(
            tau=market.tau, t_mean=t_mean)
        while self.should_keep_searching(
                market=market, search_cost=search_cost):
            firm = remaining_firms[
                np.random.choice(len(remaining_firms))]
            remaining_firms.remove(firm)
            if self.p_0_firm is None\
                    or self.p_0_firm.price > firm.price:
                self.p_0_firm = firm
            self.t_0 += (market.tau + firm.obfuscation_level)
            self.search_count += 1
            if len(remaining_firms) == 0:
                break
        # buy from firm offering lowerest price
        if self.p_0_firm is not None:
            self.p_0_firm.sell()
