from bs4 import BeautifulSoup as Bs
from match import Match
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import datetime


class TipicoScraper:
    # Constants - Soccerleagueurls
    URLS = {
        # BRASILIEN
        "CAMPEONATO_BRASILEIRO_SERIE_A": "https://www.tipico.de/de/online-sportwetten/fussball/brasilien/campeonato-brasilero-a/g83301/",
        
        # DEUTSCHLAND
        "BUNDESLIGA": "https://www.tipico.de/de/online-sportwetten/fussball/deutschland/bundesliga/g42301/",
        "2_BUNDESLIGA": "https://www.tipico.de/de/online-sportwetten/fussball/deutschland/2-bundesliga/g41301/",
        "3_BUNDESLIGA": "https://www.tipico.de/de/online-sportwetten/fussball/deutschland/3-liga/g8343301/",

        # DÄNEMARK
        "SUPERLIGAEN": "https://www.tipico.de/de/online-sportwetten/fussball/danemark/superligaen/g12301/",

        # ENGLAND
        "PREMIER_LEAGUE": "https://www.tipico.de/de/online-sportwetten/fussball/england/premier-league/g1301/",
        "CHAMPIONSHIP": "https://www.tipico.de/de/online-sportwetten/fussball/england/championship/g2301/",

        # SPANIEN
        "LA_LIGA": "https://www.tipico.de/de/online-sportwetten/fussball/spanien/la-liga/g36301/",
        "LA_LIGA_2": "https://www.tipico.de/de/online-sportwetten/fussball/spanien/la-liga-2/g37301/",

        # FRANKREICH
        "LIGUE_1": "https://www.tipico.de/de/online-sportwetten/fussball/frankreich/ligue-1/g4301/",

        # PORTUGAL
        "PRIMEIRA_LIGA": "https://www.tipico.de/de/online-sportwetten/fussball/portugal/primeira-liga/g52301/",

        # NIEDERLANDE
        "EREDIVISIE": "https://www.tipico.de/de/online-sportwetten/fussball/niederlande/eredivisie/g39301/",

        # USA
        "MLS": "https://www.tipico.de/de/online-sportwetten/fussball/usa/mls/g18301/",

        # ÖSTERREICH
        "TIPICO_BUNDESLIGA": "https://www.tipico.de/de/online-sportwetten/fussball/osterreich/tipico-bundesliga/g29301/",

        # ITALIEN
        "SERIE_A": "https://www.tipico.de/de/online-sportwetten/fussball/italien/serie-a/g33301/",
        "SERIE_B": "https://www.tipico.de/de/online-sportwetten/fussball/italien/serie-b/g34301/",

        # TÜRKEI
        "SUPERLIG": "https://www.tipico.de/de/online-sportwetten/fussball/turkei/superlig/g62301/",

        # BELGIEN
        "FIRST_DIVISION_A": "https://www.tipico.de/de/online-sportwetten/fussball/belgien/first-division-a/g38301/",

        # SCHWEIZ
        "SUPER_LEAGUE": "https://www.tipico.de/de/online-sportwetten/fussball/schweiz/super-league/g1060301/",

        # SCHWEDEN
        "ALLSVENSKAN": "https://www.tipico.de/de/online-sportwetten/fussball/schweden/allsvenskan/g24301/",

        # RUSSLAND
        "PREMIER_LEAGUE(RUSSLAND)": "https://www.tipico.de/de/online-sportwetten/fussball/russland/premier-league/g53301/",
    }

    def __init__(self):
        self.matches = []
        self.soup = None

        # init the driver
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_options=options)

    def __restart_driver(self):
        self.driver.quit()
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_options=options)

    def clear(self):
        self.matches = []

    def __read_site_soup(self, url):
        self.driver.get(url)



        self.soup = Bs(self.driver.page_source, "html.parser")

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

    def __scrape_match_date_and_time(self):
        """
        :return: 2 lists. a list with the date of the game. format: e.g Freitag, 16.08 -> Weekday, DD.MM
                 Second list contains the time of the match. format: hh.mm
        """
        time_soup = self.soup.find_all("div", attrs={"class": "w_40 bl align_c left"})
        times = []
        dates = []

        for row in time_soup:
            # time
            time = row.text.strip()
            times.append(time)

            # date
            # Only the first match of a day has in the parents sibling the date in the text.
            # For the other matches on this day this is not the case but the date stays the same ;-)
            try:
                date = row.parent.find_previous_sibling("div", attrs={"class": "t_space bg_white"}).text
            except AttributeError:
                pass
            dates.append(date)

        assert len(times) == len(dates)
        return dates, times

    def __create_matches(self, home_teams, away_teams, home_win_quotes, draw_quotes, away_win_quotes, league, dates, times):
        assert \
            len(home_teams) == \
            len(away_teams) == \
            len(home_win_quotes) == \
            len(draw_quotes) == \
            len(away_win_quotes) == \
            len(dates) == \
            len(times)

        amount_matches = len(home_teams)

        for i in range(amount_matches):
            self.matches.append(
                Match(
                    home_teams[i],
                    away_teams[i],
                    home_win_quotes[i],
                    draw_quotes[i],
                    away_win_quotes[i],
                    league,
                    dates[i],
                    times[i]
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
            dates, times = self.__scrape_match_date_and_time()
            self.__create_matches(
                home_teams,
                away_teams,
                home_win_quotes,
                draw_quotes,
                away_win_quotes,
                liga_name,
                dates,
                times
            )

            # When we click on a new league on tipico the new league opens above the old league so we would receive
            # matches multiple times. The easiest way to avoid this is to get a new browser. Better way is to delete the
            # cookies
            self.driver.delete_all_cookies()

        # close the driver (browser)
        self.driver.quit()

    def sort_matches_by_lowest_quote(self):
        self.matches.sort(key=lambda match: match.lowest_quote)

    def filter_min_lowest_quote(self, quote):
        """Filters all matches which lowest quote is lower than the quote parameter"""
        self.matches = [x for x in self.matches if x.lowest_quote >= quote]

    def filter_max_lowest_quote(self, quote):
        """Filters all matches which lowest quote is higher than the quote parameter"""
        self.matches = [x for x in self.matches if x.lowest_quote <= quote]

    def filter_time_horizon_start_in_next_days(self, start_in_next_days):
        """
        Filters all matches which are not in the next days from current time on.
        E.g Current time in 27.09.2019 14:45 and days= 2 then all matches later then 29.09.2019 14:45 are removed
        :type start_in_next_days: int
        """
        now = datetime.datetime.today()
        limit_datetime = now + + datetime.timedelta(days=start_in_next_days)

        self.matches = [x for x in self.matches if x.datetime <= limit_datetime]

    def print_matches(self):
        for match in self.matches:
            print(match.__str__("ONLY_LOWEST_QUOTE"))

# TODO scrape all quotes like handicap and under over...
# Make the quotes for Handicap and all other bets visible
# buttons = self.driver.find_elements_by_xpath("//div[@class='t_more bl align_c right']")
#
# for button in buttons:
#     button.click()

