import random

words = [
    "buffer"
]


class WordList:

    VALID_LENGTH = 6

    @classmethod
    def get_random_word(cls):
        return random.choice(words)

    @classmethod
    def is_correct_length(cls, word):
        """Return True when the provided word has the expected length."""
        return isinstance(word, str) and len(word) == cls.VALID_LENGTH

    @classmethod
    def is_known_word(cls, word):
        """Return True when the provided word is in the known words list."""
        return word in words


        
        







