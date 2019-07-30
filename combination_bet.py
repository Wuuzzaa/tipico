class CombinationBet:
    def __init__(self, bets):
        self.bets = bets
        self.combi_quote = self.calc_combi_quote()

    def __str__(self):
        head = f"Combibet-quote: {self.combi_quote} \n"
        tail = "Bets: \n"
        for bet in self.bets:
            tail += f"{str(bet)} \n"

        return head + tail

    def calc_combi_quote(self):
        combi_quote = 1

        for bet in self.bets:
            combi_quote *= bet.quote

        return round(combi_quote, 2)

