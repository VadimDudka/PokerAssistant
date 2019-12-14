from .combinations import *
from typing import List
from collections import Counter
import multiprocessing


class Game(object):
    pre_flop_combinations = 2118760
    pre_flop_functions = [royal_flush_combinations,
                          straight_flush_combinations,
                          four_of_a_kind_combinations,
                          full_house_combinations,
                          flush_combinations,
                          straight_combinations,
                          three_of_a_kind_combinations,
                          two_pair_combinations,
                          pair_combinations]
    pre_flop_opp_probs = [1 / 30940,
                          1 / 3590,
                          1 / 595,
                          1 / 38,
                          1 / 33,
                          1 / 21,
                          1 / 20,
                          4 / 17,
                          5 / 11,
                          4 / 23]

    def __init__(self, pocket: Pocket, table: Table = None, opponents_num: int = 8):
        self.pocket = pocket
        self.table = Table() if table is None else table
        self.deck = None
        self.sync_deck()
        self.opp_num = opponents_num

    def process_pre_flop(self):
        my_probs = list()
        for func in self.pre_flop_functions:
            try:
                my_probs.append(func(self.pocket) / self.pre_flop_combinations)
            except TypeError:
                my_probs.append(None)
        if my_probs[-1] is None:
            my_probs[-1] = 1 - sum(my_probs[:-1])
            my_probs.append(0)
        else:
            my_probs.append(1 - sum(my_probs))
        result_dict = {'my_probs': my_probs,
                       'opponent_probs': self.pre_flop_opp_probs,
                       'win_prob': Game.compute_win_prob(my_probs, self.pre_flop_opp_probs)}
        return result_dict

    def process_flop(self):
        my_combinations_lst = self.deck.get_combinations(2)
        my_combinations_sz = len(my_combinations_lst)
        with multiprocessing.Pool(processes=4) as pool:
            my_results = pool.map(Game.get_combination,
                                  map(lambda x: x + self.table.cards[:3] + self.pocket.cards, my_combinations_lst))
        my_count = Counter(my_results)
        my_probs = [my_count[i] for i in range(10)]
        my_probs = list(map(lambda x: x / my_combinations_sz, my_probs))

        opp_combinations_lst = self.deck.get_combinations(4)
        opp_combinations_sz = len(opp_combinations_lst)

        with multiprocessing.Pool(processes=4) as pool:
            opp_results = pool.map(Game.get_combination,
                                   map(lambda x: x + self.table.cards[:3], opp_combinations_lst),
                                   128)
        opp_count = Counter(opp_results)
        opp_probs = [opp_count[i] for i in range(10)]
        opp_probs = list(map(lambda x: x / opp_combinations_sz, opp_probs))

        result_dict = {'my_probs': my_probs,
                       'opponent_probs': opp_probs,
                       'win_prob': Game.compute_win_prob(my_probs, opp_probs)}
        return result_dict

    def process_turn(self):
        my_combinations_lst = self.deck.get_combinations(1)
        my_combinations_sz = len(my_combinations_lst)
        my_probs = [0] * 10
        for comb in my_combinations_lst:
            local_table = self.table.add_river(comb[0], inplace=False)
            combination_idx = Game.get_combination(self.pocket.cards + local_table.cards)
            my_probs[combination_idx] += 1
        my_probs = list(map(lambda x: x / my_combinations_sz, my_probs))

        opp_combinations_lst = self.deck.get_combinations(3)
        opp_combinations_sz = len(opp_combinations_lst)
        with multiprocessing.Pool(processes=4) as pool:
            opp_results = pool.map(Game.get_combination,
                                   map(lambda x: x + self.table.cards[:4], opp_combinations_lst))
        opp_count = Counter(opp_results)
        opp_probs = [opp_count[i] for i in range(10)]
        opp_probs = list(map(lambda x: x / opp_combinations_sz, opp_probs))

        result_dict = {'my_probs': my_probs,
                       'opponent_probs': opp_probs,
                       'win_prob': Game.compute_win_prob(my_probs, opp_probs)}
        return result_dict

    def process_river(self):
        my_probs = [0] * 10
        combination_idx = Game.get_combination(self.pocket.cards + self.table.cards)
        my_probs[combination_idx] += 1

        opp_combinations_lst = self.deck.get_combinations(2)
        opp_combinations_sz = len(opp_combinations_lst)
        opp_probs = [0] * 10
        for comb in opp_combinations_lst:
            local_pocket = Pocket(comb)
            combination_idx = Game.get_combination(local_pocket.cards + self.table.cards)
            opp_probs[combination_idx] += 1
        opp_probs = list(map(lambda x: x / opp_combinations_sz, opp_probs))

        result_dict = {'my_probs': my_probs,
                       'opponent_probs': opp_probs,
                       'win_prob': Game.compute_win_prob(my_probs, opp_probs)}
        return result_dict

    def open_flop(self, cards: List[Card]):
        self.table.add_flop(cards)
        self.sync_deck()

    def open_turn(self, card: Card):
        self.table.add_turn(card)
        self.sync_deck()

    def open_river(self, card: Card):
        self.table.add_river(card)
        self.sync_deck()

    def sync_deck(self):
        self.deck = Deck()
        self.deck.get_cards(set(self.pocket.cards))
        self.deck.get_cards(set(self.table.cards))

    @staticmethod
    def compute_win_prob(my_probs: list, oponent_probs: list) -> float:
        win_prob = my_probs[0] * sum(oponent_probs[1:]) + my_probs[-1] * 0.5 * oponent_probs[-1]
        for cmb_idx in range(1, 9):
            win_prob += my_probs[cmb_idx] * (sum(oponent_probs[cmb_idx + 1:]) + 0.5 * oponent_probs[cmb_idx])
        return win_prob

    @staticmethod
    def get_combination(all_cards: List[Card]):
        if has_royal_flush(all_cards=all_cards):
            return 0
        elif has_straight_flush(all_cards=all_cards):
            return 1
        elif has_four_of_a_kind(all_cards=all_cards):
            return 2
        elif has_full_house(all_cards=all_cards):
            return 3
        elif has_flush(all_cards=all_cards):
            return 4
        elif has_straight(all_cards=all_cards):
            return 5
        elif has_three_of_a_kind(all_cards=all_cards):
            return 6
        elif has_two_pair(all_cards=all_cards):
            return 7
        elif has_pair(all_cards=all_cards):
            return 8
        return 9

    @staticmethod
    def start():
        print('--- Hand ---')
        val1 = int(input('Card 1, val : '))
        suit1 = int(input('Card 1, suit : '))
        val2 = int(input('Card 2, val : '))
        suit2 = int(input('Card 2, suit : '))
        pocket = Pocket([Card(val1, suit1),
                         Card(val2, suit2)])
        game_obj = Game(pocket, opponents_num=0)
        print('--- Pre-flop ---')
        res = game_obj.process_pre_flop()
        print('Win prob: {:.2f}%'.format(100 * res['win_prob']))
        print('Opening flop')
        val1 = int(input('Card 1, val : '))
        suit1 = int(input('Card 1, suit : '))
        val2 = int(input('Card 2, val : '))
        suit2 = int(input('Card 2, suit : '))
        val3 = int(input('Card 3, val : '))
        suit3 = int(input('Card 3, suit : '))
        game_obj.open_flop([Card(val1, suit1),
                            Card(val2, suit2),
                            Card(val3, suit3)])
        print('--- Flop ---')
        res = game_obj.process_flop()
        print('Win prob: {:.2f}%'.format(100 * res['win_prob']))
        print('Opening turn')
        val = int(input('Card val : '))
        suit = int(input('Card suit : '))
        game_obj.open_turn(Card(val, suit))
        print('--- Turn ---')
        res = game_obj.process_turn()
        print('Win prob: {:.2f}%'.format(100 * res['win_prob']))
        print('Opening river')
        val = int(input('Card val : '))
        suit = int(input('Card suit : '))
        game_obj.open_river(Card(val, suit))
        print('--- River ---')
        res = game_obj.process_river()
        print('Win prob: {:.2f}%'.format(100 * res['win_prob']))
