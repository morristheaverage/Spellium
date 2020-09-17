"""Can a word be spelt using chemical symbols?

Find out with this script
"""

import sys
import os
import pandas as pd

class Element:
    """Simple info class to store
    data about each element
    """    
    def __init__(self, series):
        self.name = series['Element']
        self.symbol = series['Symbol']
        self.atomic = series['AtomicNumber']
        self.mass = series['AtomicMass']
        self.period = series['Period']
        self.group = series['Group']

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol

    def plot_data(self):
        """Used in conjunction with matplotlib.pyplot"""
        #TODO

class SpellingError(Exception):
    """Raised when spelling attempt fails"""    
    pass

def spell(word: str, table: tuple) -> list:
    """Spells given word using elements from given periodic table

    Args:
        word (str): The word to spell with chemical symbols
        table (tuple): The chemical symbols to spell the word with

    Raises:
        ValueError: You passed an empty string
        SpellingError: You passed an unspellable word

    Returns:
        list: You passed a spellable word - spelt by the elements in this list
    """
    word = word.lower()
    length = len(word)
    # You better not have...
    if length == 0:
        raise ValueError("Empty string passed")
    # Phew, a sensible person is calling this function
    if length == 1:
        # Evaluates to true if word exists in dictionary
        # Check in the dictionary of single letter symbols
        if elem := table[0].get(word):
            return [elem]
        # If nothing was found raise SpellingError
        raise SpellingError
    if length == 2:
        # Evaluates to true if word exists in dictionary
        # Check in the dictionary of two letter symbols
        if elem := table[1].get(word):
            return [elem]
        # Maybe two symbols can be joined together
        elif (a := table[0].get(word[0])) and (b:= table[0].get(word[1])):
            return [a, b]
        # If nothing was found raise SpellingError
        raise SpellingError
    if length >= 3:
        # Now we need to solve recursively
        # First try to match the first two chars
        prefix, suffix = word[:2], word[2:]
        try: # To use a two letter prefix
            #TODO
            # Q: walrus joke here...
            if prelem := table[1].get(prefix):
                suflem = spell(suffix, table)
                return [prelem] + suflem
            raise SpellingError
        except SpellingError:
            # And if you fail try a one letter prefix
            prefix, suffix = word[:1], word[1:]
            # Don't wrap this in a try except
            # If it dies it dies
            #TODO
            # A: ...walrus punchline here
            if prelem := table[0].get(prefix):
                suflem = spell(suffix, table)
                return [prelem] + suflem
    raise SpellingError




if __name__ == "__main__":
    # Make sure arguments were passed
    argc = len(sys.argv)
    if argc == 1:
        print("Expected 1 or more arguments - got 0")
        sys.exit(1)

    # If we did get arguments we will need to load the data
    DATA = pd.read_csv("Periodic Table of Elements.csv")
    print("Loaded raw data")
    # Every element is 1 or 2 characters
    PERIODIC_TABLE = ({}, {})
    for _, row in DATA.iterrows():
        lower_symbol = row['Symbol'].lower()
        PERIODIC_TABLE[len(lower_symbol) - 1][lower_symbol] = Element(row)


    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            print(f"File argument detected - {arg}")
            #TODO
        else:
            try:
                solution = spell(arg, PERIODIC_TABLE)
                for e in solution:
                    print(str(e), end='')
                print('')
            except SpellingError:
                print(f"{arg} does not have a chemical spelling")
