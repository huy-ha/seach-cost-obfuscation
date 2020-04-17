# seach-cost-obfuscation

## Usage

Requirements: python3.7, numpy, tqdm, scipy.

```
python main.py --config configs/default.json --name <name-of-experiment>
```

## TODO
 - [x] Finetune config
 - [ ] Support costless searchers
 - [ ] Compute Price Distribution + monopoly price from demand curve
 - [ ] Parallelization
 - [ ] Save results for plotting
 - [x] Allow consumers to not enter market
 - [x] Remove hardcode from Demand Curve (NegativeSigmoid)
 - [ ] Verify integral in `Consumer`
