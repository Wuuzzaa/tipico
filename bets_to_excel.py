import pandas as pd


class BetsToExcel:
    def __init__(self, combi_bets, file_name="bets.xlsx"):
        self.combi_bets = combi_bets
        self.file_name = file_name
        self.predicted_outcomes = []
        self.actual_outcomes = []
        self.leagues = []
        self.quotes = []
        self.combi_quotes = []
        self.home_teams = []
        self.away_teams = []

    def fill_data_lists(self):
        for combi_bet in self.combi_bets:
            for bet in combi_bet.bets:
                self.predicted_outcomes.append(bet.outcome)
                self.actual_outcomes.append(None)
                self.leagues.append(bet.match.liga)
                self.quotes.append(bet.quote)
                self.home_teams.append(bet.match.home_team)
                self.away_teams.append(bet.match.away_team)

                # Add the combibetquote only once per combibet
                if bet == combi_bet.bets[0]:
                    self.combi_quotes.append(combi_bet.combi_quote)
                else:
                    self.combi_quotes.append(None)

            # add empty entry for blank line in the excelfile
            self.predicted_outcomes.append(None)
            self.actual_outcomes.append(None)
            self.leagues.append(None)
            self.quotes.append(None)
            self.combi_quotes.append(None)
            self.home_teams.append(None)
            self.away_teams.append(None)

    def save_to_excel(self):
        print(f"Save bets to: {self.file_name}")

        df = pd.DataFrame(
            {
                "Combination Quote:": self.combi_quotes,
                "Quote:": self.quotes,
                "League:": self.leagues,
                "Home Team:": self.home_teams,
                "Away Team:": self.away_teams,
                "Outcome Prediction:": self.predicted_outcomes,
                "Actual Outcome:": self.actual_outcomes
            }
        )

        writer = pd.ExcelWriter(self.file_name, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='bets', index=False)
        writer.save()

        print(f"Saved bets to: {self.file_name}")