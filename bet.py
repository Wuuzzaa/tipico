class Bet:
    OUTCOMES = {"HOME", "DRAW", "AWAY"}

    def __init__(self, match, outcome):
        assert outcome in Bet.OUTCOMES

        self.match = match
        self.outcome = outcome
        self.quote = self.get_outcome_quote()

    def get_outcome_quote(self):
        if self.outcome == "HOME":
            return self.match.quote_home_win

        elif self.outcome == "DRAW":
            return self.match.quote_draw

        elif self.outcome == "AWAY":
            return self.match.quote_away_win

    def __str__(self):
        if self.outcome == "DRAW":
            return f"Draw @ {self.match.home_team} vs. {self.match.away_team} with a quote of: {self.quote}"

        else:
            return f"{self.outcome} Team win @ {self.match.home_team} vs. {self.match.away_team} with a quote of: {self.quote}"
