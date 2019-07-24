import requests
from bs4 import BeautifulSoup as Bs
from match import Match


class TipicoScraper:
    # Constants - Soccerleagueurls
    URL_BUNDESLIGA = """https://www.tipico.de/de/online-sportwetten/fussball/deutschland/bundesliga/g42301/"""
    URL_2_BUNDESLIGA = """https://www.tipico.de/de/online-sportwetten/fussball/deutschland/2-bundesliga/g41301/"""
    ULR_3_BUNDESLIGA = """https://www.tipico.de/de/online-sportwetten/fussball/deutschland/3-liga/g8343301/"""
    URL_PREMIER_LEAGUE = """https://www.tipico.de/de/online-sportwetten/fussball/england/premier-league/g1301/"""
    URL_LA_LIGA = """https://www.tipico.de/de/online-sportwetten/fussball/spanien/la-liga/g36301/"""
    URL_LIGUE_1 = """https://www.tipico.de/de/online-sportwetten/fussball/frankreich/ligue-1/g4301/"""
    URL_PRIMEIRA_LIGA = """https://www.tipico.de/de/online-sportwetten/fussball/portugal/primeira-liga/g52301/"""
    URL_EREDIVISIE = """https://www.tipico.de/de/online-sportwetten/fussball/niederlande/eredivisie/g39301/"""
    URL_MLS = """https://www.tipico.de/de/online-sportwetten/fussball/usa/mls/g18301/"""
    #todo türkeiliga hinzufügen
    #todo italienliga hinzufügen

    URLS = [
        URL_BUNDESLIGA,
        URL_2_BUNDESLIGA,
        ULR_3_BUNDESLIGA,
        URL_PREMIER_LEAGUE,
        URL_LA_LIGA,
        URL_LIGUE_1,
        URL_PRIMEIRA_LIGA,
        URL_EREDIVISIE,
        URL_MLS
    ]

    def __init__(self):
        self.matches = []
        self.soup = None

    def clear(self):
        self.matches = []

    def __read_site_soup(self, url):
        source = requests.get(url).text
        self.soup = Bs(source, "html.parser")

    def __scrape_teams(self):
        """
        :return: 2 lists home_teams, away_teams
        """
        teams_soup = self.soup.find_all("div", attrs={"class": "t_cell w_128 left"})
        teams = []

        for row in teams_soup:
            team = row.text.strip()
            teams.append(team)

        # Home Teams are the even Teams and the Away Teams are the odd ones
        home_teams = teams[::2]
        away_teams = teams[1::2]

        assert len(home_teams) == len(away_teams)

        return home_teams, away_teams

    def __scrape_quotes(self):
        """
        :return: 3 lists home_win_quotes, draw_quotes, away_win_quotes
        """
        match_quotes_soup = self.soup.find_all("div", attrs={"class": "multi_row"})

        home_win_quotes = []
        draw_quotes = []
        away_win_quotes = []

        for row in match_quotes_soup:
            quotes = row.text.strip().split("\n")
            home_win_quotes.append(quotes[0])
            draw_quotes.append(quotes[1])
            away_win_quotes.append(quotes[2])

        assert len(home_win_quotes) == len(draw_quotes) == len(away_win_quotes)

        return home_win_quotes, draw_quotes, away_win_quotes

    def __create_matches(self, home_teams, away_teams, home_win_quotes, draw_quotes, away_win_quotes, liga):
        assert \
            len(home_teams) == \
            len(away_teams) == \
            len(home_win_quotes) == \
            len(draw_quotes) == \
            len(away_win_quotes)

        matches = []
        amount_matches = len(home_teams)

        for i in range(amount_matches):
            self.matches.append(
                Match(
                    home_teams[i],
                    away_teams[i],
                    home_win_quotes[i],
                    draw_quotes[i],
                    away_win_quotes[i],
                    liga
                )
            )

    def scrape_all(self):
        """Scraps all Ligues in the URLS-Constant"""
        for url in TipicoScraper.URLS:
            print(f"scraping: {url}")
            self.__read_site_soup(url)
            home_teams, away_teams = self.__scrape_teams()
            home_win_quotes, draw_quotes, away_win_quotes = self.__scrape_quotes()
            self.__create_matches(home_teams, away_teams, home_win_quotes, draw_quotes, away_win_quotes, "1. Bundesliga")

    def sort_matches_by_lowest_quote(self):
        self.matches.sort(key=lambda match: match.lowest_quote)

    def print_matches(self):
        for match in self.matches:
            print(match)
