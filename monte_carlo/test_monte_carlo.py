import unittest
import numpy as np
import pandas as pd
from monte_carlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):
    def setUp(self):
        self.faces = np.array([1, 2, 3, 4, 5, 6])
        self.die = Die(self.faces)

    def test_init(self):
        # Test that the representation of the die is a DataFrame
        self.assertIsInstance(self.die._df, pd.DataFrame)

    def test_change_weight(self):
        self.die.change_weight(1, 2.0)
        
        # Test that the weight of the 1 face has been updated to 2
        self.assertEqual(self.die._df.loc[1, 'weight'], 2.0)

    def test_roll(self):
        result = self.die.roll(10)
        
        # Test that the number of results is equal to 10, the number of rolls
        self.assertEqual(len(result), 10)

    def test_show(self):
        df = self.die.show()
        
        # Test that the representation of the current state of the die is a DataFrame
        self.assertIsInstance(df, pd.DataFrame)

class TestGame(unittest.TestCase):
    def setUp(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        self.dice = [Die(faces), Die(faces)]
        self.game = Game(self.dice)

    def test_init(self):
        # Test that the dice input is a list
        self.assertIsInstance(self.game.dice, list)
        
        # Test that all elements in the dice list are instances of the Die class
        for die in self.game.dice:
            self.assertIsInstance(die, Die)

    def test_play(self):
        self.game.play(10)
        
        # Test that the results are a DataFrame
        self.assertIsInstance(self.game._play_results, pd.DataFrame)
        
        # Check that the number of rows in the results dataframe is equal to 10, the number of rolls
        self.assertEqual(len(self.game._play_results), 10)

    def test_show(self):
        self.game.play(10)
        df_wide = self.game.show('wide')
        df_narrow = self.game.show('narrow')
        
        # Check that the results are DataFrames
        self.assertIsInstance(df_wide, pd.DataFrame)
        self.assertIsInstance(df_narrow, pd.DataFrame)
        
        # Check that the narrow results output the Roll and Die
        self.assertEqual(df_narrow.index.names, ['Roll', 'Die'])

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        dice = [Die(faces), Die(faces)]
        game = Game(dice)
        num_rolls = 10
        game.play(num_rolls)
        self.num_rolls = num_rolls
        self.game = game
        self.analyzer = Analyzer(game)

    def test_init(self):
        # Check that the input is a Game object
        self.assertTrue(hasattr(self.analyzer.game, 'show'), "The input must be a Game object.")
        
        # Check that the results attribute is a DataFrame
        self.assertIsInstance(self.analyzer.results, pd.DataFrame)

    def test_jackpot(self):
        # Calculate jackpots
        jackpots = self.analyzer.jackpot()
        
        # Check that the result is an integer
        self.assertIsInstance(jackpots, int)
        
        # Check that the jackpot count is less than or equal to the number of rolls
        self.assertLessEqual(jackpots, self.num_rolls)

    def test_face_counts_per_roll(self):
        # Get face counts per roll
        face_counts = self.analyzer.face_counts_per_roll()
        
        # Check that the result is a DataFrame
        self.assertIsInstance(face_counts, pd.DataFrame)
        
        # Check that the number of rows in the DataFrame is equal to the number of rolls
        self.assertEqual(len(face_counts), self.num_rolls)

    def test_combo_count(self):
        combo_counts = self.analyzer.combo_count()
        perm_counts = self.analyzer.permutation_count()
        
        # Check that the result is a DataFrame
        self.assertIsInstance(combo_counts, pd.DataFrame)
        
        # Check that the number of combinations is less than or equal to the number of permutations
        self.assertLessEqual(len(combo_counts), len(perm_counts))

    def test_permutation_count(self):
        perm_counts = self.analyzer.permutation_count()
        combo_counts = self.analyzer.combo_count()

        # Check that the result is a DataFrame
        self.assertIsInstance(perm_counts, pd.DataFrame)
        
        # Check that the number of permutations is greater than or equal to the number of combinations
        self.assertGreaterEqual(len(perm_counts), len(combo_counts))

if __name__ == '__main__':
    unittest.main()