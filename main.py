from argparse import ArgumentParser
from typing import List
from utils import setup
from Consumer import Consumer
from Market import Market
from numpy import mean, max, min
from tqdm import tqdm


def run_simulation(
        consumers: List[Consumer],
        market: Market,
        tau: float) -> dict:
    for c in tqdm(consumers, desc='Consumers playing...'):
        c.play(market=market)
    return {
        'firm_profits': [f.get_profit() for f in market.firms],
        'firm_prices': [f.price for f in market.firms],
        'consumer_search_costs': [c.get_final_search_cost() for c in consumers],
        'consumer_prices': [c.get_lowest_price() for c in consumers],
        'consumer_search_count': [c.search_count for c in consumers]
    }


if __name__ == "__main__":
    parser = ArgumentParser(
        "A Search Cost Model for Obfuscation in Oligopolistic Markets")
    parser.add_argument("--config", required=True, type=str,
                        help="path of JSON config file.")
    parser.add_argument("--name", required=True, type=str,
                        help="name of experiment.")
    parser.add_argument("--seed", default=0, type=int,
                        help="seed for PRNG.")
    args = parser.parse_args()
    results = run_simulation(*setup(args))
    for result_key in results:
        print(result_key)
        print(f"\tmean: {mean(results[result_key])}")
        print(f"\tmax: {max(results[result_key])}")
        print(f"\tmin: {min(results[result_key])}")
