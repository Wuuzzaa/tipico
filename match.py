class Match:
    def __init__(self, home_team, away_team, quote_home_win, quote_draw, quote_away_win, league, date, time):
        self.home_team = home_team
        self.away_team = away_team
        self.quote_home_win = quote_home_win
        self.quote_draw = quote_draw
        self.quote_away_win = quote_away_win
        self.league = league
        self.date = date
        self.time = time
        self.lowest_quote = self.get_lowest_quote()

    def __str__(self, mode=None):
        if mode == "ONLY_LOWEST_QUOTE":
            return f"{self.league}: {self.home_team} vs. {self.away_team}: {self.lowest_quote}"

        else:
            return f"{self.league}: {self.home_team} vs. {self.away_team}: {self.quote_home_win} {self.quote_draw} {self.quote_away_win}"

    def get_lowest_quote(self):
        return min(self.quote_away_win, self.quote_draw, self.quote_home_win)

    def get_outcome_with_lowest_quote(self):
        if self.quote_home_win == self.lowest_quote:
            return "HOME"

        if self.quote_draw == self.lowest_quote:
            return "DRAW"

        if self.quote_away_win == self.lowest_quote:
            return "AWAY"

