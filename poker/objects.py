from typing import List
__package__ = 'poker.objects'


class Card(object):
    VALUES = {'2': 2,
              '3': 3,
              '4': 4,
              '5': 5,
              '6': 6,
              '7': 7,
              '8': 8,
              '9': 9,
              '10': 10,
              'J': 11,
              'Q': 12,
              'K': 13,
              'A': 14}

    SUITS = {'diamonds': 0,
             ' clubs': 1,
             ' hearts': 2,
             ' spades ': 3}

    SUITS_SH = {'d': 0,
                'c': 1,
                'h': 2,
                's': 3}

    def __init__(self, val: int, suit: int) -> None:
        self.val = val
        self.suit = suit

    def __hash__(self) -> int:
        return 100 * self.suit + self.val

    def __eq__(self, other: 'Card') -> bool:
        return (other is not None) and (self.val == other.val and self.suit == other.suit)

    def __str__(self) -> str:
        return 'Card(val:{}, suit:{})'.format(self.val, self.suit)

    def same_suit(self, other: 'Card') -> bool:
        return self.suit == other.suit

    def same_val(self, other: 'Card') -> bool:
        return self.val == other.val

    def is_prev_for(self, other: 'Card') -> bool:
        if self.val == 14 and other.val == 2:
            return True
        return self.val == other.val + 1

    def is_next_for(self, other: 'Card') -> bool:
        if self.val == 2 and other.val == 14:
            return True
        return self.val == other.val - 1


class Pocket(object):

    def __init__(self, cards: List[Card] = None) -> None:
        if not cards:
            self.cards = [None] * 2
        else:
            self.cards = cards


class Table(object):

    def __init__(self, cards: List[Card] = None) -> None:
        if not cards:
            self.cards = [None] * 5
        else:
            self.cards = cards
