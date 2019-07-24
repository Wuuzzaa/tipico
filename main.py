from tipico_scraper import TipicoScraper

scraper = TipicoScraper()
scraper.scrape_all()
scraper.sort_matches_by_lowest_quote()
scraper.print_matches()