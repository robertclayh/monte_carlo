# Monte Carlo Simulator

## Metadata
**Author:** Robert Clay Harris  
**Project Name:** Monte Carlo Simulator

## Synopsis
This project simulates rolling dice, playing games with those dice, and analyzing the results.

### Installation
To install the required packages, run:

```bash
pip install -r requirements.txt
```

## Usage

### Creating Dice

```python
import numpy as np
from die import Die

faces = np.array([1, 2, 3, 4, 5, 6])
die = Die(faces)
die.change_weight(1, 2.0)
print(die.roll(10))
```