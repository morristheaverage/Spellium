"""Create a clean text file without any tricky punctuation that messes
up spellium.py

Takes text files as input1.txt input2.txt etc.

Produces clean_input1.txt clean_input2.txt etc.
"""
import sys
from string import punctuation

def main():
    """Main function
    Processes the files passed on the command line
    """
    if len(sys.argv) == 1:
        print("0 arguments given - at least 1 needed")
        sys.exit(1)
    
    # Define a filter function
    bad_chars = punctuation + "0123456789"
    is_letter = lambda k: False if k in bad_chars else True

    # Apply to every word in every given file
    for arg in sys.argv[1:]:
        with open(arg, "r") as fin, open("clean_" + arg, "w") as fout:
            for line in fin:
                for word in line.split():
                    # Create a clean word with only letters
                    clean_word = "".join(filter(is_letter, word))
                    # Write one word per line
                    fout.write(clean_word.lower() + "\n")

if __name__ == "__main__":
    main()
