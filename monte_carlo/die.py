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