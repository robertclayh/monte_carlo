import numpy as np
import pandas as pd

class Die:
    """
    Represents a single die with customizable faces and weights.
    
    A die can be initialized with a set of faces, each having a default 
    weight of 1.0. Users can modify the weights and roll the die to generate 
    random outcomes based on these weights.
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
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces must be a NumPy array.")
        if len(faces) != len(set(faces)):
            raise ValueError("Faces must contain unique values.")
        
        self._df = pd.DataFrame({
            'face': faces,
            'weight': np.ones(len(faces))
        }).set_index('face')

    def change_weight(self, face, new_weight):
        """
        Changes the weight of a specified face.
        
        Parameters:
        face: The face value whose weight is to be changed.
        new_weight: The new weight to be assigned to the face.
        
        Raises:
        IndexError: If the face value is not found in the die faces.
        TypeError: If the new weight is not a non-negative number.
        """
        if face not in self._df.index:
            raise IndexError("Face value not found in die faces.")
        if not isinstance(new_weight, (int, float)) or new_weight < 0:
            raise TypeError("Weight must be a non-negative number.")
        
        self._df.at[face, 'weight'] = new_weight

    def roll(self, num_rolls=1):
        """
        Rolls the die one or more times.
        
        Parameters:
        num_rolls (int): The number of times to roll the die. Defaults to 1.
        
        Returns:
        list: A list of outcomes from the rolls.
        """
        return self._df.sample(n=num_rolls, weights='weight', replace=True).index.tolist()

    def show(self):
        """
        Shows the current state of the die.
        
        Returns:
        pd.DataFrame: A copy of the die's faces and weights.
        """
        return self._df.copy()
    
class Game:
    """
    Represents a game consisting of rolling one or more dice (Die objects) one or more times.
    """
    def __init__(self, dice: list):
        """
        Initializes the Game object with a list of Die objects.
        
        Parameters:
        dice (list): A list of Die objects.
        
        Raises:
        TypeError: If the list does not contain Die objects.
        """
        if not all(hasattr(die, 'roll') for die in dice):
            raise TypeError("All items in the list must be Die objects.")
        
        self.dice = dice
        self._play_results = None

    def play(self, n_rolls: int):
        """
        Rolls all dice in the game for a specified number of times.
        
        Parameters:
        n_rolls (int): The number of times to roll the dice.
        
        Saves:
        A private data frame with the results of the rolls in wide format.
        """
        if n_rolls <= 0:
            raise ValueError("Number of rolls must be a positive integer.")
        
        # Roll each die and collect results
        results = {die_idx: die.roll(n_rolls) for die_idx, die in enumerate(self.dice)}
        
        # Create DataFrame in wide format
        self._play_results = pd.DataFrame(results)
        self._play_results.index.name = 'Roll'

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
        if self._play_results is None:
            raise ValueError("No play results to show. Please play the game first.")
        
        if form == 'wide':
            return self._play_results.copy()
        elif form == 'narrow':
            return self._play_results.stack().to_frame('Outcome').rename_axis(index=['Roll', 'Die'])
        else:
            raise ValueError("Invalid form. Please choose 'wide' or 'narrow'.")
        
class Analyzer:
    """
    An Analyzer object takes the results of a single game (Game object) and computes various descriptive statistical properties about it.
    """
    def __init__(self, game):
        """
        Initializes the Analyzer object with a Game object.
        
        Parameters:
        game (Game): A Game object.
        
        Raises:
        ValueError: If the input is not a Game object.
        """
        if not hasattr(game, 'show'):
            raise ValueError("The input must be a Game object.")
        
        self.game = game
        self.results = game.show('wide')

    def jackpot(self):
        """
        Counts how many jackpots occurred in the game.
        
        Returns:
        int: The number of jackpots.
        """
        return int((self.results.nunique(axis=1) == 1).sum())

    def face_counts_per_roll(self):
        """
        Computes the count of each face value per roll.
        
        Returns:
        pd.DataFrame: A DataFrame with roll numbers as rows, face values as columns, and counts as values.
        """
        return self.results.apply(pd.Series.value_counts, axis=1).fillna(0).astype(int)

    def combo_count(self):
        """
        Computes the distinct combinations of faces rolled, along with their counts.
        
        Combinations are order-independent and may contain repetitions.
        
        Returns:
        pd.DataFrame: A DataFrame with a MultiIndex of distinct combinations and a column for the associated counts.
        """
        combos = self.results.apply(lambda row: tuple(sorted(row)), axis=1)
        combo_counts = combos.value_counts().reset_index()
        combo_counts.columns = ['Combination', 'Count']
        combo_counts.set_index('Combination', inplace=True)
        return combo_counts

    def permutation_count(self):
        """
        Computes the distinct permutations of faces rolled, along with their counts.
        
        Permutations are order-dependent and may contain repetitions.
        
        Returns:
        pd.DataFrame: A DataFrame with a MultiIndex of distinct permutations and a column for the associated counts.
        """
        perms = self.results.apply(lambda row: tuple(row), axis=1)
        perm_counts = perms.value_counts().reset_index()
        perm_counts.columns = ['Permutation', 'Count']
        perm_counts.set_index('Permutation', inplace=True)
        return perm_counts