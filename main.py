from tipico_scraper import TipicoScraper
from combination_bet_creator import CombinationBetCreator

scraper = TipicoScraper()
scraper.scrape_all()
scraper.sort_matches_by_lowest_quote()
scraper.filter_min_lowest_quote(1.15)
scraper.filter_max_lowest_quote(1.5)
scraper.print_matches()

cbc = CombinationBetCreator(scraper.matches)
cbc.sort_combi_bets_by_quote()
print(cbc)
pass

