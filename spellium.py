"""Can a word be spelt using chemical symbols?

Find out with this script
"""

import sys
import os
from itertools import product
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
        # Check in the dictionary of single letter symbols with a classy walrus operator
        if elem := table[0].get(word):
            return [elem]
        # If nothing was found raise SpellingError
        raise SpellingError
    if length == 2:
        # Evaluates to true if word exists in dictionary
        # Check in the dictionary of two letter symbols with yet another walrus boi
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
            # Q: What's the collective noun for a group of walrus operators?
            if prelem := table[1].get(prefix):
                suflem = spell(suffix, table)
                return [prelem] + suflem
            raise SpellingError
        except SpellingError:
            # And if you fail try a one letter prefix
            # But don't wrap this one in a try except statement
            # If it dies it dies
            prefix, suffix = word[:1], word[1:]
            # A: There isn't one. It's unnecessary and would just obfuscate things.
            if prelem := table[0].get(prefix):
                suflem = spell(suffix, table)
                return [prelem] + suflem
    raise SpellingError

def has_spelling(word: str, table: tuple) -> bool:
    try:
        spelling = spell(word, table)
        return True
    except SpellingError:
        return False

def chem_print(symbols: list) -> None:
    """Neatly prints a chemical spelling

    Args:
        symbols (list): The list of elements
    """    
    for symbol in symbols:
        print(str(symbol), end='')
    print('')

def word_bytes(size: int):
    # Useful constant
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    _iter = product(alphabet, size)
    # If x0 is there so is x1, x2, ... x7
    while x0 := next(_iter, False):
        # x0 was a tuple so we make it a string...
        packet = [''.join(x0)]
        # ... and then finish the full packet of 8 strings
        for _ in range(7):
            packet.append(''.join(next(_iter)))
        # And send it off
        yield packet
    # Ooh a return statement, how pythonic
    return


def preprocess(name: str, size: int) -> None:
    """Creates binary file of info for all possible strings of
    the given size

    Args:
        name (str): Name of file to save info in
        size (int): Covers all words of this length - pass value of 3 or greater
    """    
    word_bank = word_bytes(size)
    with open(name, 'wb') as fp:
        for packet in word_bank:
            bits = map(has_spelling, packet)
            result = sum(b*2**(7-i) for i, b in enumerate(bits))
            fp.write(result.to_bytes(1, 'big'))


def main():
    """Main function to process command line arguments"""
    # Make sure arguments were passed
    if len(sys.argv) == 1:
        print("Expected 1 or more arguments - got 0")
        sys.exit(1)

    # If we did get arguments we will need to load the data
    data = pd.read_csv("Periodic Table of Elements.csv")
    # Every element is 1 or 2 characters
    periodic_table = ({}, {})
    for _, row in data.iterrows():
        lower_symbol = row['Symbol'].lower()
        periodic_table[len(lower_symbol) - 1][lower_symbol] = Element(row)


    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            print(f"---\nFile argument detected - {arg}\n---")
            spelt, words = 0, 0
            with open(arg, 'r') as fp:
                for line in fp:
                    for word in line.split():
                        try:
                            words += 1
                            chem_print(spell(word, periodic_table))
                            spelt += 1
                        except SpellingError:
                            print(f"{word} does not have a chemical spelling")
            print(f"---\nFound spellings for {spelt} of the {words} words in {arg} - {100*spelt/words:.2f}%")
        else:
            try:
                solution = spell(arg, periodic_table)
                chem_print(solution)
            except SpellingError:
                print(f"--- {arg} does not have a chemical spelling ---")

if __name__ == "__main__":
    main()
