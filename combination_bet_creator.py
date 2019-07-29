from itertools import combinations
from bet import Bet
from combination_bet import CombinationBet
from copy import deepcopy
from random import shuffle


def chunks(l, n):
    """
    https://chrisalbon.com/python/data_wrangling/break_list_into_chunks_of_equal_size/
    :param l: a iterable
    :param n: chunksize
    :return:
    """
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]


class CombinationBetCreator:
    def __init__(self, matches):
        self.matches = matches
        self.bets = self.create_bets_with_outcome_lowest_quote()
        self.combi_bets = self.create_random_combi_bets()
        # self.all_combinations = None
        # self.best_combinations = None

    # def create_all_combinations(self, amount_of_matches=3):
    #     self.all_combinations = set(combinations(self.matches, amount_of_matches))
    #
    # def print_all_combinations(self):
    #     for comb in self.all_combinations:
    #         print(comb)

    def create_bets_with_outcome_lowest_quote(self):
        bets = []

        for match in self.matches:
            outcome = match.get_outcome_with_lowest_quote()
            bets.append(Bet(match, outcome))

        return bets

    def create_random_combi_bets(self, combination_size=3):
        bets = deepcopy(self.bets)
        shuffle(bets)
        combi_bets = []

        combi_bets_matches = list(chunks(bets, combination_size))

        for combi in combi_bets_matches:
            combi_bets.append(CombinationBet(combi))

        # remove combibets which not contain enough bets
        not_used_combi_bets = [combi for combi in combi_bets if len(combi.bets) != combination_size]
        combi_bets = [combi for combi in combi_bets if len(combi.bets) == combination_size]

        if not_used_combi_bets:
            print("Not enough matches to create combo. Following matches are not used")
            for combi in not_used_combi_bets:
                print(combi)

        return combi_bets

    def __str__(self):
        text = "Combination Bets: \n"
        for combi_bet in self.combi_bets:
            text += f"{str(combi_bet)} \n"

        return text
