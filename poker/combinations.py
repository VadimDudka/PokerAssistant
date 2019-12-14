from collections import Counter
from .objects import *


def has_royal_flush(pocket: Pocket, table: Table):
    all_cards = pocket.cards + table.cards
    suit_numbers = Counter([card.suit for card in all_cards])
    most_common_suit_val = suit_numbers.most_common(1)[0][0]
    most_common_suit_number = suit_numbers.most_common(1)[0][1]
    if most_common_suit_number < 5:
        return False
    filtered_cards = list(filter(lambda x: x.suit == most_common_suit_val, all_cards))
    filtered_cards_values = [card.val for card in filtered_cards]
    if {14, 13, 12, 11, 10}.issubset(filtered_cards_values):
        return True
    return False


def has_straight_flush(pocket: Pocket, table: Table):
    all_cards = pocket.cards + table.cards
    suit_numbers = Counter([card.suit for card in all_cards])
    most_common_suit_val = suit_numbers.most_common(1)[0][0]
    most_common_suit_number = suit_numbers.most_common(1)[0][1]
    if most_common_suit_number < 5:
        return False
    filtered_cards = list(filter(lambda x: x.suit == most_common_suit_val, all_cards))
    filtered_cards_values = [card.val for card in filtered_cards]

    if {14, 2, 3, 4, 5}.issubset(filtered_cards_values):
        return True
    for i in range(2, 11):
        if {i, i + 1, i + 2, i + 3, i + 4}.issubset(filtered_cards_values):
            return True
    return False


def has_four_of_a_kind(pocket: Pocket, table: Table):
    all_cards = pocket.cards + table.cards
    val_numbers = Counter([card.val for card in all_cards])
    if val_numbers.most_common(1)[0][1] == 4:
        return True
    return False


def has_full_house(pocket: Pocket, table: Table):
    all_cards = pocket.cards + table.cards
    val_numbers = Counter([card.val for card in all_cards])
    if val_numbers.most_common(2)[0][1] == 3 and val_numbers.most_common(2)[1][1] == 2:
        return True
    return False


def has_flush(pocket: Pocket, table: Table):
    all_cards = pocket.cards + table.cards
    suit_numbers = Counter([card.suit for card in all_cards])
    if suit_numbers.most_common(1)[0][1] >= 5:
        return True
    return False


def has_straight(pocket: Pocket, table: Table):
    all_cards = pocket.cards + table.cards
    cards_values = [card.val for card in all_cards]

    if {14, 2, 3, 4, 5}.issubset(cards_values):
        return True
    for i in range(2, 11):
        if {i, i + 1, i + 2, i + 3, i + 4}.issubset(cards_values):
            return True
    return False


def has_three_of_a_kind(pocket: Pocket, table: Table):
    all_cards = pocket.cards + table.cards
    val_numbers = Counter([card.val for card in all_cards])
    if val_numbers.most_common(1)[0][1] == 3:
        return True
    return False


def has_two_pair(pocket: Pocket, table: Table):
    all_cards = pocket.cards + table.cards
    val_numbers = Counter([card.val for card in all_cards])
    if val_numbers.most_common(2)[0][1] == 2 and val_numbers.most_common(2)[1][1] == 2:
        return True
    return False


def has_pair(pocket: Pocket, table: Table):
    all_cards = pocket.cards + table.cards
    val_numbers = Counter([card.val for card in all_cards])
    if val_numbers.most_common(2)[0][1] == 2:
        return True
    return False


def royal_flush_combinations(pocket: Pocket):
    if (pocket.cards[0].val >= 10) and (pocket.cards[1].val >= 10) and (pocket.cards[0].suit == pocket.cards[1].suit):
        return 1084
    elif (pocket.cards[0].val >= 10) and (pocket.cards[1].val >= 10):
        return 94
    elif (pocket.cards[0].val >= 10) or (pocket.cards[1].val >= 10):
        return 49
    else:
        return 4


def straight_flush_combinations(pocket: Pocket):
    if not pocket.cards[0].same_suit(pocket.cards[1]):
        return 250
    else:
        if pocket.cards[0].val != 14 and pocket.cards[1].val != 14:
            dif = abs(pocket.cards[0].val - pocket.cards[1].val)
            min_val = min(pocket.cards[0].val, pocket.cards[1].val)
        else:
            not_a_val = pocket.cards[0].val if pocket.cards[1].val == 14 else pocket.cards[1].val
            dif = not_a_val - 1 if not_a_val < 8 else 14 - not_a_val
            min_val = not_a_val if not_a_val >= 8 else 14

        if dif == 1:
            if 4 <= min_val <= 9:
                return 4200
            elif min_val in (3, 10):
                return 3150
            elif min_val in (2, 11):
                return 2120
            elif min_val == 13:
                return 78
            else:
                return 1100
        elif dif == 2:
            if 3 <= min_val <= 9:
                return 3240
            elif min_val in (2, 10):
                return 2170
            elif min_val == 12:
                return 122
            else:
                return 1100
        elif dif == 3:
            if 2 <= min_val <= 9:
                return 2210
            elif min_val == 11:
                return 166
            else:
                return 1150
        elif dif == 4:
            if min_val == 10:
                return 210
            else:
                return 1250
        else:
            return 250


def four_of_a_kind_combinations(pocket: Pocket):
    if pocket.cards[0].same_val(pocket.cards[1]):
        return 17848
    else:
        return 2668


def full_house_combinations(pocket: Pocket):
    if pocket.cards[0].same_val(pocket.cards[1]):
        return 176880
    else:
        return 46464


def flush_combinations(pocket: Pocket):
    if pocket.cards[0].same_suit(pocket.cards[1]):
        return 138000
    else:
        return 41450


def straight_combinations(pocket: Pocket):
    one_card_combinations = {2: 25000,
                             3: 33000,
                             4: 41000,
                             5: 49000,
                             6: 48100,
                             7: 48300,
                             8: 48300,
                             9: 48100,
                             10: 49000,
                             11: 41000,
                             12: 33000,
                             13: 25000,
                             14: 24000}
    if pocket.cards[0].val != 14 and pocket.cards[1].val != 14:
        dif = abs(pocket.cards[0].val - pocket.cards[1].val)
        min_val = min(pocket.cards[0].val, pocket.cards[1].val)
    elif not (pocket.cards[0].val == 14 and pocket.cards[1].val == 14):
        not_a_val = pocket.cards[0].val if pocket.cards[1].val == 14 else pocket.cards[1].val
        dif = not_a_val - 1 if not_a_val < 8 else 14 - not_a_val
        min_val = not_a_val if not_a_val > 7 else 14
    else:
        return 24000

    if dif == 0:
        return one_card_combinations[min_val]
    elif dif == 1:
        if 4 <= min_val <= 10:
            combinations = 193500
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        elif min_val in [3, 11]:
            combinations = 150272
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        elif min_val in [2, 12]:
            combinations = 106134
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        else:
            combinations = 69954
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
    elif dif == 2:
        if 5 <= min_val <= 8:
            combinations = 164600
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        elif min_val in [3, 4, 9, 10]:
            combinations = 157700
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        elif min_val in [2, 11]:
            combinations = 114092
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        else:
            combinations = 77912
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
    elif dif == 3:
        if 5 <= min_val <= 7:
            combinations = 136500
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        elif min_val in [4, 8]:
            combinations = 129018
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        elif min_val in [2, 3, 9, 10]:
            combinations = 121500
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        else:
            combinations = 85870
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
    elif dif == 4:
        if min_val in [5, 6]:
            combinations = 108754
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        elif min_val in [4, 7]:
            combinations = 100796
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        elif min_val in [3, 8]:
            combinations = 92838
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        elif min_val in [2, 9]:
            combinations = 84880
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
        else:
            combinations = 93828
            if pocket.cards[0].same_suit(pocket.cards[1]):
                return int(combinations * 0.9385)
            else:
                return combinations
    else:
        return int((one_card_combinations[pocket.cards[0].val] + one_card_combinations[pocket.cards[1].val]) * 0.84)


def three_of_a_kind_combinations(pocket: Pocket):
    if pocket.cards[0].same_val(pocket.cards[1]):
        return 253000
    else:
        if pocket.cards[0].same_suit(pocket.cards[1]):
            return int(94500 * 0.98)
        else:
            return 94500


def two_pair_combinations(pocket: Pocket):
    if pocket.cards[0].same_val(pocket.cards[1]):
        return 838200
    else:
        if pocket.cards[0].same_suit(pocket.cards[1]):
            return int(478500 * 0.977)
        else:
            return 478500


def pair_combinations(pocket: Pocket):
    if pocket.cards[0].same_val(pocket.cards[1]):
        return None
    else:
        if pocket.cards[0].same_suit(pocket.cards[1]):
            return int(955000 * 0.949)
        else:
            return 955000
