from numpy.random import normal
from typing import Callable
from scipy.stats import norm as scipy_norm


class Distribution:
    def __init__(self):
        pass

    def sample(self) -> float:
        raise NotImplementedError

    def get_cdf(self) -> Callable:
        raise NotImplementedError


class Normal(Distribution):
    def __init__(self, mu, sigma, lower_bound=None):
        self.mu = mu
        self.sigma = sigma
        self.lower_bound = lower_bound
        super().__init__()

    def sample(self) -> float:
        retval = normal(self.mu, self.sigma)
        if self.lower_bound is not None:
            retval = max(self.lower_bound, retval)
        return retval

    def get_cdf(self) -> Callable:
        return lambda x:\
            scipy_norm.cdf((x - self.mu) / self.sigma)


def create_distribution(dist_config: dict) -> Distribution:
    dist_type = dist_config['type']
    del dist_config['type']
    if dist_type == 'normal':
        return Normal(**dist_config)
    else:
        print("[Distributions] Unsupported distribution:",
              dist_type)
        exit()
