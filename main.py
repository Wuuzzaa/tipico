from tipico_scraper import TipicoScraper
from combi_betting_optimizer import CombiBettingOptimizer

scraper = TipicoScraper()
scraper.scrape_all()
scraper.sort_matches_by_lowest_quote()
scraper.filter_min_lowest_quote(1.15)
scraper.filter_max_lowest_quote(1.5)
scraper.print_matches()

optimizer = CombiBettingOptimizer(scraper.matches)
optimizer.create_all_combinations(3)
optimizer.print_all_combinations()
