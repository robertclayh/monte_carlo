import unittest
import numpy as np
import pandas as pd
from die import Die
from game import Game
from analyzer import Analyzer

class TestDie(unittest.TestCase):
    def setUp(self):
        self.faces = np.array([1, 2, 3, 4, 5, 6])
        self.die = Die(self.faces)

    def test_init(self):
        self.assertIsInstance(self.die._df, pd.DataFrame)

    def test_change_weight(self):
        self.die.change_weight(1, 2.0)
        self.assertEqual(self.die._df.loc[1, 'weight'], 2.0)

    def test_roll(self):
        result = self.die.roll(10)
        self.assertEqual(len(result), 10)

    def test_show(self):
        df = self.die.show()
        self.assertIsInstance(df, pd.DataFrame)

class TestGame(unittest.TestCase):
    def setUp(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        self.dice = [Die(faces), Die(faces)]
        self.game = Game(self.dice)

    def test_init(self):
        self.assertIsInstance(self.game.dice, list)

    def test_play(self):
        self.game.play(10)
        self.assertIsInstance(self.game._play_results, pd.DataFrame)
        self.assertEqual(len(self.game._play_results), 10)

    def test_show(self):
        self.game.play(10)
        df_wide = self.game.show('wide')
        df_narrow = self.game.show('narrow')
        self.assertIsInstance(df_wide, pd.DataFrame)
        self.assertIsInstance(df_narrow, pd.DataFrame)
        self.assertEqual(df_narrow.index.names, ['Roll', 'Die'])

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        dice = [Die(faces), Die(faces)]
        game = Game(dice)
        game.play(10)
        self.analyzer = Analyzer(game)

    def test_init(self):
        self.assertIsInstance(self.analyzer.results, pd.DataFrame)

    def test_jackpot(self):
        jackpots = self.analyzer.jackpot()
        self.assertIsInstance(jackpots, int)

    def test_face_counts_per_roll(self):
        face_counts = self.analyzer.face_counts_per_roll()
        self.assertIsInstance(face_counts, pd.DataFrame)

    def test_combo_count(self):
        combo_counts = self.analyzer.combo_count()
        self.assertIsInstance(combo_counts, pd.DataFrame)

    def test_permutation_count(self):
        perm_counts = self.analyzer.permutation_count()
        self.assertIsInstance(perm_counts, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()