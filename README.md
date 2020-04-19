# seach-cost-obfuscation

## Usage

Requirements: python3.7, numpy, tqdm, scipy.

To run a basic simulation
```
python main.py --config configs/default.json --name <name-of-experiment>
```

To generate graphs with increasing levels of obfuscation
```
python main.py --task obfuscate --config configs/default.json --name <name-of-experiment>
```

## TODO
 - [x] Finetune config
 - [ ] Support costless searchers
 - [ ] Compute Price Distribution + monopoly price from demand curve
 - [ ] Parallelization
 - [ ] Plot min and max as well as mean in `plot_result()`
 - [x] Save results for plotting
 - [x] Allow consumers to not enter market
 - [x] Remove hardcode from Demand Curve (NegativeSigmoid)
 - [ ] Verify integral in `Consumer`
