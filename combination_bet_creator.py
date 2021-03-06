from itertools import combinations
from bet import Bet
from combination_bet import CombinationBet
from copy import deepcopy
from random import shuffle
import statistics


def chunks(l, n):
    """
    Generates a list of lists with size of n of a iterable input
    source: https://chrisalbon.com/python/data_wrangling/break_list_into_chunks_of_equal_size/
    :param l: a iterable
    :param n: chunksize
    """
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]


class CombinationBetCreator:
    def __init__(self, matches=None, bets=None, combi_bets=None, combination_size=3):
        self.combination_size = combination_size
        self.matches = matches
        self.bets = bets
        self.combi_bets = combi_bets
        self.mean = None
        self.stdev = None
        self.amount_of_combi_bets = None

        # Ensure that some matches are found on the website.
        # todo ugly here:
        if matches is not None and combi_bets is None:
            assert (len(matches) >= combination_size), \
                "Not enough matches to create combibets. Check configs. Maybe no games in the planed time?"

    def create_bets_with_outcome_lowest_quote(self):
        self.bets = []

        for match in self.matches:
            outcome = match.get_outcome_with_lowest_quote()
            self.bets.append(Bet(match, outcome))

        return self.bets

    def create_random_combi_bets(self):
        """
        Method creates random combibets of combination_size size. Creates only complete combi_bets and print the not
        used ones
        :return:
        """
        bets = deepcopy(self.bets)
        shuffle(bets)
        self.combi_bets = []

        combi_bets_matches = list(chunks(bets, self.combination_size))

        for combi in combi_bets_matches:
            self.combi_bets.append(CombinationBet(combi))

        # remove combibets which not contain enough bets
        not_used_combi_bets = [combi for combi in self.combi_bets if len(combi.bets) != self.combination_size]
        self.combi_bets = [combi for combi in self.combi_bets if len(combi.bets) == self.combination_size]

        if not_used_combi_bets:
            print("Not enough matches to create combo. Following matches are not used")
            for combi in not_used_combi_bets:
                print(combi)

        return self.combi_bets

    def __str__(self, mode=None):
        """
        Print statistics like amount of combibets, mean and stdev.
        :param mode: SHORT. The combinationbets are not printed
        :return:
        """
        text = \
            f"Statistics: \n" \
            f"Amount of Combibets: {self.amount_of_combi_bets}\n" \
            f"Mean: {self.mean}\n" \
            f"Stdev: {self.stdev}\n"

        if mode != "SHORT":
            text += f"Combination Bets: \n"

            for combi_bet in self.combi_bets:
                text += f"{str(combi_bet)} \n"

        return text

    def calc_combi_bets_mean(self):
        values = []
        for combi_bet in self.combi_bets:
            values.append(combi_bet.combi_quote)

        return round(statistics.mean(values), 2)

    def calc_combi_bets_stdev(self):
        values = []
        for combi_bet in self.combi_bets:
            values.append(combi_bet.combi_quote)

        return round(statistics.pstdev(values), 4)

    def refresh_statistics(self):
        self.mean = self.calc_combi_bets_mean()
        self.stdev = self.calc_combi_bets_stdev()
        self.amount_of_combi_bets = len(self.combi_bets)

    def sort_combi_bets_by_quote(self):
        self.combi_bets.sort(key=lambda combi_bet: combi_bet.combi_quote)

    def sort_combi_bets_by_stdev(self, l):
        l.sort(key=lambda combi_bet: combi_bet.stdev)
        return l

    def optimize(self):
        """Method optimizes the matches in the combination bets to minimize the stdev"""
        low = 0
        high = len(self.combi_bets) - 1

        while not low == high:
            stdev_before = self.stdev

            #todo optimize low and high to two new combibets
            all_bets = set(self.combi_bets[low].bets + self.combi_bets[high].bets)
            combis = set(combinations(all_bets, self.combination_size))
            pairs = []

            # generate all possible combination pairs
            for i in combis:
                x = set(i)
                y = all_bets - x

                combi_bet_1 = CombinationBet(list(x))
                combi_bet_2 = CombinationBet(list(y))
                pair = CombinationBetCreator(combi_bets=[combi_bet_1, combi_bet_2])
                pair.refresh_statistics()
                pairs.append(pair)

            pairs = self.sort_combi_bets_by_stdev(pairs)

            # get the combi with the lowest stdev
            combi_bet_1 = pairs[0].combi_bets[0]
            combi_bet_2 = pairs[0].combi_bets[1]

            # remove the old ones (low and high)
            x = self.combi_bets[low]
            y = self.combi_bets[high]
            self.combi_bets.remove(x)
            self.combi_bets.remove(y)

            # add the new optimized ones
            self.combi_bets.append(combi_bet_1)
            self.combi_bets.append(combi_bet_2)

            #todo end here
            self.refresh_statistics()
            stdev_after = self.stdev

            if stdev_before == stdev_after:
                low += 1

                if low == high:
                    low = 0
                    high -= 1

            elif stdev_before < stdev_after:
                raise ValueError("stdev_before < stdev_after")

            elif stdev_before > stdev_after:
                low = 0
                high = len(self.combi_bets) - 1

            self.sort_combi_bets_by_quote()
