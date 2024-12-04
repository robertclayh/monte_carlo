import pandas as pd

class Game:
    """
    Represents a game consisting of rolling one or more similar dice (Die objects) one or more times.
    
    Each die in a given game has the same number of sides and associated faces, but each die object may have its own weights.
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