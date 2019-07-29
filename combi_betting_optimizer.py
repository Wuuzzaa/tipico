from itertools import combinations


class CombiBettingOptimizer:
    def __init__(self, matches):
        self.matches = matches
        self.all_combinations = None
        self.best_combinations = None

    def create_all_combinations(self, amount_of_matches=3):
        self.all_combinations = set(combinations(self.matches, amount_of_matches))

    def print_all_combinations(self):
        for comb in self.all_combinations:
            print(comb)