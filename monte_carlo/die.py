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
        new_weight: The new weight (numeric) for the face.
        
        Raises:
        IndexError: If the face value is not in the die.
        TypeError: If the new weight is not numeric.
        """
        if face not in self._df.index:
            raise IndexError("The face value is not valid.")
        try:
            new_weight = float(new_weight)
        except ValueError:
            raise TypeError("The weight must be numeric.")
        if new_weight < 0:
            raise ValueError("The weight must be a positive number.")
        
        self._df.loc[face, 'weight'] = new_weight

    def roll(self, n_rolls=1):
        """
        Rolls the die one or more times.
        
        Parameters:
        n_rolls (int): Number of rolls (default is 1).
        
        Returns:
        list: A list of outcomes from rolling the die.
        """
        outcomes = self._df.sample(
            n=n_rolls,
            weights='weight',
            replace=True
        ).index.tolist()
        return outcomes

    def show(self):
        """
        Displays the current state of the die.
        
        Returns:
        pd.DataFrame: A copy of the private die data frame.
        """
        return self._df.copy()