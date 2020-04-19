from os.path import (
    basename, dirname, splitext, exists
)
from json import load
from copy import deepcopy
import numpy as np
from Distributions import create_distribution
from Curves import create_curve
from Consumer import Consumer
from Market import Market
from time import time
from tqdm import tqdm
from matplotlib import pyplot as plt


def run_simulation(
        create_consumers_fn,
        create_market_fn,
        use_tqdm=True) -> dict:
    consumers = create_consumers_fn()
    market = create_market_fn()
    start = time()

    consumers_iter = consumers
    if use_tqdm:
        consumers_iter = tqdm(consumers, desc='Consumers playing')

    for c in consumers_iter:
        c.play(market=market)
    print("[Main] run_simulation() took {:.2f}s".format(float(time() - start)))
    return {
        'firm_profits': [f.get_profit() for f in market.firms],
        'firm_prices': [f.price for f in market.firms],
        'consumer_search_costs': [c.get_final_search_cost()
                                  for c in consumers],
        'consumer_prices': [c.get_lowest_price() for c in consumers],
        'consumer_search_count': [c.search_count for c in consumers]
    }


def merge(a: dict, b: dict):
    """
    merges two dictionaries
    """
    if isinstance(b, dict) and isinstance(a, dict):
        a_and_b = a.keys() & b.keys()
        every_key = a.keys() | b.keys()
        return {k: merge(a[k], b[k]) if k in a_and_b else
                deepcopy(a[k] if k in a else b[k]) for k in every_key}
    return deepcopy(b)


def load_config(path: str, merge_with_default=True):
    base_dirname = basename(dirname(path))
    merge_with_default = (base_dirname == 'configs')

    if splitext(basename(path))[0] != 'default'\
            and merge_with_default:
        config = load(open(dirname(path) + '/default.json'))
        additional_config = load(open(path))
        config = merge(config, additional_config)
    else:
        config = load(open(path))
    return config


def setup(args):
    config = load_config(args.config)
    np.random.seed(args.seed)
    if exists(args.name):
        print(f"[Setup] {args.name} already exists.",
              " Please specify another --name.")
        exit()

    def create_market(obfuscation_dist=None):
        return Market(
            tau=config['tau'],
            N_firms=config['N_firms'],
            price_dist=create_distribution(config['price_dist']),
            obfuscation_dist=create_distribution(config['obfuscation_dist'])
            if obfuscation_dist is None else obfuscation_dist,
            demand_curve=create_curve(config['demand']))

    config['search_cost']['upper_bound'] = np.inf
    search_cost = create_curve(config['search_cost'])

    def create_consumers():
        return [Consumer(search_cost=search_cost)
                for _ in range(config['N_consumers'])]

    return create_consumers, create_market


def plot_result(x, y, x_label, y_label):
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
