from argparse import ArgumentParser
from utils import setup, run_simulation, plot_result
from numpy import mean, max, min
from Distributions import create_distribution
import ray


def simulate(args):
    # Default simulation
    results = run_simulation(*setup(args))
    for result_key in results:
        print(result_key)
        print(f"\tmean: {mean(results[result_key])}")
        print(f"\tmax: {max(results[result_key])}")
        print(f"\tmin: {min(results[result_key])}")


def obfuscate(args):
    # How market is affected by increasing obfuscation levels
    create_consumers_fn, create_market_fn = setup(args)
    ray.init()
    @ray.remote(num_cpus=1)
    def remote_simulate(consumer_fn, market_fn):
        return run_simulation(
            consumer_fn,
            market_fn,
            use_tqdm=False)
    obfuscation_mus = [i * 0.2 for i in range(40)]
    results = ray.get([remote_simulate.remote(
        create_consumers_fn,
        lambda: create_market_fn(
            obfuscation_dist=create_distribution({
                'type': 'normal',
                'mu': obsfuscation_mu,
                'sigma': 0.5,
                'lower_bound': 0.0
            })))
        for obsfuscation_mu in obfuscation_mus])
    for result_key in [
        'firm_profits',
        'consumer_search_costs',
        'consumer_search_count',
            'consumer_prices']:
        result = [mean(r[result_key]) for r in results]
        plot_result(x=obfuscation_mus,
                    y=result,
                    x_label='obfuscation_level',
                    y_label=result_key)


if __name__ == "__main__":
    parser = ArgumentParser(
        "A Search Cost Model for Obfuscation in Oligopolistic Markets")
    parser.add_argument("--config", required=True, type=str,
                        help="path of JSON config file.")
    parser.add_argument("--name", required=True, type=str,
                        help="name of experiment.")
    parser.add_argument("--seed", default=0, type=int,
                        help="seed for PRNG.")
    parser.add_argument("--task",
                        choices=[
                            'simulate',
                            'obfuscate'
                        ],
                        default='simulate',
                        help="seed for PRNG.")
    args = parser.parse_args()
    if args.task == 'simulate':
        simulate(args)
    elif args.task == 'obfuscate':
        obfuscate(args)
