# player.py

# written by: <Your name> <Date>
# changed by: <Your name> <Date>

import random
import math
import copy

# module constants
HAND_SIZE=10 # 'default' hand-size
VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'

WORDLIST_FILENAME = "words_alpha.txt"

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4,
    'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3,
    'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
    'y': 4, 'z': 10
}


# ---------------------------------------------------------------------

class WordGameWords(object):
    def __init__(self, filename=WORDLIST_FILENAME):
        """
        Returns a list of valid words. Words are strings of lowercase letters.

        Depending on the size of the word list, this function may
        take a while to finish.
        """


        self.word_dict = {}

        with open(filename, 'r') as infile:
            # wordlist: list of strings
            # skip all single character words (here + RETURN character)
            self.word_dict = {line.strip().lower():self.word2value(line.strip().lower()) for line in infile if len(line) > 2}



    def word2value(self, word):
        word_score = 0
        for letter in word:
            word_score += SCRABBLE_LETTER_VALUES[letter]

        return word_score


    def __contains__(self, arg):
            """
            Returns a boolean if the argument arg is in the list of words.

            Technically it redirects the functionality to the list self.wordlist!

            returns: bool
            """
            return self.word_dict.__contains__(arg)


    def get_word_score(self, word, n, letter_values=SCRABBLE_LETTER_VALUES):
        """
        Returns the score for a word. Assumes the word is a
        valid word.

        You may assume that the input word is always either a string of
        letters, or the empty string "". You may not assume that the
        string will only contain lowercase letters, so you will have to
        handle uppercase and mixed case strings appropriately.

            The score for a word is the product of two components:

            The first component is the sum of the points for letters in the word.
            The second component is the larger of:
                1, or
                7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
                and n is the hand length when the word was played

            Letters are scored as in Scrabble; A is worth 1, B is
            worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

        word: string
        n: int >= 0
        letter_values: dict of values for lower case letters
        returns: int >= 0

        """
        # make sure that the whole word is in lowercase first
        word = word.lower()
        word_score = 0

        if word != "":
            word_score = self.word_dict[word]

            word_score *= max(1, 7 * len(word) - 3 * (n - len(word)))

        return word_score

#----------

class WordGameHand(object):
    def __init__(self, word_list, content=None,
                n=HAND_SIZE, vowels=VOWELS, consonants=CONSONANTS ):
        """
        Initialize a random hand containing n lowercase letters.
        ceil(n/3) letters in the hand should be VOWELS (note,
        ceil(n/3) means the smallest integer not less than n/3).

        Hands are represented as dictionaries. The keys are
        letters and the values are the number of times the
        particular letter is repeated in that hand.

        word_list: WordGameWords object
        content: default None, dict with default content (for testing)
        n: int >= 0
        vowels: string of vowels
        consonants: string of consonants
        """

        self.word_list = word_list

        if (content is not None) and (isinstance(content, dict)):
            self.hand = dict(content)
        else:
            self.hand = {}
            num_vowels = int(math.ceil(n / 3))

            for i in range(num_vowels):
                x = random.choice(vowels)
                self.hand[x] = self.hand.get(x, 0) + 1

            for i in range(num_vowels, n):
                x = random.choice(consonants)
                self.hand[x] = self.hand.get(x, 0) + 1


    def __copy__(self):
        res = type(self)(self.word_list, content=self.hand)
        return res


    def __str__(self):
        letters = ''
        for key in self.hand:
          letters += key * self.hand[key]

        return letters


    def __len__(self):
        """
        __len__  returns the length of the current hand
        """
        l = 0
        for key in self.hand:
            l += self.hand[key]

        return l


    def get_frequency_dict(self, sequence):
        """
        Returns a dictionary where the keys are elements of the sequence
        and the values are integer counts, for the number of times that
        an element is repeated in the sequence.

        sequence: string or list
        return: dictionary
        """

        # freqs: dictionary (element_type -> int)
        freq = {}
        for x in sequence:
            freq[x] = freq.get(x,0) + 1
        return freq



    def update(self, word):
        """
        Does NOT assume that hand contains every letter in word at least as
        many times as the letter appears in word. Letters in word that don't
        appear in hand should be ignored. Letters that appear in word more times
        than in hand should never result in a negative count; instead, set the
        count in the returned hand to 0 (or remove the letter from the
        dictionary, depending on how your code is structured).

        Updates the hand: uses up the letters in the given word
        and returns the new hand, without those letters in it.


        word: string
        returns: dictionary (string -> int)


        depends on:
        self.hand: dictionary (string -> int)
        """
        pass

        word = word.lower()

        for letter in word:
            if letter in self.hand:
                self.hand[letter] = max(0, self.hand[letter] - 1)


    def is_valid_word(self, word):
        """
        Returns True if word is in the word_list and is entirely
        composed of letters in the hand. Otherwise, returns False.

        word: string
        returns: boolean


        depends on:
        self.hand: dictionary (string -> int)
        self.word_list: WordGameWords object
        """

        word = word.lower()
        is_valid = True

        # first test whether the word is directly in the wordlist
        # or when we substitute a joker with a vowel:
        word_exists = False


        if ('*' not in word) and (word in self.word_list):
            word_exists = True
        else:
            for vowel in VOWELS:
                if word.replace('*', vowel) in self.word_list:
                    word_exists = True

        if word_exists == True:
            letters_dict = self.get_frequency_dict(word)

            for letter in letters_dict:
                if letters_dict[letter] > self.hand.get(letter, 0):
                    is_valid = False
        else:
            is_valid = False

        return is_valid






"""
WordGamePlayer is the base class for a human or a computer player
"""
class WordGamePlayer(object):
    def __init__(self, wordlist, hand, name=None,
                 n=HAND_SIZE, vowels=VOWELS, consonants=CONSONANTS):
        self._wordlist = wordlist
        if (name is None) or (name == ''):
            self._name = f'Player{random.randint(100,10000):05d}'
        else:
           self._name = name

        self._hand = copy.copy(hand)
        self._score = 0
        self._has_finished = False

    def isComputerplayer(self):
        """
        dummy method
        """
        raise NotImplementedError

    def getName(self):
        """
        getName returns the name of the player
        """
        return self._name

    def getHand(self):
        """
        getHand returns the hand for displaying
        """
        return self._hand

    def getScore(self):
        """
        getScore returns the score for this player
        """
        return self._score

    def getFinished(self):
        """
        getFinished returns if this player has finised playing
        """
        return self._has_finished

    def setFinished(self):
        """
        setFinished sets the status, that this player has finished playing
        """
        self._has_finished = True


