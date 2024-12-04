# Monte Carlo Simulator

## Metadata
**Author:** Robert Clay Harris  
**Project Name:** Monte Carlo Simulator

## Synopsis
This project simulates rolling dice, playing games with those dice, and analyzing the results.

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

### Playing a Game

```python
from game import Game

dice = [Die(faces), Die(faces)]
game = Game(dice)
game.play(10)
print(game.show('wide'))
```

### Analyzing a Game

```python
from analyzer import Analyzer

analyzer = Analyzer(game)
print(analyzer.jackpot())
print(analyzer.face_counts_per_roll())
print(analyzer.combo_count())
print(analyzer.permutation_count())
```

## API Description

### Die Class

```python
class Die:
    """
    Represents a single die with customizable faces and weights.
    """
    def __init__(self, faces: np.ndarray):
        """
        Initializes the Die object with faces and equal weights.
        
        Parameters:
        faces (np.ndarray): A NumPy array of unique face values (strings or numbers).
        
        Raises:
        TypeError: If `faces` is not a NumPy array.
        ValueError: If the values in `faces` are not unique.
        """
    def change_weight(self, face, new_weight):
        """
        Changes the weight of a specified face.
        
        Parameters:
        face (int or str): The face value whose weight is to be changed.
        new_weight (int or float): The new weight to be assigned to the face.
        
        Raises:
        IndexError: If the face value is not found in the die faces.
        TypeError: If the new weight is not a non-negative number.
        """
    def roll(self, num_rolls=1):
        """
        Rolls the die one or more times.
        
        Parameters:
        num_rolls (int): The number of times to roll the die. Defaults to 1.
        
        Returns:
        list: A list of outcomes from the rolls.
        """
    def show(self):
        """
        Shows the current state of the die.
        
        Returns:
        pd.DataFrame: A copy of the die's faces and weights.
        """
```

### Game Class

```python
class Game:
    """
    Represents a game consisting of rolling one or more similar dice (Die objects) one or more times.
    """
    def __init__(self, dice: list):
        """
        Initializes the Game object with a list of Die objects.
        
        Parameters:
        dice (list): A list of Die objects.
        
        Raises:
        TypeError: If the list does not contain Die objects.
        """
    def play(self, n_rolls: int):
        """
        Rolls all dice in the game for a specified number of times.
        
        Parameters:
        n_rolls (int): The number of times to roll the dice.
        
        Saves:
        A private data frame with the results of the rolls in wide format.
        """
    def show(self, form='wide'):
        """
        Shows the results of the most recent play.
        
        Parameters:
        form (str): The format of the returned data frame, either 'wide' or 'narrow'. Defaults to 'wide'.
        
        Returns:
        pd.DataFrame: A copy of the play results in the specified format.
        
        Raises:
        ValueError: If the form parameter is not 'wide' or 'narrow'.
        """
```

### Analyzer Class

```python
class Analyzer:
    """
    An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it.
    """
    def __init__(self, game):
        """
        Initializes the Analyzer object with a Game object.
        
        Parameters:
        game (Game): A Game object.
        
        Raises:
        ValueError: If the input is not a Game object.
        """
    def jackpot(self):
        """
        Counts how many jackpots occurred in the game.
        
        Returns:
        int: The number of jackpots.
        """
    def face_counts_per_roll(self):
        """
        Computes the count of each face value per roll.
        
        Returns:
        pd.DataFrame: A DataFrame with roll numbers as rows, face values as columns, and counts as values.
        """
    def combo_count(self):
        """
        Computes the distinct combinations of faces rolled, along with their counts.
        
        Combinations are order-independent and may contain repetitions.
        
        Returns:
        pd.DataFrame: A DataFrame with a MultiIndex of distinct combinations and a column for the associated counts.
        """
    def permutation_count(self):
        """
        Computes the distinct permutations of faces rolled, along with their counts.
        
        Permutations are order-dependent and may contain repetitions.
        
        Returns:
        pd.DataFrame: A DataFrame with a MultiIndex of distinct permutations and a column for the associated counts.
        """
```