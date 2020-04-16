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
    market = Market(
        tau=config['tau'],
        N_firms=config['N_firms'],
        price_dist=create_distribution(config['price_dist']),
        obfuscation_dist=create_distribution(config['obfuscation_dist']),
        demand_curve=create_curve(config['demand']))

    config['search_cost']['upper_bound'] = np.inf
    search_cost = create_curve(config['search_cost'])
    consumer = [Consumer(search_cost=search_cost)
                for _ in range(config['N_consumers'])]
    return consumer, market, config['tau']
