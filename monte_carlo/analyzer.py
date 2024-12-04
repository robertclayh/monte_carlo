import pandas as pd
from itertools import combinations_with_replacement, permutations

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