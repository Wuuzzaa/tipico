import requests
from bs4 import BeautifulSoup as Bs
from match import Match


class TipicoScraper:
    # Constants - Soccerleagueurls
    URLS = {
        "BUNDESLIGA": "https://www.tipico.de/de/online-sportwetten/fussball/deutschland/bundesliga/g42301/",
        "2_BUNDESLIGA": "https://www.tipico.de/de/online-sportwetten/fussball/deutschland/2-bundesliga/g41301/",
        "3_BUNDESLIGA": "https://www.tipico.de/de/online-sportwetten/fussball/deutschland/3-liga/g8343301/",
        "PREMIER_LEAGUE": "https://www.tipico.de/de/online-sportwetten/fussball/england/premier-league/g1301/",
        "LA_LIGA": "https://www.tipico.de/de/online-sportwetten/fussball/spanien/la-liga/g36301/",
        "LIGUE_1": "https://www.tipico.de/de/online-sportwetten/fussball/frankreich/ligue-1/g4301/",
        "PRIMEIRA_LIGA": "https://www.tipico.de/de/online-sportwetten/fussball/portugal/primeira-liga/g52301/",
        "EREDIVISIE": "https://www.tipico.de/de/online-sportwetten/fussball/niederlande/eredivisie/g39301/",
        "MLS": "https://www.tipico.de/de/online-sportwetten/fussball/usa/mls/g18301/",
        "TIPICO_BUNDESLIGA": "https://www.tipico.de/de/online-sportwetten/fussball/osterreich/tipico-bundesliga/g29301/",
        "SERIE_A": "https://www.tipico.de/de/online-sportwetten/fussball/italien/serie-a/g33301/",
        "SUPERLIG": "https://www.tipico.de/de/online-sportwetten/fussball/turkei/superlig/g62301/",
        "FIRST_DIVISION_A": "https://www.tipico.de/de/online-sportwetten/fussball/belgien/first-division-a/g38301/",
        "SUPER_LEAGUE": "https://www.tipico.de/de/online-sportwetten/fussball/schweiz/super-league/g1060301/"
    }

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
            home_win_quotes.append(float(quotes[0].replace(",", ".")))
            draw_quotes.append(float(quotes[1].replace(",", ".")))
            away_win_quotes.append(float(quotes[2].replace(",", ".")))

        assert len(home_win_quotes) == len(draw_quotes) == len(away_win_quotes)

        return home_win_quotes, draw_quotes, away_win_quotes

    def __create_matches(self, home_teams, away_teams, home_win_quotes, draw_quotes, away_win_quotes, liga):
        assert \
            len(home_teams) == \
            len(away_teams) == \
            len(home_win_quotes) == \
            len(draw_quotes) == \
            len(away_win_quotes)

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
        self.clear()

        for liga_name, url in TipicoScraper.URLS.items():
            print(f"scraping: {liga_name}")
            self.__read_site_soup(url)
            home_teams, away_teams = self.__scrape_teams()
            home_win_quotes, draw_quotes, away_win_quotes = self.__scrape_quotes()
            self.__create_matches(home_teams, away_teams, home_win_quotes, draw_quotes, away_win_quotes, liga_name)

    def sort_matches_by_lowest_quote(self):
        self.matches.sort(key=lambda match: match.lowest_quote)

    def filter_min_lowest_quote(self, quote):
        """Filters all matches which lowest quote is lower than the quote parameter"""
        self.matches = [x for x in self.matches if x.lowest_quote >= quote]

    def filter_max_lowest_quote(self, quote):
        """Filters all matches which lowest quote is higher than the quote parameter"""
        self.matches = [x for x in self.matches if x.lowest_quote <= quote]

    def print_matches(self):
        for match in self.matches:
            print(match.__str__("ONLY_LOWEST_QUOTE"))


