import pandas as pd
from itertools import combinations_with_replacement, permutations

class Analyzer:
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
        return (self.results.nunique(axis=1) == 1).sum()

    def face_counts_per_roll(self):
        """
        Computes the count of each face value per roll.
        
        Returns:
        pd.DataFrame: A DataFrame with roll numbers as rows, face values as columns, and counts as values.
        """
        return self.results.apply(pd.Series.value_counts, axis=1).fillna(0).astype(int)

    def combo_count(self):
        """
        Computes the distinct combinations of faces rolled and their counts.
        
        Returns:
        pd.DataFrame: A DataFrame with a MultiIndex of combinations and a column for counts.
        """
        sorted_rolls = self.results.apply(sorted, axis=1)
        combinations = sorted_rolls.apply(tuple)
        combo_counts = combinations.value_counts().reset_index()
        combo_counts.columns = ['Combination', 'Count']
        return combo_counts.set_index('Combination')

    def permutation_count(self):
        """
        Computes the distinct permutations of faces rolled and their counts.
        
        Returns:
        pd.DataFrame: A DataFrame with a MultiIndex of permutations and a column for counts.
        """
        permuted_rolls = self.results.apply(lambda x: list(permutations(x)), axis=1)
        flat_permutations = [tuple(p) for sublist in permuted_rolls for p in sublist]
        perm_counts = pd.Series(flat_permutations).value_counts().reset_index()
        perm_counts.columns = ['Permutation', 'Count']
        return perm_counts.set_index('Permutation')